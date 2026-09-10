TITULO = "Análisis Bursátil"
VERSION = "0.1.0"

PERIODOS = {
    1: "1mo",
    2: "3mo",
    3: "6mo",
    4: "1y",
    5: "2y",
    6: "5y"
}

MEDIAS_MOVILES = {
    "1mo": {
        1: 5,
        2: 10
    },
    "3mo": {
        1: 10,
        2: 20
    },
    "6mo": {
        1: 20,
        2: 50
    },
    "1y": {
        1: 20,
        2: 50,
        3: 100,
        4: 200
    }
}

INDICADORES_TECNICOS = {
    1: {"nombre": "SMA", "tipo": "overlay"},
    2: {"nombre": "EMA", "tipo": "overlay"},
    3: {"nombre": "RSI", "tipo": "panel"},
    4: {"nombre": "MACD", "tipo": "panel"},
    5: {"nombre": "BB", "tipo": "overlay"},
    6: {"nombre": "ATR", "tipo": "panel"},
    7: {"nombre": "OBV", "tipo": "panel"},
    8: {"nombre": "ADX", "tipo": "panel"}    
}

MACD_RAPIDA = 12
MACD_LENTA = 26
MACD_SENAL = 9

PERIODOS_DESCARGA = {
    "1mo": "3mo",
    "3mo": "6mo",
    "6mo": "1y",
    "1y": "2y",
    "2y": "5y",
    "5y": "10y"
}

PERIODOS_GRAFICO = {
    "1mo": 22,
    "3mo": 66,
    "6mo": 132,
    "1y": 252,
    "2y": 504,
    "5y": 1260
}