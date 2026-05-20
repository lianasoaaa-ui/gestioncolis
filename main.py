# =====================================================
# GESTION DES COLIS MADAGASCAR
# VERSION COMPLETE AVEC LOGIN + IMPRESSION
# =====================================================


from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard

from datetime import datetime
import json
import os
# 🔥 AJOUT PDF
from reportlab.pdfgen import canvas
from android.storage import primary_external_storage_path

Window.clearcolor = (1,1,1,1)

# =====================================================
# FICHIERS
# =====================================================

FICHIER_COLIS = "colis.json"
FICHIER_USER = "users.json"

# =====================================================
# VILLES
# =====================================================

villes_madagascar = [

    "Antananarivo",
    "Toamasina",
    "Mahajanga",
    "Fianarantsoa",
    "Toliara",
    "Antsiranana",
    "Antsirabe",
    "Morondava",
    "Sambava",
    "Nosy Be",
    "ambanja",
    "antsalaka",

]

# =====================================================
# UTILISATEURS
# =====================================================

def charger_users():

    if os.path.exists(FICHIER_USER):

        try:

            with open(FICHIER_USER, "r") as f:

                return json.load(f)

        except:

            return {}

    return {}

def sauvegarder_users(data):

    with open(FICHIER_USER, "w") as f:

        json.dump(data, f)

# =====================================================
# LOGIN SCREEN
# =====================================================

class LoginScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20
        )

        titre = Label(
            text="CONNEXION",
            font_size=30,
            color=(0,0,1,1)
        )

        self.username = TextInput(
            hint_text="Nom utilisateur",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.password = TextInput(
            hint_text="Mot de passe",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=50
        )

        btn_login = Button(
            text="SE CONNECTER",
            size_hint_y=None,
            height=60,
            background_color=(0,1,0,1)
        )

        btn_register = Button(
            text="CREER COMPTE",
            size_hint_y=None,
            height=60,
            background_color=(0,0.5,1,1)
        )

        btn_login.bind(on_press=self.login)
        btn_register.bind(on_press=self.register)

        layout.add_widget(titre)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(btn_login)
        layout.add_widget(btn_register)

        self.add_widget(layout)

    def login(self, instance):

        users = charger_users()

        user = self.username.text.strip()
        pwd = self.password.text.strip()

        if user in users and users[user] == pwd:

            self.manager.current = "gestion"

        else:

            popup = Popup(
                title="Erreur",
                content=Label(
                    text="Nom ou mot de passe incorrect"
                ),
                size_hint=(0.7,0.3)
            )

            popup.open()

    def register(self, instance):

        users = charger_users()

        user = self.username.text.strip()
        pwd = self.password.text.strip()

        if user == "" or pwd == "":

            popup = Popup(
                title="Erreur",
                content=Label(
                    text="Remplir tous les champs"
                ),
                size_hint=(0.7,0.3)
            )

            popup.open()

            return

        if user in users:

            popup = Popup(
                title="Erreur",
                content=Label(
                    text="Utilisateur existe déjà"
                ),
                size_hint=(0.7,0.3)
            )

            popup.open()

            return

        users[user] = pwd

        sauvegarder_users(users)

        popup = Popup(
            title="Succès",
            content=Label(
                text="Compte créé"
            ),
            size_hint=(0.7,0.3)
        )

        popup.open()

# =====================================================
# GESTION COLIS
# =====================================================


    
    
    
class GestionColis(BoxLayout):

    def alerte_colis(self, lieu):

        son = SoundLoader.load("alerte.mp3")

        if son:
            son.play()

        popup = Popup(
            title="ALERTE COLIS",
            content=Label(
                text=f"Le colis est arrivé à {lieu}"
            ),
            size_hint=(0.8, 0.4)
        )
      
        popup.open()
    
    
    

    def __init__(self, **kwargs):

        super().__init__(orientation='vertical', **kwargs)

        self.colis_data = []

        self.charger_donnees()

        self.search = TextInput(
            hint_text="Recherche colis ou mpanera...",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.search.bind(
            text=self.rechercher_colis
        )

        self.add_widget(self.search)

        scroll = ScrollView()

        self.layout = GridLayout(
            cols=2,
            spacing=10,
            padding=10,
            size_hint_y=None
        )

        self.layout.bind(
            minimum_height=self.layout.setter('height')
        )

        self.layout.add_widget(
            Label(text="Date", color=(0,0,0,1))
        )

        self.date_spinner = Spinner(
            text=datetime.now().strftime("%d/%m/%Y"),
            values=[datetime.now().strftime("%d/%m/%Y")],
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(self.date_spinner)

        self.layout.add_widget(
            Label(text="Départ", color=(0,0,0,1))
        )

        self.depart = Spinner(
            text="Choisir départ",
            values=villes_madagascar,
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(self.depart)

        self.layout.add_widget(
            Label(text="Vers", color=(0,0,0,1))
        )

        self.vers = Spinner(
            text="Choisir destination",
            values=villes_madagascar,
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(self.vers)

        self.numero_colis = self.add_input("Numéro colis")
        self.nom_mpandefa = self.add_input("Nom mpandefa")
        self.tel_mpandefa = self.add_input("Téléphone mpandefa")

        self.nom_mpaka = self.add_input("Nom mpaka")
        self.tel_mpaka = self.add_input("Téléphone mpaka")

        self.karazana = self.add_input("Karazana entana")
        self.isany = self.add_input("Isany")

        self.layout.add_widget(
            Label(text="Toerana", color=(0,0,0,1))
        )

        # ============================
        # TOERANA PAR CASE VIDE
        # ============================

        self.toerana = TextInput(
            hint_text="Saisir toerana",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(self.toerana)

        self.frais = self.add_input("Frais")
        self.paye = self.add_input("PAYE")
        self.pa = self.add_input("P.A")

        self.mpanera = self.add_input("Mpanera")
        self.prix = self.add_input("Prix")
        self.prix_booste = self.add_input("Prix booste")

        self.layout.add_widget(
            Label(text="Pourcentage", color=(0,0,0,1))
        )

        self.pourcentage = Spinner(
            text="1%",
            values=[f"{i}%" for i in range(1,101)],
            size_hint_y=None,
            height=50
        )

        self.pourcentage.bind(
            text=self.calcul_pourcentage
        )

        self.layout.add_widget(self.pourcentage)

        self.layout.add_widget(
            Label(text="Montant %", color=(0,0,0,1))
        )

        self.resultat_pourcentage = TextInput(
            readonly=True,
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(self.resultat_pourcentage)

        # =====================================================
        # BOUTONS
        # =====================================================

        self.btn_save = Button(
            text="ENREGISTRER",
            size_hint_y=None,
            height=60,
            background_color=(0,1,0,1)
        )

        self.btn_save.bind(
            on_press=self.enregistrer
        )

        self.layout.add_widget(self.btn_save)

        self.btn_actualiser = Button(
            text="ACTUALISER",
            size_hint_y=None,
            height=60,
            background_color=(0,0.5,1,1)
        )

        self.btn_actualiser.bind(
            on_press=self.actualiser_tout
        )

        self.layout.add_widget(self.btn_actualiser)

        self.layout.add_widget(
            Label(
                text="LISTE DES COLIS",
                color=(0,0,1,1),
                size_hint_y=None,
                height=60
            )
        )

        self.layout.add_widget(Label())

        self.liste_container = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )

        self.liste_container.bind(
            minimum_height=self.liste_container.setter('height')
        )

        self.layout.add_widget(self.liste_container)

        scroll.add_widget(self.layout)

        self.add_widget(scroll)

        self.afficher_listes()

    # =====================================================
    # INPUT
    # =====================================================

    def add_input(self, titre):

        self.layout.add_widget(
            Label(text=titre, color=(0,0,0,1))
        )

        champ = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(champ)

        return champ

    # =====================================================
    # SAUVEGARDE
    # =====================================================

    def sauvegarder_donnees(self):

        with open(FICHIER_COLIS, "w") as fichier:

            json.dump(self.colis_data, fichier)

    # =====================================================
    # CHARGER
    # =====================================================

    def charger_donnees(self):

        if os.path.exists(FICHIER_COLIS):

            try:

                with open(FICHIER_COLIS, "r") as fichier:

                    self.colis_data = json.load(fichier)

            except:

                self.colis_data = []

    # =====================================================
    # CALCUL %
    # =====================================================

    def calcul_pourcentage(self, *args):

        try:

            prix = float(self.prix.text or 0)

            p = int(
                self.pourcentage.text.replace("%","")
            )

            resultat = (prix * p) / 100

            self.resultat_pourcentage.text = str(resultat)

        except:

            self.resultat_pourcentage.text = "0"

    # =====================================================
    # ENREGISTRER
    # =====================================================

    def enregistrer(self, instance):

        colis = {

            "date": self.date_spinner.text,
            "depart": self.depart.text,
            "vers": self.vers.text,

            "numero": self.numero_colis.text,

            "mpandefa": self.nom_mpandefa.text,
            "tel_mpandefa": self.tel_mpandefa.text,

            "mpaka": self.nom_mpaka.text,
            "tel_mpaka": self.tel_mpaka.text,

            "karazana": self.karazana.text,
            "isany": self.isany.text,

            "toerana": self.toerana.text,

            "frais": self.frais.text,
            "paye": self.paye.text,
            "pa": self.pa.text,

            "mpanera": self.mpanera.text,
            "prix": self.prix.text,
            "prix_booste": self.prix_booste.text,

            "pourcentage": self.resultat_pourcentage.text

        }

        self.colis_data.append(colis)

        self.sauvegarder_donnees()
        # ============================
        # ALERTE AUTOMATIQUE
        # ============================

        lieux_alertes = [
            "Antsirabe",
            "Mahajanga",
            "itaosy",
            "Toamasina",
            "Toliara"
        ]

        if self.toerana.text.strip() in lieux_alertes:
            self.alerte_colis(self.toerana.text)

        self.afficher_listes()

        popup = Popup(
            title="Succès",
            content=Label(text="Colis enregistré"),
            size_hint=(0.7,0.3)
        )

        popup.open()

        self.actualiser(None)
  
# =====================================================
    # IMPRESSION PDF (AMÉLIORÉE)
    # =====================================================

    def imprimer_un_colis(self, colis):

        try:
            base_path = primary_external_storage_path()
            download_dir = os.path.join(base_path, "Download")

            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            file_path = os.path.join(download_dir, f"COLIS_{colis.get('numero','')}.pdf")

            c = canvas.Canvas(file_path)

            y = 800

            c.setFont("Helvetica-Bold", 16)
            c.drawString(200, y, "FICHE COLIS")
            y -= 40

            c.setFont("Helvetica", 11)

            def ligne(label, value):
                nonlocal y
                c.drawString(50, y, f"{label} : {value}")
                y -= 18

            ligne("NUMERO", colis.get("numero",""))
            ligne("MPANDEFA", colis.get("mpandefa",""))
            ligne("TEL MPANDEFA", colis.get("tel_mpandefa",""))

            y -= 10
            ligne("MPAKA", colis.get("mpaka",""))
            ligne("TEL MPAKA", colis.get("tel_mpaka",""))

            y -= 10
            ligne("KARAZANA", colis.get("karazana",""))
            ligne("ISANY", colis.get("isany",""))
            ligne("TOERANA", colis.get("toerana",""))

            y -= 10
            ligne("FRAIS", f"{colis.get('frais','')} Ar")
            ligne("PAYE", f"{colis.get('paye','')} Ar")
            ligne("P.A", f"{colis.get('pa','')} Ar")

            y -= 10
            ligne("MPANERA", colis.get("mpanera",""))
            ligne("PRIX", f"{colis.get('prix','')} Ar")
            ligne("BOOSTE", f"{colis.get('prix_booste','')} Ar")

            c.save()

            Popup(
                title="Impression PDF",
                content=Label(text=f"PDF créé dans Download\nCOLIS_{colis.get('numero','')}.pdf"),
                size_hint=(0.8,0.4)
            ).open()

        except Exception as e:
            Popup(title="Erreur", content=Label(text=str(e)), size_hint=(0.8,0.4)).open()

  
            # =====================================================
    # ACTUALISER
    # =====================================================

    def actualiser(self, instance):

        self.numero_colis.text = ""
        self.nom_mpandefa.text = ""
        self.tel_mpandefa.text = ""

        self.nom_mpaka.text = ""
        self.tel_mpaka.text = ""

        self.karazana.text = ""
        self.isany.text = ""

        self.frais.text = ""
        self.paye.text = ""
        self.pa.text = ""

        self.mpanera.text = ""
        self.prix.text = ""
        self.prix_booste.text = ""

        self.resultat_pourcentage.text = ""

    def actualiser_tout(self, instance):

        self.actualiser(None)

        self.search.text = ""

        self.afficher_listes()

    # =====================================================
    # MODIFIER
    # =====================================================

    def remplir_champs(self, colis):

        self.numero_colis.text = colis.get("numero","")
        self.nom_mpandefa.text = colis.get("mpandefa","")
        self.tel_mpandefa.text = colis.get("tel_mpandefa","")

        self.nom_mpaka.text = colis.get("mpaka","")
        self.tel_mpaka.text = colis.get("tel_mpaka","")

        self.karazana.text = colis.get("karazana","")
        self.isany.text = colis.get("isany","")

        self.toerana.text = colis.get("toerana","")

        self.frais.text = colis.get("frais","")
        self.paye.text = colis.get("paye","")
        self.pa.text = colis.get("pa","")

        self.mpanera.text = colis.get("mpanera","")
        self.prix.text = colis.get("prix","")
        self.prix_booste.text = colis.get("prix_booste","")

        self.resultat_pourcentage.text = str(
            colis.get("pourcentage",0)
        )

    # =====================================================
    # SUPPRIMER
    # =====================================================

    def supprimer_ligne(self, colis):

        if colis in self.colis_data:

            self.colis_data.remove(colis)

        self.sauvegarder_donnees()

        self.afficher_listes()

    # =====================================================
    # RECHERCHE COMPLETE
    # =====================================================

    def rechercher_colis(self, instance, valeur):

        valeur = valeur.lower().strip()

        self.liste_container.clear_widgets()

        if valeur == "":

            self.afficher_listes()

            return

        total_prix = 0
        total_pct = 0
        total_booste = 0

        nom_mpanera = ""

        for colis in self.colis_data:

            if (
               valeur in colis.get("date","").lower()or
               

                valeur in colis.get("numero","").lower()
                or valeur in colis.get("mpandefa","").lower()
                or valeur in colis.get("tel_mpandefa","").lower()
                or valeur in colis.get("mpaka","").lower()
                or valeur in colis.get("tel_mpaka","").lower()
                or valeur in colis.get("mpanera","").lower()
                or valeur in colis.get("toerana","").lower()

            ):

                nom_mpanera = colis.get("mpanera","")

                try:
                    prix = float(colis.get("prix",0))
                except:
                    prix = 0

                try:
                    pct = float(
                        colis.get("pourcentage",0)
                    )
                except:
                    pct = 0

                try:
                    booste = float(
                        colis.get("prix_booste",0)
                    )
                except:
                    booste = 0

                total_prix += prix
                total_pct += pct
                total_booste += booste

                card = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=850,
                    padding=10,
                    spacing=10
                )

                texte = Label(

                    text=(
                        f"[b]DATE : {colis.get('date','')}[/b]\n\n"

                        f"[b]{colis.get('numero','')}[/b]\n\n"

                        f"MPANDEFA : {colis.get('mpandefa','')}\n"
                        f"TEL MPANDEFA : {colis.get('tel_mpandefa','')}\n\n"

                        f"MPAKA : {colis.get('mpaka','')}\n"
                        f"TEL MPAKA : {colis.get('tel_mpaka','')}\n\n"

                        f"KARAZANA : {colis.get('karazana','')}\n"
                        f"ISANY : {colis.get('isany','')}\n"

                        f"FRAIS : {colis.get('frais','')} Ar\n"
                        f"PAYE : {colis.get('paye','')} Ar\n"
                        f"P.A : {colis.get('pa','')} Ar\n\n"

                        f"TOERANA : {colis.get('toerana','')}\n\n"

                        f"MPANERA : {colis.get('mpanera','')}\n"
                        f"PRIX : {colis.get('prix',0)} Ar\n"
                        f"PRIX BOOSTE : {colis.get('prix_booste',0)} Ar\n"
                        f"POURCENTAGE : {colis.get('pourcentage',0)} Ar"

                    ),

                    markup=True,
                    color=(0,0,0,1),
                    halign="left",
                    valign="top",
                    text_size=(550,None),
                    size_hint_y=None

                )

                texte.bind(
                    texture_size=texte.setter('size')
                )

                boutons = BoxLayout(
                    size_hint_y=None,
                    height=50,
                    spacing=5
                )

                btn_modifier = Button(
                    text="MODIFIER",
                    background_color=(1,0.5,0,1)
                )

                btn_modifier.bind(
                    on_press=lambda x, c=colis:
                    self.remplir_champs(c)
                )

                btn_supprimer = Button(
                    text="SUPPRIMER",
                    background_color=(1,0,0,1)
                )

                btn_supprimer.bind(
                    on_press=lambda x, c=colis:
                    self.supprimer_ligne(c)
                )

                btn_imprimer = Button(
                    text="IMPRIMER",
                    background_color=(0.5,0,1,1)
                )

                btn_imprimer.bind(
                    on_press=lambda x, c=colis:
                    self.imprimer_un_colis(c)
                )

                boutons.add_widget(btn_modifier)
                boutons.add_widget(btn_supprimer)
                boutons.add_widget(btn_imprimer)

                card.add_widget(texte)
                card.add_widget(boutons)

                self.liste_container.add_widget(card)

        total_label = Label(

            text=(

                f"MPANERA : {nom_mpanera}\n"
                f"TOTAL PRIX : {total_prix} Ar\n"
                f"TOTAL BOOSTE : {total_booste} Ar\n"
                f"MONTANT % : {total_pct} Ar"

            ),

            color=(0,0,1,1),
            size_hint_y=None,
            height=150

        )

        self.liste_container.add_widget(total_label)
        # =====================================================
    # AFFICHER
    # =====================================================

    def afficher_listes(self):

        self.liste_container.clear_widgets()

        for i, colis in enumerate(
            self.colis_data,
            start=1
        ):

            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=850,
                padding=10,
                spacing=10
            )

            texte = Label(

                text=(
                    f"[b]DATE : {colis.get('date','')}[/b]\n\n"

                    f"[b]{i}) {colis.get('numero','')}[/b]\n\n"

                    f"MPANDEFA : {colis.get('mpandefa','')}\n"
                    f"TEL MPANDEFA : {colis.get('tel_mpandefa','')}\n\n"

                    f"MPAKA : {colis.get('mpaka','')}\n"
                    f"TEL MPAKA : {colis.get('tel_mpaka','')}\n\n"

                    f"KARAZANA : {colis.get('karazana','')}\n"
                    f"ISANY : {colis.get('isany','')}\n"

                    f"FRAIS : {colis.get('frais','')} Ar\n"
                    f"PAYE : {colis.get('paye','')} Ar\n"
                    f"P.A : {colis.get('pa','')} Ar\n\n"

                    f"TOERANA : {colis.get('toerana','')}\n\n"

                    f"MPANERA : {colis.get('mpanera','')}\n"
                    f"PRIX : {colis.get('prix',0)} Ar\n"
                    f"PRIX BOOSTE : {colis.get('prix_booste',0)} Ar\n"
                    f"POURCENTAGE : {colis.get('pourcentage',0)} Ar"

                ),

                markup=True,
                color=(0,0,0,1),
                halign="left",
                valign="top",
                text_size=(550,None),
                size_hint_y=None

            )

            texte.bind(
                texture_size=texte.setter('size')
            )

            boutons = BoxLayout(
                size_hint_y=None,
                height=50,
                spacing=5
            )

            btn_modifier = Button(
                text="MODIFIER",
                background_color=(1,0.5,0,1)
            )

            btn_modifier.bind(
                on_press=lambda x, c=colis:
                self.remplir_champs(c)
            )

            btn_supprimer = Button(
                text="SUPPRIMER",
                background_color=(1,0,0,1)
            )

            btn_supprimer.bind(
                on_press=lambda x, c=colis:
                self.supprimer_ligne(c)
            )

            btn_imprimer = Button(
                text="IMPRIMER",
                background_color=(0.5,0,1,1)
            )

            btn_imprimer.bind(
                on_press=lambda x, c=colis:
                self.imprimer_un_colis(c)
            )

            boutons.add_widget(btn_modifier)
            boutons.add_widget(btn_supprimer)
            boutons.add_widget(btn_imprimer)

            card.add_widget(texte)
            card.add_widget(boutons)

            self.liste_container.add_widget(card)

# =====================================================
# TOTAUX GENERAUX
# =====================================================

        total_frais = 0
        total_paye = 0
        total_pa = 0

        for colis in self.colis_data:

            try:
                total_frais += float(colis.get("frais", 0))
            except:
                pass

            try:
                total_paye += float(colis.get("paye", 0))
            except:
                pass

            try:
                total_pa += float(colis.get("pa", 0))
            except:
                pass

        total_general = Label(

            text=(

                f"[b]TOTAL GENERAL[/b]\n\n"

                f"TOTAL FRAIS : {total_frais} Ar\n\n"
                f"TOTAL PAYE : {total_paye} Ar\n\n"
                f"TOTAL P.A : {total_pa} Ar"

            ),

            markup=True,
            color=(0,0,1,1),
            halign="center",
            valign="middle",
            text_size=(Window.width - 50, None),
            size_hint_y=None,
            height=250

        )

        self.liste_container.add_widget(total_general)

# =====================================================
# SCREEN GESTION
# =====================================================

class GestionScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.add_widget(GestionColis())

# =====================================================
# APP
# =====================================================

class MonApp(App):

    def build(self):

        sm = ScreenManager()

        sm.add_widget(
            LoginScreen(name="login")
        )

        sm.add_widget(
            GestionScreen(name="gestion")
        )

        return sm

# =====================================================
# EXECUTION
# =====================================================

if __name__ == "__main__":

    MonApp().run()