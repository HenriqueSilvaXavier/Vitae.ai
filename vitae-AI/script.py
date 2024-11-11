import os
import openai
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize

# Defina sua chave de API aqui
openai.api_key = "SUA_CHAVE_DE_API"

# Baixar o pacote 'punkt' do NLTK (apenas uma vez)
nltk.download('punkt')

def verificar_estrutura(curriculo):
    # Pré-processamento
    tokens = word_tokenize(curriculo)

    # Normalização para evitar problemas de codificação
    tokens = [token.lower() for token in tokens]  # Converter para minúsculas
    if "experiência" in tokens and "educação" in tokens:
        print("Estrutura básica encontrada.")
    else:
        print("Estrutura básica não encontrada.")

# Carregar o currículo (exemplo)
with open('curriculo.txt', 'r', encoding='utf-8') as f:
    texto_curriculo = f.read()

verificar_estrutura(texto_curriculo)

def processar_curriculo(pdf_file):
    # Abrir o arquivo PDF
    with open(pdf_file, 'rb') as pdf_file_obj:
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        page_obj = pdf_reader.pages[0]
        texto_curriculo = page_obj.extract_text()

    # Limpeza e tokenização (simplificada)
    texto_limpo = texto_curriculo.lower()

    # Utilizando o ChatGPT para extrair informações (exemplo)
    prompt = f"Extraia as habilidades técnicas mencionadas no seguinte texto: {texto_limpo}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # ou "gpt-4" se você tiver acesso
        messages=[
            {"role": "system", "content": "Você é um assistente que extrai habilidades técnicas de currículos."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.5
    )

    habilidades = response.choices[0].message['content'].split(',')

    return habilidades

# Exemplo de uso
habilidades_encontradas = processar_curriculo("meu_curriculo.pdf")
print(habilidades_encontradas)
