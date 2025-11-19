from pathlib import Path

# Caminho do diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Pastas de dados
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

# Arquivos das fontes (você renomeia depois com os arquivos reais)
MIN_SAUDE_FILE = DATA_RAW / "saude_ministerio.csv"
IBGE_FILE = DATA_RAW / "ibge_pns.csv"
CDC_FILE = DATA_RAW / "cdc_usa.csv"

# Colunas padrão do dataset final
STANDARD_COLUMNS = [
    "source",
    "year",
    "region",
    "indicator_name",
    "disorder_type",
    "value",
]
