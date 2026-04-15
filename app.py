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
        width: 100% !important; font-size: 18px !important; font-weight: bold !important; height: 70px !important;
    }
    label, p, h1, h2, h3 { color: #ffffff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- LINKS ---
LINK_GRUPO_WHATSAPP = "https://chat.whatsapp.com/IBneTrHJemMLla4wzU8Wbj"
CENTRALIZADOR = "https://luhveestore-unbgvh5h.manus.space"
INSTAGRAM = "@luhveestore"
TIKTOK = "@luhvee.stores"

# --- LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("1000396187.jpeg")
    except:
        st.header("✨ LUHVEE STORES")

st.markdown("<h2 style='text-align: center;'>SUA OPINIÃO VALE MUITO ❤️</h2>", unsafe_allow_html=True)

# --- FORMULÁRIO ---
with st.form("form_vendas", clear_on_submit=True):
    nome = st.text_input("Seu Nome Completo")
    whatsapp_cliente = st.text_input("Seu WhatsApp (com DDD)")
    
    escolha = st.selectbox("O que você mais gosta?", [
        "Perfumes e Bodysplash", "Scarpins e Saltos", "Moda Adulto e Infantil", 
        "Tênis Adulto e Infantil", "Lingerie e Sexshop", "Outros ✨"
    ])
    
    submit = st.form_submit_button("RECEBER PROMOÇÕES E VITRINES ❤️")

if submit:
    if nome and whatsapp_cliente:
        # Mensagem Profissional para o privado do cliente
        texto_zap = (
            f"Olá {nome.title()}! ❤️\n\n"
            f"Agora você faz parte da comunidade *LuhVee Stores*! 🥰\n\n"
            f"Aqui estão os links das nossas vitrines de *{escolha}*:\n"
            f"👉 {CENTRALIZADOR}\n\n"
            f"🚀 Quer receber ofertas exclusivas antes de todo mundo? Participe do nosso Grupo VIP:\n"
            f"🔗 {LINK_GRUPO_WHATSAPP}\n\n"
            f"Siga-nos no Instagram: {INSTAGRAM}\n\n"
            f"Boas compras! ❤️🌸"
        )
        
        msg_encoded = urllib.parse.quote(texto_zap)
        num_limpo = "".join(filter(str.isdigit, whatsapp_cliente))
        if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
        
        link_zap_privado = f"https://wa.me/{num_limpo}?text={msg_encoded}"
        
        # Interface de Sucesso
        st.success(f"Tudo pronto, {nome.split()[0]}! Enviando para o seu WhatsApp...")
        
        # Botão extra para o Grupo (Opcional para o cliente)
        st.markdown(f"### 🎁 Presente Extra:")
        st.link_button("ENTRAR NO GRUPO VIP (OPCIONAL)", LINK_GRUPO_WHATSAPP)
        
        # Redirecionamento automático para o privado dele
        st.markdown(f'<meta http-equiv="refresh" content="2;URL={link_zap_privado}">', unsafe_allow_html=True)
        
    else:
        st.error("❌ Por favor, preencha o Nome e o WhatsApp.")
