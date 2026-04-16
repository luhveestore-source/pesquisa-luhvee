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
MEU_WHATSAPP = "5511948021428" # O teu número comercial

# --- CABEÇALHO ---
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

    loja_selecionada = st.radio("Onde você prefere comprar?", ["Shopee", "Mercado Livre"])
    
    submit = st.form_submit_button("RECEBA PROMOÇÕES ❤️")

if submit:
    if nome and whatsapp_cliente and email:
        # Tratamento do número do cliente
        num_limpo = "".join(filter(str.isdigit, whatsapp_cliente))
        if len(num_limpo) <= 11: num_limpo = "55" + num_limpo
        primeiro_nome = nome.split()[0].title()

        # --- ENVIO PARA A PLANILHA ---
        payload = {
            "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "CLIENTE": nome.upper(),
            "WHATSAPP": num_limpo,
            "E-MAIL": email.lower(),
            "INTERESSE": escolha,
            "LOJA": loja_selecionada 
        }
        
        try:
            # Envia para o SheetDB - Certifique-se que a coluna F se chama LOJA (em maiúsculas)
            requests.post(API_URL, json={"data": [payload]}, timeout=5)
        except:
            pass

        # --- DICIONÁRIO DE MENSAGENS POR NICHO ---
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

        # --- LÓGICA DE DESTINO E MENSAGEM ---
        if escolha == "Outros ✨":
            # Manda para a LUANA (Dona da loja)
            texto_zap = (
                f"Olá Luana! ✨\n\n"
                f"Meu nome é {primeiro_nome} e acabei de responder sua pesquisa. 🥰\n\n"
                f"Escolhi a opção *'Outros'* porque procuro algo especial que não encontrei na vitrine. Pode me ajudar? 🛍️"
            )
            destino_final = MEU_WHATSAPP
            msg_sucesso = f"Tudo pronto, {primeiro_nome}! Clique abaixo para falar diretamente comigo no WhatsApp:"
        else:
            # Manda para o CLIENTE
            texto_zap = (
                f"Olá {primeiro_nome}! ✨\n\n"
                f"Aqui é da *LuhVee Stores*. Já separei achadinhos de *{escolha}* {frase_nicho}\n\n"
                f"Confira tudo agora no nosso *Hub Oficial* e nos siga nas redes sociais:\n"
                f"👉 {NOVO_HUB}\n\n"
                f"🎁 *Grupo VIP de Ofertas:* {LINK_GRUPO}\n\n"
                f"Qualquer dúvida, é só me chamar! Bjs e boas compras! 🛍️✨"
            )
            destino_final = num_limpo
            msg_sucesso = f"Tudo pronto, {primeiro_nome}! Clique abaixo para receber seus links no WhatsApp:"

        msg_encoded = urllib.parse.quote(texto_zap)
        link_final = f"https://wa.me/{destino_final}?text={msg_encoded}"
        
        st.success(msg_sucesso)
        st.link_button("🎁 ABRIR WHATSAPP", link_final)
    else:
        st.error("❌ Por favor, preencha Nome, E-mail e WhatsApp.")
