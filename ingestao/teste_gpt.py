import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Defina sua chave de API do OpenAI

# Caminho para o seu arquivo CSV
file_path = '/Users/Anselmo/arquivos_salic/salic_consolidado.csv'

# Carregar o conteúdo do arquivo
with open(file_path, 'r') as file:
    file_content = file.read()

# Definir o prompt para a análise de dados
prompt = f"Por favor analise os dados do seguinte arquivo csv\n\n{file_content}\n\nMe dê insights interessantes sobre esses dados, incluindo estatísticas encontradas e qualquer outro padrão que achar interessante."

# Fazer a chamada para a API do OpenAI
response = client.completions.create(model="text-davinci-003",  # Especifique o modelo que você está usando
prompt=prompt,
max_tokens=2048,
temperature=0.7  # Pode ajustar a temperatura conforme necessário)

# Imprimir a resposta
print(response.choices[0].text.strip())