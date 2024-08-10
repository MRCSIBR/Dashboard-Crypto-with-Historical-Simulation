import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta

# Fecha: Sabado, 6 Julio 2024
# Update:           10.8.2024

# Configuración de tema de Streamlit para imitar los colores de Binance
st.set_page_config(page_title="Crypto Dashboard", page_icon="📊", layout="centered")

# Colores de Binance
BINANCE_YELLOW = "#F0B90B"
BINANCE_BLACK = "#1E2026"
BINANCE_DARK_GRAY = "#2B3139"
BINANCE_LIGHT_GRAY = "#474D57"
POSITIVE_GREEN = "#0ECB81"
NEGATIVE_RED = "#F6465D"

# Aplicar estilos CSS personalizados
st.markdown("""
    <style>
    .stApp {
    background-color: black;
    }
    .reportview-container {
        background-color: #1E2026;
        color: #FFFFFF;
    }
    .sidebar .sidebar-content {
        background-color: #2B3139;
    }
    .Widget>label {
        color: #F0B90B !important;
    }
    .stProgress .st-bo {
        background-color: #F0B90B;
    }
    </style>
    """, unsafe_allow_html=True)

# Lista de criptomonedas (incluyendo USDT y SOL)
MONEDAS = ["BTC", "XRP", "ETH", "DOGE", "USDT", "SOL"]

# Mapeo de criptomonedas a sus símbolos en Yahoo Finance
SIMBOLOS_YAHOO = {
    "BTC": "BTC-USD",
    "XRP": "XRP-USD",
    "ETH": "ETH-USD",
    "DOGE": "DOGE-USD",
    "USDT": "USDT-USD",
    "SOL": "SOL-USD"
}

def obtener_datos_historicos(simbolos, fecha_inicio):
    """Obtiene datos históricos de precios para los símbolos dados desde Yahoo Finance."""
    try:
        datos = yf.download(simbolos, start=fecha_inicio, end=datetime.now())
        return datos['Close']
    except Exception as e:
        st.error("Error al obtener datos históricos. Por favor, verifique su conexión a internet.")
        st.stop()

def main():
    st.title("Panel de Control de Cartera de Criptomonedas")

    # Añadir párrafo explicativo de uso
    st.markdown("""
    **Cómo usar este panel de control:**
    1. Utilice la barra lateral izquierda para ingresar sus tenencias en USD para cada criptomoneda.
    2. Seleccione una fecha de inicio para la simulación histórica.
    3. Explore los gráficos y estadísticas generados automáticamente:
       - Gráfico circular que muestra la distribución actual de su cartera.
       - Gráfico de líneas del valor total de su cartera a lo largo del tiempo.
       - Gráfico de líneas que muestra el rendimiento individual de BTC, ETH, DOGE y SOL.
       - Tabla de resumen con detalles actuales de su cartera.
       - Estadísticas clave de rendimiento de la cartera.
       - Actualice sus tenencias en cualquier momento para ver cómo cambian los resultados.
    """)

    # Entrada de usuario para tenencias y fecha de inicio
    st.sidebar.header("Ingrese sus Tenencias y Fecha de Inicio")
    tenencias = {}
    for moneda in MONEDAS:
        tenencias[moneda] = st.sidebar.number_input(f"Tenencias de {moneda} (USD):", min_value=0.0, value=0.0, step=1.0)

    fecha_inicio = st.sidebar.date_input("Seleccione fecha de inicio:", value=datetime.now() - timedelta(days=365))

    # Obtener datos históricos
    datos_historicos = obtener_datos_historicos([SIMBOLOS_YAHOO[moneda] for moneda in MONEDAS], fecha_inicio)

    # Calcular el valor diario de la cartera
    valor_cartera = pd.DataFrame(index=datos_historicos.index)
    for moneda in MONEDAS:
        valor_cartera[moneda] = tenencias[moneda] / datos_historicos[SIMBOLOS_YAHOO[moneda]].iloc[0] * datos_historicos[SIMBOLOS_YAHOO[moneda]]
    valor_cartera['Total'] = valor_cartera.sum(axis=1)

    # Crear gráfico circular de la asignación actual de la cartera
    asignacion_actual = valor_cartera.iloc[-1][:-1]  # Exclude 'Total'

    # Filtrar valores 0
    asignacion_filtrada = asignacion_actual[asignacion_actual > 0.01]  # Adjust threshold as needed
    fig_circular = px.pie(
        values=asignacion_filtrada,
        names=asignacion_filtrada.index,
        title="Asignación Actual de la Cartera"
    )
    fig_circular.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(colors=[BINANCE_YELLOW, BINANCE_LIGHT_GRAY, BINANCE_DARK_GRAY, "#A3A6B4", "#7D7F87", "#6750A4"]),
        showlegend=True
    )
    fig_circular.update_layout(
        paper_bgcolor=BINANCE_BLACK,
        plot_bgcolor=BINANCE_BLACK,
        font_color="white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    st.plotly_chart(fig_circular)

    # Crear gráfico de líneas del valor total de la cartera a lo largo del tiempo
    log_scale = st.checkbox("Mostrar en escala logarítmica")
    fig_total = go.Figure()
    fig_total.add_trace(go.Scatter(x=valor_cartera.index, y=valor_cartera['Total'],
                                   mode='lines', name='Valor Total de la Cartera', line=dict(color=BINANCE_YELLOW)))
    fig_total.update_layout(
        title='Valor Histórico Total de la Cartera',
        xaxis_title='Fecha',
        yaxis_title='Valor de la Cartera (USD)',
        height=400,
        paper_bgcolor=BINANCE_BLACK,
        plot_bgcolor=BINANCE_BLACK,
        font_color="white"
    )
    if log_scale:
        fig_total.update_yaxes(type="log")
    st.plotly_chart(fig_total)

    # Crear gráfico de líneas de los valores individuales de las criptomonedas a lo largo del tiempo
    fig_individual = go.Figure()
    colors = [BINANCE_YELLOW, BINANCE_LIGHT_GRAY, BINANCE_DARK_GRAY, "#6750A4"]
    for i, moneda in enumerate(["BTC", "ETH", "DOGE", "SOL"]):  # Monedas de ejemplo, incluyendo SOL
        fig_individual.add_trace(go.Scatter(x=valor_cartera.index, y=valor_cartera[moneda],
                                            mode='lines', name=moneda, line=dict(color=colors[i])))
    fig_individual.update_layout(
        title='Valores Históricos de Criptomonedas Individuales',
        xaxis_title='Fecha',
        yaxis_title='Valor (USD)',
        height=400,
        paper_bgcolor=BINANCE_BLACK,
        plot_bgcolor=BINANCE_BLACK,
        font_color="white"
    )
    st.plotly_chart(fig_individual)

    # Mostrar resumen actual de la cartera
    st.header("Resumen Actual de la Cartera")
    precios_actuales = datos_historicos.iloc[-1]
    precios_iniciales = datos_historicos.iloc[0]
    df_resumen = pd.DataFrame({
        'Moneda': MONEDAS,
        'Tenencias (USD)': [tenencias[moneda] for moneda in MONEDAS],
        'Precio Actual': [precios_actuales[SIMBOLOS_YAHOO[moneda]] for moneda in MONEDAS],
        'Precio Inicial': [precios_iniciales[SIMBOLOS_YAHOO[moneda]] for moneda in MONEDAS],
        'Cantidad Inicial': [tenencias[moneda] / precios_iniciales[SIMBOLOS_YAHOO[moneda]] for moneda in MONEDAS],
        'Cantidad Actual': [tenencias[moneda] / precios_actuales[SIMBOLOS_YAHOO[moneda]] for moneda in MONEDAS],
        'Valor Actual': [tenencias[moneda] for moneda in MONEDAS]
    })
    df_resumen['Porcentaje'] = df_resumen['Valor Actual'] / df_resumen['Valor Actual'].sum() * 100
    df_resumen = df_resumen.sort_values('Valor Actual', ascending=False).reset_index(drop=True)
    st.table(df_resumen.style.format({
        'Tenencias (USD)': '${:.2f}',
        'Precio Actual': '${:.2f}',
        'Precio Inicial': '${:.2f}',
        'Cantidad Inicial': '{:.6f}',
        'Cantidad Actual': '{:.6f}',
        'Valor Actual': '${:.2f}',
        'Porcentaje': '{:.2f}%'
    }).set_properties(**{'background-color': BINANCE_DARK_GRAY,
                         'color': 'white',
                         'border-color': BINANCE_LIGHT_GRAY}))

    # Mostrar estadísticas de la cartera
    st.header("Estadísticas de la Cartera")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Valor Inicial", f"${valor_cartera['Total'].iloc[0]:.0f}")
        st.metric("Valor Máximo", f"${valor_cartera['Total'].max():.2f}")

    with col2:
        valor_actual = valor_cartera['Total'].iloc[-1]
        valor_inicial = valor_cartera['Total'].iloc[0]
        delta_valor = valor_actual - valor_inicial
        delta_porcentaje = (delta_valor / valor_inicial) * 100
        st.metric(
            "Valor Actual",
            f"${valor_actual:.0f}",
            delta=f"{delta_porcentaje:+.2f}%",
            delta_color="normal"
        )
        st.metric("Valor Mínimo", f"${valor_cartera['Total'].min():.2f}")

    with col3:
        retorno_total = ((valor_cartera['Total'].iloc[-1] / valor_cartera['Total'].iloc[0]) - 1) * 100
        st.metric(
            "Retorno Total",
            f"{retorno_total:.2f}%",
            delta=f"{retorno_total:+.2f}%",
            delta_color="normal"
        )

if __name__ == "__main__":
    main()
