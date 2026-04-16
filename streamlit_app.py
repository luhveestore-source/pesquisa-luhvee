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
        width: 100% !important; font-size: 18px !important; font-weight: bold !important; height: 75px !important;
    }
    label, p, h1, h2, h3 { color: #ffffff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
API_URL = "https://sheetdb.io/api/v1/4s035f0bwuwxy" 
LINK_GRUPO = "https://chat.whatsapp.com/IBneTrHJemMLla4wzU8Wbj"
NOVO_HUB = "https://links-luhveestore.streamlit.app/"

# --- LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center; color: #ff69b4;'>LuhVee Stores</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>SUA OPINIÃO VALE MUITO ❤️</h2>", unsafe_allow_html=True)

# --- FORMULÁRIO ---
with st.form("form_vendas", clear_on_submit=True):
    nome = st.text_input("Seu Nome Completo")
    email = st.text_input("Seu E-mail") # CAMPO NOVO
    whatsapp_cliente = st.text_input("Seu WhatsApp (Ex: 11999999999)")
    
    escolha = st.selectbox("O que você procura hoje?", [
        "Perfumes e Bodysplash (Fem/Masc)", "Scarpins e Saltos", "Moda Adulto e Infantil", 
        "Mamãe e Bebê", "Pets", "Eletrodomésticos", "Cama, Mesa e Banho", 
        "Ferramentas", "Jardinagem", "Tênis Adulto e Infantil", "Informática", 
        "Móveis", "Lingerie", "Sexshop", "Brinquedos", "Outros ✨"
    ])

    loja_pref = st.radio("Onde você prefere comprar?", ["Shopee", "Mercado Livre"]) # CAMPO NOVO
    
    submit = st.form_submit_button("RECEBA PROMOÇÕES ❤️")

if submit:
    if nome and whatsapp_cliente and email:
        # Tratamento do número
        num_limpo = "".join(filter(str.isdigit, whatsapp_cliente))
        if len(num_limpo) <= 11: num_limpo = "55" + num_limpo
        primeiro_nome = nome.split()[0].title()

        # --- SALVAMENTO NA PLANILHA ---
        payload = {
            "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "CLIENTE": nome.upper(),
            "WHATSAPP": num_limpo,
            "E-MAIL": email.lower(),
            "INTERESSE": escolha,
            "LOJA": loja_pref
        }
        try:
            requests.post(API_URL, json={"data": [payload]}, timeout=5)
        except:
            pass

        # --- LÓGICA DA MENSAGEM PERSONALIZADA ---
        if escolha == "Outros ✨":
            texto_zap = (
                f"Olá {primeiro_nome}, tudo bem? 🥰\n\n"
                f"Recebi sua resposta e fiquei super curiosa! ✨\n\n"
                f"Vi que você marcou que tem interesse em outros produtos que ainda não temos na vitrine. "
                f"Como a LuhVee Stores quer ser sua parceira número 1 em achadinhos, me conta por aqui: "
                f"o que você está procurando e ainda não encontrou com um preço legal? 🛍️\n\n"
                f"Vou adorar caçar essa oferta exclusiva para você!\n\n"
                f"Enquanto isso, aproveite o nosso Hub Oficial:\n"
                f"🔗 {NOVO_HUB}"
            )
        else:
            texto_zap = (
                f"Olá {primeiro_nome}! ✨\n\n"
                f"Aqui é da LuhVee Stores. Que bom saber que você tem interesse em {escolha}! 😍\n\n"
                f"Preparamos uma curadoria especial para você aproveitar na {loja_pref}:\n\n"
                f"👉 Acesse agora: {NOVO_HUB}\n\n"
                f"Entra no nosso grupo VIP para receber ofertas diárias:\n"
                f"🎁 {LINK_GRUPO}\n\n"
                f"Bjs e boas compras! 🛍️✨"
            )
        
        msg_encoded = urllib.parse.quote(texto_zap)
        link_final = f"https://wa.me/{num_limpo}?text={msg_encoded}"
        
        st.success(f"Tudo pronto, {primeiro_nome}! Clique abaixo:")
        st.link_button("🎁 ABRIR MEU WHATSAPP", link_final)
    else:
        st.error("❌ Por favor, preencha o Nome, E-mail e o WhatsApp.")
