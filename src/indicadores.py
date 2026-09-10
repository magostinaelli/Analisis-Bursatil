import pandas as pd
from src.config import MACD_LENTA, MACD_RAPIDA, MACD_SENAL


def media_movil(df: pd.DataFrame, periodo: int) -> pd.DataFrame:

    df["SMA"] = df["Close"].rolling(window=periodo).mean()

    return df

def media_exponencial(df: pd.DataFrame, periodo: int) -> pd.DataFrame:

    df["EMA"] = df["Close"].ewm(span=periodo).mean()

    return df

def rsi(df: pd.DataFrame, periodo: int) -> pd.DataFrame:

    Delta = df["Close"].diff()
    Perdida = -Delta.clip(upper=0)
    Ganancia = Delta.clip(lower=0)
    Ganancia_Promedio = Ganancia.rolling(window=periodo).mean()
    Perdida_Promedio = Perdida.rolling(window=periodo).mean()
    rs = Ganancia_Promedio / Perdida_Promedio
    df["RSI"] = 100 - (100 / (1 + rs))

    return df

def macd(df: pd.DataFrame) -> pd.DataFrame:

    ema_rapida = df["Close"].ewm(span=MACD_RAPIDA).mean()
    ema_lenta = df["Close"].ewm(span=MACD_LENTA).mean()
    macd = ema_rapida - ema_lenta
    df["MACD"] = macd

    senal = macd.ewm(span=MACD_SENAL).mean()
    df["Señal"] = senal

    histograma = macd - senal
    df["Histograma"] = histograma

    return df

def bandas_bollinger(df: pd.DataFrame) -> pd.DataFrame:

    media = df["Close"].rolling(window=20).mean()
    desviacion = df["Close"].rolling(window=20).std()

    banda_media = media
    banda_superior = media + (2 * desviacion)
    banda_inferior = media - (2 * desviacion)

    df["Banda Superior"] = banda_superior
    df["Banda Media"] = banda_media
    df["Banda Inferior"] = banda_inferior

    return df

def atr(df: pd.DataFrame, periodo: int = 14) -> pd.DataFrame:

    high_low = df["High"] - df["Low"]
    high_close_prev = (df["High"] - df["Close"].shift(1)).abs()
    low_close_prev = (df["Low"] - df["Close"].shift(1)).abs()

    true_range = pd.concat(
        [high_low, high_close_prev, low_close_prev],
        axis=1
    ).max(axis=1)

    df["ATR"] = true_range.ewm(alpha=1/periodo, adjust=False).mean()

    return df

def obv(df: pd.DataFrame) -> pd.DataFrame:

    direccion = df["Close"].diff().apply(
        lambda x: 1 if x > 0 else (-1 if x < 0 else 0)
    )

    df["OBV"] = (direccion * df["Volume"]).cumsum()

    return df

def adx(df: pd.DataFrame, periodo: int = 14) -> pd.DataFrame:

    high_diff = df["High"].diff()
    low_diff = -df["Low"].diff()

    dm_positivo = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0.0)
    dm_negativo = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0.0)

    high_low = df["High"] - df["Low"]
    high_close_prev = (df["High"] - df["Close"].shift(1)).abs()
    low_close_prev = (df["Low"] - df["Close"].shift(1)).abs()

    true_range = pd.concat(
        [high_low, high_close_prev, low_close_prev],
        axis=1
    ).max(axis=1)

    tr_suavizado = true_range.ewm(alpha=1/periodo, adjust=False).mean()
    dm_positivo_suavizado = dm_positivo.ewm(alpha=1/periodo, adjust=False).mean()
    dm_negativo_suavizado = dm_negativo.ewm(alpha=1/periodo, adjust=False).mean()

    di_positivo = 100 * (dm_positivo_suavizado / tr_suavizado)
    di_negativo = 100 * (dm_negativo_suavizado / tr_suavizado)

    dx = 100 * (di_positivo - di_negativo).abs() / (di_positivo + di_negativo)

    df["+DI"] = di_positivo
    df["-DI"] = di_negativo
    df["ADX"] = dx.ewm(alpha=1/periodo, adjust=False).mean()

    return df

def calcular_indicador(df: pd.DataFrame, indicador: dict, periodo: int) -> pd.DataFrame:

    if indicador["nombre"] == "SMA":
        media_movil(df, periodo)
    elif indicador["nombre"] == "EMA":
        media_exponencial(df, periodo)
    elif indicador["nombre"] == "RSI":
        rsi(df, 14)
    elif indicador["nombre"] == "MACD":
        macd(df)    
    elif indicador["nombre"] == "BB":
        bandas_bollinger(df) 
    elif indicador["nombre"] == "ATR":
        atr(df)    
    elif indicador["nombre"] == "OBV":
        obv(df) 
    elif indicador["nombre"] == "ADX":
        adx(df)    
    return df

