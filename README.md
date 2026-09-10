# 📈 Análisis Bursátil

Aplicación web interactiva para analizar acciones del mercado, calcular indicadores técnicos y evaluar estrategias de trading mediante backtesting, construida con Streamlit y Python.

## Funcionalidades

- **Análisis de mercados**: seleccioná un mercado predefinido (Tecnología, Farmacéuticas, Bancos) o armá tu propia selección de tickers del S&P 500.
- **Mercados personalizados**: guardá tus propias combinaciones de tickers para reutilizarlas después.
- **Métricas por acción**: promedio, máximo, mínimo, rendimiento %, volatilidad % y rango %, con tabla comparativa ordenada por rendimiento.
- **Gráfico de velas interactivo** con indicadores técnicos superpuestos: SMA, EMA, Bandas de Bollinger, RSI, MACD, ATR, OBV y ADX.
- **Comparación de rendimiento** normalizado entre 2 y 5 acciones simultáneamente.
- **Backtesting de estrategias**: probá estrategias basadas en cruces de medias móviles y RSI (SMA 10/50 + RSI, o RSI vs. su media móvil), con métricas de resultado (tasa de acierto, rendimiento total) y visualización de las operaciones sobre el gráfico de precios.
- **Curva de equity**: simulá la evolución de un capital inicial a lo largo de las operaciones del backtest.

## Stack técnico

- **Python**
- **Streamlit** — interfaz web
- **Pandas** — procesamiento y análisis de datos
- **yfinance** — descarga de datos históricos de mercado
- **lightweight-charts** — gráficos de velas interactivos
- **BeautifulSoup / lxml (vía pandas.read_html)** — obtención de la lista de tickers del S&P 500 desde Wikipedia

## Uso
streamlit run app.py

La aplicación se abre automáticamente en el navegador.

1. Elegí un mercado predefinido o armá una selección personalizada de tickers del S&P 500.
2. Seleccioná el período de análisis y presioná **"Analizar mercado"**.
3. Explorá las métricas, graficá un ticker en particular con indicadores técnicos, compará varias acciones entre sí, o corré un backtest de estrategia.

## Estructura del proyecto

```
├── app.py                          # Aplicación principal (Streamlit)
└── src/
    ├── config.py                   # Constantes y configuración general
    ├── mercado.py                  # Descarga de datos de mercado (yfinance)
    ├── mercados.py                 # Mercados predefinidos
    ├── mercados_personalizados.py  # Guardado/carga de mercados custom
    ├── analisis.py                 # Cálculo de métricas y rendimiento normalizado
    ├── indicadores.py              # Indicadores técnicos (SMA, EMA, RSI, MACD, BB, ATR, OBV, ADX)
    └── backtesting.py              # Lógica de backtesting y curva de equity
```

## Posibles mejoras a futuro

- Persistencia de mercados personalizados en una base de datos en lugar de un archivo JSON local.
- Más estrategias de backtesting configurables desde la interfaz.
- Exportar resultados de backtest a CSV/Excel.
- Tests automatizados para los módulos de cálculo (`analisis.py`, `indicadores.py`, `backtesting.py`).

## Nota

Este proyecto es de carácter educativo/demostrativo. No constituye asesoramiento financiero.

---

[https://www.linkedin.com/in/agostina-elli/)]
