"""Coleta de dados na web (cotações de moedas e criptoativos)."""
import logging
from datetime import datetime
from typing import TypedDict

import requests

from src.config import API_URL, CURRENCY_PAIRS, REQUEST_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)


class Quote(TypedDict):
    label: str
    price: float
    variation_pct: float
    timestamp: datetime


def fetch_quotes() -> dict[str, Quote]:
    """Busca as cotações configuradas na API pública AwesomeAPI.

    Retorna um dicionário {codigo_par: Quote}. Levanta requests.RequestException
    em caso de falha de rede/HTTP para que o chamador decida como lidar (retry, log etc).
    """
    pairs_param = ",".join(CURRENCY_PAIRS.keys())
    url = API_URL.format(pairs=pairs_param)

    response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    raw = response.json()

    quotes: dict[str, Quote] = {}
    for pair_code, label in CURRENCY_PAIRS.items():
        api_key = pair_code.replace("-", "")
        item = raw.get(api_key)
        if item is None:
            logger.warning("Par %s não retornado pela API", pair_code)
            continue

        quotes[pair_code] = Quote(
            label=label,
            price=float(item["bid"]),
            variation_pct=float(item["pctChange"]),
            timestamp=datetime.now(),
        )

    return quotes
