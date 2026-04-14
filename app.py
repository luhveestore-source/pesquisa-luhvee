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
INSTAGRAM_USER = "@luhveestore"
LINK_INSTAGRAM = "https://instagram.com/luhveestore"
LINK_SHOPEE = "https://collshp.com/luhveestores?view=storefront"
LINK_ML = "https://www.mercadolivre.com.br/social/axwelloliveira"
SENHA_ADMIN = "luhvee2026"

# Lista de Produtos Atualizada
produtos = {
    "Perfumes e Bodysplash (Fem/Masc)": "Fragrâncias irresistíveis para marcar presença! ✨",
    "Scarpins e Saltos": "Elegância e poder em cada passo! 👠",
    "Moda Adulto e Infantil": "Estilo para toda a família! 👗👕",
    "Mamãe e Bebê": "Cuidado e conforto para os pequenos! 👶🍼",
    "Pets": "Mimos especiais para o seu melhor amigo! 🐾",
    "Eletrodomésticos": "Praticidade para facilitar o seu dia! 🏠🔌",
    "Cama, Mesa e Banho": "Sua casa com muito mais aconchego! 🛏️🚿",
    "Ferramentas": "Qualidade para os seus projetos! 🛠️🔩",
    "Jardinagem": "Beleza e vida para o seu jardim! 🌻🌿",
    "Tênis Adulto e Infantil": "Conforto e estilo para o dia a dia! 👟✨",
    "Informática": "Performance e tecnologia ao seu alcance! 💻🖱️",
    "Móveis": "Design e sofisticação para o seu lar! 🛋️🏠",
    "Lingerie": "Autoestima e delicadeza em cada peça! 👙💖",
    "Sexshop": "Momentos especiais com total discrição! 🔥🤫",
    "Brinquedos": "Muita diversão e criatividade! 🧸🪁",
    "Outros": "Diga-nos o que você deseja! ✨"
}

if 'historico' not in st.session_state:
    st.session_state['historico'] = []

# --- EXIBIÇÃO DA LOGO ---
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    try:
        st.image("1000396187.jpeg", use_container_width=True)
    except:
        st.write("✨ LUHVEE STORES")

# --- NAVEGAÇÃO ---
menu = st.sidebar.radio("Navegação", ["Fazer Pesquisa", "Painel Administrativo"])

if menu == "Fazer Pesquisa":
    st.markdown("### Encontre o seu produto favorito! 🛍️")
    
    with st.form("form_luhvee"):
        nome = st.text_input("Seu Nome")
        whatsapp = st.text_input("WhatsApp (com DDD)")
        categoria = st.selectbox("O que você procura hoje?", list(produtos.keys()))
        plataforma = st.radio("Qual plataforma você prefere?", ["Shopee", "Mercado Livre", "WhatsApp Direto"])
        submit = st.form_submit_button("CONCLUIR E RECEBER LISTA 💖")

    if submit:
        if nome and whatsapp:
            # Salvar no histórico
            st.session_state['historico'].append({
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Nome": nome, "WhatsApp": whatsapp, "Produto": categoria, "Plataforma": plataforma
            })
            st.balloons()
            
            # Escolha do Link
            link_final = LINK_SHOPEE if plataforma == "Shopee" else LINK_ML if plataforma == "Mercado Livre" else f"https://wa.me/{SEU_WHATSAPP}"
            
            # --- MENSAGEM PERSONALIZADA (BEM ATRATIVA) ---
            texto_formatado = (
                f"Olá {nome}! ✨\n\n"
                f"Ficamos muito felizes com a sua participação na nossa pesquisa! 💖\n\n"
                f"Aqui está a nossa vitrine de produtos atualizada na plataforma que você escolheu ({plataforma}):\n"
                f"👉 {link_final}\n\n"
                f"Aproveite para nos seguir no Instagram e conferir as novidades diárias:\n"
                f"📸 {LINK_INSTAGRAM}\n\n"
                f"Qualquer dúvida, é só nos chamar! 🌸\n"
                f"LuhVee Stores agradece seu carinho! ❤️"
            )
            
            msg_encoded = urllib.parse.quote(texto_formatado)
            num_limpo = "".join(filter(str.isdigit, whatsapp))
            if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
            
            st.success(f"Tudo pronto, {nome}! Clique no botão rosa abaixo para receber os detalhes no seu WhatsApp.")
            st.link_button("📲 RECEBER MINHA VITRINE NO WHATSAPP", f"https://wa.me/{num_limpo}?text={msg_encoded}")
        else:
            st.error("Por favor, preencha Nome e WhatsApp.")

else:
    st.markdown("### 🔐 Painel Administrativo")
    acesso = st.text_input("Senha de Acesso:", type="password")
    
    if acesso == SENHA_ADMIN:
        if st.session_state['historico']:
            df = pd.DataFrame(st.session_state['historico'])
            st.write("### Pesquisas Realizadas")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Ainda não há novas pesquisas registradas.")
    elif acesso != "":
        st.error("Senha incorreta!")
