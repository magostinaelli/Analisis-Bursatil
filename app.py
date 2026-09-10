import requests
import io
import streamlit as st
import pandas as pd
from src.mercados_personalizados import cargar_mercados_personalizados, guardar_mercado_personalizado
from src.backtesting import calcular_curva_equity, ejecutar_backtest_rsi_ma, ejecutar_backtest_sma_rsi
from src.config import PERIODOS_DESCARGA, PERIODOS_GRAFICO, TITULO, VERSION, INDICADORES_TECNICOS
from src.mercado import obtener_datos
from src.analisis import calcular_metricas, calcular_rendimiento_normalizado
from src.mercados import MERCADOS
from src.indicadores import calcular_indicador
from lightweight_charts.widgets import StreamlitChart


st.set_page_config(page_title=TITULO, layout="wide")

st.title(TITULO)
st.caption(f"Versión: {VERSION}")

@st.cache_data
def obtener_lista_sp500():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}

    respuesta = requests.get(url, headers=headers)
    tabla = pd.read_html(io.StringIO(respuesta.text))[0]

    tabla = tabla[["Symbol", "Security"]].rename(
        columns={"Symbol": "symbol", "Security": "name"}
    )

    return tabla


mercados_personalizados = cargar_mercados_personalizados()
mercados_todos = {**MERCADOS, **mercados_personalizados}

modo = st.radio(
    "¿Qué desea analizar?",
    ["Mercado predefinido / guardado", "Tickers sueltos"]
)

if modo == "Mercado predefinido / guardado":

    mercado = st.selectbox("Seleccione un mercado", list(mercados_todos.keys()))
    tickers_ingresados = mercados_todos[mercado]

else:

    lista_sp500 = obtener_lista_sp500()

    opciones = [
        f"{fila['symbol']} - {fila['name']}"
        for _, fila in lista_sp500.iterrows()
    ]

    seleccionados = st.multiselect(
        "Busque y seleccione empresas (S&P 500)",
        opciones
    )

    tickers_ingresados = [s.split(" - ")[0] for s in seleccionados]
    mercado = "Personalizado"

    guardar = st.checkbox("Guardar como mercado personalizado")

    if guardar:
        nombre_nuevo_mercado = st.text_input("Nombre para este mercado")



periodo_nombre = st.selectbox(
    "Seleccione un período",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
)

if st.button("Analizar mercado"):

    tickers = tickers_ingresados

    if modo == "Tickers sueltos" and guardar and nombre_nuevo_mercado:
        guardar_mercado_personalizado(nombre_nuevo_mercado, tickers_ingresados)
        st.success(f"Mercado '{nombre_nuevo_mercado}' guardado.")

        
    periodo_descarga = PERIODOS_DESCARGA[periodo_nombre]

    resultados = []
    datos_acciones = {}

    for ticker in tickers:

        try:
            df = obtener_datos(ticker, periodo_descarga)
        except ValueError as error:
            st.warning(str(error))
            continue

        datos_acciones[ticker] = df

        df_metricas = df.tail(PERIODOS_GRAFICO[periodo_nombre])

        metricas = calcular_metricas(df_metricas)
        metricas["Ticker"] = ticker

        resultados.append(metricas)

    df_resultados = pd.DataFrame(resultados)

    df_resultados = df_resultados[
        [
            "Ticker",
            "Promedio",
            "Máximo",
            "Fecha Máximo",
            "Mínimo",
            "Fecha Mínimo",
            "Rendimiento %",
            "Volatilidad %",
            "Rango %",
        ]
    ]

    df_resultados = df_resultados.sort_values(by="Rendimiento %", ascending=False)

    st.session_state["mercado"] = mercado
    st.session_state["periodo_nombre"] = periodo_nombre
    st.session_state["datos_acciones"] = datos_acciones
    st.session_state["df_resultados"] = df_resultados

if "df_resultados" in st.session_state:

    df_resultados = st.session_state["df_resultados"]
    datos_acciones = st.session_state["datos_acciones"]
    periodo_nombre = st.session_state["periodo_nombre"]

    st.subheader(f"Resultados: {st.session_state['mercado']}")

    def color_rendimiento(val):
        color = "background-color: #2e7d4f; color: white" if val >= 0 else "background-color: #c94f4f; color: white"
        return color

    styled_df = df_resultados.style.map(
        color_rendimiento, subset=["Rendimiento %"]
    )

    st.dataframe(styled_df, width="stretch")

    st.subheader("Rendimiento por acción")
    st.bar_chart(df_resultados.set_index("Ticker")["Rendimiento %"])

    st.divider()
    st.subheader("Ver gráfico de un ticker")

    ticker_elegido = st.selectbox("Seleccione un ticker", list(datos_acciones.keys()))

    indicadores_nombres = st.multiselect(
        "Seleccione indicadores",
        [i["nombre"] for i in INDICADORES_TECNICOS.values()]
    )

    if st.button("Ver gráfico de precio"):

        df = datos_acciones[ticker_elegido].copy()

        indicadores_elegidos = [
            i for i in INDICADORES_TECNICOS.values() if i["nombre"] in indicadores_nombres
        ]

        periodo_media_default = 20

        for indicador in indicadores_elegidos:
            calcular_indicador(df, indicador, periodo_media_default)

        df = df.tail(PERIODOS_GRAFICO[periodo_nombre])

        datos = (
            df.reset_index()[["Date", "Open", "High", "Low", "Close", "Volume"]]
            .rename(columns={
                "Date": "time", "Open": "open", "High": "high",
                "Low": "low", "Close": "close", "Volume": "volume"
            })
        )

        datos["time"] = pd.to_datetime(datos["time"]).dt.tz_localize(None).astype("datetime64[ns]")

        chart = StreamlitChart(height=500)
        chart.legend(visible=True)
        chart.set(datos)
        for indicador in indicadores_elegidos:

            if indicador["nombre"] == "SMA":

                linea = chart.create_line(name=f"SMA {periodo_media_default}", color="#2962FF", width=2)

                datos_sma = (
                    df.reset_index()[["Date", "SMA"]]
                    .rename(columns={"Date": "time", "SMA": f"SMA {periodo_media_default}"})
                )

                datos_sma["time"] = pd.to_datetime(datos_sma["time"]).dt.tz_localize(None).astype("datetime64[ns]")

                linea.set(datos_sma)        
            elif indicador["nombre"] == "EMA":

                    linea = chart.create_line(name=f"EMA {periodo_media_default}", color="#FF9800", width=2)

                    datos_ema = (
                        df.reset_index()[["Date", "EMA"]]
                        .rename(columns={"Date": "time", "EMA": f"EMA {periodo_media_default}"})
                    )

                    datos_ema["time"] = pd.to_datetime(datos_ema["time"]).dt.tz_localize(None).astype("datetime64[ns]")

                    linea.set(datos_ema)

            elif indicador["nombre"] == "BB":

                for columna, nombre, color in [
                    ("Banda Superior", "BB Superior", "#808080"),
                    ("Banda Media", "BB Media", "#808080"),
                    ("Banda Inferior", "BB Inferior", "#808080"),
                ]:

                    linea_bb = chart.create_line(name=nombre, color=color, width=1)

                    datos_bb = (
                        df.reset_index()[["Date", columna]]
                        .rename(columns={"Date": "time", columna: nombre})
                    )

                    datos_bb["time"] = pd.to_datetime(datos_bb["time"]).dt.tz_localize(None).astype("datetime64[ns]")

                    linea_bb.set(datos_bb)

        chart.load()

        if "RSI" in indicadores_nombres:

            st.subheader("RSI")
            st.line_chart(df.set_index(df.index)["RSI"])

        if "MACD" in indicadores_nombres:

            st.subheader("MACD")
            st.line_chart(df.set_index(df.index)[["MACD", "Señal"]])

        if "ATR" in indicadores_nombres:

            st.subheader("ATR")
            st.line_chart(df.set_index(df.index)["ATR"])

        if "OBV" in indicadores_nombres:

            st.subheader("OBV")
            st.line_chart(df.set_index(df.index)["OBV"])

        if "ADX" in indicadores_nombres:

            st.subheader("ADX")
            st.line_chart(df.set_index(df.index)[["ADX", "+DI", "-DI"]])     

    st.divider()
    st.subheader("Comparar rendimiento de varias acciones")

    tickers_comparar = st.multiselect(
        "Seleccione entre 2 y 5 tickers para comparar",
        list(datos_acciones.keys())
    )

    if st.button("Comparar"):

        if len(tickers_comparar) < 2 or len(tickers_comparar) > 5:
            st.warning("Debe seleccionar entre 2 y 5 tickers.")

        else:

            df_comparacion = calcular_rendimiento_normalizado(
                datos_acciones,
                tickers_comparar,
                PERIODOS_GRAFICO[periodo_nombre]
            )

            st.line_chart(df_comparacion)               

    st.divider()
    st.subheader("Backtesting")

    ticker_backtest = st.selectbox("Seleccione un ticker para el backtest", list(datos_acciones.keys()), key="ticker_bt")

    estrategia_nombre = st.selectbox(
        "Seleccione una estrategia",
        ["SMA 10/50 + RSI 40/60", "SMA 10/50 + RSI 30/70", "RSI vs su media móvil (9 períodos)"]
    )

    ventana_rsi = st.selectbox("Ventana de días para validar señal RSI", [3, 5, 7, 10, 15])

    if st.button("Correr backtest"):

        df_backtest = obtener_datos(ticker_backtest, "5y")

        if estrategia_nombre == "SMA 10/50 + RSI 40/60":
            resultado_backtest = ejecutar_backtest_sma_rsi(
                df_backtest, rsi_sobreventa=40, rsi_sobrecompra=60, ventana_rsi=ventana_rsi
            )
        elif estrategia_nombre == "SMA 10/50 + RSI 30/70":
            resultado_backtest = ejecutar_backtest_sma_rsi(
                df_backtest, rsi_sobreventa=30, rsi_sobrecompra=70, ventana_rsi=ventana_rsi
            )
        else:
            resultado_backtest = ejecutar_backtest_rsi_ma(df_backtest, ventana_rsi=ventana_rsi)

        st.session_state["df_backtest"] = df_backtest
        st.session_state["resultado_backtest"] = resultado_backtest
        st.session_state["ticker_backtest"] = ticker_backtest

    if "resultado_backtest" in st.session_state:

        resultado_backtest = st.session_state["resultado_backtest"]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total operaciones", resultado_backtest["total_operaciones"])
        col2.metric("Ganadoras", resultado_backtest["ganadoras"])
        col3.metric("Tasa de acierto", f"{resultado_backtest['tasa_acierto']}%")
        col4.metric("Rendimiento total", f"{resultado_backtest['rendimiento_total']}%")



        df_operaciones = pd.DataFrame(resultado_backtest["operaciones"])

        if not df_operaciones.empty:
            df_operaciones["Fecha Entrada"] = df_operaciones["Fecha Entrada"].dt.strftime("%Y-%m-%d")
            df_operaciones["Fecha Salida"] = df_operaciones["Fecha Salida"].dt.strftime("%Y-%m-%d")

        st.dataframe(df_operaciones, width="stretch")         

        if st.button("Ver gráfico con marcadores"):

            df_backtest = st.session_state["df_backtest"]

            datos_marcadores = (
                df_backtest.reset_index()[["Date", "Open", "High", "Low", "Close", "Volume"]]
                .rename(columns={
                    "Date": "time", "Open": "open", "High": "high",
                    "Low": "low", "Close": "close", "Volume": "volume"
                })
            )

            datos_marcadores["time"] = pd.to_datetime(datos_marcadores["time"]).dt.tz_localize(None).astype("datetime64[ns]")

            chart_marcadores = StreamlitChart(height=500)
            chart_marcadores.legend(visible=True)
            chart_marcadores.set(datos_marcadores)

            for operacion in resultado_backtest["operaciones"]:

                fecha_entrada = pd.to_datetime(operacion["Fecha Entrada"]).tz_localize(None)
                fecha_salida = pd.to_datetime(operacion["Fecha Salida"]).tz_localize(None)

                chart_marcadores.marker(
                    time=fecha_entrada, position="below", shape="arrowUp", color="#26a69a", text="Compra"
                )
                chart_marcadores.marker(
                    time=fecha_salida, position="above", shape="arrowDown", color="#ef5350", text="Venta"
                )

            chart_marcadores.load()    

        capital_inicial = st.number_input("Capital inicial", min_value=1.0, value=10000.0, step=100.0)

        if st.button("Ver curva de equity"):

            df_backtest = st.session_state["df_backtest"]

            curva_equity = calcular_curva_equity(
                resultado_backtest["operaciones"],
                capital_inicial
            )

            curva_equity[0]["Fecha"] = df_backtest.index[0]

            df_equity = pd.DataFrame(curva_equity).rename(columns={"Fecha": "time"})
            df_equity["time"] = pd.to_datetime(df_equity["time"]).dt.tz_localize(None)
            df_equity = df_equity.set_index("time")

            st.line_chart(df_equity["Capital"])                