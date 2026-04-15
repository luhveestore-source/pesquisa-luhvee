import streamlit as st
import urllib.parse
import requests  # <-- Essa linha corrige o erro da foto!
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="LuhVee Stores", page_icon="🛍️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    input, textarea, [data-baseweb="select"] { background-color: #ffffff !important; color: #000000 !important; }
    .stButton>button {
        background-color: #000000 !important; color: #ff69b4 !important; 
        border: 3px solid #ffd700 !important; border-radius: 15px !important;
        width: 100% !important; font-size: 22px !important; font-weight: bold !important; height: 65px !important;
    }
    label, p, h1, h2, h3 { color: #ffffff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
API_URL = "https://sheetdb.io/api/v1/4s035f0bwuwxy" 
SEU_WHATSAPP_NUMERO = "5511948021428"
SEU_EMAIL_CONTATO = "seuemail@exemplo.com" # Coloque seu e-mail aqui
SEU_TELEGRAM_LINK = "https://t.me/seunome" # Coloque seu link do Telegram aqui
CENTRALIZADOR = "https://luhveestore-unbgvh5h.manus.space"
INSTAGRAM = "@luhveestore"
TIKTOK = "@luhvee.stores"
LINK_SHOPEE = "https://collshp.com/luhveestores?view=storefront"
LINK_ML = "https://www.mercadolivre.com.br/social/axwelloliveira"

produtos = {
    "Perfumes e Bodysplash (Fem/Masc)": "Fragrâncias irresistíveis! ✨",
    "Scarpins e Saltos": "Elegância em cada passo! 👠",
    "Moda Adulto e Infantil": "Estilo para toda a família! 👗",
    "Mamãe e Bebê": "Cuidado para os pequenos! 👶",
    "Pets": "Mimos para seu pet! 🐾",
    "Eletrodomésticos": "Tecnologia para o seu lar! 🏠",
    "Cama, Mesa e Banho": "Conforto e elegância! 🛏️",
    "Tênis Adulto e Infantil": "Conforto para o dia a dia! 👟",
    "Informática": "Performance ao seu alcance! 💻",
    "Lingerie": "Autoestima em cada detalhe! 👙",
    "Sexshop": "Momentos especiais com sigilo! 🔥",
    "Brinquedos": "Diversão garantida! 🧸",
    "Outros / Encomenda Especial ✨": "Eu busco o produto dos seus sonhos!"
}

# --- LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("1000396187.jpeg")
    except:
        st.header("✨ LUHVEE STORES")

# --- INTERFACE ---
st.markdown("<h2 style='text-align: center;'>SUA OPINIÃO VALE MUITO ❤️</h2>", unsafe_allow_html=True)

with st.form("form_vendas", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    whatsapp = st.text_input("WhatsApp (com DDD)")
    email_cliente = st.text_input("Seu melhor E-mail")
    escolha = st.selectbox("O que você procura hoje?", list(produtos.keys()))
    plataforma = st.radio("Onde prefere comprar?", ["Shopee", "Mercado Livre", "WhatsApp Direto"])
    submit = st.form_submit_button("FINALIZAR E RECEBER VITRINE ❤️")

if submit:
    if nome and whatsapp and email_cliente:
        # 1. Salva na planilha (SheetDB)
        payload = {
            "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "CLIENTE": nome.upper(),
            "WHATSAPP": whatsapp,
            "E-MAIL": email_cliente.lower(),
            "INTERESSE": escolha,
            "LOJA": plataforma
        }
        try:
            requests.post(API_URL, json={"data": [payload]})
        except:
            pass 

        # 2. Define o Link Principal
        link_final = CENTRALIZADOR if plataforma == "WhatsApp Direto" else LINK_SHOPEE if plataforma == "Shopee" else LINK_ML

        # 3. Monta a Mensagem (Agora com E-mail e Telegram incluídos para o cliente ver)
        texto_zap = (
            f"Olá {nome.upper()}! ❤️\n\n"
            f"Ficamos muito felizes com sua participação! 🥰\n\n"
            f"Aqui está o acesso para *{escolha}*:\n👉 {link_final}\n\n"
            f"🔗 Central de Links: {CENTRALIZADOR}\n"
            f"📱 WhatsApp: {SEU_WHATSAPP_NUMERO}\n"
            f"✈️ Telegram: {SEU_TELEGRAM_LINK}\n"
            f"✉️ E-mail: {SEU_EMAIL_CONTATO}\n\n"
            f"Siga-nos:\n📸 Insta: {INSTAGRAM} | 🎥 TikTok: {TIKTOK}\n\n"
            f"LuhVee Stores agradece! ❤️🌸"
        )
        
        msg_encoded = urllib.parse.quote(texto_zap, safe='')
        num_limpo = "".join(filter(str.isdigit, whatsapp))
        if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
        
        link_whatsapp = f"https://wa.me/{num_limpo}?text={msg_encoded}"

        # Redirecionamento Automático
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={link_whatsapp}">', unsafe_allow_html=True)
        st.success("Abrindo seu WhatsApp... ❤️")
        st.link_button("Clique aqui se não abrir sozinho", link_whatsapp)
    else:
        st.error("❌ Por favor, preencha todos os campos.")
