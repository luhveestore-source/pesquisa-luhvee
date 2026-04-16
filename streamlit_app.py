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

# --- LINKS OFICIAIS ---
API_URL = "https://sheetdb.io/api/v1/4s035f0bwuwxy" 
NOVO_HUB = "https://links-luhveestore.streamlit.app/"
LINK_GRUPO = "https://chat.whatsapp.com/IBneTrHJemMLla4wzU8Wbj"
INSTAGRAM = "https://www.instagram.com/luhveestore"
TIKTOK = "https://www.tiktok.com/@luhvee.stores"
LINK_SHOPEE = "https://collshp.com/luhveestores?view=storefront"
LINK_ML = "https://www.mercadolivre.com.br/social/axwelloliveira"

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

        # Envio para SheetDB
        payload = {"DATA": datetime.now().strftime("%d/%m/%Y %H:%M"), "CLIENTE": nome.upper(), "WHATSAPP": num_limpo, "E-MAIL": email.lower(), "INTERESSE": escolha, "LOJA": loja_pref}
        try: requests.post(API_URL, json={"data": [payload]}, timeout=5)
        except: pass

        # --- LÓGICA DE MENSAGENS POR NICHO ---
        mensagens_nicho = {
            "Perfumes e Bodysplash (Fem/Masc)": "para você ficar sempre perfumada(o) e marcante! 🧴✨",
            "Scarpins e Saltos": "para você arrasar em qualquer ocasião com muito estilo! 👠🔥",
            "Moda Adulto e Infantil": "com as últimas tendências para toda a família! 👗👕",
            "Mamãe e Bebê": "escolhidos com todo carinho para esse momento especial! 🍼👶",
            "Pets": "para mimar o seu melhor amigo como ele merece! 🐾🐶",
            "Eletrodomésticos": "para facilitar sua vida e deixar sua casa moderna! 🏠⚡",
            "Cama, Mesa e Banho": "para transformar sua casa num verdadeiro hotel 5 estrelas! 🛌☁️",
            "Tênis Adulto e Infantil": "que unem conforto e performance para o dia a dia! 👟💨",
            "Lingerie": "para elevar sua autoestima com peças incríveis! 💖👙",
            "Sexshop": "para apimentar sua rotina com total discrição e prazer! 🔥🤫",
            "Brinquedos": "para garantir a diversão e o sorriso da garotada! 🧸🎈"
        }

        # Complemento baseado no nicho
        complemento = mensagens_nicho.get(escolha, "com as melhores ofertas que encontramos hoje! ✨")
        link_loja_alvo = LINK_SHOPEE if loja_pref == "Shopee" else LINK_ML
        emoji_loja = "🛍️" if loja_pref == "Shopee" else "📦"

        # Construção da Mensagem
        if escolha == "Outros ✨":
            texto_zap = (
                f"Olá {primeiro_nome}, tudo bem? 🥰\n\n"
                f"Recebi sua resposta e fiquei super curiosa! ✨\n\n"
                f"Vi que você tem interesse em produtos que ainda não temos na vitrine. Me conta: o que você está procurando? 🛍️\n\n"
                f"Vou caçar essa oferta exclusiva para você!\n\n"
            )
        else:
            texto_zap = (
                f"Olá {primeiro_nome}! ✨\n\n"
                f"Aqui é da LuhVee Stores. Separamos achadinhos de {escolha} {complemento}\n\n"
                f"Sua plataforma favorita é o {loja_pref}, então aqui está o atalho:\n"
                f"{emoji_loja} Vitrine {loja_pref}: {link_loja_alvo}\n\n"
            )

        # Bloco de Fechamento (Sempre presente)
        texto_zap += (
            f"🔗 Nosso Hub de Ofertas: {NOVO_HUB}\n"
            f"🎁 Grupo VIP (Ofertas Diárias): {LINK_GRUPO}\n\n"
            f"Acompanhe nossos achadinhos:\n"
            f"📸 Instagram: {INSTAGRAM}\n"
            f"🎥 TikTok: {TIKTOK}\n\n"
            f"Bjs e boas compras! 🛍️✨"
        )
        
        msg_encoded = urllib.parse.quote(texto_zap)
        link_final = f"https://wa.me/{num_limpo}?text={msg_encoded}"
        
        st.success(f"Tudo pronto, {primeiro_nome}! Clique no botão abaixo:")
        st.link_button("🎁 RECEBER MEUS LINKS NO WHATSAPP", link_final)
    else:
        st.error("❌ Por favor, preencha Nome, E-mail e WhatsApp.")
