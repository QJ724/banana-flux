import streamlit as st
import requests
import io
from PIL import Image

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Wimbly Studio BETA", page_icon="W")

st.title("Wimbly Studio BETA")
st.write("Genera immagini incredibili usando l'AI.")
st.write("Modello: FLUX.1-schnell di Hugging Face")


# --- RECUPERO LA CHIAVE SEGRETA ---
# Il codice cerca la chiave nei "Secrets" di Streamlit Cloud
try:
    hf_token = st.secrets["HF_TOKEN"]
except:
    # Se siamo sul tuo PC e non hai impostato i secrets, te la chiede a mano
    st.warning("⚠️ Chiave segreta non trovata. Inseriscila manualmente.")
    hf_token = st.text_input("Hugging Face Token", type="password")

# --- AREA PRINCIPALE ---
prompt = st.text_area(
    "Descrivi la tua immagine:", 
    "Un gatto cyberpunk che beve caffè al neon, realistico",
    height=100
)

API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

def query_hugging_face(payload, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

if st.button("✨ Genera Immagine", type="primary"):
    if not hf_token:
        st.error("Chiave mancante!")
    else:
        with st.spinner('L\'AI sta disegnando per te...'):
            try:
                image_bytes = query_hugging_face({"inputs": prompt}, hf_token)
                
                if b"error" in image_bytes:
                    st.error(f"Errore momentaneo del server AI. Riprova tra poco!")
                else:
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption="Generata da AI", use_container_width=True)
                    
                    # Bottone Download
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button(
                        label="⬇️ Scarica in HD",
                        data=buf.getvalue(),
                        file_name="wimblyfile.png",
                        mime="image/png"
                    )

            except Exception as e:
                st.error(f"Qualcosa è andato storto: {e}")