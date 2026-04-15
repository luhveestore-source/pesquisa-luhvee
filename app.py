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
        width: 100% !important; font-size: 16px !important; font-weight: bold !important; height: 70px !important;
    }
    label, p, h1, h2, h3 { color: #ffffff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- LINKS ---
LINK_GRUPO_WHATSAPP = "https://chat.whatsapp.com/IBneTrHJemMLla4wzU8Wbj"
CENTRALIZADOR = "https://luhveestore-unbgvh5h.manus.space"
INSTAGRAM = "@luhveestore"

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
    
    st.write("---")
    quero_grupo = st.checkbox("Quero entrar no Grupo VIP para promoções diárias! 🎁")
    
    submit = st.form_submit_button("RECEBA PROMOÇÕES E VITRINES DA LUHVEE STORES ❤️")

if submit:
    if nome and whatsapp_cliente:
        # Mensagem Profissional
        msg_corpo = (
            f"Olá {nome.title()}! ❤️\n\n"
            f"Agora você faz parte da comunidade *LuhVee Stores*! 🥰\n\n"
            f"Aqui estão os links das nossas vitrines de *{escolha}*:\n"
            f"👉 {CENTRALIZADOR}\n\n"
        )
        
        if quero_grupo:
            msg_corpo += f"🚀 Como você escolheu entrar no grupo, aqui está o link VIP:\n🔗 {LINK_GRUPO_WHATSAPP}\n\n"
        
        msg_corpo += f"Siga-nos no Instagram: {INSTAGRAM}\n\nBoas compras! ❤️🌸"
        
        msg_encoded = urllib.parse.quote(msg_corpo)
        num_limpo = "".join(filter(str.isdigit, whatsapp_cliente))
        if not num_limpo.startswith("55"): num_limpo = "55" + num_limpo
        
        link_zap = f"https://wa.me/{num_limpo}?text={msg_encoded}"
        
        st.success(f"Tudo pronto, {nome.split()[0]}! Estamos te enviando as vitrines...")
        
        # Redirecionamento Automático
        st.markdown(f'<meta http-equiv="refresh" content="1;URL={link_zap}">', unsafe_allow_html=True)
        st.link_button("CLIQUE AQUI SE NÃO ABRIR SOZINHO", link_zap)
    else:
        st.error("❌ Por favor, preencha o Nome e o WhatsApp.")
