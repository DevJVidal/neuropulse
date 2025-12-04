
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-green?style=for-the-badge&color=green)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&color=blue)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red?style=for-the-badge&color=red)

# 🧠 NeuroPulse — Interactive Mental Health Dashboard
Analysis of the Prevalence of Depression in Brazil (PNS/IBGE – 2019)

📊 Academic Project – Big Data in Python Course

---------------------------------------------------------------------------------------------------------------------------


## 📘 About the Project

NeuroPulse is an interactive dashboard developed in Python using Streamlit, created to analyze the prevalence of depression diagnosed by mental health professionals in Brazil.
This project uses real data, extracted directly from SIDRA/IBGE (PNS 2019), focusing on three dimensions:

Federal Units (States)

Sex (Male / Female / Total)

Age ranges

The main objective is to demonstrate, in a visual and intuitive way, how depression is distributed throughout the Brazilian population — allowing for simple and interactive comparisons, filters, and exploratory analyses.

---------------------------------------------------------------------------------------------------------------------------


## 🎯 Project Purpose

This project was developed as part of the Big Data in Python course, with the following purposes:

Apply ETL (Extract, Transform, Load) concepts to real data.

Working with data manipulation using pandas.

Perform the necessary transformations, corrections, and standardizations for cleaning government data.

Create interactive visualizations using Plotly.

Build a complete dashboard with Streamlit, simulating a real-world system for analyzing public health indicators.

To explore official data related to mental health, contributing to studies and discussions on public policies.

---------------------------------------------------------------------------------------------------------------------------


## 📊 Data Used (Official Sources)  

All data used is real and comes from:

SIDRA/IBGE — National Health Survey (PNS – 2019)

Data worked:

Diagnosis of depression by a mental health professional (%)

Distribution by UF

Distribution by sex

Distribution by age group (18 to 29 years, 30 to 59 years, etc.)

The CSV files were processed in an ETL pipeline developed specifically for this project.

---------------------------------------------------------------------------------------------------------------------------


## 🛠️ Technologies Used
**Language:**  

Python 3

**Main Libraries:**

Streamlit — creating the interactive panel

Pandas — data cleaning, transformation, and manipulation

Plotly Express — interactive charts (bar and map charts)

Pathlib — directory organization

Unicodedata — standardization of state names (UFs)

---------------------------------------------------------------------------------------------------------------------------

## 🔄 ETL Pipeline Used

The etl_neuropulse.py file performs the following:

Extraction of raw CSVs from SIDRA.

Cleaning and standardization:

Removing "Notes" columns

removing rows with metadata

standardization of Brazilian states

Number conversion from BR standard to US standard.

Transformation:

unification of sex data

unification of age range data

Consolidation of datasets into a single database.

Load:

Final file generation:
neuropulse_pns_depressao.csv  

This file is used by the dashboard to populate the visualizations.

---------------------------------------------------------------------------------------------------------------------------


##📍 Main Features of the Dashboard  

Filter by state (UF)

Filter by gender

Filter by age group

Bar chart by state

Comparison between sexes

Interactive map of depression prevalence in Brazil.

Full table of filtered data

Fully styled interface with custom CSS.

---------------------------------------------------------------------------------------------------------------------------


## 🌎 Possible Applications

NeuroPulse can be used for:

Academic studies on mental health

Analyses of regional inequalities  

Support for public policies

Monitoring the prevalence of depression in the adult population.

Demonstration of skills in data manipulation and interactive visualization.

---------------------------------------------------------------------------------------------------------------------------

## 📌 Conclusion

NeuroPulse demonstrates how public data can be transformed into visually clear and useful information for decision-making.
In addition to its technical focus on Big Data and Python, the project also highlights the importance of analyzing mental health data in Brazil.
---------------------------------------------------------------------------------------------------------------------------

## 👨‍💻 Author

Janderson Dias

Project developed for the **Big Data in Python** course.
