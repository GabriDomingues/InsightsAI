import google.generativeai as genai
import pandas as pd
import streamlit as st

genai.configure(api_key="AIzaSyBk4hjHMedwFJTgoW7ja8ZT-YoAvLRuXDE")
model = genai.GenerativeModel("gemini-1.5-flash")


# df = pd.read_csv('uploads/acidentesJan2024_todas_causas_tipos.csv', encoding='latin-1', sep=";").to_string()
# df = pd.read_excel('./uploads/acidentesJan2024_todas_causas_tipos_ex.xlsx').to_string()
def gerar_insights(modelo, prompt, dataframe):
    # Converter os dados do DataFrame para string (limitado para não exceder tokens)
    dados_csv = dataframe.head(100).to_string(index=False)
    prompt_completo = f"{prompt}\n\nAqui estão os dados do arquivo CSV:\n{dados_csv}"

    # Chamada à IA do Gemini
    resposta = modelo.generate_content(prompt_completo)
    return resposta.text


# Título do app
st.title("Dashboard Inteligente com IA")
st.write("Faça upload de um arquivo CSV e solicite insights personalizados.")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])

# Verifica se o arquivo foi carregado e salva no session_state
if uploaded_file and "dataframe" not in st.session_state:
    st.session_state.dataframe = pd.read_csv(uploaded_file, encoding='latin-1', sep=";")
    st.success("Arquivo carregado com sucesso!")

# Se o DataFrame estiver no session_state, mostre os dados
if "dataframe" in st.session_state:
    st.write("### Dados do Arquivo:")
    st.dataframe(st.session_state.dataframe)

    # Área de texto para o prompt
    txt = st.text_area("Digite sua solicitação de insights", placeholder="Exemplo: Quantos registros existem?")
    df = st.session_state.dataframe
    # Pré-processamento: Exemplo de contagem de homens e mulheres
    homens = df[df['sexo'].str.lower() == 'Masculino'].shape[0]
    mulheres = df[df['sexo'].str.lower() == 'Feminino'].shape[0]

    # Construir uma resposta consistente
    dados_processados = f"Número de homens: {homens}\nNúmero de mulheres: {mulheres}"
    # Botão para gerar insights
    if st.button("Gerar Insights"):
        if txt:
            # Inicializar o modelo Gemini
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Gerar insights
            try:
                insights = gerar_insights(model, txt, st.session_state.dataframe)
                st.write("### Insights da IA:")
                st.write(insights)
            except Exception as e:
                st.error(f"Erro ao gerar insights: {e}")
        else:
            st.warning("Por favor, insira uma solicitação antes de gerar insights.")
else:
    st.warning("Por favor, carregue um arquivo CSV primeiro.")

# response = model.generate_content(f"Me dê insights detalhados sobre tipos de acidente da tabela: {df}")
# st.write(response.text)
