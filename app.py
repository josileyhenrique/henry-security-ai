import streamlit as st
from google import genai

# --- 1. CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit) ---
st.set_page_config(
    page_title="Henry Security AI", 
    page_icon="🛡️", 
    layout="wide"
)

# --- 2. ESTILIZAÇÃO ÉPICA (CSS Limpo e Sem Conflitos) ---
# --- 2. ESTILIZAÇÃO SOFISTICADA HENRY SECURITY (Versão Unificada) ---
st.markdown("""
    <style>
    /* Fundo Dark Profundo */
    .stApp { 
        background-color: #0b0e14; 
    }
    
    /* Tipografia Elegante */
    h1, h2, h3, [data-testid="stMarkdownContainer"] p, label {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 1px;
    }

    /* Ajuste do Título Principal para Verde Esmeralda */
    h1 {
        color: #00c853 !important;
        letter-spacing: 3px !important;
        text-transform: uppercase;
    }

    /* Área de Upload Estilo Glassmorphism */
    [data-testid="stFileUploader"] {
        border: 1px solid rgba(0, 200, 83, 0.2);
        background-color: rgba(22, 27, 34, 0.5);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 15px;
    }

    /* Cores dos textos internos do Uploader */
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small, 
    [data-testid="stFileUploadDropzone"] div {
        color: #8b949e !important;
    }

    /* Botão Sofisticado (Borda Fina e Elegante) */
    .stButton>button {
        width: 100%;
        background-color: transparent;
        color: #00c853 !important;
        border: 1px solid #00c853;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.9rem;
        letter-spacing: 2px;
        height: 3.5em;
        transition: all 0.3s ease;
        margin-top: 20px;
    }

    .stButton>button:hover {
        background-color: #00c853;
        color: #0b0e14 !important;
        box-shadow: 0 0 20px rgba(0, 200, 83, 0.4);
        transform: translateY(-2px);
    }

    /* Caixa do Relatório Final (Documento Técnico) */
    .report-box {
        background-color: rgba(26, 31, 41, 0.8);
        border-left: 4px solid #00c853;
        padding: 25px;
        border-radius: 0 10px 10px 0;
        color: #e0e0e0;
        font-family: 'Consolas', monospace;
        line-height: 1.6;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE BACKEND (Processamento de Dados) ---
def preparar_logs(texto_bruto):
    """Limpa e limita o tamanho dos logs para otimizar a cota da IA."""
    linhas = [l.strip() for l in texto_bruto.split('\n') if l.strip()]
    # Enviamos as últimas 45 linhas para manter o foco no contexto recente
    return "\n".join(linhas[-45:])

# Inicialização Segura do Cliente

API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# --- 4. INTERFACE DO USUÁRIO (Fluxo Linear) ---
st.title("🛡️ HENRY SECURITY")
st.subheader("SISTEMA DE INTELIGÊNCIA EM DEFESA CIBERNÉTICA")

# Área de Entrada
arquivo = st.file_uploader("SISTEMA DE INGESTÃO DE LOGS (.TXT / .LOG)", type=["txt", "log"])

if arquivo:
    conteudo_bruto = arquivo.read().decode("utf-8")
    logs_prontos = preparar_logs(conteudo_bruto)
    
    st.info(f"SISTEMA PRONTO: {len(logs_prontos.splitlines())} linhas de dados normalizadas.")

    # Ação de Análise
    if st.button("EXECUTAR PROTOCOLO DE ANÁLISE"):
        with st.spinner("🚀 AGENTE HENRY EM OPERAÇÃO..."):
            try:
               
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=(
                        "Atue como um Especialista Sênior em Blue Team. "
                        "Analise os logs a seguir, identifique ataques (SQLi, Brute Force, etc.) "
                        "e gere um relatório técnico curto com recomendações de bloqueio: \n\n"
                        f"{logs_prontos}"
                    )
                )
                
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
