import pandas as pd
from src.indicadores import adx, atr, bandas_bollinger, macd, obv, rsi
from src.indicadores import media_movil, media_exponencial

def test_media_movil_valores_basicos():

    fechas = pd.date_range("2026-01-01", periods=5, freq="D")

    df = pd.DataFrame({
        "Close": [10, 20, 30, 40, 50]
    }, index=fechas)

    resultado = media_movil(df, periodo=3)

    # Los primeros 2 valores no tienen suficientes datos -> NaN
    assert pd.isna(resultado["SMA"].iloc[0])
    assert pd.isna(resultado["SMA"].iloc[1])

    # SMA del día 3 = (10+20+30)/3 = 20
    assert resultado["SMA"].iloc[2] == 20

    # SMA del día 4 = (20+30+40)/3 = 30
    assert resultado["SMA"].iloc[3] == 30

    # SMA del día 5 = (30+40+50)/3 = 40
    assert resultado["SMA"].iloc[4] == 40

    
def test_media_exponencial_valores_basicos():

    fechas = pd.date_range("2026-01-01", periods=5, freq="D")

    df = pd.DataFrame({
        "Close": [10, 20, 30, 40, 50]
    }, index=fechas)

    resultado = media_exponencial(df, periodo=3)

    esperado = [10.0, 16.666667, 24.285714, 32.666667, 41.612903]

    for i, valor in enumerate(esperado):
        assert round(resultado["EMA"].iloc[i], 4) == round(valor, 4)

def test_rsi_valores_basicos():

    fechas = pd.date_range("2026-01-01", periods=8, freq="D")

    df = pd.DataFrame({
        "Close": [100, 102, 101, 105, 103, 107, 106, 110]
    }, index=fechas)

    resultado = rsi(df, periodo=3)

    assert pd.isna(resultado["RSI"].iloc[0])
    assert pd.isna(resultado["RSI"].iloc[1])
    assert pd.isna(resultado["RSI"].iloc[2])

    assert round(resultado["RSI"].iloc[3], 4) == round(85.714286, 4)
    assert round(resultado["RSI"].iloc[4], 4) == round(57.142857, 4)
    assert round(resultado["RSI"].iloc[5], 4) == round(80.0, 4)
    assert round(resultado["RSI"].iloc[6], 4) == round(57.142857, 4)
    assert round(resultado["RSI"].iloc[7], 4) == round(88.888889, 4)        


def test_macd_valores_basicos():

    precios = [
        100, 102, 101, 105, 103, 107, 106, 110, 109, 112,
        111, 115, 113, 117, 116, 120, 119, 123, 122, 126,
        125, 129, 128, 132, 131, 135, 134, 138, 137, 141
    ]

    fechas = pd.date_range("2026-01-01", periods=len(precios), freq="D")

    df = pd.DataFrame({"Close": precios}, index=fechas)

    resultado = macd(df)

    assert round(resultado["MACD"].iloc[-1], 4) == round(5.632516468086507, 4)
    assert round(resultado["Señal"].iloc[-1], 4) == round(4.598833775993777, 4)
    assert round(resultado["Histograma"].iloc[-1], 4) == round(1.0336826920927304, 4)

def test_bandas_bollinger_valores_basicos():

    precios = [
        100, 102, 101, 105, 103, 107, 106, 110, 109, 112,
        111, 115, 113, 117, 116, 120, 119, 123, 122, 126
    ]

    fechas = pd.date_range("2026-01-01", periods=len(precios), freq="D")

    df = pd.DataFrame({"Close": precios}, index=fechas)

    resultado = bandas_bollinger(df)

    assert round(resultado["Banda Media"].iloc[-1], 4) == round(111.85, 4)
    assert round(resultado["Banda Superior"].iloc[-1], 4) == round(127.4134524650406, 4)
    assert round(resultado["Banda Inferior"].iloc[-1], 4) == round(96.28654753495938, 4)    

def test_atr_valores_basicos():

    fechas = pd.date_range("2026-01-01", periods=8, freq="D")

    df = pd.DataFrame({
        "High":  [102, 104, 103, 106, 105, 108, 107, 110],
        "Low":   [99, 100, 100, 102, 101, 104, 103, 106],
        "Close": [101, 103, 101, 105, 103, 107, 105, 109]
    }, index=fechas)

    resultado = atr(df, periodo=3)

    esperado = [3.0, 3.333333, 3.222222, 3.814815, 3.876543, 4.251029, 4.167353, 4.444902]

    for i, valor in enumerate(esperado):
        assert round(resultado["ATR"].iloc[i], 4) == round(valor, 4)    

def test_obv_valores_basicos():

    fechas = pd.date_range("2026-01-01", periods=6, freq="D")

    df = pd.DataFrame({
        "Close":  [100, 102, 101, 101, 105, 103],
        "Volume": [1000, 1500, 1200, 900, 2000, 1100]
    }, index=fechas)

    resultado = obv(df)

    esperado = [0, 1500, 300, 300, 2300, 1200]

    for i, valor in enumerate(esperado):
        assert resultado["OBV"].iloc[i] == valor        

def test_adx_valores_basicos():

    fechas = pd.date_range("2026-01-01", periods=10, freq="D")

    df = pd.DataFrame({
        "High":  [102, 104, 103, 106, 105, 108, 107, 110, 109, 112],
        "Low":   [99, 100, 100, 102, 101, 104, 103, 106, 105, 108],
        "Close": [101, 103, 101, 105, 103, 107, 105, 109, 107, 111]
    }, index=fechas)

    resultado = adx(df, periodo=3)

    assert round(resultado["+DI"].iloc[-1], 4) == round(38.749789762852494, 4)
    assert round(resultado["-DI"].iloc[-1], 4) == round(8.052923697931266, 4)
    assert round(resultado["ADX"].iloc[-1], 4) == round(59.075465931591175, 4)