import streamlit as st
import urllib.parse

st.set_page_config(page_title="LuhVee Stores", page_icon="🛍️")

# Estilo para ficar pretinho e bonito
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    input { background-color: #ffffff !important; color: #000000 !important; }
    .stButton>button {
        background-color: #000000 !important; color: #ff69b4 !important; 
        border: 2px solid #ffd700 !important; width: 100%; font-weight: bold;
    }
    label, h2 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>SUA OPINIÃO VALE MUITO ❤️</h2>", unsafe_allow_html=True)

with st.form("meu_form", clear_on_submit=True):
    nome = st.text_input("Seu Nome Completo")
    whatsapp = st.text_input("Seu WhatsApp (Ex: 11999999999)")
    escolha = st.selectbox("O que você procura hoje?", ["Perfumes", "Moda", "Calçados", "Cama, Mesa e Banho", "Outros"])
    submit = st.form_submit_button("RECEBA PROMOÇÕES ❤️")

if submit:
    if nome and whatsapp:
        # Garante o 55 no número
        num = "".join(filter(str.isdigit, whatsapp))
        if len(num) <= 11: num = "55" + num
        
        # Sua mensagem animada
        msg = (
            f"Olá {nome.split()[0].title()}, tudo bem? 🥰\n\n"
            f"Obrigada por participar! Seguem os links:\n\n"
            f"🛍️ Shopee: https://collshp.com/luhveestores\n"
            f"📦 Mercado Livre: https://www.mercadolivre.com.br/social/axwelloliveira\n\n"
            f"🚀 Grupo VIP: https://chat.whatsapp.com/IBneTrHJemMLla4wzU8Wbj\n\n"
            f"Bjs e boas compras! 🛍️✨"
        )
        
        link_final = f"https://api.whatsapp.com/send?phone={num}&text={urllib.parse.quote(msg)}"
        
        st.success("Redirecionando... ❤️")
        st.markdown(f'<meta http-equiv="refresh" content="1;URL={link_final}">', unsafe_allow_html=True)
        st.link_button("CLIQUE AQUI PARA ABRIR", link_final)
    else:
        st.error("Preencha Nome e Whats!")
