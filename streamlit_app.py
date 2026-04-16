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

# --- LINKS PRINCIPAIS ---
API_URL = "https://sheetdb.io/api/v1/4s035f0bwuwxy" 
NOVO_HUB = "https://links-luhveestore.streamlit.app/"
LINK_GRUPO = "https://chat.whatsapp.com/IBneTrHJemMLla4wzU8Wbj"

# --- LOGO ---
st.markdown("<h1 style='text-align: center; color: #ff69b4;'>LuhVee Stores</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>SUA OPINIÃO VALE MUITO ❤️</h2>", unsafe_allow_html=True)

# --- FORMULÁRIO ---
with st.form("form_vendas", clear_on_submit=True):
    nome = st.text_input("Seu Nome Completo")
    email = st.text_input("Seu E-mail")
    whatsapp_cliente = st.text_input("Seu WhatsApp (Ex: 11999999999)")
    
    escolha = st.selectbox("O que você procura hoje?", [
        "Perfumes e Bodysplash (Fem/Masc)", "Scarpins e Saltos", "Moda Adulto e Infantil", 
        "Mamãe e Bebê", "Pets", "Eletrodomésticos", "Cama, Mesa e Banho", 
        "Ferramentas", "Jardinagem", "Tênis Adulto e Infantil", "Informática", 
        "Móveis", "Lingerie", "Sexshop", "Brinquedos", "Outros ✨"
    ])

    loja_pref = st.radio("Onde você prefere comprar?", ["Shopee", "Mercado Livre"])
    
    submit = st.form_submit_button("RECEBA PROMOÇÕES ❤️")

if submit:
    if nome and whatsapp_cliente and email:
        num_limpo = "".join(filter(str.isdigit, whatsapp_cliente))
        if len(num_limpo) <= 11: num_limpo = "55" + num_limpo
        primeiro_nome = nome.split()[0].title()

        # Registro no SheetDB
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

        # --- DICIONÁRIO DE MENSAGENS PERSONALIZADAS ---
        mensagens_nicho = {
            "Perfumes e Bodysplash (Fem/Masc)": "para você ficar sempre perfumada(o) e marcante! 🧴✨",
            "Scarpins e Saltos": "para você arrasar com muito estilo e elegância! 👠🔥",
            "Moda Adulto e Infantil": "com as últimas tendências para toda a família! 👗👕",
            "Mamãe e Bebê": "escolhidos com todo carinho para você e seu pequeno! 🍼👶",
            "Pets": "para mimar o seu melhor amigo como ele merece! 🐾🐶",
            "Eletrodomésticos": "para deixar sua casa moderna e funcional! 🏠⚡",
            "Cama, Mesa e Banho": "para transformar sua casa num lugar de puro conforto! 🛌☁️",
            "Tênis Adulto e Infantil": "conforto e estilo para os seus passos! 👟💨",
            "Lingerie": "peças incríveis para elevar sua autoestima! 💖👙",
            "Sexshop": "para apimentar sua rotina com total discrição! 🔥🤫",
            "Brinquedos": "diversão garantida para a criançada! 🧸🎈"
        }

        frase_nicho = mensagens_nicho.get(escolha, "com as melhores ofertas que encontramos hoje! ✨")

        # --- CONSTRUÇÃO DO TEXTO DO WHATSAPP ---
        if escolha == "Outros ✨":
            texto_zap = (
                f"Olá {primeiro_nome}, tudo bem? 🥰\n\n"
                f"Recebi sua resposta e fiquei super curiosa! ✨\n\n"
                f"Vi que você tem interesse em produtos que ainda não temos na vitrine. Me conta aqui: o que você está procurando? 🛍️\n\n"
                f"Vou adorar caçar essa oferta exclusiva para você!\n\n"
                f"Enquanto isso, dá uma olhadinha no nosso Hub e aproveite para nos seguir nas redes sociais:\n"
                f"🔗 {NOVO_HUB}\n\n"
            )
        else:
            texto_zap = (
                f"Olá {primeiro_nome}! ✨\n\n"
                f"Aqui é da LuhVee Stores. Já separei achadinhos de {escolha} {frase_nicho}\n\n"
                f"Confira tudo agora no nosso Hub Oficial e não esqueça de nos seguir para acompanhar as novidades:\n"
                f"👉 {NOVO_HUB}\n\n"
            )

        # Rodapé fixo da mensagem
        texto_zap += (
            f"🎁 Entre no nosso Grupo VIP de Ofertas: {LINK_GRUPO}\n\n"
            f"Te esperamos lá! Bjs e boas compras! 🛍️✨"
        )
        
        msg_encoded = urllib.parse.quote(texto_zap)
        link_final = f"https://wa.me/{num_limpo}?text={msg_encoded}"
        
        st.success(f"Tudo pronto, {primeiro_nome}! Seu acesso está logo abaixo:")
        st.link_button("🎁 RECEBER LINK NO WHATSAPP", link_final)
    else:
        st.error("❌ Por favor, preencha todos os campos corretamente.")
