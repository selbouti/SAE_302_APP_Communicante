VoitureView
===========

Cette page documente la vue ``VoitureView`` utilisée pour gérer
la voiture associée à un utilisateur.

---

Création de la vue
------------------

La vue hérite de ``QWidget`` et reçoit la fenêtre principale
afin de permettre la navigation.

.. code-block:: python

   class VoitureView(QWidget):
       def __init__(self, main_window):
           super().__init__()
           self.main_window = main_window

---

Titre de la vue
---------------

Un titre centré est affiché en haut de la vue.

.. code-block:: python

   title = QLabel("🚗 Ma voiture")
   title.setAlignment(Qt.AlignCenter)

---

Champs de saisie du véhicule
----------------------------

Les informations du véhicule sont stockées dans des champs texte.

.. code-block:: python

   self.marque = QLineEdit()
   self.modele = QLineEdit()
   self.chevaux = QLineEdit()
   self.places_totales = QLineEdit()
   self.taux_co2 = QLineEdit()
   self.plaque = QLineEdit()

---

Choix de la motorisation
------------------------

La motorisation est sélectionnée via une liste déroulante.

.. code-block:: python

   self.motorisation = QComboBox()
   self.motorisation.addItems(
       ["thermique", "hybride", "electrique", "hydrogene"]
   )

---

Mode lecture seule par défaut
-----------------------------

Les champs sont verrouillés tant que l'utilisateur n'a pas activé
le mode édition.

.. code-block:: python

   for field in self.fields:
       field.setReadOnly(True)

   self.motorisation.setEnabled(False)

---

Boutons d'action
----------------

Les boutons permettent de modifier, enregistrer, supprimer
ou revenir au profil.

.. code-block:: python

   self.btn_edit = QPushButton("✏️ Modifier")
   self.btn_save = QPushButton("💾 Enregistrer")
   self.btn_delete = QPushButton("❌ Supprimer")
   self.btn_back = QPushButton("⬅ Retour")

---

Activation du mode édition
--------------------------

Lorsque l'utilisateur clique sur **Modifier**, les champs deviennent éditables.

.. code-block:: python

   def enable_edit(self):
       for field in self.fields:
           field.setReadOnly(False)
       self.motorisation.setEnabled(True)

---

Enregistrement de la voiture
----------------------------

Les données sont envoyées à l'API après conversion des champs numériques.

.. code-block:: python

   data = {
       "marque": self.marque.text(),
       "modele": self.modele.text(),
       "chevaux_fiscaux": int(self.chevaux.text()),
       "places_totales": int(self.places_totales.text()),
       "taux_co2": int(self.taux_co2.text()),
       "motorisation": self.motorisation.currentText(),
       "plaque": self.plaque.text()
   }

---

Appel au contrôleur voiture
---------------------------

Le contrôleur est responsable de l'envoi des données au serveur.

.. code-block:: python

   VoitureController.save_voiture(user_id, data)

---

Suppression du véhicule
-----------------------

La voiture associée à l'utilisateur peut être supprimée.

.. code-block:: python

   VoitureController.delete_voiture(user_id)

---

Retour vers le profil
---------------------

Le bouton **Retour** permet de revenir à la vue Profil.

.. code-block:: python

   self.main_window.switch_to("profile")

---

Chargement automatique des données
----------------------------------

Les données du véhicule sont chargées lorsque la vue devient visible.

.. code-block:: python

   def showEvent(self, event):
       super().showEvent(event)
       resp, status = VoitureController.get_voiture(user_id)

---

Remplissage des champs
----------------------

Les champs sont remplis à partir des données reçues depuis l'API.

.. code-block:: python

   self.marque.setText(v.get("marque", ""))
   self.chevaux.setText(str(v.get("chevaux_fiscaux", "")))
   self.taux_co2.setText(str(v.get("taux_co2", "")))
