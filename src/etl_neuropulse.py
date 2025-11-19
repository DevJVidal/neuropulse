import pandas as pd
from pathlib import Path
import unicodedata  # para remover acentos

# ===============================
# CONFIGURAÇÕES DE DIRETÓRIOS
# ===============================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


# ===============================
# HELPER: PADRONIZA UFs
# ===============================

def _padroniza_uf(serie_uf: pd.Series) -> pd.Series:
    """
    Padroniza nomes de UF para evitar duplicação:
    - remove espaços extras
    - remove acentos para comparar
    - mapeia para um nome canônico (com acento correto)
    """
    s = serie_uf.astype(str).str.strip()

    # remove acentos e deixa maiúsculo para chave do dicionário
    chave = (
        s.str.normalize("NFKD")
         .str.encode("ascii", "ignore")
         .str.decode("ascii")
         .str.upper()
    )

    mapa_uf = {
        "ACRE": "Acre",
        "ALAGOAS": "Alagoas",
        "AMAPA": "Amapá",
        "AMAZONAS": "Amazonas",
        "BAHIA": "Bahia",
        "CEARA": "Ceará",
        "DISTRITO FEDERAL": "Distrito Federal",
        "ESPIRITO SANTO": "Espírito Santo",
        "GOIAS": "Goiás",
        "MARANHAO": "Maranhão",
        "MATO GROSSO": "Mato Grosso",
        "MATO GROSSO DO SUL": "Mato Grosso do Sul",
        "MINAS GERAIS": "Minas Gerais",
        "PARA": "Pará",
        "PARAIBA": "Paraíba",
        "PARANA": "Paraná",
        "PERNAMBUCO": "Pernambuco",
        "PIAUI": "Piauí",
        "RIO DE JANEIRO": "Rio de Janeiro",
        "RIO GRANDE DO NORTE": "Rio Grande do Norte",
        "RIO GRANDE DO SUL": "Rio Grande do Sul",
        "RONDONIA": "Rondônia",
        "RORAIMA": "Roraima",
        "SANTA CATARINA": "Santa Catarina",
        "SAO PAULO": "São Paulo",
        "SERGIPE": "Sergipe",
        "TOCANTINS": "Tocantins",
        "BRASIL": "Brasil",
    }

    return chave.map(mapa_uf).fillna(s)


# ===============================
# FUNÇÃO BASE PARA CSV DO SIDRA (TRANSPOSTO)
# ===============================

def _load_sidra_transposto(csv_path: Path) -> pd.DataFrame:
    """
    Lê CSV exportado do SIDRA no formato 'transposto':
    - primeiras linhas = metadados
    - cabeçalho com UFs nas colunas
    - última linha (Fonte) removida

    Retorna um DataFrame longo com colunas:
    UF | valor
    """

    df = pd.read_csv(csv_path, sep=";", encoding="latin1", skiprows=6)

    # Remove linha da fonte (geralmente começa com "Fonte:")
    primeira_col = df.columns[0]
    df = df[~df[primeira_col].astype(str).str.contains("Fonte:", na=False)]

    # Remove colunas indesejadas, como "Notas" ou vazias
    colunas_remover = [
        c for c in df.columns
        if isinstance(c, str) and ("Notas" in c or c.strip() == "")
    ]
    if colunas_remover:
        print("Removendo colunas extras:", colunas_remover)
        df = df.drop(columns=colunas_remover, errors="ignore")

    # Remove qualquer linha que contenha "Notas"
    df = df[~df.apply(lambda row: row.astype(str).str.contains("Notas").any(), axis=1)]

    # Derrete colunas de UF em linhas
    long_df = df.melt(var_name="UF", value_name="valor")

    # PADRONIZA UFs
    long_df["UF"] = _padroniza_uf(long_df["UF"])

    # Limpa vírgula decimal → ponto, espaços, etc.
    long_df["valor"] = (
        long_df["valor"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "")
    )

    # Converte para número, ignorando erros
    long_df["valor"] = pd.to_numeric(long_df["valor"], errors="coerce")

    # Remove linhas sem valor numérico
    long_df = long_df.dropna(subset=["valor"])

    return long_df


# ===============================
# VARIAÇÃO: COM GRUPO (NÃO USADA EM IDADE AGORA, MAS MANTIDA)
# ===============================

def _load_sidra_transposto_com_grupo(csv_path: Path, nome_col_grupo: str) -> pd.DataFrame:
    """
    Versão do loader que preserva a 1ª coluna como um 'grupo'
    (ex: faixa de idade).

    Retorna um DataFrame longo com colunas:
    nome_col_grupo | UF | valor
    """

    df = pd.read_csv(csv_path, sep=";", encoding="latin1", skiprows=6)

    # Remove linha da fonte (geralmente começa com "Fonte:")
    primeira_col = df.columns[0]
    df = df[~df[primeira_col].astype(str).str.contains("Fonte:", na=False)]

    # Remove colunas indesejadas, como "Notas" ou vazias
    colunas_remover = [
        c for c in df.columns
        if isinstance(c, str) and ("Notas" in c or c.strip() == "")
    ]
    if colunas_remover:
        print("Removendo colunas extras:", colunas_remover)
        df = df.drop(columns=colunas_remover, errors="ignore")

    # Remove qualquer linha que contenha "Notas"
    df = df[~df.apply(lambda row: row.astype(str).str.contains("Notas").any(), axis=1)]

    # Renomeia a 1ª coluna para o nome do grupo (ex.: "faixa_idade")
    df = df.rename(columns={primeira_col: nome_col_grupo})

    # Derrete as UFs em linhas, preservando o grupo
    long_df = df.melt(
        id_vars=[nome_col_grupo],
        var_name="UF",
        value_name="valor"
    )

    # PADRONIZA UFs
    long_df["UF"] = _padroniza_uf(long_df["UF"])

    # Limpa vírgula decimal → ponto, espaços, etc.
    long_df["valor"] = (
        long_df["valor"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "")
    )

    # Converte para número, ignorando erros
    long_df["valor"] = pd.to_numeric(long_df["valor"], errors="coerce")

    # Remove linhas sem valor numérico
    long_df = long_df.dropna(subset=["valor"])

    return long_df


# ===============================
# TABELA 4694 — SEXO × UF
# ===============================

def _load_pns_sexo(csv_path: Path, sexo_rotulo: str) -> pd.DataFrame:
    """
    Lê um CSV da Tabela 4694 (já filtrado por 1 sexo)
    e devolve no formato padrão do projeto.
    """
    df_long = _load_sidra_transposto(csv_path)

    df_long["year"] = 2019
    df_long["sexo"] = sexo_rotulo      # "Total", "Masculino" ou "Feminino"
    df_long["faixa_idade"] = "Total"
    df_long["domicilio"] = "Total"
    df_long["indicador"] = "depressao_diagnosticada_percentual"
    df_long["transtorno"] = "Depressão"

    df_long = df_long[
        [
            "year",
            "UF",
            "sexo",
            "faixa_idade",
            "domicilio",
            "transtorno",
            "indicador",
            "valor",
        ]
    ]

    return df_long


def load_pns_depressao_sexo(
    csv_total: Path,
    csv_masc: Path,
    csv_fem: Path,
) -> pd.DataFrame:
    """
    Junta os três arquivos de sexo:
    - pns_depressao_sexo_total.csv      -> sexo = "Total"
    - pns_depressao_sexo_masculino.csv  -> sexo = "Masculino"
    - pns_depressao_sexo_feminino.csv   -> sexo = "Feminino"
    """
    df_total = _load_pns_sexo(csv_total, "Total")
    df_masc = _load_pns_sexo(csv_masc, "Masculino")
    df_fem = _load_pns_sexo(csv_fem, "Feminino")

    df_sexo = pd.concat([df_total, df_masc, df_fem], ignore_index=True)
    return df_sexo


# ===============================
# TABELA 4695 — IDADE × UF (FORMATO LONGO)
# ===============================

def load_pns_depressao_idade(csv_path: Path) -> pd.DataFrame:
    """
    Lê o CSV da tabela 4695 NO FORMATO LONGO, como você mostrou:
    "Grupo de idade";"Unidade da Federação";""
    "18 a 29 anos";"Rondônia";"7,2"
    ...

    Converte para o padrão do projeto.
    """
    # pula as 4 primeiras linhas de metadados e usa a 5ª como cabeçalho
    df = pd.read_csv(csv_path, sep=";", encoding="latin1", skiprows=4, header=0)

    # Garante nomes de colunas (independe do nome exato da terceira)
    cols = df.columns.tolist()
    # Esperado: [ "Grupo de idade", "Unidade da Federação", <valor> ]
    if len(cols) < 3:
        raise ValueError(f"CSV de idade tem menos de 3 colunas: {cols}")

    df = df.rename(
        columns={
            cols[0]: "faixa_idade",
            cols[1]: "UF",
            cols[2]: "valor",
        }
    )

    # Remove linha de Fonte, se existir
    df = df[~df["faixa_idade"].astype(str).str.contains("Fonte", na=False)]

    # Tira espaços e padroniza
    df["faixa_idade"] = df["faixa_idade"].astype(str).str.strip()
    df["UF"] = _padroniza_uf(df["UF"])

    # Limpa valor (vírgula → ponto)
    df["valor"] = (
        df["valor"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "")
    )
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.dropna(subset=["valor"])

    # Remove linha agregada "Brasil", se tiver
    df = df[df["UF"] != "Brasil"]

    # Adiciona colunas fixas
    df["year"] = 2019
    df["sexo"] = "Total"      # tabela já é agregada (Total)
    df["domicilio"] = "Total"
    df["indicador"] = "depressao_diagnosticada_percentual"
    df["transtorno"] = "Depressão"

    df = df[
        [
            "year",
            "UF",
            "sexo",
            "faixa_idade",
            "domicilio",
            "transtorno",
            "indicador",
            "valor",
        ]
    ]

    return df


# ===============================
# FUNÇÃO PRINCIPAL (MASTER)
# ===============================

def build_neuropulse_base():
    # Arquivos de sexo (como você salvou na pasta data/raw)
    csv_sexo_total = DATA_RAW / "pns_depressao_sexo_total.csv"
    csv_sexo_masc  = DATA_RAW / "pns_depressao_sexo_masculino.csv"
    csv_sexo_fem   = DATA_RAW / "pns_depressao_sexo_feminino.csv"

    # Arquivo de idade
    csv_idade = DATA_RAW / "pns_depressao_uf_idade.csv"

    print(f"Lendo (sexo - total):      {csv_sexo_total}")
    print(f"Lendo (sexo - masculino):  {csv_sexo_masc}")
    print(f"Lendo (sexo - feminino):   {csv_sexo_fem}")
    df_sexo = load_pns_depressao_sexo(csv_sexo_total, csv_sexo_masc, csv_sexo_fem)

    print(f"Lendo (idade):             {csv_idade}")
    df_idade = load_pns_depressao_idade(csv_idade)

    # Junta tudo
    base = pd.concat([df_sexo, df_idade], ignore_index=True)

    # Só por segurança, remove qualquer duplicata exata
    base = base.drop_duplicates()

    out_path = DATA_PROCESSED / "neuropulse_pns_depressao.csv"
    base.to_csv(out_path, index=False, encoding="utf-8")

    print(f"\n✅ Dataset final salvo em:\n{out_path}\n")
    print(base.head())


# ===============================
# EXECUÇÃO DIRETA
# ===============================

if __name__ == "__main__":
    build_neuropulse_base()

    print("\n✅ Tudo certo!\n")