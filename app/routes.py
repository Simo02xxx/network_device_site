from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login  import login_user, logout_user, login_required, current_user
from datetime     import datetime, timedelta
from .models      import User, Device, DeviceSelection
from .forms       import CSRFOnlyForm, RegisterForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from .            import db, login_manager, mail
from flask_mail   import Message
from .mail_utils  import generate_otp, send_reset_email


main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ======================
# PAGE D’ACCUEIL
# ======================
@main.route('/')
def home():
    return render_template('home.html', current_year=datetime.utcnow().year)


# ======================
# INSCRIPTION
# ======================
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email déjà utilisé", "danger")
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Inscription réussie !", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


# ======================
# CONNEXION
# ======================
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):

            # 1) Générer un OTP
            otp = generate_otp()
            user.otp_code        = otp
            user.otp_expiration  = datetime.utcnow() + timedelta(minutes=5)
            db.session.commit()

            # 2) Envoyer l’e-mail (→ nouvelle fonction juste après)
            send_otp_email(user, otp)                       # NEW/EDIT ✓

            # 3) Stocker l’id pour la vérification
            session['user_id_otp'] = user.id
            flash("Un code de vérification a été envoyé par email.", "info")
            return redirect(url_for('main.verify_otp'))

        flash("Identifiants incorrects", "danger")
    return render_template('login.html', form=form)

# ======================
# DÉCONNEXION
# ======================
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie", "info")
    return redirect(url_for('main.login'))


# ======================
# TABLEAU DE BORD
# ======================
@main.route('/dashboard')
@login_required
def dashboard():
    selections = DeviceSelection.query.filter_by(user_id=current_user.id).all()
    total = sum(item.quantity * item.device.price for item in selections)
    form = CSRFOnlyForm()
    return render_template('dashboard.html', user=current_user, selections=selections, total=total, form=form, current_year=2025)

@main.route('/delete_device/<int:selection_id>', methods=['POST'])
@login_required
def delete_device(selection_id):
    selection = DeviceSelection.query.get_or_404(selection_id)
    if selection.user_id != current_user.id:
        flash("Action non autorisée.", "danger")
        return redirect(url_for('main.dashboard'))

    db.session.delete(selection)
    db.session.commit()
    flash("Périphérique supprimé avec succès.", "success")
    return redirect(url_for('main.dashboard'))


# ======================
# SÉLECTION DE PÉRIPHÉRIQUES
# ======================
@main.route('/select_devices', methods=['GET', 'POST'])
@login_required
def select_devices():
    form = CSRFOnlyForm()
    devices = Device.query.all()

    if form.validate_on_submit():
        added_any = False
        for device in devices:
            qty_str = request.form.get(f'quantity_{device.id}')
            if qty_str and qty_str.isdigit():
                qty = int(qty_str)
                if qty > 0:
                    # Chercher si une sélection existe déjà pour cet utilisateur + device
                    selection = DeviceSelection.query.filter_by(user_id=current_user.id, device_id=device.id).first()
                    if selection:
                        selection.quantity += qty
                    else:
                        selection = DeviceSelection(
                            device_id=device.id,
                            quantity=qty,
                            user_id=current_user.id
                        )
                        db.session.add(selection)
                    added_any = True

        if added_any:
            db.session.commit()
            flash("Périphériques ajoutés avec succès", "success")
        else:
            flash("Aucun périphérique sélectionné.", "warning")

        return redirect(url_for('main.dashboard'))

    return render_template('select_devices.html', devices=devices, form=form)

from flask import make_response
from io import BytesIO
from xhtml2pdf import pisa

@main.route('/telecharger_facture')
@login_required
def telecharger_facture():
    selections = DeviceSelection.query.filter_by(user_id=current_user.id).all()
    total = sum(sel.quantity * sel.device.price for sel in selections)
    
    html = render_template('facture.html', user=current_user, selections=selections, total=total, date=datetime.utcnow())
    
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_file)

    if pisa_status.err:
        return "Erreur lors de la génération du PDF", 500

    pdf_file.seek(0)
    response = make_response(pdf_file.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=facture.pdf'
    return response

@main.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('Si cet email est enregistré, un lien de réinitialisation a été envoyé.', 'info')
        return redirect(url_for('main.login'))
    return render_template('reset_request.html', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Réinitialisation du mot de passe',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    link = url_for('main.reset_token', token=token, _external=True)
    msg.body = f'''Pour réinitialiser votre mot de passe, cliquez sur ce lien :
{link}

Si vous n'avez pas demandé cette réinitialisation, ignorez ce mail.
'''
    mail.send(msg)

@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Lien invalide ou expiré', 'warning')
        return redirect(url_for('main.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Mot de passe réinitialisé avec succès !', 'success')
        return redirect(url_for('main.login'))
    return render_template('reset_token.html', form=form)


@main.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    user_id = session.get('user_id_otp')
    if not user_id:
        flash("Veuillez vous connecter d'abord.", "warning")
        return redirect(url_for('main.login'))
    
    user = User.query.get(user_id)
    if not user:
        flash("Utilisateur introuvable.", "danger")
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        otp_input = request.form.get('otp')
        if user.otp_code == otp_input and datetime.utcnow() < user.otp_expiration:
            login_user(user)
            # Nettoyage
            user.otp_code = None
            user.otp_expiration = None
            db.session.commit()
            session.pop('user_id_otp', None)
            flash("Connexion réussie avec authentification à deux facteurs !", "success")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Code invalide ou expiré", "danger")

    return render_template('verify_otp.html')

def send_otp_email(user, otp):                              # signature EDIT ✓
    """Envoie le code OTP à l’utilisateur."""
    msg = Message(
        subject = 'Votre code de vérification',
        sender   = 'noreply@demo.com',
        recipients=[user.email])
    msg.body = f"""Bonjour {user.name},

Voici votre code de vérification : {otp}
(Validité : 5 minutes)

Si vous n'êtes pas à l'origine de cette demande, ignorez ce message.
"""
    mail.send(msg)

# (Gardez send_reset_email dans mail_utils.py OU dans routes, mais **pas en double**)