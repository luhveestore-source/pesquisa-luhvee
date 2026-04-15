import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

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

# --- LINK DA PLANILHA DIRETO NO CÓDIGO ---
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1BMo0YmnJ4T3b5YFq3FEsAPWNHS65TXEa_G2OwKSjLMM/edit?usp=sharing"

# --- CONEXÃO COM GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Aqui o código usa o link direto
    data_existente = conn.read(spreadsheet=URL_PLANILHA, worksheet="Página1", ttl=0)
except Exception:
    data_existente = pd.DataFrame(columns=["DATA", "CLIENTE", "WHATSAPP", "E-MAIL", "INTERESSE", "LOJA"])

# --- CONFIGURAÇÕES ---
SEU_WHATSAPP = "5511948021428"
CENTRALIZADOR = "https://luhveestore-unbgvh5h.manus.space"
INSTAGRAM = "@luhveestore"
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
menu = st.sidebar.radio("Navegação:", ["Fazer Pesquisa", "Dashboard ADM"])

if menu == "Fazer Pesquisa":
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
            novo_lead = pd.DataFrame([{
                "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "CLIENTE": nome.upper(),
                "WHATSAPP": whatsapp,
                "E-MAIL": email.lower(),
                "INTERESSE": escolha,
                "LOJA": plataforma
            }])
            try:
                updated_df = pd.concat([data_existente, novo_lead], ignore_index=True)
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Página1", data=updated_df)
                st.success("Salvo com sucesso na planilha! ✅")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

            link_final = LINK_SHOPEE if plataforma == "Shopee" else LINK_ML if plataforma == "Mercado Livre" else f"https://wa.me/{SEU_WHATSAPP}"
            texto_zap = f"Olá {nome.upper()}! ❤️\n\nVitrine de *{escolha}* na {plataforma}:\n👉 {link_final}\n\nLuhVee Stores agradece! ❤️🌸"
            msg_encoded = urllib.parse.quote(texto_zap, safe='')
            num_limpo = "".join(filter(str.isdigit, whatsapp))
            if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
            st.link_button("🎁 RECEBER NO WHATSAPP", f"https://wa.me/{num_limpo}?text={msg_encoded}")
        else:
            st.error("❌ Preencha todos os campos.")

else:
    st.title("📊 GESTÃO DE CLIENTES")
    senha = st.text_input("Senha Admin", type="password")
    if senha == SENHA_ADMIN:
        try:
            df_google = conn.read(spreadsheet=URL_PLANILHA, worksheet="Página1", ttl=0)
            st.table(df_google)
        except:
            st.warning("Erro ao carregar os dados da planilha.")
