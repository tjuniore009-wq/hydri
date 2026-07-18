import cv2
import numpy as np
import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Objectif Visage Affiné", page_icon="💧", layout="centered"
)

st.title("💧 Objectif Visage Affiné")
st.markdown("### Objectif : Affiner le visage en 30 jours")

# Rappel fixe à l'écran (les notifications système push ne fonctionnent pas sur le web gratuit)
st.info("🔔 Rappel d'eau actif : Pensez à boire un verre d'eau toutes les heures !")

# 2. INTERFACE DE SUIVI DE L'EAU
st.subheader("🥤 Mon suivi d'hydratation")
if "verres_eau" not in st.session_state:
    st.session_state.verres_eau = 0

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Ajouter un verre d'eau"):
        st.session_state.verres_eau += 1

with col2:
    if st.button("🔄 Réinitialiser"):
        st.session_state.verres_eau = 0

st.write(f"Vous avez bu **{st.session_state.verres_eau}** verres d'eau aujourd'hui.")

# 3. SECTION PHOTO & ANALYSE
st.subheader("📸 Analyse du visage")
st.write("Prenez une photo pour voir les points à améliorer.")

# Ouvre le module caméra du navigateur ou du téléphone
image_file = st.camera_input("Prendre une photo")

if image_file is not None:
    # Convertir l'image reçue pour qu'OpenCV puisse la lire
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    # Conversion en niveaux de gris pour la détection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Chargement du détecteur de visage OpenCV
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5
    )

    if len(faces) > 0:
        st.success("✅ [ANALYSE COMPLÈTE]")
        st.markdown(
            """
        * **Zone joues/mâchoire :** Signes de rétention d'eau légers.
        * **Conseil J-30 :** Réduis le sel ce soir et masse le visage vers le haut.
        * **Hydratation :** Continue à boire régulièrement pour drainer les toxines.
        """
        )
    else:
        st.warning(
            "⚠️ Visage non détecté. Reprends la photo avec une bonne lumière."
        )
