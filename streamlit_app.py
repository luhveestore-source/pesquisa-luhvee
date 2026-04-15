import streamlit as st
import urllib.parse

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

# --- LINKS ---
LINK_GRUPO = "https://chat.whatsapp.com/IBneTrHJemMLla4wzU8Wbj"
CENTRALIZADOR = "https://luhveestore-unbgvh5h.manus.space"
INSTAGRAM = "https://www.instagram.com/luhveestore"
TIKTOK = "https://www.tiktok.com/@luhvee.stores"
LINK_SHOPEE = "https://collshp.com/luhveestores?view=storefront"
LINK_ML = "https://www.mercadolivre.com.br/social/axwelloliveira"

# --- LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center; color: #ff69b4;'>LuhVee Stores</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>SUA OPINIÃO VALE MUITO ❤️</h2>", unsafe_allow_html=True)

# --- FORMULÁRIO ---
with st.form("form_vendas", clear_on_submit=True):
    nome = st.text_input("Seu Nome Completo")
    whatsapp_cliente = st.text_input("Seu WhatsApp (Ex: 11999999999)")
    
    escolha = st.selectbox("O que você procura hoje?", [
        "Perfumes e Bodysplash (Fem/Masc)", "Scarpins e Saltos", "Moda Adulto e Infantil", 
        "Mamãe e Bebê", "Pets", "Eletrodomésticos", "Cama, Mesa e Banho", 
        "Ferramentas", "Jardinagem", "Tênis Adulto e Infantil", "Informática", 
        "Móveis", "Lingerie", "Sexshop", "Brinquedos", "Outros ✨"
    ])
    
    submit = st.form_submit_button("RECEBA PROMOÇÕES ❤️")

if submit:
    if nome and whatsapp_cliente:
        # Garante o 55 no número
        num_limpo = "".join(filter(str.isdigit, whatsapp_cliente))
        if len(num_limpo) <= 11: num_limpo = "55" + num_limpo
            
        primeiro_nome = nome.split()[0].title()
        
        # Sua Mensagem Personalizada
        texto_zap = (
            f"Olá {primeiro_nome}, tudo bem? 🥰\n\n"
            f"Obrigada por participar da nossa pesquisa! Como prometido, seguem os links para você arrasar nas compras:\n\n"
            f"🛍️ *Shopee:* {LINK_SHOPEE}\n"
            f"📦 *Mercado Livre:* {LINK_ML}\n\n"
            f"Nos segue lá, as promoções não param! 🔥\n"
            f"📸 *Instagram:* {INSTAGRAM}\n"
            f"🎥 *TikTok:* {TIKTOK}\n"
            f"🔗 *Centralizador:* {CENTRALIZADOR}\n\n"
            f"Se quiser ficar sempre conectado e receber ofertas diárias, entra no nosso grupo *LuhVee Stores*! 🎁\n"
            f"👉 Segue o link: {LINK_GRUPO}\n\n"
            f"Bjs e boas compras! 🛍️✨"
        )
        
        msg_encoded = urllib.parse.quote(texto_zap)
        # Usamos o link direto para não dar erro de conexão recusada
        link_final = f"https://wa.me/{num_limpo}?text={msg_encoded}"
        
        st.success(f"Tudo pronto, {primeiro_nome}! Clique no botão abaixo para receber tudo no seu WhatsApp:")
        
        # BOTÃO GRANDE PARA O WHATSAPP (Isso evita o erro da foto)
        st.link_button("🎁 CLIQUE AQUI PARA ABRIR SEU WHATSAPP", link_final)
    else:
        st.error("❌ Por favor, preencha o Nome e o WhatsApp.")
