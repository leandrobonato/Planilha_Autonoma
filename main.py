"""Ponto de entrada: agenda e executa as atualizações automáticas da planilha."""
import logging
import time

import schedule
from requests import RequestException

from src.config import LOG_FILE, SPREADSHEET_PATH, UPDATE_INTERVAL_MINUTES
from src.data_fetcher import fetch_quotes
from src.spreadsheet_manager import update_spreadsheet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger("main")


def job() -> None:
    logger.info("Iniciando ciclo de atualização...")
    try:
        quotes = fetch_quotes()
        update_spreadsheet(quotes)
    except RequestException as exc:
        logger.error("Falha ao buscar dados da web: %s", exc)
    except Exception:
        logger.exception("Erro inesperado durante o ciclo de atualização.")


def main() -> None:
    logger.info("Planilha Autônoma iniciada.")
    logger.info("Arquivo alvo: %s", SPREADSHEET_PATH)
    logger.info("Intervalo de atualização: %s minuto(s).", UPDATE_INTERVAL_MINUTES)

    job()  # primeira execução imediata
    schedule.every(UPDATE_INTERVAL_MINUTES).minutes.do(job)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Encerrado pelo usuário.")


if __name__ == "__main__":
    main()
