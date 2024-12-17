import google.generativeai as genai
import pandas as pd


# df = pd.read_csv('uploads/acidentesJan2024_todas_causas_tipos.csv', encoding='latin-1', sep=";").to_string()
df = pd.read_excel('./uploads/acidentesJan2024_todas_causas_tipos_ex.xlsx').to_string()

# total = df.count(self,) .columns("Gênero").count()
# print((df['Genero'] == 'Masculino').sum())
genai.configure(api_key="AIzaSyBk4hjHMedwFJTgoW7ja8ZT-YoAvLRuXDE")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(f"Me dê insights detalhados sobre tipos de acidente da tabela: {df}")

print(response.text)