import pandas as pd
from pathlib import Path

# ===============================
# CONFIGURAÇÕES DE DIRETÓRIOS
# ===============================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# ===============================
# FUNÇÃO BASE PARA CSV DO SIDRA
# ===============================

def _load_sidra_transposto(csv_path: Path) -> pd.DataFrame:
    """
    Lê CSV exportado do SIDRA no formato 'transposto':
    - primeiras 6 linhas = metadados
    - linha 7 = cabeçalho verdadeiro (UFs)
    - linha 8 = valores
    - última linha (Fonte) precisa ser removida

    Retorna um DataFrame longo com colunas:
    UF | valor
    """

    # Lê pulando os metadados
    df = pd.read_csv(csv_path, sep=";", encoding="latin1", skiprows=6)

    # Remove linha da fonte (geralmente começa com "Fonte:")
    primeira_col = df.columns[0]
    df = df[~df[primeira_col].astype(str).str.contains("Fonte:", na=False)]

    # 🔥 Remove colunas indesejadas, como "Notas" ou vazias
    colunas_remover = [
        c for c in df.columns
        if isinstance(c, str) and ("Notas" in c or c.strip() == "")
    ]
    if colunas_remover:
        print("Removendo colunas extras:", colunas_remover)
        df = df.drop(columns=colunas_remover, errors="ignore")

    # 🔥 Remove qualquer linha que contenha "Notas"
    df = df[~df.apply(lambda row: row.astype(str).str.contains("Notas").any(), axis=1)]

    # Derrete colunas de UF em linhas
    long_df = df.melt(var_name="UF", value_name="valor")

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
# TABELA 4695 — IDADE × UF
# ===============================

def load_pns_depressao_idade(csv_path: Path) -> pd.DataFrame:
    df_long = _load_sidra_transposto(csv_path)

    df_long["year"] = 2019
    df_long["sexo"] = "Total"
    df_long["faixa_idade"] = "Total"   # CSV veio sem separação de idades
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


# ===============================
# FUNÇÃO PRINCIPAL (MASTER)
# ===============================

def build_neuropulse_base():
    # Arquivos de sexo (como você salvou na pasta data/raw)
    csv_sexo_total = DATA_RAW / "pns_depressao_sexo_total.csv"
    csv_sexo_masc  = DATA_RAW / "pns_depressao_sexo_masculino.csv"
    csv_sexo_fem   = DATA_RAW / "pns_depressao_sexo_feminino.csv"

    # Arquivo de idade (mantido como estava)
    csv_idade = DATA_RAW / "pns_depressao_uf_idade.csv"

    print(f"Lendo (sexo - total):      {csv_sexo_total}")
    print(f"Lendo (sexo - masculino):  {csv_sexo_masc}")
    print(f"Lendo (sexo - feminino):   {csv_sexo_fem}")
    df_sexo = load_pns_depressao_sexo(csv_sexo_total, csv_sexo_masc, csv_sexo_fem)

    print(f"Lendo (idade):             {csv_idade}")
    df_idade = load_pns_depressao_idade(csv_idade)

    # Junta tudo
    base = pd.concat([df_sexo, df_idade], ignore_index=True)

    out_path = DATA_PROCESSED / "neuropulse_pns_depressao.csv"
    base.to_csv(out_path, index=False, encoding="utf-8")

    print(f"\n✅ Dataset final salvo em:\n{out_path}\n")
    print(base.head())


# ===============================
# EXECUÇÃO DIRETA
# ===============================

if __name__ == "__main__":
    build_neuropulse_base()
