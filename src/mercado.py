import yfinance as yf
import pandas as pd

def obtener_datos(ticker: str, periodo: str) -> pd.DataFrame:

    activo = yf.Ticker(ticker)
    datos = activo.history(period=periodo)

    if datos.empty:
        raise ValueError(f"No se encontraron datos para el ticker '{ticker}'.")

    datos.index = datos.index.tz_localize(None)
    return datos