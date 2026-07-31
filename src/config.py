"""Configurações centrais da aplicação."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

SPREADSHEET_PATH = DATA_DIR / "planilha_cotacoes.xlsx"
LOG_FILE = LOG_DIR / "app.log"

# API pública e gratuita (sem necessidade de chave/token) para cotações de moedas e cripto.
API_URL = "https://economia.awesomeapi.com.br/last/{pairs}"

# Pares monitorados: código-da-api -> nome amigável exibido na planilha.
CURRENCY_PAIRS = {
    "USD-BRL": "Dólar (USD/BRL)",
    "EUR-BRL": "Euro (EUR/BRL)",
    "BTC-BRL": "Bitcoin (BTC/BRL)",
}

SHEET_DASHBOARD = "Dashboard"
SHEET_HISTORY = "Histórico"

# Intervalo entre atualizações automáticas, em minutos.
UPDATE_INTERVAL_MINUTES = 30

# Máximo de linhas de histórico mantidas por ativo antes de começar a compactar.
MAX_HISTORY_ROWS = 2000

REQUEST_TIMEOUT_SECONDS = 10
