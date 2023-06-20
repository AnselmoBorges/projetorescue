DROP DATABASE IF EXISTS projetorescue.rescue_b cascade; 

CREATE DATABASE IF NOT EXISTS projetorescue.rescue_b;

DROP TABLE IF EXISTS hive_metastore.rescue_b.dados_consolidados;

CREATE TABLE IF NOT EXISTS projetorescue.rescue_b.dados_consolidados (
    cpf_cnpj STRING COMMENT 'CNPJ da empresa incentivadora',
    incentivador STRING COMMENT 'Nome da empresa incentivadora ',
    nro_projeto STRING COMMENT 'Numero do projeto cultural cadastrado no Ministério da Cultura',
    nome_projeto STRING COMMENT 'Nome do projeto cultural incentivado',
    uf_projeto STRING COMMENT 'Estado em que aconteceu o projeto e incentivo',
    valor_incentivo STRING COMMENT 'Valor do incentivo em Reais',
    ano STRING COMMENT 'Ano em que aconteceu o incentivo'
) 
USING delta
COMMENT 'Dados das empresas incentivadoras de projetos culturais cadastrados na base do Ministerio da Cultura de 1993 a 2023';

ALTER TABLE projetorescue.rescue_b.dados_consolidados SET TBLPROPERTIES(mergeSchema = True);