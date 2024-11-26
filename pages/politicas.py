# 1. Importaciones
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import pandas as pd
from utils import crear_resumen_ejecutivo, crear_seccion_contenido

# 2. Definición de variables globales
# Colores definidos
colors = {
    'primary': '#1C3D5A',
    'secondary': '#3E7CB1',
    'accent': '#A3D5FF',
    'background': '#FFFFFF',
    'text': '#333333'
}

# 3. Datos para los gráficos
years = list(range(2010, 2024))
gasto_publico = [22.5, 22.8, 23.1, 23.5, 23.9, 24.2, 24.6, 25.0, 25.4, 25.8, 32.1, 28.5, 27.2, 26.5]
inversion_publica = [3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5]
deuda_publica = [8.6, 11.1, 11.9, 12.8, 15.0, 17.3, 21.0, 23.6, 25.6, 28.0, 32.5, 34.9, 36.3, 38.1]
presion_fiscal = [19.5, 20.0, 20.5, 19.8, 19.6, 20.4, 20.2, 20.1, 21.1, 20.7, 19.3, 21.6, 22.1, 21.8]

df = pd.DataFrame({
    'Año': years,
    'Gasto Público (% PIB)': gasto_publico,
    'Inversión Pública (% PIB)': inversion_publica,
    'Deuda Pública (% PIB)': deuda_publica,
    'Presión Fiscal (% PIB)': presion_fiscal
})

# 4. Diccionario con los análisis para cada indicador
analisis_indicadores = {
    'Gasto Público (% PIB)': """
    El gasto público de Chile ha experimentado un crecimiento significativo, pasando del 22.5% del PIB en 2010 al 26.5% en 2023:
    
    - **Aumento por pandemia**: El pico del 32.1% en 2020 refleja las medidas de emergencia adoptadas durante la crisis del COVID-19.
    - **Rigidez presupuestaria**: Gran parte del gasto está comprometido en partidas inflexibles, limitando la capacidad de respuesta a nuevas necesidades.
    - **Eficiencia cuestionada**: A pesar del aumento, persisten deficiencias en servicios públicos clave como salud y educación.
    - **Desafíos futuros**: El envejecimiento de la población y las demandas sociales crecientes presionarán aún más el gasto público en los próximos años.

    Fuentes: Dirección de Presupuestos (DIPRES), Ministerio de Hacienda, FMI
    """,
    'Inversión Pública (% PIB)': """
    La inversión pública en Chile ha mostrado un crecimiento modesto pero constante, aumentando del 3.2% del PIB en 2010 al 4.5% en 2023:
    
    - **Infraestructura rezagada**: A pesar del aumento, Chile aún enfrenta un déficit significativo en infraestructura crítica.
    - **Concentración geográfica**: La inversión tiende a concentrarse en la región metropolitana, exacerbando las desigualdades regionales.
    - **Desafíos de ejecución**: Frecuentemente se observan retrasos y sobrecostos en proyectos de inversión pública.
    - **Necesidad de diversificación**: Se requiere mayor inversión en sectores estratégicos como energías renovables y tecnología.

    Fuentes: Ministerio de Obras Públicas, Banco Interamericano de Desarrollo (BID), CEPAL
    """,
    'Deuda Pública (% PIB)': """
    La deuda pública de Chile ha experimentado un aumento sustancial, pasando del 8.6% del PIB en 2010 al 38.1% en 2023:
    
    - **Crecimiento acelerado**: El ritmo de crecimiento de la deuda es preocupante, cuadruplicándose en poco más de una década.
    - **Presiones coyunturales**: La pandemia y las demandas sociales han acelerado el endeudamiento en los últimos años.
    - **Sostenibilidad a largo plazo**: Aunque aún manejable, la tendencia actual plantea dudas sobre la sostenibilidad fiscal a largo plazo.
    - **Calificación crediticia**: El aumento de la deuda podría afectar la calificación crediticia del país, encareciendo el financiamiento futuro.

    Fuentes: Banco Central de Chile, Ministerio de Hacienda, Fitch Ratings
    """,
    'Presión Fiscal (% PIB)': """
    La presión fiscal en Chile ha mostrado un ligero aumento, pasando del 19.5% del PIB en 2010 al 21.8% en 2023:
    
    - **Baja recaudación relativa**: A pesar del incremento, Chile mantiene una presión fiscal inferior al promedio de la OCDE (34%).
    - **Estructura regresiva**: El sistema tributario chileno depende en gran medida de impuestos indirectos, afectando más a los sectores de menores ingresos.
    - **Evasión y elusión**: Se estima que la evasión fiscal representa alrededor del 7% del PIB, limitando la capacidad recaudatoria del Estado.
    - **Reformas pendientes**: Existe un debate continuo sobre la necesidad de una reforma tributaria integral para aumentar la recaudación y mejorar la progresividad.

    Fuentes: Servicio de Impuestos Internos (SII), OCDE, Centro de Estudios Públicos (CEP)
    """
}

# 5. Definición del layout
def create_layout(app):
    return html.Div([
        html.Div([
            crear_resumen_ejecutivo("""
            El análisis de las políticas públicas en Chile revela un panorama complejo, con avances significativos
            pero también desafíos persistentes. El gasto público ha aumentado, reflejando una mayor intervención
            estatal, especialmente en respuesta a crisis como la pandemia. Sin embargo, la eficiencia y el impacto
            de este gasto siguen siendo cuestionados. La inversión pública, aunque creciente, aún no logra cerrar
            las brechas de infraestructura y desarrollo regional. El rápido aumento de la deuda pública plantea
            interrogantes sobre la sostenibilidad fiscal a largo plazo, mientras que la presión fiscal,
            aunque en aumento, sigue siendo baja en comparación con otros países de la OCDE.
            """),
            
            crear_seccion_contenido("Indicadores Clave de Políticas Públicas", [
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                id={'type': 'indicator-dropdown', 'page': 'politicas'},
                                options=[
                                    {'label': 'Gasto Público (% PIB)', 'value': 'Gasto Público (% PIB)'},
                                    {'label': 'Inversión Pública (% PIB)', 'value': 'Inversión Pública (% PIB)'},
                                    {'label': 'Deuda Pública (% PIB)', 'value': 'Deuda Pública (% PIB)'},
                                    {'label': 'Presión Fiscal (% PIB)', 'value': 'Presión Fiscal (% PIB)'}
                                ],
                                value='Gasto Público (% PIB)',
                                clearable=False
                            ),
                        ], style={'width': '100%', 'marginBottom': '20px'}),
                        dcc.Graph(
                            id={'type': 'indicator-graph', 'page': 'politicas'},
                            style={'height': '400px', 'width': '100%'}
                        ),
                    ], className="column-left", style={'width': '50%'}),
                    html.Div([
                        html.Div(id={'type': 'indicator-analysis', 'page': 'politicas'}, className="analysis-text")
                    ], className="column-right", style={'width': '50%'}),
                ], className="two-column-layout", style={'display': 'flex', 'justifyContent': 'space-between'}),
            ]),

            html.Div([
                html.H3("Reflexiones sobre el Modelo de Políticas Públicas en Chile", className="section-title"),
                dcc.Markdown("""
                El análisis de los indicadores de políticas públicas en Chile revela tensiones y contradicciones en el modelo de desarrollo del país:

                1. **Rol del Estado en la economía**: El aumento del gasto público refleja una mayor intervención estatal, alejándose del modelo neoliberal ortodoxo. Sin embargo, la eficacia de esta intervención sigue siendo cuestionada.
                
                2. **Desafíos de la inversión pública**: A pesar del aumento en la inversión, persisten brechas significativas en infraestructura y desarrollo regional, evidenciando la necesidad de una planificación más estratégica y de largo plazo.
                
                3. **Sostenibilidad fiscal**: El rápido aumento de la deuda pública plantea interrogantes sobre la sostenibilidad del modelo económico a largo plazo y la capacidad del Estado para responder a futuras crisis.
                
                4. **Equidad y sistema tributario**: La baja presión fiscal y la estructura regresiva del sistema tributario limitan la capacidad del Estado para implementar políticas redistributivas efectivas.
                
                5. **Desafíos demográficos y sociales**: El envejecimiento de la población y las crecientes demandas sociales ejercerán una presión adicional sobre el gasto público en los próximos años.

                Para abordar estos desafíos, Chile necesita:

                - Repensar el rol del Estado en la economía, buscando un equilibrio entre la intervención necesaria y la eficiencia del mercado.
                - Implementar una reforma tributaria integral que aumente la recaudación y mejore la progresividad del sistema.
                - Desarrollar una estrategia de inversión pública a largo plazo, enfocada en reducir las desigualdades regionales y preparar al país para los desafíos futuros.
                - Mejorar la eficiencia y transparencia del gasto público para asegurar que los recursos se traduzcan en mejoras tangibles en la calidad de vida de los ciudadanos.
                - Fomentar un debate nacional sobre el modelo de desarrollo deseado, buscando un nuevo consenso que equilibre crecimiento económico, equidad social y sostenibilidad ambiental.

                Fuentes principales: Ministerio de Hacienda, Banco Central de Chile, DIPRES, OCDE, CEPAL
                """, className="conclusion-text", style={'color': colors['text']})
            ], className="conclusion-section")
        ], className="page-content"),
    ], className="main-container")

# 6. Funciones auxiliares
def create_indicator_figure(indicator):
    try:
        trace = go.Scatter(
            x=df['Año'],
            y=df[indicator],
            mode='lines+markers',
            name=indicator,
            line=dict(color=colors['primary'], width=2),
            marker=dict(size=8, color=colors['secondary'])
        )

        layout = go.Layout(
            title=f'{indicator} en Chile (2010-2023)',
            xaxis=dict(
                title='Año',
                tickmode='array',
                tickvals=df['Año'][::2],  # Selecciona cada segundo año
                ticktext=df['Año'][::2].astype(str),
                tickangle=0
            ),
            yaxis=dict(title=indicator),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font=dict(family="Roboto", size=12, color=colors['text'])
        )

        return {'data': [trace], 'layout': layout}
    except Exception as e:
        return go.Figure()  # Figura vacía en caso de error

# 7. Callbacks
@callback(
    [Output({'type': 'indicator-graph', 'page': 'politicas'}, 'figure'),
     Output({'type': 'indicator-analysis', 'page': 'politicas'}, 'children')],
    [Input({'type': 'indicator-dropdown', 'page': 'politicas'}, 'value')]
)
def update_politicas_content(selected_indicator):
    if not selected_indicator:
        raise PreventUpdate

    try:
        fig = create_indicator_figure(selected_indicator)
        analysis = dcc.Markdown(analisis_indicadores[selected_indicator])
        return fig, analysis
    except Exception as e:
        return go.Figure(), f"Error: {str(e)}"

# 8. Inicialización de callbacks (si es necesario)
def init_callbacks(app):
    pass