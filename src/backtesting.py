import pandas as pd
from src.indicadores import rsi


def ejecutar_backtest_sma_rsi (
    df: pd.DataFrame,
    sma_rapida: int = 10,
    sma_lenta: int = 50,
    rsi_periodo: int = 14,
    rsi_sobreventa: int = 30,
    rsi_sobrecompra: int = 70,
    ventana_rsi: int = 10
) -> dict:

    datos = df.copy()

    datos["SMA_rapida"] = datos["Close"].rolling(window=sma_rapida).mean()
    datos["SMA_lenta"] = datos["Close"].rolling(window=sma_lenta).mean()

    datos = rsi(datos, rsi_periodo)

    datos["Cruce_arriba"] = (
        (datos["SMA_rapida"] > datos["SMA_lenta"]) &
        (datos["SMA_rapida"].shift(1) <= datos["SMA_lenta"].shift(1))
    )

    datos["Cruce_abajo"] = (
        (datos["SMA_rapida"] < datos["SMA_lenta"]) &
        (datos["SMA_rapida"].shift(1) >= datos["SMA_lenta"].shift(1))
    )

    rsi_sobreventa_reciente = (
        (datos["RSI"] < rsi_sobreventa)
        .rolling(window=ventana_rsi)
        .max()
        .fillna(0)
        .astype(bool)
    )

    rsi_sobrecompra_reciente = (
        (datos["RSI"] > rsi_sobrecompra)
        .rolling(window=ventana_rsi)
        .max()
        .fillna(0)
        .astype(bool)
    )

    posicion_abierta = False
    precio_entrada = None
    fecha_entrada = None
    operaciones = []

    for fecha, fila in datos.iterrows():

        if not posicion_abierta:

            if fila["Cruce_arriba"] and rsi_sobreventa_reciente.loc[fecha]:
                posicion_abierta = True
                precio_entrada = fila["Close"]
                fecha_entrada = fecha

        else:

            if fila["Cruce_abajo"] and rsi_sobrecompra_reciente.loc[fecha]:
                precio_salida = fila["Close"]
                rendimiento_operacion = ((precio_salida - precio_entrada) / precio_entrada) * 100

                operaciones.append({
                    "Fecha Entrada": fecha_entrada,
                    "Precio Entrada": round(precio_entrada, 2),
                    "Fecha Salida": fecha,
                    "Precio Salida": round(precio_salida, 2),
                    "Rendimiento %": round(rendimiento_operacion, 2)
                })

                posicion_abierta = False

    total_operaciones = len(operaciones)
    ganadoras = len([op for op in operaciones if op["Rendimiento %"] > 0])
    tasa_acierto = (ganadoras / total_operaciones * 100) if total_operaciones > 0 else 0
    rendimiento_total = sum(op["Rendimiento %"] for op in operaciones)

    return {
        "operaciones": operaciones,
        "total_operaciones": total_operaciones,
        "ganadoras": ganadoras,
        "tasa_acierto": round(tasa_acierto, 2),
        "rendimiento_total": round(rendimiento_total, 2)
    }


def ejecutar_backtest_rsi_ma(
    df: pd.DataFrame,
    rsi_periodo: int = 14,
    media_rsi_periodo: int = 9,
    rsi_sobreventa: int = 30,
    rsi_sobrecompra: int = 70,
    ventana_rsi: int = 10
) -> dict:

    datos = df.copy()
    datos = rsi(datos, rsi_periodo)

    datos["Media_RSI"] = datos["RSI"].rolling(window=media_rsi_periodo).mean()

    datos["Cruce_arriba"] = (
        (datos["RSI"] > datos["Media_RSI"]) &
        (datos["RSI"].shift(1) <= datos["Media_RSI"].shift(1))
    )

    datos["Cruce_abajo"] = (
        (datos["RSI"] < datos["Media_RSI"]) &
        (datos["RSI"].shift(1) >= datos["Media_RSI"].shift(1))
    )

    rsi_sobreventa_reciente = (
        (datos["RSI"] < rsi_sobreventa)
        .rolling(window=ventana_rsi)
        .max()
        .fillna(0)
        .astype(bool)
    )

    rsi_sobrecompra_reciente = (
        (datos["RSI"] > rsi_sobrecompra)
        .rolling(window=ventana_rsi)
        .max()
        .fillna(0)
        .astype(bool)
    )

    posicion_abierta = False
    precio_entrada = None
    fecha_entrada = None
    operaciones = []

    for fecha, fila in datos.iterrows():

        if not posicion_abierta:

            if fila["Cruce_arriba"] and rsi_sobreventa_reciente.loc[fecha]:
                posicion_abierta = True
                precio_entrada = fila["Close"]
                fecha_entrada = fecha

        else:

            if fila["Cruce_abajo"] and rsi_sobrecompra_reciente.loc[fecha]:
                precio_salida = fila["Close"]
                rendimiento_operacion = ((precio_salida - precio_entrada) / precio_entrada) * 100

                operaciones.append({
                    "Fecha Entrada": fecha_entrada,
                    "Precio Entrada": round(precio_entrada, 2),
                    "Fecha Salida": fecha,
                    "Precio Salida": round(precio_salida, 2),
                    "Rendimiento %": round(rendimiento_operacion, 2)
                })

                posicion_abierta = False

    total_operaciones = len(operaciones)
    ganadoras = len([op for op in operaciones if op["Rendimiento %"] > 0])
    tasa_acierto = (ganadoras / total_operaciones * 100) if total_operaciones > 0 else 0
    rendimiento_total = sum(op["Rendimiento %"] for op in operaciones)

    return {
        "operaciones": operaciones,
        "total_operaciones": total_operaciones,
        "ganadoras": ganadoras,
        "tasa_acierto": round(tasa_acierto, 2),
        "rendimiento_total": round(rendimiento_total, 2)
    }

def calcular_curva_equity(operaciones: list, capital_inicial: float = 10000) -> list:

    capital = capital_inicial

    curva = [{
        "Fecha": None,
        "Capital": round(capital, 2)
    }]

    for operacion in operaciones:

        capital = capital * (1 + operacion["Rendimiento %"] / 100)

        curva.append({
            "Fecha": operacion["Fecha Salida"],
            "Capital": round(capital, 2)
        })

    return curva

