import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta

# Github: MRCSIBR
# Lista de criptomonedas (incluyendo USDT)
MONEDAS = ["BTC", "XRP", "ETH", "DOGE", "USDT"]

# Mapeo de criptomonedas a sus símbolos en Yahoo Finance
SIMBOLOS_YAHOO = {
    "BTC": "BTC-USD",
    "XRP": "XRP-USD",
    "ETH": "ETH-USD",
    "DOGE": "DOGE-USD",
    "USDT": "USDT-USD"
}

def obtener_datos_historicos(simbolos, fecha_inicio):
    """Obtiene datos históricos de precios para los símbolos dados desde Yahoo Finance."""
    datos = yf.download(simbolos, start=fecha_inicio, end=datetime.now())
    return datos['Close']

def main():
    st.title("Cartera de Criptomonedas con Simulación Histórica")

    # Añadir párrafo explicativo de uso
    st.markdown("""
    **Cómo usar este panel de control:**
    1. Utilice la barra lateral izquierda para ingresar sus tenencias en USD para cada criptomoneda.
    2. Seleccione una fecha de inicio para la simulación histórica.
    3. Explore los gráficos y estadísticas generados automáticamente:
       - Gráfico circular que muestra la distribución actual de su cartera.
       - Gráfico de líneas del valor total de su cartera a lo largo del tiempo.
       - Gráfico de líneas que muestra el rendimiento individual de BTC, ETH y DOGE.
       - Tabla de resumen con detalles actuales de su cartera.
       - Estadísticas clave de rendimiento de la cartera.
    
    4. Ejemplo de fecha: 12 de marzo de 2020: "Jueves Negro" de las criptomonedas

        El precio de Bitcoin cayó más del **50% en un solo día***, Bitcoin cotizaba a menos de $4,000.
        Este crash coincidió con una caída en los mercados tradicionales debido a las preocupaciones por la pandemia de COVID-19.
    
    Actualice sus tenencias en cualquier momento para ver cómo cambian los resultados.
    
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
    asignacion_actual = valor_cartera.iloc[-1][:-1]  # Excluir 'Total'
    fig_circular = px.pie(values=asignacion_actual, names=asignacion_actual.index, title="Asignación Actual de la Cartera")
    st.plotly_chart(fig_circular)

    # Crear gráfico de líneas del valor total de la cartera a lo largo del tiempo
    fig_total = go.Figure()
    fig_total.add_trace(go.Scatter(x=valor_cartera.index, y=valor_cartera['Total'],
                                   mode='lines', name='Valor Total de la Cartera'))
    fig_total.update_layout(
        title='Valor Histórico Total de la Cartera',
        xaxis_title='Fecha',
        yaxis_title='Valor de la Cartera (USD)',
        height=400
    )
    st.plotly_chart(fig_total)

    # Crear gráfico de líneas de los valores individuales de las criptomonedas a lo largo del tiempo
    fig_individual = go.Figure()
    for moneda in ["BTC", "ETH", "DOGE"]:  # Monedas de ejemplo
        fig_individual.add_trace(go.Scatter(x=valor_cartera.index, y=valor_cartera[moneda],
                                            mode='lines', name=moneda))
    fig_individual.update_layout(
        title='Valores Históricos de Criptomonedas Individuales',
        xaxis_title='Fecha',
        yaxis_title='Valor (USD)',
        height=400
    )
    st.plotly_chart(fig_individual)

    # Mostrar resumen actual de la cartera
    st.header("Resumen Actual de la Cartera")
    precios_actuales = datos_historicos.iloc[-1]
    df_resumen = pd.DataFrame({
        'Moneda': MONEDAS,
        'Tenencias (USD)': [tenencias[moneda] for moneda in MONEDAS],
        'Precio Actual': [precios_actuales[SIMBOLOS_YAHOO[moneda]] for moneda in MONEDAS],
        'Cantidad': [tenencias[moneda] / precios_actuales[SIMBOLOS_YAHOO[moneda]] for moneda in MONEDAS],
        'Valor Actual': [tenencias[moneda] for moneda in MONEDAS]
    })
    df_resumen['Porcentaje'] = df_resumen['Valor Actual'] / df_resumen['Valor Actual'].sum() * 100
    df_resumen = df_resumen.sort_values('Valor Actual', ascending=False).reset_index(drop=True)
    st.table(df_resumen.style.format({
        'Tenencias (USD)': '${:.2f}',
        'Precio Actual': '${:.2f}',
        'Cantidad': '{:.6f}',
        'Valor Actual': '${:.2f}',
        'Porcentaje': '{:.2f}%'
    }))

    # Mostrar estadísticas de la cartera
    st.header("Estadísticas de la Cartera")
    st.write(f"Valor Inicial: ${valor_cartera['Total'].iloc[0]:.2f}")
    st.write(f"Valor Actual: ${valor_cartera['Total'].iloc[-1]:.2f}")
    st.write(f"Retorno Total: {((valor_cartera['Total'].iloc[-1] / valor_cartera['Total'].iloc[0]) - 1) * 100:.2f}%")
    st.write(f"Valor Máximo: ${valor_cartera['Total'].max():.2f}")
    st.write(f"Valor Mínimo: ${valor_cartera['Total'].min():.2f}")

if __name__ == "__main__":
    main()
