from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
import glob

# Função para aguardar o download completo do arquivo
def wait_for_download(download_dir):
    # Espera até que o arquivo .crdownload não esteja mais no diretório
    while any(".crdownload" in filename for filename in os.listdir(download_dir)):
        time.sleep(1)

# Diretório para salvar os downloads
download_dir = "/Users/Anselmo/arquivos_salic"
download_dir = os.path.abspath(download_dir)  # Converte para caminho absoluto se necessário

# Configuração das opções do Chrome
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,  # Para desativar a confirmação de download
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Inicializa o WebDriver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# Maximiza a janela do navegador
driver.maximize_window()

# Define um tempo máximo de espera para os elementos serem encontrados
wait = WebDriverWait(driver, 10)

# Loop para cada ano
for ano in range(1993, 2025):
    # Verifica se o arquivo já existe para o ano atual
    if os.path.exists(os.path.join(download_dir, f'dados_salic_pj_{ano}.xls')):
        print(f"Arquivo para o ano {ano} já existe, pulando para o próximo ano.")
        continue
    try:
        # Restante do seu código para acessar a página, baixar e renomear arquivos...
        # ...

        # Se precisar interagir com a página principal novamente
        driver.switch_to.default_content()

        # Aguarda um tempo para garantir que a ação tenha sido realizada
        time.sleep(5)

    except Exception as e:
        print(f"Ocorreu um erro no ano {ano}: {e}")
        continue  # Continua para o próximo ano no caso de erro

# Fecha o navegador
driver.quit()

## Segunda parte do código, pega todos os XLS baixados e converte para CSV, com verificação.

# Diretório onde os arquivos .xls estão localizados
xls_dir = "/Users/Anselmo/arquivos_salic"

# Lista todos os arquivos .xls no diretório
xls_files = [f for f in os.listdir(xls_dir) if f.endswith('.xls')]

# Loop para verificar, converter e mover os arquivos
for xls_file in xls_files:
    # Obtém o caminho completo para o arquivo .xls
    xls_path = os.path.join(xls_dir, xls_file)

    # Remove a extensão .xls do nome do arquivo e adiciona .csv
    csv_file = os.path.splitext(xls_file)[0] + '.csv'

    # Obtém o caminho completo para o arquivo .csv (no mesmo diretório)
    csv_path = os.path.join(xls_dir, csv_file)

    # Verifica se o arquivo CSV correspondente já existe
    if os.path.exists(csv_path):
        print(f"Arquivo CSV '{csv_file}' já existe. Pulando conversão para este arquivo.")
        continue

    # Lê o arquivo .xls usando o pandas
    df = pd.read_excel(xls_path, engine='xlrd')  # Use o engine='xlrd' para arquivos .xls

    # Salva o DataFrame como um arquivo .csv
    df.to_csv(csv_path, index=False, encoding='utf-8')

    # Exclui o arquivo .xls após a conversão
    os.remove(xls_path)

# Parte para consolidar os arquivos .csv em um único arquivo

# Lista todos os arquivos .csv no diretório após a conversão
csv_files = [f for f in os.listdir(xls_dir) if f.endswith('.csv')]

# Inicializa uma lista vazia para armazenar os DataFrames
df_list = []

# Lê cada arquivo .csv e armazena o DataFrame na lista
for csv_file in csv_files:
    csv_path = os.path.join(xls_dir, csv_file)
    df = pd.read_csv(csv_path, encoding='utf-8')
    df_list.append(df)

# Concatena todos os DataFrames da lista em um único DataFrame
consolidated_df = pd.concat(df_list, ignore_index=True)

# Salva o DataFrame consolidado em um novo arquivo .csv
consolidated_csv_path = os.path.join(xls_dir, 'salic_consolidado.csv')
consolidated_df.to_csv(consolidated_csv_path, index=False, encoding='utf-8')

# Remove os arquivos .csv individuais após a consolidação
for csv_file in csv_files:
    os.remove(os.path.join(xls_dir, csv_file))

print("Consolidação concluída e arquivos individuais .csv excluídos.")
