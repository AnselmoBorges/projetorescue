# Projeto Mentoria Rescue
Esse projeto foi criado em Janeiro de 2023 com o intuito de auxiliar quem está começando na área de dados a ter um overview sobre algumas ferramentas da área de Engenharia de dados podem ser usadas para cada uma das partes do processo.
* Ingestão, pipeline básico e ferramentas
* Ferramentas de Data Plataform
* Ferramentas de tratamento dos dados
* Ferramentas de CI/CD e controle de versão como Github e Github Actions
* Ferramentas de visualização analitica.

## O desafio
Vamos pegar dados que estão disponíveis no site do Ministério da Cultura (salicNet), são os dados de incentivadores (Pessoa Juridica nesse caso) que contribuiram em algum projeto cultural de 1992 até o ano atual (2023), esses dados estão disponiveis no site (http://sistemas.cultura.gov.br/salicnet/Salicnet/Salicnet.php#) e estão divididos por ano, o primeiro desafio é centralizar esses dados que tem na sua origem a extensão `.xsl`o que não é viável pra gente, precisamos converte-los para `.csv`, centralizar todos os anos em um único arquivo e faço algumas melhorias nele como:
* mudança do header (cabeçalho) colocando strings mais fáceis de busca sem espaço como vem nos arquivos origem
* os campos string com nome da empresa e nome do projeto cultural, alguns foram inseridos em maiúsculo outros minúsculo, fiz uma padronização por todos maiúsculos.
* como cada arquivo representa um ano, no arquivo em si não consta a data dos incentivos, sendo assim atribui uma nova coluna para os dados de acordo com o ano que vem no arquivo `.xls`. Caso precise fazer calculos referente a anos por exemplo fica melhor.
* com tudo concluido vamos disponibilizar esse `.csv` em um storage account Azure para que seja criada uma tabela BRONZE/RAW no Databricks a partir dele.
* vamos fazer os tratamentos adequados e criação de tabelas fato e dimensão via DBT, documentando todo processo e fazendo um controle de versão. Outra vantagem desse step é o uso do Databricks SQL Analytics e armazenamento dos dados das tabelas no formato Delta, trazendo menor uso de espaço e melhor performance nas consultas analíticas.
* Com os dados todos disponíveis vamos realizar a exibição dos Dashboards usando o Superset.

## O que vai ser necessário?
Vou dividir o que vai ser necessário em cada uma das etapas e se você ainda não manja sobre cada uma delas, não esquenta, eu passo uns links de uns cursos que você pode fazer primeiro e depois voltar aqui sem problemas.
* Conhecimento básico de Python
* Conhecimento básico de Airflow
* Conhecimento básico sobre Storage Account Azure
* Conhecimento básico sobre Databricks
* Conhecimento básico sobre DBT
* Conhecimento básico de SQL
* Conhecimento básico de Docker

Caso não manje nenhum desses como já disse não esquenta, estou deixando o máximo mastigadinho o processo e vou linkar cada um desses com treinamentos rápidos a respeito, não se preocupe em fazer esse projeto rápido, é um cenário mais próximo do real onde você vai pegar TODOS os passos do processo, tem gente que trabalha a anos com isso e não conhece metade dessas ferramentas. Vai, estude o link que eu deixar, volte aqui e retome.


### Ingestão dos dados:
* Pontos necessários para essa fase:
** Instalação do Docker na sua máquina
** Criação de uma conta na Azure (use o tempo free caso não tenha, é de graça)
** Criação de um Storage Account na Azure
** Instalação do Airflow no seu Docker
** SEU PC TER MAIS DE 8GB DE RAM SENÃO O AIRFLOW VAI RODAR QUE NEM UMA CARROÇA!
** Ter um editor de texto instalado na sua maquina, preferencialmente o Visual Studio
** Seguir certinho os passos desse tutorial ;)

#### Instalando o Docker
Baixe o Docker desktop de acordo com seu sistema operacional (se for Windows ele precisa ser PRO)
* Windows - https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module
* MAC/OS - https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module
* Linux - https://docs.docker.com/desktop/linux/install/

Siga a orientação do proprio site para fazer a instalação mas não tem muito segredo e pra saber qual a função do Docker vou deixar um videozinho rápido pra você sair do zero.

#### Instalando o Airflow
Com o Docker instalado, vamos fazer o Download do `astro cli` que vai nos auxiliar na criação de um Airflow básico pra podermos dar sequência ao nosso projeto.



