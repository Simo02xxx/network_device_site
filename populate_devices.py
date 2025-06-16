from app import create_app, db
from app.models import Device

app = create_app()

devices = [
    {"icon": "🖧", "name": "Switch manageable 24 ports", "price": 150, "description": "Switch intelligent pour gérer le trafic réseau sur 24 ports RJ45."},
    {"icon": "🔌", "name": "Switch non manageable 8 ports", "price": 40, "description": "Switch simple plug & play pour de petites connexions locales."},
    {"icon": "📶", "name": "Routeur Wi-Fi dual-band", "price": 80, "description": "Permet la connexion Internet sans fil sur deux bandes (2.4 GHz & 5 GHz)."},
    {"icon": "📡", "name": "Point d’accès Wi-Fi", "price": 100, "description": "Étend la portée du signal Wi-Fi existant dans un bâtiment ou bureau."},
    {"icon": "🛡️", "name": "Pare-feu matériel (firewall)", "price": 300, "description": "Sécurise le trafic réseau entrant et sortant avec filtrage avancé."},
    {"icon": "📞", "name": "Modem câble", "price": 60, "description": "Convertit le signal câble coaxial en signal Internet."},
    {"icon": "📞", "name": "Modem DSL", "price": 50, "description": "Permet la connexion Internet via ligne téléphonique DSL."},
    {"icon": "🔁", "name": "Convertisseur média fibre", "price": 120, "description": "Convertit un signal Ethernet en fibre optique, et vice versa."},
    {"icon": "📡", "name": "Répéteur Wi-Fi", "price": 40, "description": "Renforce le signal Wi-Fi dans les zones mal couvertes."},
    {"icon": "🧵", "name": "Câble Ethernet Cat6 (10m)", "price": 10, "description": "Câble réseau performant pour connexions jusqu'à 1 Gbps."},
    {"icon": "🧵", "name": "Câble Ethernet Cat6 (1m)", "price": 3, "description": "Petit câble réseau pratique pour le câblage interne."},
    {"icon": "🔗", "name": "Câble fibre optique (1m)", "price": 15, "description": "Connexion ultra-rapide pour équipements fibre optique."},
    {"icon": "🔬", "name": "Module SFP fibre optique", "price": 70, "description": "Permet la connexion fibre optique sur un switch compatible."},
    {"icon": "🧩", "name": "Contrôleur réseau PCIe", "price": 40, "description": "Carte réseau interne à insérer dans un PC ou serveur."},
    {"icon": "🗄️", "name": "Serveur NAS", "price": 400, "description": "Stockage réseau centralisé pour sauvegarde et partage de fichiers."},
    {"icon": "📡", "name": "Antenne Wi-Fi externe", "price": 30, "description": "Améliore la portée du signal Wi-Fi pour un routeur ou PC."},
    {"icon": "🔋", "name": "Onduleur (UPS) pour réseau", "price": 200, "description": "Protège les équipements réseau contre les coupures de courant."},
    {"icon": "⚡", "name": "Switch PoE 8 ports", "price": 120, "description": "Alimente des caméras ou AP via câble réseau Ethernet (PoE)."},
    {"icon": "⚡", "name": "Switch PoE 24 ports", "price": 350, "description": "Switch PoE haute capacité pour réseaux d’entreprise."},
    {"icon": "🔒", "name": "Routeur VPN", "price": 250, "description": "Assure la communication chiffrée via VPN pour un réseau privé."},
    {"icon": "🌐", "name": "Firewall virtuel", "price": 0, "description": "Pare-feu logiciel déployé sur un serveur ou cloud."},
    {"icon": "🔀", "name": "Bridge réseau", "price": 70, "description": "Relie deux segments réseau distincts entre eux."},
    {"icon": "🔧", "name": "Hub Ethernet 4 ports", "price": 20, "description": "Distribue simplement un signal réseau (non intelligent)."},
    {"icon": "🔧", "name": "Hub Ethernet 8 ports", "price": 30, "description": "Hub pour connecter jusqu'à 8 périphériques."},
    {"icon": "🛰️", "name": "Contrôleur de réseau sans fil", "price": 180, "description": "Gère plusieurs points d’accès Wi-Fi de manière centralisée."},
    {"icon": "📱", "name": "Routeur 5G", "price": 400, "description": "Routeur supportant les réseaux mobiles 5G pour Internet rapide."},
    {"icon": "🏗️", "name": "Switch empilable 48 ports", "price": 700, "description": "Switch entreprise empilable pour datacenter ou campus."},
    {"icon": "🧵", "name": "Câble réseau plat (10m)", "price": 12, "description": "Câble Cat6 fin et souple pour passages sous moquette."},
    {"icon": "🔌", "name": "Prise murale réseau RJ45", "price": 5, "description": "Permet de terminer un câblage réseau proprement."},
    {"icon": "📋", "name": "Patch panel 24 ports", "price": 70, "description": "Organise les câbles réseau dans une baie de brassage."},
    {"icon": "📦", "name": "Boîtier de distribution fibre", "price": 150, "description": "Centralise les connexions fibre optique dans un coffret."},
    {"icon": "📺", "name": "Répartiteur réseau coaxial", "price": 25, "description": "Permet de partager une source coaxiale sur plusieurs équipements."},
    {"icon": "🔄", "name": "Convertisseur USB vers Ethernet", "price": 40, "description": "Ajoute un port réseau à un appareil via USB."},
    {"icon": "⚡", "name": "Adaptateur Powerline", "price": 80, "description": "Utilise le courant électrique pour transporter les données réseau."},
    {"icon": "📶", "name": "Contrôleur Wi-Fi Mesh", "price": 200, "description": "Gère un réseau maillé sans fil (Wi-Fi Mesh)."},
    {"icon": "📈", "name": "Amplificateur de signal Wi-Fi", "price": 50, "description": "Renforce la portée du signal Wi-Fi existant."},
    {"icon": "📡", "name": "Antenne directionnelle Wi-Fi", "price": 60, "description": "Concentre le signal Wi-Fi dans une direction spécifique."},
    {"icon": "🏭", "name": "Switch industriel robuste", "price": 1000, "description": "Switch conçu pour des environnements extrêmes (chaleur, poussière, etc.)."},
    {"icon": "🚦", "name": "Routeur de bordure", "price": 600, "description": "Fait le lien entre le réseau local et Internet."},
    {"icon": "💡", "name": "Module SFP+ 10Gbps", "price": 300, "description": "Module pour connexion très haut débit 10 Gbps."},
    {"icon": "⚙️", "name": "Switch 10Gbps 24 ports", "price": 4000, "description": "Switch hautes performances pour datacenters ou entreprises exigeantes."},
    {"icon": "☎️", "name": "Routeur DSL avec VoIP", "price": 120, "description": "Combine Internet DSL et téléphonie VoIP."},
    {"icon": "☀️", "name": "Point d’accès Wi-Fi extérieur", "price": 180, "description": "AP conçu pour résister à la pluie et à la chaleur."},
    {"icon": "🧠", "name": "Contrôleur réseau SDN", "price": 1500, "description": "Gère dynamiquement les flux réseau via software-defined networking."},
    {"icon": "📥", "name": "Module transceiver RJ45", "price": 50, "description": "Permet la connexion cuivre via module RJ45."},
    {"icon": "📥", "name": "Module transceiver SFP", "price": 100, "description": "Module pour connexion fibre via port SFP."},
    {"icon": "🧳", "name": "Boîtier fibre optique", "price": 200, "description": "Protection et terminaison des câbles fibre optique."},
    {"icon": "🏢", "name": "Router Core pour data center", "price": 8000, "description": "Routeur ultra-performant pour cœur de réseau."},
    {"icon": "🛡️", "name": "Firewall UTM", "price": 2500, "description": "Unité de sécurité tout-en-un avec antivirus, IDS, VPN, etc."},
    {"icon": "🧱", "name": "Switch stackable 12 ports", "price": 600, "description": "Switch compact pouvant être empilé."},
    {"icon": "📺", "name": "Câble HDMI réseau (Ethernet)", "price": 30, "description": "Transporte à la fois le signal vidéo et réseau Ethernet."},
    {"icon": "🕵️", "name": "Serveur proxy", "price": 0, "description": "Filtre et surveille les accès Internet pour les clients internes."},
    {"icon": "📡", "name": "Routeur sans fil 802.11ax", "price": 150, "description": "Routeur Wi-Fi de dernière génération (Wi-Fi 6)."},
    {"icon": "🎛️", "name": "Switch KVM (contrôle clavier)", "price": 120, "description": "Permet de contrôler plusieurs ordinateurs avec un seul clavier/souris."},
    {"icon": "☁️", "name": "Contrôleur réseau cloud", "price": 1000, "description": "Gestion centralisée à distance des équipements réseau via cloud."},
    {"icon": "⚡", "name": "Module Power over Ethernet (PoE)", "price": 60, "description": "Injecte du courant via le câble réseau vers un appareil PoE."},
    {"icon": "📶", "name": "Antenne Wi-Fi 6 interne", "price": 40, "description": "Supporte le standard Wi-Fi 6 pour performances améliorées."},
    {"icon": "🔒", "name": "Câble réseau blindé Cat7", "price": 20, "description": "Protège contre les interférences pour installations sensibles."},
    {"icon": "🧩", "name": "Switch modulaire", "price": 2000, "description": "Switch dont on peut remplacer ou ajouter des modules."},
    {"icon": "🚨", "name": "Firewall de nouvelle génération", "price": 3000, "description": "Filtrage réseau intelligent avec détection comportementale."}
]

with app.app_context():
    if Device.query.count() == 0:
        for d in devices:
            device = Device(name=d["name"], price=d["price"], icon=d["icon"], description=d["description"])
            db.session.add(device)
        db.session.commit()
        print(f"✅ {len(devices)} périphériques insérés avec succès.")
    else:
        print("⚠️ La table Device n'est pas vide, insertion ignorée.")
