import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÕES DO NEGÓCIO ---
SEU_WHATSAPP = "5511948021428"
LINK_INSTAGRAM = "https://instagram.com/luhveestore"
LINK_SHOPEE = "https://collshp.com/luhveestores?view=storefront"
LINK_ML = "https://www.mercadolivre.com.br/social/axwelloliveira"
SENHA_ADMIN = "luhvee2026" # Altera se quiseres

# --- BASE DE DADOS DE PRODUTOS ---
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

# --- FUNÇÃO PARA SALVAR DADOS (SIMULADA PARA O DASHBOARD) ---
if 'historico' not in st.session_state:
    st.session_state['historico'] = []

# --- INTERFACE ---
st.set_page_config(page_title="LuhVee Stores", page_icon="🛍️")

# Estilização para centralizar a logo
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    try:
        st.image("1000396187.jpg", use_container_width=True) # Nome do ficheiro que enviaste
    except:
        st.header("✨ LuhVee Stores")

# Menu de Navegação
menu = st.sidebar.radio("Ir para:", ["Fazer Pesquisa", "Painel Administrativo"])

if menu == "Fazer Pesquisa":
    st.markdown("<h2 style='text-align: center;'>Pesquisa de Produtos</h2>", unsafe_allow_html=True)
    
    with st.form("form_cliente"):
        nome = st.text_input("Nome Completo")
        whatsapp = st.text_input("WhatsApp (com DDD)")
        email = st.text_input("E-mail")
        categoria = st.selectbox("O que você procura?", list(produtos.keys()))
        plataforma = st.radio("Sua plataforma favorita:", ["Shopee", "Mercado Livre", "WhatsApp Direto"])
        obs = st.text_area("Algum detalhe específico?")
        
        btn_enviar = st.form_submit_button("CONCLUIR E RECEBER LINKS")

    if btn_enviar:
        if nome and whatsapp:
            # Salvar no "Dashboard" interno
            novo_registro = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Nome": nome,
                "WhatsApp": whatsapp,
                "Produto": categoria,
                "Plataforma": plataforma
            }
            st.session_state['historico'].append(novo_registro)
            
            st.balloons()
            st.success(f"Ficamos muito felizes pela sua pesquisa, {nome}! ✨")
            
            # Links de Redirecionamento
            link_final = LINK_SHOPEE if plataforma == "Shopee" else LINK_ML if plataforma == "Mercado Livre" else f"https://wa.me/{SEU_WHATSAPP}"
            
            st.markdown(f"### 👉 [CLIQUE AQUI PARA VER OS PRODUTOS]({link_final})")
            st.info(f"Conheça também nosso Instagram: [{LINK_INSTAGRAM}]({LINK_INSTAGRAM})")
            
            # Botão para você enviar no zap do cliente
            texto_zap = f"Olá {nome}! Obrigado por escolher a LuhVee Stores. Aqui está o link da categoria {categoria}: {link_final}"
            st.link_button("📲 Enviar link para o cliente agora", f"https://wa.me/55{whatsapp.replace(' ', '')}?text={urllib.parse.quote(texto_zap)}")
        else:
            st.error("Preencha o Nome e WhatsApp!")

else:
    st.title("📊 Dashboard LuhVee")
    acesso = st.text_input("Senha de acesso:", type="password")
    
    if acesso == SENHA_ADMIN:
        if st.session_state['historico']:
            df = pd.DataFrame(st.session_state['historico'])
            
            # Métricas
            c1, c2 = st.columns(2)
            c1.metric("Total de Leads", len(df))
            c2.metric("Mais procurado", df['Produto'].mode()[0])
            
            st.write("### Histórico de Pesquisas")
            st.dataframe(df, use_container_width=True)
            
            st.write("### Preferência de Plataforma")
            st.bar_chart(df['Plataforma'].value_counts())
        else:
            st.info("Ainda não existem pesquisas registradas.")
    elif acesso != "":
        st.error("Senha incorreta!")