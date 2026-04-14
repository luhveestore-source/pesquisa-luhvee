import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL PREMIUM (CSS) ---
st.set_page_config(page_title="LuhVee Stores", page_icon="🛍️", layout="centered")

# CSS para Fundo Preto, Letras Brancas e Botões Rosa/Dourado
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #ff69b4;
    }
    label {
        color: white !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #ff69b4;
        color: white;
        border-radius: 20px;
        border: 1px solid #ffd700;
        width: 100%;
        font-size: 20px;
        height: 3em;
    }
    .stButton>button:hover {
        background-color: #ff1493;
        border: 1px solid #ffffff;
    }
    h1, h2, h3, p, span {
        color: #ffffff !important;
        text-align: center;
    }
    /* Estilo para o rádio e selectbox */
    div[data-baseweb="radio"] > div {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES DO NEGÓCIO ---
SEU_WHATSAPP = "5511948021428"
LINK_INSTAGRAM = "https://instagram.com/luhveestore"
LINK_SHOPEE = "https://collshp.com/luhveestores?view=storefront"
LINK_ML = "https://www.mercadolivre.com.br/social/axwelloliveira"
SENHA_ADMIN = "luhvee2026"

produtos = {
    "Moda Adulto e Infantil": "Estilo para toda a família! 👗",
    "Mamãe e Bebê": "Tudo para o conforto da mamãe e do bebê! 👶",
    "Pets": "Seu amiguinho merece o melhor! 🐾",
    "Eletrodomésticos": "Tecnologia para o seu lar! 🏠",
    "Cama, Mesa e Banho": "Conforto e elegância! 🛏️",
    "Ferramentas": "Praticidade para seus projetos! 🛠️",
    "Jardinagem": "Para um jardim mais vivo! 🌻",
    "Tênis Adulto e Infantil": "Pisada firme e estilo! 👟",
    "Informática": "Conectividade e performance! 💻",
    "Móveis": "Sua casa de cara nova! 🛋️",
    "Lingerie": "Autoestima em cada detalhe! 👙",
    "Sexshop": "Bem-estar com total sigilo! 🔥",
    "Brinquedos": "A diversão está garantida! 🧸",
    "Outros": "Conte-me o que você precisa! ✨"
}

if 'historico' not in st.session_state:
    st.session_state['historico'] = []

# --- EXIBIÇÃO DA LOGO ---
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    try:
        # Tenta carregar o arquivo exatamente como está no seu GitHub
        st.image("1000396187.jpeg", use_container_width=True)
    except:
        st.write("✨ LUHVEE STORES")

# --- NAVEGAÇÃO ---
menu = st.sidebar.radio("Navegação", ["Pesquisa de Clientes", "Área Administrativa"])

if menu == "Pesquisa de Clientes":
    st.markdown("### Encontre o que você precisa")
    
    with st.form("form_luhvee"):
        nome = st.text_input("Nome Completo")
        whatsapp = st.text_input("WhatsApp (com DDD)")
        categoria = st.selectbox("O que você procura?", list(produtos.keys()))
        plataforma = st.radio("Onde prefere comprar?", ["Shopee", "Mercado Livre", "WhatsApp Direto"])
        obs = st.text_area("Algum pedido especial?")
        
        btn = st.form_submit_button("CONCLUIR E VER PRODUTOS")

    if btn:
        if nome and whatsapp:
            st.session_state['historico'].append({
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Nome": nome, "WhatsApp": whatsapp, "Produto": categoria, "Plataforma": plataforma
            })
            st.balloons()
            st.success(f"Obrigado, {nome}! ✨ Redirecionando...")
            
            link_final = LINK_SHOPEE if plataforma == "Shopee" else LINK_ML if plataforma == "Mercado Livre" else f"https://wa.me/{SEU_WHATSAPP}"
            
            st.markdown(f"## [🛒 CLIQUE AQUI PARA VER OS PRODUTOS]({link_final})")
            
            # Formatação para o seu WhatsApp
            num_limpo = "".join(filter(str.isdigit, whatsapp))
            if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
            msg_cliente = urllib.parse.quote(f"Olá {nome}! Aqui está o link da categoria {categoria}: {link_final}")
            
            st.link_button("📲 Enviar link no Zap do Cliente", f"https://wa.me/{num_limpo}?text={msg_cliente}")
        else:
            st.error("Por favor, preencha Nome e WhatsApp.")

else:
    st.title("📊 Painel Admin")
    acesso = st.text_input("Senha:", type="password")
    if acesso == SENHA_ADMIN:
        df = pd.DataFrame(st.session_state['historico'])
        st.dataframe(df)
    else:
        st.write("Acesso restrito.")
