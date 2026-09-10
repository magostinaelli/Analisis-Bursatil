import pandas as pd
from src.analisis import calcular_metricas


def test_calcular_metricas_valores_basicos():

    fechas = pd.date_range("2026-01-01", periods=5, freq="D")

    df = pd.DataFrame({
        "Close": [100, 110, 90, 120, 105]
    }, index=fechas)

    resultado = calcular_metricas(df)

    assert resultado["Promedio"] == 105.0
    assert resultado["Máximo"] == 120
    assert resultado["Fecha Máximo"] == "2026-01-04"
    assert resultado["Mínimo"] == 90
    assert resultado["Fecha Mínimo"] == "2026-01-03"
    assert resultado["Rendimiento %"] == 5.0
    assert resultado["Rango %"] == round(((120 - 90) / 90) * 100, 2)