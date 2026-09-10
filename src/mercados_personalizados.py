import json
import os

RUTA_ARCHIVO = os.path.join(os.path.dirname(__file__), "mercados_personalizados.json")


def cargar_mercados_personalizados() -> dict:

    if not os.path.exists(RUTA_ARCHIVO):
        return {}

    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_mercado_personalizado(nombre: str, tickers: list):

    mercados = cargar_mercados_personalizados()

    mercados[nombre] = tickers

    with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(mercados, f, ensure_ascii=False, indent=2)