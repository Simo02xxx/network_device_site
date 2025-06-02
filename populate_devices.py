from app import create_app, db
from app.models import Device

app = create_app()

# Exemple : liste de périphériques (tu peux compléter jusqu'à 60)
devices = [
    {"name": "Switch manageable 24 ports", "price": 150},
    {"name": "Switch non manageable 8 ports", "price": 40},
    {"name": "Routeur Wi-Fi dual-band", "price": 80},
    {"name": "Point d’accès Wi-Fi", "price": 100},
    {"name": "Pare-feu matériel (firewall)", "price": 300},
    {"name": "Modem câble", "price": 60},
    {"name": "Modem DSL", "price": 50},
    {"name": "Convertisseur média fibre", "price": 120},
    {"name": "Répéteur Wi-Fi", "price": 40},
    {"name": "Câble Ethernet Cat6 (10m)", "price": 10},
    {"name": "Câble Ethernet Cat6 (1m)", "price": 3},
    {"name": "Câble fibre optique (1m)", "price": 15},
    {"name": "Module SFP fibre optique", "price": 70},
    {"name": "Contrôleur réseau PCIe", "price": 40},
    {"name": "Serveur NAS", "price": 400},
    {"name": "Antenne Wi-Fi externe", "price": 30},
    {"name": "Onduleur (UPS) pour réseau", "price": 200},
    {"name": "Switch PoE 8 ports", "price": 120},
    {"name": "Switch PoE 24 ports", "price": 350},
    {"name": "Routeur VPN", "price": 250},
    {"name": "Firewall virtuel", "price": 0},
    {"name": "Bridge réseau", "price": 70},
    {"name": "Hub Ethernet 4 ports", "price": 20},
    {"name": "Hub Ethernet 8 ports", "price": 30},
    {"name": "Contrôleur de réseau sans fil", "price": 180},
    {"name": "Routeur 5G", "price": 400},
    {"name": "Switch empilable 48 ports", "price": 700},
    {"name": "Câble réseau plat (10m)", "price": 12},
    {"name": "Prise murale réseau RJ45", "price": 5},
    {"name": "Patch panel 24 ports", "price": 70},
    {"name": "Boîtier de distribution fibre", "price": 150},
    {"name": "Répartiteur réseau coaxial", "price": 25},
    {"name": "Convertisseur USB vers Ethernet", "price": 40},
    {"name": "Adaptateur Powerline", "price": 80},
    {"name": "Contrôleur Wi-Fi Mesh", "price": 200},
    {"name": "Amplificateur de signal Wi-Fi", "price": 50},
    {"name": "Antenne directionnelle Wi-Fi", "price": 60},
    {"name": "Switch industriel robuste", "price": 1000},
    {"name": "Routeur de bordure", "price": 600},
    {"name": "Module SFP+ 10Gbps", "price": 300},
    {"name": "Switch 10Gbps 24 ports", "price": 4000},
    {"name": "Routeur DSL avec VoIP", "price": 120},
    {"name": "Point d’accès Wi-Fi extérieur", "price": 180},
    {"name": "Contrôleur réseau SDN", "price": 1500},
    {"name": "Module transceiver RJ45", "price": 50},
    {"name": "Module transceiver SFP", "price": 100},
    {"name": "Boîtier fibre optique", "price": 200},
    {"name": "Router Core pour data center", "price": 8000},
    {"name": "Firewall UTM", "price": 2500},
    {"name": "Switch stackable 12 ports", "price": 600},
    {"name": "Câble HDMI réseau (Ethernet)", "price": 30},
    {"name": "Serveur proxy", "price": 0},
    {"name": "Routeur sans fil 802.11ax", "price": 150},
    {"name": "Switch KVM (contrôle clavier)", "price": 120},
    {"name": "Contrôleur réseau cloud", "price": 1000},
    {"name": "Module Power over Ethernet (PoE)", "price": 60},
    {"name": "Antenne Wi-Fi 6 interne", "price": 40},
    {"name": "Câble réseau blindé Cat7", "price": 20},
    {"name": "Switch modulaire", "price": 2000},
    {"name": "Firewall de nouvelle génération", "price": 3000}
]

with app.app_context():
    # Vérifie si la table est déjà remplie
    if Device.query.count() == 0:
        for d in devices:
            device = Device(name=d["name"], price=d["price"])
            db.session.add(device)
        db.session.commit()
        print(f"✅ {len(devices)} périphériques insérés avec succès.")
    else:
        print("⚠️ La table Device n'est pas vide, insertion ignorée.")
