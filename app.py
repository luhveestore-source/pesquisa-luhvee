import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="LuhVee Stores", page_icon="🛍️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    input, textarea, [data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stButton>button {
        background-color: #000000 !important; 
        color: #ff69b4 !important; 
        border: 3px solid #ffd700 !important;
        border-radius: 15px !important;
        width: 100% !important;
        font-size: 22px !important;
        font-weight: bold !important;
        height: 65px !important;
    }
    .stButton>button:hover {
        background-color: #ff69b4 !important;
        color: #000000 !important;
    }
    label, p, h1, h2, h3 { color: #ffffff !important; font-weight: bold; }
    [data-testid="stTable"] { background-color: #ffffff; color: #000000; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA DO DASHBOARD ---
if 'historico_vendas' not in st.session_state:
    st.session_state['historico_vendas'] = []

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
    "Eletrodomésticos": "Tecnologia para o seu lar! 🏠",
    "Cama, Mesa e Banho": "Conforto e elegância! 🛏️",
    "Ferramentas": "Qualidade para seus projetos! 🛠️",
    "Jardinagem": "Beleza para o seu jardim! 🌻",
    "Tênis Adulto e Infantil": "Conforto para o dia a dia! 👟",
    "Informática": "Performance ao seu alcance! 💻",
    "Móveis": "Design para o seu lar! 🛋️",
    "Lingerie": "Autoestima em cada detalhe! 👙",
    "Sexshop": "Momentos especiais com sigilo! 🔥",
    "Brinquedos": "Diversão garantida! 🧸",
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
menu = st.sidebar.radio("Navegação:", ["Fazer Pesquisa", "Dashboard ADM"])

if menu == "Fazer Pesquisa":
    st.markdown("<h2 style='text-align: center;'>SUA OPINIÃO VALE MUITO ❤️</h2>", unsafe_allow_html=True)
    
    with st.form("form_vendas"):
        nome = st.text_input("Nome Completo")
        whatsapp = st.text_input("WhatsApp (com DDD)")
        escolha = st.selectbox("Qual categoria você quer ver?", list(produtos.keys()))
        plataforma = st.radio("Onde prefere comprar?", ["Shopee", "Mercado Livre", "WhatsApp Direto"])
        
        st.write("---")
        st.write("📢 *CLIQUE ABAIXO PARA FINALIZAR:*")
        submit = st.form_submit_button("FINALIZAR PESQUISA 💖")

    if submit:
        if nome and whatsapp:
            # Salvar no Dashboard
            st.session_state['historico_vendas'].append({
                "Data": datetime.now().strftime("%d/%m %H:%M"),
                "Cliente": nome.upper(),
                "WhatsApp": whatsapp,
                "Interesse": escolha,
                "Loja": plataforma
            })
            
            st.balloons() # Fogos/Balões de comemoração
            st.markdown(f"<h1 style='text-align: center; color: #ff69b4;'>OBRIGADA, {nome.upper()}! 🥰</h1>", unsafe_allow_html=True)
            
            link_final = LINK_SHOPEE if plataforma == "Shopee" else LINK_ML if plataforma == "Mercado Livre" else f"https://wa.me/{SEU_WHATSAPP}"
            
            # --- MENSAGEM DO WHATSAPP ATUALIZADA ---
            texto_zap = (
                f"Olá {nome.upper()}! ❤️\n\n"
                f"Ficamos muito felizes com sua participação! 🥰\n\n"
                f"Aqui está nossa vitrine atualizada de {escolha} na plataforma {plataforma}:\n"
                f"👉 {link_final}\n\n"
                f"Caso queira conferir produtos em outras plataformas, segue nossa central de links:\n"
                f"🔗 {CENTRALIZADOR}\n\n"
                f"Siga-nos também:\n"
                f"📸 Instagram: {INSTAGRAM}\n"
                f"🎥 TikTok: {TIKTOK}\n\n"
                f"LuhVee Stores agradece seu carinho! ❤️🌸"
            )
            
            msg_encoded = urllib.parse.quote(texto_zap)
            num_limpo = "".join(filter(str.isdigit, whatsapp))
            if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
            
            st.link_button("🎁 CLIQUE AQUI PARA RECEBER SEU LINK", f"https://wa.me/{num_limpo}?text={msg_encoded}")
        else:
            st.error("❌ Por favor, preencha Nome e WhatsApp.")

else:
    st.title("📊 DASHBOARD DE VENDAS")
    senha = st.text_input("Senha de Acesso", type="password")
    
    if senha == SENHA_ADMIN:
        if st.session_state['historico_vendas']:
            df = pd.DataFrame(st.session_state['historico_vendas'])
            st.table(df)
        else:
            st.warning("Ainda não há pesquisas registradas.")
    elif senha != "":
        st.error("Senha Incorreta")
