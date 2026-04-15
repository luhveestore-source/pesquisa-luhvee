import streamlit as st
from streamlit_gsheets import GSheetsConnection
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
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #ff69b4 !important;
        color: #000000 !important;
    }
    label, p, h1, h2, h3 { color: #ffffff !important; font-weight: bold; }
    [data-testid="stTable"] { background-color: #ffffff; color: #000000; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Lendo os dados existentes (A aba deve se chamar Página1)
    data_existente = conn.read(worksheet="Página1", ttl=0)
except Exception as e:
    data_existente = pd.DataFrame(columns=["DATA", "CLIENTE", "WHATSAPP", "E-MAIL", "INTERESSE", "LOJA"])

# --- CONFIGURAÇÕES DO NEGÓCIO ---
SEU_WHATSAPP = "5511948021428"
CENTRALIZADOR = "https://luhveestore-unbgvh5h.manus.space"
INSTAGRAM = "@luhveestore"
TIKTOK = "@luhvee.stores"
LINK_SHOPEE = "https://collshp.com/luhveestores?view=storefront"
LINK_ML = "https://www.mercadolivre.com.br/social/axwelloliveira"
SENHA_ADMIN = "luhvee2026"

produtos = {
    "Perfumes e Bodysplash (Fem/Masc)": "Fragrâncias irresistíveis!",
    "Scarpins e Saltos": "Elegância em cada passo!",
    "Moda Adulto e Infantil": "Estilo para toda a família!",
    "Mamãe e Bebê": "Cuidado para os pequenos!",
    "Pets": "Mimos para seu pet!",
    "Eletrodomésticos": "Tecnologia para o seu lar!",
    "Cama, Mesa e Banho": "Conforto e elegância!",
    "Ferramentas": "Qualidade para seus projetos!",
    "Jardinagem": "Beleza para o seu jardim!",
    "Tênis Adulto e Infantil": "Conforto para o dia a dia!",
    "Informática": "Performance ao seu alcance!",
    "Móveis": "Design para o seu lar!",
    "Lingerie": "Autoestima em cada detalhe!",
    "Sexshop": "Momentos especiais com sigilo!",
    "Brinquedos": "Diversão garantida!",
    "Outros / Encomenda Especial ✨": "Eu busco o produto dos seus sonhos!"
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
    
    with st.form("form_vendas", clear_on_submit=True):
        nome = st.text_input("Nome Completo")
        whatsapp = st.text_input("WhatsApp (com DDD)")
        email = st.text_input("Seu melhor E-mail")
        escolha = st.selectbox("Qual categoria você quer ver?", list(produtos.keys()))
        plataforma = st.radio("Onde você prefere comprar?", ["Shopee", "Mercado Livre", "WhatsApp Direto"])
        
        st.info("💡 Dica: Se não encontrar o que deseja, escolha 'Outros' e me chame no Zap!")
        submit = st.form_submit_button("CONCLUIR PESQUISA 💖")

    if submit:
        if nome and whatsapp and email:
            # Criando a nova linha para a planilha
            novo_lead = pd.DataFrame([{
                "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "CLIENTE": nome.upper(),
                "WHATSAPP": whatsapp,
                "E-MAIL": email.lower(),
                "INTERESSE": escolha,
                "LOJA": plataforma
            }])
            
            # Atualizando a Planilha do Google
            try:
                updated_df = pd.concat([data_existente, novo_lead], ignore_index=True)
                conn.update(worksheet="Página1", data=updated_df)
                st.success("Sua pesquisa foi salva na nossa base! ✅")
            except Exception as e:
                st.error("Erro ao salvar na planilha. Verifique os Segredos e se a aba chama Página1.")

            st.markdown(f"<h1 style='text-align: center; color: #ff69b4;'>OBRIGADA, {nome.upper()}! ❤️</h1>", unsafe_allow_html=True)
            
            link_final = LINK_SHOPEE if plataforma == "Shopee" else LINK_ML if plataforma == "Mercado Livre" else f"https://wa.me/{SEU_WHATSAPP}"
            
            msg_encomenda = "\n\n📢 AVISO: Vi que não encontrou o que queria. Me conte o que busca que eu encontro para você! ✨" if "Outros" in escolha else ""

            texto_zap = (
                f"Olá {nome.upper()}! ❤️\n\n"
                f"Ficamos muito felizes com sua participação! 🥰\n\n"
                f"Aqui está nossa vitrine atualizada de {escolha} na plataforma {plataforma}:\n"
                f"👉 {link_final}{msg_encomenda}\n\n"
                f"Caso queira conferir produtos em outras plataformas, segue nossa central de links:\n"
                f"🔗 {CENTRALIZADOR}\n\n"
                f"Siga-nos também:\n"
                f"📸 Instagram: {INSTAGRAM}\n"
                f"🎥 TikTok: {TIKTOK}\n\n"
                f"LuhVee Stores agradece seu carinho! ❤️🌸"
            )
            
            msg_encoded = urllib.parse.quote(texto_zap, safe='')
            num_limpo = "".join(filter(str.isdigit, whatsapp))
            if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
            
            st.link_button("🎁 CLIQUE PARA RECEBER NO WHATSAPP", f"https://wa.me/{num_limpo}?text={msg_encoded}")
        else:
            st.error("❌ Por favor, preencha todos os campos.")

else:
    st.title("📊 GESTÃO PERMANENTE DE CLIENTES")
    senha = st.text_input("Senha de Acesso", type="password")
    if senha == SENHA_ADMIN:
        try:
            df_google = conn.read(worksheet="Página1", ttl=0)
            st.write("### Dados salvos no Google Sheets:")
            st.table(df_google)
        except:
            st.warning("Verifique a conexão com a planilha nos Secrets.")
    elif senha != "":
        st.error("Senha Incorreta")
