import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="LuhVee Stores", page_icon="🛍️", layout="centered")

# CSS para Corrigir o Botão e o Visual do Dashboard
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    /* Campos de texto brancos para contraste no fundo preto */
    input, textarea, [data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* BOTÃO DE CONCLUIR - AGORA VISÍVEL E BONITO */
    .stButton>button {
        background-color: #000000 !important; 
        color: #ff69b4 !important; 
        border: 3px solid #ffd700 !important;
        border-radius: 15px !important;
        width: 100% !important;
        font-size: 24px !important;
        font-weight: bold !important;
        height: 70px !important;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        background-color: #ff69b4 !important;
        color: #000000 !important;
    }

    label, p, h1, h2, h3 { color: #ffffff !important; font-weight: bold; }
    
    /* Estilo para a tabela do Dashboard */
    [data-testid="stTable"] { background-color: #ffffff; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE MEMÓRIA (DASHBOARD) ---
if 'banco_dados' not in st.session_state:
    st.session_state['banco_dados'] = []

# --- CONFIGURAÇÕES ---
SEU_WHATSAPP = "5511948021428"
CENTRALIZADOR = "https://luhveestore-unbgvh5h.manus.space"
INSTAGRAM = "@luhveestore"
TIKTOK = "@luhvee.stores"
LINK_SHOPEE = "https://collshp.com/luhveestores?view=storefront"
LINK_ML = "https://www.mercadolivre.com.br/social/axwelloliveira"
SENHA_ADMIN = "luhvee2026"

produtos = {
    "Perfumes e Bodysplash (Fem/Masc)": "Fragrâncias irresistíveis! ✨",
    "Scarpins e Saltos": "Elegância em cada passo! 👠",
    "Moda Adulto e Infantil": "Estilo para toda a família! 👗",
    "Mamãe e Bebê": "Cuidado para os pequenos! 👶",
    "Pets": "Mimos para seu pet! 🐾",
    "Outros": "Diga-nos o que deseja! ✨"
}

# --- LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("1000396187.jpeg")
    except:
        st.header("✨ LUHVEE STORES")

# --- MENU ---
menu = st.sidebar.radio("Ir para:", ["Fazer Pesquisa", "Ver Dashboard (ADM)"])

if menu == "Fazer Pesquisa":
    st.markdown("<h2 style='text-align: center;'>SUA OPINIÃO VALE MUITO ❤️</h2>", unsafe_allow_html=True)
    
    with st.form("main_form"):
        nome = st.text_input("Nome Completo")
        whatsapp = st.text_input("WhatsApp (com DDD)")
        escolha = st.selectbox("Qual categoria você quer ver?", list(produtos.keys()))
        plataforma = st.radio("Onde você prefere comprar?", ["Shopee", "Mercado Livre", "WhatsApp Direto"])
        
        st.write("---")
        st.write("📢 *QUASE LÁ! CLIQUE ABAIXO PARA FINALIZAR:*")
        submit = st.form_submit_button("FINALIZAR PESQUISA 💖")

    if submit:
        if nome and whatsapp:
            # SALVAR NO DASHBOARD
            novo_lead = {
                "Data": datetime.now().strftime("%d/%m %H:%M"),
                "Cliente": nome,
                "Whats": whatsapp,
                "Interesse": escolha,
                "Loja": plataforma
            }
            st.session_state['banco_dados'].append(novo_lead)
            
            # EFEITO ESPECIAL (Chuva de Neve/Brilho)
            st.snow() 
            
            st.markdown(f"<h1 style='color: #ff69b4;'>OBRIGADA, {nome.upper()}! 🥰</h1>", unsafe_allow_html=True)
            
            link_final = LINK_SHOPEE if plataforma == "Shopee" else LINK_ML if plataforma == "Mercado Livre" else f"https://wa.me/{SEU_WHATSAPP}"
            
            # MENSAGEM DO WHATSAPP
            texto = (
                f"Olá {nome}! ❤️\n\n"
                f"Ficamos felizes com sua participação! 🥰\n\n"
                f"Aqui está sua vitrine ({plataforma}):\n"
                f"👉 {link_final}\n\n"
                f"Central de Links:\n🔗 {CENTRALIZADOR}\n\n"
                f"Siga-nos:\n📸 Instagram: {INSTAGRAM}\n🎥 TikTok: {TIKTOK}\n\n"
                f"LuhVee Stores agradece! ❤️🌸"
            )
            
            msg_link = urllib.parse.quote(texto)
            num = "".join(filter(str.isdigit, whatsapp))
            if not num.startswith("55"): num = "55" + num
            
            st.link_button("🎁 CLIQUE AQUI PARA RECEBER SEU LINK", f"https://wa.me/{num}?text={msg_link}")
        else:
            st.error("❌ Por favor, preencha seu Nome e WhatsApp.")

else:
    st.title("📊 RELATÓRIO DE PESQUISAS")
    senha = st.text_input("Senha Admin", type="password")
    
    if senha == SENHA_ADMIN:
        if st.session_state['banco_dados']:
            st.write("### CLIENTES QUE PARTICIPARAM:")
            st.table(pd.DataFrame(st.session_state['banco_dados']))
        else:
            st.warning("Ainda não recebemos pesquisas nesta sessão.")
    elif senha != "":
        st.error("Senha Incorreta")
