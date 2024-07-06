
# Dashboard para Portafolio Cripto con Simulación Histórica

## Descripción General

Esta `webapp` basada en Streamlit proporciona un panel de control completo para el seguimiento y análisis de un portafolio de criptomonedas. Permite a los usuarios introducir sus tenencias de criptomonedas, visualizar el rendimiento histórico del portafolio y ver las estadísticas actuales del mismo.    

Podemos realizar una simulacion historica y comparar la evolucion de nuestra inversión en el tiempo.

## Características

- **Soporte para Múltiples Criptomonedas**: Seguimiento de BTC, XRP, ETH, DOGE y USDT.
- **Entrada de Tenencias Personalizada**: Introduce la cantidad de cada criptomoneda en tu portafolio.
- **Simulación Histórica**: Visualiza el rendimiento de tu portafolio desde una fecha de inicio seleccionada (por defecto: 1 de enero de 2021) hasta el presente.
- **Gráfico Interactivo**: Visualiza el valor total de tu portafolio a lo largo del tiempo con un gráfico de líneas interactivo.
- **Resumen del Portafolio Actual**: Observa un desglose de tus tenencias actuales, incluyendo precios actuales y porcentajes.
- **Estadísticas del Portafolio**: Visualiza estadísticas clave como el valor inicial, valor actual, rendimiento total, valor más alto y valor más bajo.

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/MRCSIBR/Dashboard-Crypto-with-Historical-Simulation.git
   cd panel-control-criptomonedas
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
   ```

3. Instala los paquetes requeridos:
   ```
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta la aplicación Streamlit:
   ```
   streamlit run panel_control_criptomonedas.py
   ```

2. Abre tu navegador web y ve a la URL mostrada en la terminal (normalmente `http://localhost:8501`).

3. Usa la barra lateral para introducir tus tenencias de criptomonedas y seleccionar una fecha de inicio para la simulación histórica.

4. La página principal mostrará:
   - Un gráfico que muestra el valor histórico de tu portafolio
   - Un resumen de tu portafolio actual
   - Estadísticas clave sobre el rendimiento de tu portafolio

## Fuente de Datos

Este panel de control utiliza Yahoo Finance (a través de la biblioteca `yfinance`) para obtener datos históricos de precios de criptomonedas.

## Personalización

Puedes modificar fácilmente las listas `CURRENCIES` y `YAHOO_SYMBOLS` en el script para añadir o eliminar criptomonedas del panel de control.

## Limitaciones

- La precisión de la simulación depende de la disponibilidad y exactitud de los datos históricos de Yahoo Finance.
- El panel de control no tiene en cuenta las comisiones de transacción, impuestos u otros costos asociados con el trading de criptomonedas.

## Contribuciones

¡Las contribuciones para mejorar el panel de control son bienvenidas! Por favor, no dudes en enviar issues o pull requests.

## Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

