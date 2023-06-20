## Importando o que a gente vai precisar:
### Airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.contrib.hooks.wasb_hook import WasbHook
from airflow.models import Variable

### Airflow > Databricks
from airflow.providers.databricks.operators.databricks_sql import (
    DatabricksCopyIntoOperator,
    DatabricksSqlOperator,
)

### Python
from datetime import datetime, timedelta
import xlrd, os, glob, re, csv, shutil
import pandas as pd

## Variaveis
### Paths:
PastaXLS = Variable.get("dados") + '/DadosSalicNetXLS'
PastaCSV = Variable.get("dados_temp")


### Cointainer Azure:
wh = WasbHook(wasb_conn_id='dados_rescue')
container_name = 'dados'
blob_name = 'dados_consolidados.csv'
arquivo_final = Variable.get("dados_finais") + blob_name
arquivo_final_adls = Variable.get("adls_path") + blob_name

### Variaveis Databricks:
connection_id = 'databricks'
http_path = Variable.get("http_path")

lista_arquivos = os.listdir(PastaXLS)

## Funçoes:
def _converte_arquivos():
    for i in lista_arquivos:
        ano = (re.findall("dados_pj_(\d+).xls", i))[0]
        wb = xlrd.open_workbook(PastaXLS + '/' + i, encoding_override='ISO-8859-1')
        arquivoExcel = pd.read_excel(wb).assign(ano_corrente=ano)
        nome = i.rpartition('.')[0]
        arquivo = PastaCSV + '/' + nome + '.csv'
        print('Gerando o arquivo: ' + arquivo)
        arquivoExcel.to_csv(arquivo, index = None, header=True)

        ## Mudando o nome do header dos arquivos
        headerCagado = arquivo
        headerBacana = os.path.splitext(headerCagado)[0] + "_nh.csv"

        with open(headerCagado, newline='') as entrada, open(headerBacana, 'w', newline='') as saida:
            r = csv.reader(entrada)
            w = csv.writer(saida)

            next(r, None)
            w.writerow(['cpf_cnpj','incentivador','nro_projeto','nome_projeto','uf_projeto','valor_incentivo','ano'])

            for row in r:
                w.writerow(row)

        ## Sobrescrevendo o CSV zuado com o corrigido:
        shutil.move(headerBacana, arquivo)
        print('Corrigindo o header do arquivo: ' + arquivo)

def _dataframe_consolidado():
    ## Unindo os CSVs em um único Dataframe
    lista_csvs = glob.glob(os.path.join(PastaCSV, "*.csv"))
    dados = pd.DataFrame()
    dados = pd.concat([pd.read_csv(l) for l in lista_csvs], ignore_index=True)
    
    ## Tratando os datatypes:
    dados = dados.fillna(0)
    dados = dados.astype({'cpf_cnpj': 'str','incentivador':'str','nro_projeto':'str','nome_projeto':'str','uf_projeto':'str','valor_incentivo': 'str', 'ano': 'int'})

    ## Gerando as linhas cagadas com o ano igual a zero:
    dados_cagados = dados.loc[dados['ano'] == 0]
    print(dados_cagados)
    arquivo_cagado= Variable.get("dados_finais") + '/arquivo_cagado.csv'
    dados_cagados.to_csv (arquivo_cagado, index = None, header=True)

    ## Formatando os dados corrigidos
    corrigido = pd.DataFrame()
    corrigido = pd.read_csv(Variable.get("dados") + '/arquivo_corrigido.csv')

    ## Removendo as linhas com ano 0 
    dados = dados.loc[dados['ano'] != 0]

    ## Fazendo a junção e ordenando os dados por ano
    dados = pd.concat([dados, corrigido], ignore_index=True)
    dados['incentivador'] = dados['incentivador'].str.upper()
    dados['nome_projeto'] = dados['nome_projeto'].str.upper()
    dados = dados.sort_values('ano')

    csv_final= Variable.get("dados_finais") + '/dados_consolidados.csv'
    dados.to_csv (csv_final, index = None, header=True)

def _valida_azureSA():
    return (wh.check_for_blob(container_name, blob_name))

def _envia_arquivo():
    wh.delete_blobs(container_name, blob_name)
    wh.load_file(arquivo_final, container_name, blob_name)
    return('Arquivo consolidado enviado para o Storage Account Azure!')

## Default_args serve pra setarmos alguns valores padrões que serão usados
## nas DAGS, sem a necessidade de repetirmos varias vezes no código.
default_args = {'owner': 'airflow',
                'start_date': datetime(2023,1,28),
                'concurrency': 1,
                'retry': 3,
                'retry_interval': timedelta(minutes=1)
                }

## Declarando a DAG:
with DAG (dag_id='ingestao_rescue', 
          schedule_interval=timedelta(minutes=30), 
          start_date=datetime(2023,1,28), 
          catchup=False) as dag:

    cria_diretorio_temp = BashOperator(
        task_id="cria_diretorio_temp",
        bash_command='mkdir -p /tmp/dados/DadosSalicNetCSV'
    )

    convertendo_dados = PythonOperator(
        task_id='convertendo_dados',
        python_callable=_converte_arquivos
    )

    dataframe_consolidado = PythonOperator(
        task_id='dataframe_consolidado',
        python_callable=_dataframe_consolidado
    )

    limpa_diretorio_temp = BashOperator(
        task_id="limpa_diretorio_temp",
        bash_command='rm -rf /tmp/dados/DadosSalicNetCSV/*.csv'
    )

    valida_azure = PythonOperator(
        task_id='valida_azure',
        python_callable=_valida_azureSA
    )

    envia_arquivo = PythonOperator(
        task_id='envia_arquivo',
        python_callable=_envia_arquivo
    )

    cria_estrutura_db = DatabricksSqlOperator(
        databricks_conn_id=connection_id,
        http_path=http_path,
        task_id="cria_estrutura_db",
        sql='sql/tabelaraw.sql'
    )

    ingestao_raw_db = DatabricksCopyIntoOperator(
        task_id="ingestao_raw_db",
        databricks_conn_id=connection_id,
        http_path=http_path,
        table_name="hive_metastore.rescue_b.dados_consolidados",
        file_format="CSV",
        file_location=arquivo_final_adls,
        format_options={"header": "true"},
        force_copy=True,
    )

cria_diretorio_temp >> convertendo_dados >> dataframe_consolidado >> limpa_diretorio_temp 
dataframe_consolidado >> valida_azure >> envia_arquivo
dataframe_consolidado >> cria_estrutura_db >> ingestao_raw_db

### Fim!