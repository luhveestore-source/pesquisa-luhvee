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

# --- CONFIGURAÇÕES E LINKS ---
API_URL = "https://sheetdb.io/api/v1/4s035f0bwuwxy" 
NOVO_HUB = "https://links-luhveestore.streamlit.app/"
LINK_GRUPO = "https://chat.whatsapp.com/IBneTrHJemMLla4wzU8Wbj"

# --- LOGO ---
st.markdown("<h1 style='text-align: center; color: #ff69b4;'>LuhVee Stores</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>SUA OPINIÃO VALE MUITO ❤️</h2>", unsafe_allow_html=True)

# --- FORMULÁRIO ---
with st.form("form_vendas", clear_on_submit=True):
    nome = st.text_input("Seu Nome Completo")
    email = st.text_input("Seu MELHOR E-mail")
    whatsapp_cliente = st.text_input("Seu WhatsApp (Ex: 11999999999)")
    
    # Campo que vai para a coluna 'LOJA' no Excel
    loja_preferida = st.radio("Qual sua plataforma preferida para compras?", ["Shopee", "Mercado Livre"])
    
    escolha = st.selectbox("O que você procura hoje?", [
        "Perfumes e Bodysplash (Fem/Masc)", "Scarpins e Saltos", "Moda Adulto e Infantil", 
        "Mamãe e Bebê", "Pets", "Eletrodomésticos", "Cama, Mesa e Banho", 
        "Ferramentas", "Jardinagem", "Tênis Adulto e Infantil", "Informática", 
        "Móveis", "Lingerie", "Sexshop", "Brinquedos", "Outros ✨"
    ])
    
    submit = st.form_submit_button("RECEBA OFERTAS EXCLUSIVAS ❤️")

if submit:
    if nome and whatsapp_cliente and email:
        # Tratamento do número
        num_limpo = "".join(filter(str.isdigit, whatsapp_cliente))
        if len(num_limpo) <= 11: num_limpo = "55" + num_limpo
        primeiro_nome = nome.split()[0].title()

        # --- SALVAMENTO NA PLANILHA (Ajustado para as tuas colunas) ---
        payload = {
            "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "CLIENTE": nome.upper(),
            "WHATSAPP": num_limpo,
            "E-MAIL": email.lower(), # Ajustado para bater com a imagem
            "INTERESSE": escolha,
            "LOJA": loja_preferida # Envia Shopee ou Mercado Livre para a coluna LOJA
        }
        
        try:
            requests.post(API_URL, json={"data": [payload]}, timeout=5)
        except:
            pass 

        # --- LÓGICA DA MENSAGEM ---
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
                f"Preparamos uma curadoria especial no nosso novo Hub de Ofertas para você aproveitar na {loja_preferida}:\n\n"
                f"👉 Acesse agora: {NOVO_HUB}\n\n"
                f"Não esqueça de entrar no nosso grupo VIP para não perder as promoções de hoje:\n"
                f"🎁 {LINK_GRUPO}\n\n"
                f"Boas compras! 🛍️✨"
            )
        
        msg_encoded = urllib.parse.quote(texto_zap)
        link_final = f"https://wa.me/{num_limpo}?text={msg_encoded}"
        
        st.success(f"Obrigado, {primeiro_nome}! Clique abaixo para resgatar suas ofertas.")
        st.link_button("🎁 ABRIR MEU WHATSAPP AGORA", link_final)
    else:
        st.error("❌ Por favor, preencha o Nome, E-mail e WhatsApp.")
