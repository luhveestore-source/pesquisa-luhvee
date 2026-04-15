import streamlit as st
import urllib.parse
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
        width: 100% !important; font-size: 18px !important; font-weight: bold !important; height: 70px !important;
    }
    label, p, h1, h2, h3 { color: #ffffff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
SEU_WHATSAPP_NUMERO = "5511948021428"
CENTRALIZADOR = "https://luhveestore-unbgvh5h.manus.space"
INSTAGRAM = "@luhveestore"
TIKTOK = "@luhvee.stores"
LINK_SHOPEE = "https://collshp.com/luhveestores?view=storefront"
LINK_ML = "https://www.mercadolivre.com.br/social/axwelloliveira"

# --- LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("1000396187.jpeg")
    except:
        st.header("✨ LUHVEE STORES")

st.markdown("<h2 style='text-align: center;'>SUA OPINIÃO VALE MUITO ❤️</h2>", unsafe_allow_html=True)

# --- FORMULÁRIO ---
with st.form("form_vendas", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    whatsapp = st.text_input("WhatsApp (com DDD)")
    email = st.text_input("Seu melhor E-mail")
    escolha = st.selectbox("O que você procura hoje?", [
        "Perfumes e Bodysplash", "Scarpins e Saltos", "Moda Adulto e Infantil", 
        "Tênis Adulto e Infantil", "Lingerie e Sexshop", "Outros / Encomenda Especial ✨"
    ])
    plataforma = st.radio("Onde prefere comprar?", ["Shopee", "Mercado Livre", "WhatsApp Direto"])
    
    submit = st.form_submit_button("RECEBA PROMOÇÕES DIÁRIAS DA LUHVEE STORES ❤️")

if submit:
    if nome and whatsapp:
        # Define o link baseado na escolha
        link_final = CENTRALIZADOR if plataforma == "WhatsApp Direto" else LINK_SHOPEE if plataforma == "Shopee" else LINK_ML
        
        # Monta a mensagem
        texto_zap = (
            f"Olá {nome.upper()}! ❤️\n\n"
            f"Obrigada por participar! 🥰\n\n"
            f"Aqui está o seu acesso para *{escolha}*:\n👉 {link_final}\n\n"
            f"🔗 Central de Links: {CENTRALIZADOR}\n"
            f"📱 Meu Whats: {SEU_WHATSAPP_NUMERO}\n\n"
            f"Siga-nos:\n📸 Insta: {INSTAGRAM} | 🎥 TikTok: {TIKTOK}\n\n"
            f"LuhVee Stores agradece! ❤️🌸"
        )
        
        msg_encoded = urllib.parse.quote(texto_zap)
        num_limpo = "".join(filter(str.isdigit, whatsapp))
        if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
        
        link_whatsapp = f"https://wa.me/{num_limpo}?text={msg_encoded}"
        
        # Redirecionamento limpo
        st.success("Tudo pronto! Redirecionando para as promoções... 🚀")
        st.markdown(f'<meta http-equiv="refresh" content="1;URL={link_whatsapp}">', unsafe_allow_html=True)
        st.link_button("CLIQUE AQUI PARA ENTRAR NO WHATSAPP", link_whatsapp)
    else:
        st.error("❌ Por favor, preencha o Nome e o WhatsApp.")
