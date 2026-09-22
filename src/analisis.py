import pandas as pd
import numpy as np

def calcular_metricas(df: pd.DataFrame) -> dict:

    promedio = df["Close"].mean()
    maximo = df["Close"].max()
    minimo = df["Close"].min()

    primer_cierre = df["Close"].iloc[0]
    ultimo_cierre = df["Close"].iloc[-1]

    rendimiento = ((ultimo_cierre - primer_cierre) / primer_cierre) * 100

    volatilidad = df["Close"].pct_change().std() * 100

    fecha_max = df[df["Close"] == maximo].index[0].strftime("%Y-%m-%d")
    fecha_min = df[df["Close"] == minimo].index[0].strftime("%Y-%m-%d")

    rango_pct = ((maximo - minimo) / minimo) * 100
    
    return {
        "Promedio": round(promedio, 2),
        "Máximo": round(maximo, 2),
        "Fecha Máximo": fecha_max,
        "Mínimo": round(minimo, 2),
        "Fecha Mínimo": fecha_min,
        "Rendimiento %": round(rendimiento, 2),
        "Volatilidad %": round(volatilidad, 2),
        "Rango %": round(rango_pct, 2)
    }

def calcular_rendimiento_normalizado(datos_acciones: dict, tickers: list, periodo_grafico: int) -> pd.DataFrame:

    rendimientos = {}

    for ticker in tickers:

        df = datos_acciones[ticker].tail(periodo_grafico)
        close = df["Close"]

        rendimiento = ((close / close.iloc[0] - 1) * 100).round(2)

        rendimientos[ticker] = rendimiento.values

    resultado = pd.DataFrame(
        rendimientos,
        index=datos_acciones[tickers[0]].tail(periodo_grafico).index
    )

    return resultado


def calcular_metricas_riesgo(df: pd.DataFrame, tasa_libre_riesgo_anual: float = 0.0) -> dict:

    precios = df["Close"].to_numpy()
    retornos = df["Close"].pct_change().dropna().to_numpy()

    # Volatilidad anualizada
    volatilidad_anualizada = retornos.std() * np.sqrt(252)

    # Sharpe ratio
    tasa_libre_riesgo_diaria = tasa_libre_riesgo_anual / 252
    exceso_retorno = retornos - tasa_libre_riesgo_diaria
    sharpe_anual = (exceso_retorno.mean() / exceso_retorno.std()) * np.sqrt(252)

    # Máximo drawdown
    maximo_acumulado = np.maximum.accumulate(precios)
    drawdown = (precios - maximo_acumulado) / maximo_acumulado
    max_drawdown = drawdown.min()

    return {
        "Volatilidad Anualizada %": round(volatilidad_anualizada * 100, 2),
        "Sharpe Ratio": round(sharpe_anual, 2),
        "Máximo Drawdown %": round(max_drawdown * 100, 2),
    }