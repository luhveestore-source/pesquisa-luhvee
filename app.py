import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="LuhVee Stores", page_icon="🛍️", layout="centered")

# CSS para Visual Premium Black & Pink
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #1a1a1a; color: white; border: 1px solid #ff69b4;
    }
    label { color: white !important; font-weight: bold; }
    .stButton>button {
        background-color: #ff69b4; color: white; border-radius: 20px;
        border: 1px solid #ffd700; width: 100%; font-size: 18px; font-weight: bold;
    }
    h1, h2, h3, p, span { color: #ffffff !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES DO NEGÓCIO ---
SEU_WHATSAPP = "5511948021428"
CENTRALIZADOR = "https://luhveestore-unbgvh5h.manus.space"
INSTAGRAM = "@luhveestore"
TIKTOK = "@luhvee.stores"
LINK_SHOPEE = "https://collshp.com/luhveestores?view=storefront"
LINK_ML = "https://www.mercadolivre.com.br/social/axwelloliveira"
SENHA_ADMIN = "luhvee2026"

# Lista de Produtos Completa
produtos = {
    "Perfumes e Bodysplash (Fem/Masc)": "Fragrâncias irresistíveis! ✨",
    "Scarpins e Saltos": "Elegância em cada passo! 👠",
    "Moda Adulto e Infantil": "Estilo para toda a família! 👗👕",
    "Mamãe e Bebê": "Cuidado para os pequenos! 👶🍼",
    "Pets": "Mimos para o seu melhor amigo! 🐾",
    "Eletrodomésticos": "Praticidade para o seu lar! 🏠🔌",
    "Cama, Mesa e Banho": "Sua casa mais aconchegante! 🛏️🚿",
    "Ferramentas": "Qualidade para seus projetos! 🛠️🔩",
    "Jardinagem": "Beleza para o seu jardim! 🌻🌿",
    "Tênis Adulto e Infantil": "Conforto para o dia a dia! 👟✨",
    "Informática": "Performance ao seu alcance! 💻🖱️",
    "Móveis": "Design para o seu lar! 🛋️🏠",
    "Lingerie": "Autoestima e delicadeza! 👙💖",
    "Sexshop": "Momentos especiais com sigilo! 🔥🤫",
    "Brinquedos": "Diversão garantida! 🧸🪁",
    "Outros": "Diga-nos o que você deseja! ✨"
}

if 'historico' not in st.session_state:
    st.session_state['historico'] = []

# --- LOGO ---
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    try:
        st.image("1000396187.jpeg", use_container_width=True)
    except:
        st.write("✨ LUHVEE STORES")

# --- INTERFACE ---
menu = st.sidebar.radio("Navegação", ["Fazer Pesquisa", "Painel Administrativo"])

if menu == "Fazer Pesquisa":
    st.markdown("### Encontre o seu produto favorito! ❤️")
    
    with st.form("form_luhvee"):
        nome = st.text_input("Seu Nome")
        whatsapp = st.text_input("WhatsApp (com DDD)")
        categoria = st.selectbox("O que você procura hoje?", list(produtos.keys()))
        plataforma = st.radio("Sua plataforma favorita:", ["Shopee", "Mercado Livre", "WhatsApp Direto"])
        submit = st.form_submit_button("CONCLUIR E RECEBER LISTA 💖")

    if submit:
        if nome and whatsapp:
            st.session_state['historico'].append({
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Nome": nome, "WhatsApp": whatsapp, "Produto": categoria, "Plataforma": plataforma
            })
            st.balloons()
            
            link_final = LINK_SHOPEE if plataforma == "Shopee" else LINK_ML if plataforma == "Mercado Livre" else f"https://wa.me/{SEU_WHATSAPP}"
            
            # --- MENSAGEM BONITINHA (COM EMOJIS CORRIGIDOS) ---
            texto_formatado = (
                f"Olá {nome}! ❤️\n\n"
                f"Ficamos muito felizes com a sua participação na nossa pesquisa! 🥰\n\n"
                f"Aqui está a nossa vitrine de produtos atualizada na plataforma que você escolheu ({plataforma}):\n"
                f"👉 {link_final}\n\n"
                f"Confira também nossa central de links:\n"
                f"🔗 {CENTRALIZADOR}\n\n"
                f"Não esqueça de nos seguir:\n"
                f"📸 Instagram: {INSTAGRAM}\n"
                f"🎥 TikTok: {TIKTOK}\n\n"
                f"Qualquer dúvida, é só nos chamar! ✨\n"
                f"LuhVee Stores agradece seu carinho! ❤️🌸"
            )
            
            # Ajuste para garantir que emojis funcionem no link
            msg_encoded = urllib.parse.quote(texto_formatado)
            num_limpo = "".join(filter(str.isdigit, whatsapp))
            if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
            
            st.success(f"Tudo pronto, {nome}! Toque no botão abaixo para receber sua mensagem carinhosa.")
            st.link_button("📲 RECEBER MINHA VITRINE NO WHATSAPP", f"https://wa.me/{num_limpo}?text={msg_encoded}")
        else:
            st.error("Por favor, preencha Nome e WhatsApp.")

else:
    st.markdown("### 🔐 Painel Administrativo")
    acesso = st.text_input("Senha de Acesso:", type="password")
    if acesso == SENHA_ADMIN:
        if st.session_state['historico']:
            st.dataframe(pd.DataFrame(st.session_state['historico']), use_container_width=True)
        else:
            st.info("Nenhuma pesquisa ainda.")
    elif acesso != "":
        st.error("Senha incorreta!")
