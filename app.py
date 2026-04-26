import streamlit as st
from google import genai
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit) ---
st.set_page_config(
    page_title="Henry Security AI", 
    page_icon="🛡️", 
    layout="wide"
)


# --- 2. ESTILIZAÇÃO ELITE HENRY SECURITY (Versão 3.0) ---
st.markdown("""
    <style>
    /* Importando fontes sofisticadas */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&family=Space+Grotesk:wght@300;500;700&display=swap');

    .stApp { 
        background: radial-gradient(circle at top right, #111827, #0b0e14);
    }
    
    /* Títulos com Tipografia 'Space Grotesk' */
    h1 {
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -1px !important;
        font-size: 3rem !important;
        margin-bottom: 0px !important;
    }

    h3, p, label {
        color: #9ca3af !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 300 !important;
    }

    /* Badge 'PRO' ou Status */
    .status-badge {
        background: rgba(0, 200, 83, 0.1);
        color: #00c853;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        border: 1px solid rgba(0, 200, 83, 0.3);
        display: inline-block;
        margin-bottom: 20px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Área de Ingestão de Dados (Uploader) */
    [data-testid="stFileUploader"] {
        border: 1px solid rgba(255, 255, 255, 0.1);
        background-color: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    /* Botão de Comando (Sofisticação em cada pixel) */
    /* Botão Estilo 'Ghost' com Inversão de Cor no Hover */
    .stButton>button {
        width: 100%;
        background-color: transparent !important;
        color: #00c853 !important; /* Texto Verde Esmeralda (Repouso) */
        border: 1px solid #00c853 !important;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: bold;
        font-size: 0.85rem;
        letter-spacing: 2px;
        height: 3.5em;
        transition: all 0.3s ease-in-out;
        text-transform: uppercase;
    }

    /* Efeito de Inversão de Contraste */
    .stButton>button:hover {
        background-color: #00c853 !important; /* Fundo Verde */
        color: #0b0e14 !important; /* TEXTO MUDA PARA PRETO NO HOVER */
        box-shadow: 0 0 25px rgba(0, 200, 83, 0.5);
        transform: translateY(-2px);
    }

    /* Garante que o texto permaneça visível durante o clique */
    .stButton>button:active {
        color: #0b0e14 !important;
        background-color: #00e676 !important;
    }

    /* Caixa de Resposta (Output do Sistema) */
    .report-box {
        background-color: #0b0e14;
        border: 1px solid rgba(0, 200, 83, 0.2);
        padding: 30px;
        border-radius: 15px;
        color: #d1d5db;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        line-height: 1.8;
        position: relative;
        overflow: hidden;
    }

    .report-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: #00c853;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CHAMADA DO TÍTULO COM O BADGE ---
st.markdown('<div class="status-badge">SISTEMA ATIVO V3.0</div>', unsafe_allow_html=True)
st.title("Henry Security")
st.subheader("Inteligência Avançada de Logs e Detecção de Ameaças")
# --- 3. LÓGICA DE BACKEND (Processamento de Dados) ---
def preparar_logs(texto_bruto):
    """Limpa e limita o tamanho dos logs para otimizar a cota da IA."""
    linhas = [l.strip() for l in texto_bruto.split('\n') if l.strip()]
    # Enviamos as últimas 45 linhas para manter o foco no contexto recente
    return "\n".join(linhas[-45:])

# Inicialização Segura do Cliente

API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)


# Área de Entrada
arquivo = st.file_uploader("SISTEMA DE INGESTÃO DE LOGS (.TXT / .LOG)", type=["txt", "log"])

if arquivo:
    conteudo_bruto = arquivo.read().decode("utf-8")
    logs_prontos = preparar_logs(conteudo_bruto)
    
    st.info(f"SISTEMA PRONTO: {len(logs_prontos.splitlines())} linhas de dados normalizadas.")
# Ação de Análise
    if st.button("EXECUTAR PROTOCOLO DE ANÁLISE"):
        try:
            # 1. Barra de progresso (Agora identada corretamente)
            progresso = st.progress(0)
            for i in range(100):
                time.sleep(0.01)  # Simula o carregamento dos módulos
                progresso.progress(i + 1)
            
            # 2. Chamada da IA
            with st.spinner("AGENT HENRY ANALISANDO PADRÕES..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash", # Mantendo o 1.5 para estabilidade
                    contents=(
                        "Atue como um Especialista Sênior em Blue Team. "
                        "Analise os logs a seguir, identifique ataques (SQLi, Brute Force, etc.) "
                        "e gere um relatório técnico curto com recomendações de bloqueio: \n\n"
                        f"{logs_prontos}"
                    )
                )
                
                # Remove a barra de progresso após finalizar
                progresso.empty()
                
                st.success("PROTOCOLO FINALIZADO COM SUCESSO.")
                
                # Exibição do Relatório
                st.markdown("### 📋 RELATÓRIO TÉCNICO DE SEGURANÇA")
                st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ QUOTA EXCEDIDA: O motor de IA está em cooldown. Aguarde 60 segundos.")
            else:
                st.error(f"FALHA CRÍTICA NO MOTOR: {e}")

# --- 5. RODAPÉ ---
st.divider()
st.caption("Henry Security © 2026 | Desenvolvido por [Josiley Henrique] | AI Engineer Portfolio")
