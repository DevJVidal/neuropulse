# 🧠 NeuroPulse — Painel Interativo de Saúde Mental
Análise da Prevalência de Depressão no Brasil (PNS/IBGE – 2019)

📊 Projeto Acadêmico – Disciplina de Big Data em Python

---------------------------------------------------------------------------------------------------------------------------


## 📘 Sobre o Projeto

O NeuroPulse é um painel interativo desenvolvido em Python com uso de Streamlit, criado para analisar a prevalência de depressão diagnosticada por profissional de saúde mental no Brasil.
Este projeto utiliza dados reais, extraídos diretamente do SIDRA/IBGE (PNS 2019), com foco em três dimensões:

Unidades Federativas (UFs)

Sexo (Masculino / Feminino / Total)

Faixas etárias

O objetivo principal é demonstrar, de forma visual e intuitiva, como a depressão está distribuída pela população brasileira — permitindo comparações, filtros e análises exploratórias de forma simples e interativa.

---------------------------------------------------------------------------------------------------------------------------


## 🎯 Finalidade do Projeto

Este projeto foi desenvolvido como parte da disciplina Big Data em Python, com os seguintes propósitos:

Aplicar conceitos de ETL (Extract, Transform, Load) em dados reais.

Trabalhar manipulação de dados com pandas.

Realizar transformações, correções e padronizações necessárias para limpeza de dados governamentais.

Criar visualizações interativas utilizando Plotly.

Construir um dashboard completo com Streamlit, simulando um sistema real de análise de indicadores de saúde pública.

Explorar dados oficiais relacionados à saúde mental, contribuindo para estudos e discussões sobre políticas públicas.

---------------------------------------------------------------------------------------------------------------------------


## 📊 Dados Utilizados (Fontes Oficiais)

Todos os dados utilizados são reais, provenientes do:

SIDRA/IBGE — Pesquisa Nacional de Saúde (PNS – 2019)

Dados trabalhados:

Diagnóstico de depressão por profissional de saúde mental (%)

Distribuição por UF

Distribuição por sexo

Distribuição por faixa etária (18 a 29 anos, 30 a 59 anos, etc.)

Os arquivos CSV foram tratados em um pipeline ETL desenvolvido especialmente para este projeto.

---------------------------------------------------------------------------------------------------------------------------


## 🛠️ Tecnologias Utilizadas
Linguagem:

Python 3

Bibliotecas Principais:

Streamlit — criação do painel interativo

Pandas — limpeza, transformação e manipulação de dados

Plotly Express — gráficos interativos (barras e mapas)

Pathlib — organização dos diretórios

Unicodedata — padronização dos nomes dos estados (UFs)

---------------------------------------------------------------------------------------------------------------------------

## 🔄 Pipeline ETL Utilizado

O arquivo etl_neuropulse.py realiza:

Extração dos CSVs brutos do SIDRA.

Limpeza e padronização:

remoção de colunas “Notas”

remoção de linhas com metadados

padronização de UFs

conversão de números no padrão BR → padrão US

Transformação:

unificação dos dados de sexo

unificação dos dados de faixa etária

consolidação dos datasets em uma base única

Carga:

Geração do arquivo final:
neuropulse_pns_depressao.csv

Esse arquivo é utilizado pelo dashboard para alimentar as visualizações.

---------------------------------------------------------------------------------------------------------------------------


##📍 Principais Funcionalidades do Dashboard

Filtro por estado (UF)

Filtro por sexo

Filtro por faixa etária

Gráfico de barras por estado

Comparação entre sexos

Mapa interativo da prevalência de depressão no Brasil

Tabela completa dos dados filtrados

Interface totalmente estilizada com CSS customizado

---------------------------------------------------------------------------------------------------------------------------


## 🌎 Possíveis Aplicações

O NeuroPulse pode ser utilizado para:

Estudos acadêmicos sobre saúde mental

Análises de desigualdades regionais

Suporte a políticas públicas

Monitoramento da prevalência de depressão na população adulta

Demonstração de habilidades em manipulação de dados e visualização interativa

---------------------------------------------------------------------------------------------------------------------------

## 📌 Conclusão

O NeuroPulse demonstra como dados públicos podem ser transformados em informações visualmente claras e úteis para tomada de decisão.
Além do foco técnico em Big Data e Python, o projeto também destaca a importância da análise de dados de saúde mental no Brasil.
---------------------------------------------------------------------------------------------------------------------------

## 👨‍💻 Autor

Janderson Dias

Projeto desenvolvido para a disciplina **Big Data em Python**
