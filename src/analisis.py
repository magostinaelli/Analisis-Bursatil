import pandas as pd

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