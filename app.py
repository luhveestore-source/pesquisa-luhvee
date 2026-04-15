import streamlit as st
import urllib.parse
import requests
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

# --- LINK DO SEU SHEETDB INTEGRADO ---
API_URL = "https://sheetdb.io/api/v1/4s035f0bwuwxy" 

SEU_WHATSAPP = "5511948021428"
CENTRALIZADOR = "https://luhveestore-unbgvh5h.manus.space"
INSTAGRAM = "@luhveestore"
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
    email = st.text_input("Seu melhor E-mail")
    escolha = st.selectbox("O que você procura hoje?", list(produtos.keys()))
    plataforma = st.radio("Onde prefere comprar?", ["Shopee", "Mercado Livre", "WhatsApp Direto"])
    submit = st.form_submit_button("CONCLUIR PESQUISA ❤️")

if submit:
    if nome and whatsapp and email:
        # Dados para enviar ao SheetDB (Devem ser iguais aos títulos da sua planilha)
        payload = {
            "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "CLIENTE": nome.upper(),
            "WHATSAPP": whatsapp,
            "E-MAIL": email.lower(),
            "INTERESSE": escolha,
            "LOJA": plataforma
        }
        
        try:
            # Envia os dados para a planilha
            res = requests.post(API_URL, json={"data": [payload]})
            if res.status_code == 201:
                st.success("Dados salvos com sucesso na planilha! ✅")
            else:
                st.warning("Recebemos sua pesquisa! Clique no botão abaixo para o link.")
        except:
            st.error("Erro ao conectar com o banco de dados, mas você pode seguir pelo WhatsApp.")

        # Preparação do link de redirecionamento
        link_final = LINK_SHOPEE if plataforma == "Shopee" else LINK_ML if plataforma == "Mercado Livre" else f"https://wa.me/{SEU_WHATSAPP}"
        
        texto_zap = (
            f"Olá {nome.upper()}! ❤️\n\n"
            f"Aqui está sua vitrine de *{escolha}* na {plataforma}:\n"
            f"👉 {link_final}\n\n"
            f"LuhVee Stores agradece seu carinho! ❤️🌸"
        )
        
        msg_encoded = urllib.parse.quote(texto_zap, safe='')
        num_limpo = "".join(filter(str.isdigit, whatsapp))
        if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
        
        st.link_button("🎁 CLIQUE PARA RECEBER NO WHATSAPP", f"https://wa.me/{num_limpo}?text={msg_encoded}")
    else:
        st.error("❌ Por favor, preencha todos os campos.")
