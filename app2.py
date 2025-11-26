import streamlit as st
import requests
import io
from PIL import Image

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Wimbly Studio BETA", page_icon="W", layout="wide")


# --- RECUPERO LA CHIAVE SEGRETA ---
try:
    hf_token = st.secrets["HF_TOKEN"]
except:
    st.warning("⚠️ Chiave segreta non trovata. Inseriscila manualmente nella sidebar.")
    hf_token = None

# --- IL MENU DEI MODELLI (Il cuore dell'aggiornamento) ---
# Qui colleghiamo nomi facili a URL complessi
MODELS = {
    "🚀 Flux Schnell (Veloce & Realistico)": "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell",
    "🎨 Stable Diffusion XL (Artistico)": "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0",
    "👾 Animagine XL (Stile Anime)": "https://router.huggingface.co/hf-inference/models/cagliostrolab/animagine-xl-3.1"
}

# --- IL MENU DELLE RISOLUZIONI ---
SIZES = {
    "Quadrato (1:1 - Instagram)": (1024, 1024),
    "Paesaggio (16:9 - YouTube)": (1280, 720),
    "Ritratto (9:16 - TikTok/Stories)": (720, 1280),
    "Standard (4:3)": (1024, 768)
}

# --- INTERFACCIA UTENTE ---
st.title("Wimbly Studio BETA")
st.write("Genera immagini incredibili usando l'AI.")


# Dividiamo lo schermo in due colonne (Sidebar e Main)
with st.sidebar:
    st.header("⚙️ Impostazioni")
    
    # 1. Scelta Modello
    selected_model_name = st.selectbox("Scegli il Modello AI", list(MODELS.keys()))
    api_url = MODELS[selected_model_name]
    
    # 2. Scelta Formato
    selected_size_name = st.selectbox("Formato Immagine", list(SIZES.keys()))
    width, height = SIZES[selected_size_name]
    
    st.divider()
    
    # Se non c'è il segreto, mostra l'input manuale
    if not hf_token:
        hf_token = st.text_input("Hugging Face Token", type="password")

# --- LOGICA DI CHIAMATA ---
def query_hugging_face(payload, token, url):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, json=payload)
    return response.content

# --- AREA CENTRALE ---
col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_area(
        "Descrivi la tua immaginazione:", 
        "Un astronauta che cavalca un cavallo su Marte, fotorealistico, 8k, illuminazione cinematografica",
        height=150
    )
    
    generate_btn = st.button("✨ Genera Opera d'Arte", type="primary", use_container_width=True)

with col2:
    st.info(f"**Modello:** {selected_model_name}\n\n**Misure:** {width}x{height}px")

# --- ESECUZIONE ---
if generate_btn:
    if not hf_token:
        st.error("🛑 Manca il Token! Inseriscilo nei Secrets o nella barra laterale.")
    else:
        with st.spinner(f'Sto chiedendo a {selected_model_name} di disegnare...'):
            try:
                # Costruiamo il pacchetto dati con le dimensioni
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "width": width,
                        "height": height
                    }
                }
                
                image_bytes = query_hugging_face(payload, hf_token, api_url)
                
                if b"error" in image_bytes:
                    st.error(f"Errore dal server: {image_bytes}")
                else:
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    # Mostra l'immagine grande
                    st.image(image, caption=f"{selected_model_name}", use_container_width=True)
                    
                    # Bottone Download
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button(
                        label="⬇️ Scarica Immagine",
                        data=buf.getvalue(),
                        file_name="wimblyfile.png",
                        mime="image/png",
                        use_container_width=True
                    )
                    st.success("Creazione completata!")

            except Exception as e:
                st.error(f"Qualcosa è andato storto: {e}")