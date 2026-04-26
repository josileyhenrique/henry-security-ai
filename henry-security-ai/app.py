import streamlit as st
from google import genai

# --- 1. CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit) ---
st.set_page_config(
    page_title="Henry Security AI", 
    page_icon="🛡️", 
    layout="wide"
)

# --- 2. ESTILIZAÇÃO ÉPICA (CSS Limpo e Sem Conflitos) ---
st.markdown("""
  <style>
    /* Fundo Principal */
    .stApp { 
        background-color: #0b0e14; 
    }
    
    /* Títulos e Subtítulos (Seletores específicos para evitar bugs) */
    h1, h2, h3, [data-testid="stMarkdownContainer"] p {
        color: #00ff41 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Ajuste do File Uploader (Onde estava o erro de texto encavalado) */
    [data-testid="stFileUploader"] {
        border: 1px dashed #00ff41;
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
    }

    /* Corrigindo a cor dos textos internos do Uploader que estavam bugados */
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small, 
    [data-testid="stFileUploadDropzone"] div {
        color: #00ff41 !important;
    }

    /* Botão Profissional e Legível */
    .stButton>button {
        width: 100%;
        background-color: #0000;
        color: #0b0e14 !important;
        border-radius: 6px;    
        border: 0 4px 15px rgba(0, 255, 65, 0.1);
        font-weight: 900;
        font-size: 1.1rem;
        height: 3.5em;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(0, 255, 65, 0.1);
    }

    .stButton>button:hover {
        background-color: #018723;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.4);
        transform: translateY(-2px);
    }

    /* Caixa do Relatório Final */
    .report-box {
        background-color: #1a1f29;
        border-left: 5px solid #00ff41;
        padding: 20px;
        border-radius: 0 8px 8px 0;
        color: #f0f0f0;
        font-family: 'Consolas', monospace;
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