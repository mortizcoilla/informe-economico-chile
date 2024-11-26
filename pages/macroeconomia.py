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
gdp_growth = [5.8, 6.1, 5.3, 4.0, 1.8, 2.3, 1.7, 1.2, 3.9, 1.1, -5.8, 11.7, 2.4, 0.2]
inequality = [0.51, 0.505, 0.505, 0.495, 0.495, 0.485, 0.48, 0.475, 0.47, 0.465, 0.46, 0.455, 0.45, 0.445]
productivity = [100, 102, 103, 104, 105, 106, 106, 107, 108, 109, 107, 110, 111, 112]
inflation = [1.4, 3.3, 3.0, 1.9, 4.4, 4.3, 2.7, 2.3, 2.6, 3.0, 3.0, 4.5, 11.6, 7.6]
unemployment = [8.2, 7.1, 6.4, 5.9, 6.4, 6.2, 6.5, 6.7, 7.0, 7.2, 10.8, 9.5, 7.9, 8.5]

df = pd.DataFrame({
    'Año': years,
    'Crecimiento del PIB (%)': gdp_growth,
    'Desigualdad (Gini)': inequality,
    'Índice de Productividad': productivity,
    'Inflación (%)': inflation,
    'Desempleo (%)': unemployment
})

# 4. Diccionario con los análisis para cada indicador
analisis_indicadores = {
    'Crecimiento del PIB (%)': """
    El crecimiento del PIB chileno, celebrado por muchos como un indicador de éxito económico, merece un escrutinio más profundo:
    - **Concentración de la riqueza**: A pesar del crecimiento, el 1% más rico de la población concentra el 25.5% de la riqueza, cuestionando quién se beneficia realmente de este crecimiento.
    - **Dependencia de materias primas**: El sector minero representa el 10% del PIB, exponiendo a Chile a volatilidades del mercado global y perpetuando un modelo extractivista insostenible.
    - **Baja productividad**: A pesar del crecimiento, la productividad laboral se ha estancado, revelando deficiencias estructurales en innovación y desarrollo de capital humano.
    Fuentes: Banco Central de Chile, World Inequality Database, INE Chile
    """,
    'Desigualdad (Gini)': """
    La desigualdad sigue siendo el talón de Aquiles del modelo de desarrollo chileno:
    - **Concentración de riqueza**: El 1% más rico concentra el 26.5% de la riqueza total, mientras el 50% más pobre apenas posee el 2.1%.
    - **Movilidad social estancada**: Un niño nacido en el 20% más pobre de la población necesitaría, en promedio, 6 generaciones para alcanzar el ingreso medio.
    - **Segregación espacial**: El 60% de la población urbana vive en barrios altamente segregados, perpetuando ciclos de pobreza y exclusión.
    - **Brecha de género**: Las mujeres ganan, en promedio, 31.7% menos que los hombres por trabajos equivalentes.
    Fuentes: Banco Mundial, PNUD, Fundación SOL
    """,
    'Inflación (%)': """
    La aparente estabilidad inflacionaria esconde realidades preocupantes:
    - **Disparidad en la canasta básica**: Mientras la inflación general es del 7.6%, los precios de alimentos básicos han aumentado un 9.9%, afectando desproporcionadamente a los más vulnerables.
    - **Vivienda inalcanzable**: El aumento de los precios inmobiliarios (10.4%) supera ampliamente la inflación oficial, exacerbando la crisis habitacional.
    - **Política monetaria cuestionable**: La obsesión por mantener baja la inflación ha llevado a políticas que pueden estar frenando el crecimiento y el empleo.
    Fuentes: Banco Central de Chile, INE Chile
    """,
    'Desempleo (%)': """
    El desempleo oficial del 8.5% oculta una realidad laboral mucho más precaria:
    - **Subempleo generalizado**: Un 12.8% de los trabajadores están subempleados o en empleos precarios sin protección social adecuada.
    - **Brecha de género persistente**: Las mujeres enfrentan una tasa de desempleo 1.5% mayor que los hombres, reflejando desigualdades estructurales.
    - **Desempleo juvenil alarmante**: El 17% de los jóvenes están desempleados, poniendo en riesgo el futuro productivo del país.
    Fuentes: INE Chile, OIT
    """,
    'Índice de Productividad': """
    El estancamiento de la productividad revela desafíos estructurales en la economía chilena:
    - **Brecha tecnológica**: La inversión en I+D es apenas el 0.36% del PIB, muy por debajo del promedio de la OCDE (2.4%), limitando la innovación y la competitividad.
    - **Concentración económica**: Los sectores de alta productividad (como minería) emplean a una fracción pequeña de la fuerza laboral, mientras que sectores de baja productividad concentran el empleo.
    - **Educación y habilidades**: Existe un desajuste entre las habilidades demandadas por el mercado laboral y las proporcionadas por el sistema educativo.
    - **Infraestructura y logística**: Deficiencias en infraestructura y altos costos logísticos limitan el crecimiento de la productividad en diversos sectores.
    Fuentes: OCDE, Comisión Nacional de Productividad, Banco Central de Chile
    """
}

def create_layout(app):
    return html.Div([
        html.Div([
            crear_resumen_ejecutivo("""
            La economía chilena, a menudo vista como un modelo exitoso, presenta una realidad compleja y contradictoria. 
            Aunque el PIB ha crecido un 0.2% post-pandemia, persisten profundas desigualdades y una peligrosa dependencia
            de la exportación de materias primas. La inflación, controlada al 7.6%, afecta más a los sectores de menores
            ingresos. El desempleo oficial del 8.5% no refleja la creciente precariedad laboral y la informalidad. La deuda
            pública del 38.1% del PIB, aunque moderada, plantea dudas sobre la sostenibilidad del modelo económico,
            especialmente ante desafíos como el cambio climático y la transición energética.
            """),
            
            crear_seccion_contenido("Indicadores Económicos Clave", [
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                id={'type': 'indicator-dropdown', 'page': 'macroeconomia'},
                                options=[
                                    {'label': 'Crecimiento del PIB (%)', 'value': 'Crecimiento del PIB (%)'},
                                    {'label': 'Desigualdad (Gini)', 'value': 'Desigualdad (Gini)'},
                                    {'label': 'Inflación (%)', 'value': 'Inflación (%)'},
                                    {'label': 'Desempleo (%)', 'value': 'Desempleo (%)'},
                                    {'label': 'Índice de Productividad', 'value': 'Índice de Productividad'}
                                ],
                                value='Crecimiento del PIB (%)',
                                clearable=False
                            ),
                        ], style={'width': '100%', 'marginBottom': '20px'}),
                        dcc.Graph(
                            id={'type': 'indicator-graph', 'page': 'macroeconomia'},
                            style={'height': '400px', 'width': '100%'}
                        ),
                    ], className="column-left", style={'width': '50%'}),
                    html.Div([
                        html.Div(id={'type': 'indicator-analysis', 'page': 'macroeconomia'}, className="analysis-text")
                    ], className="column-right", style={'width': '50%'}),
                ], className="two-column-layout", style={'display': 'flex', 'justifyContent': 'space-between'}),
            ]),

            html.Div([
                html.H3("Repensar el modelo económico chileno", className="section-title"),
                dcc.Markdown("""
                Más allá de los indicadores macroeconómicos aparentemente positivos, Chile enfrenta desafíos estructurales profundos que amenazan su estabilidad y desarrollo a largo plazo. Es imperativo repensar el modelo económico, priorizando:

                1. Diversificación económica y reducción de la dependencia de materias primas.
                2. Políticas redistributivas efectivas para abordar la desigualdad crónica.
                3. Inversión en innovación y capital humano para aumentar la productividad.
                4. Reforma del sistema laboral para abordar la precariedad y el subempleo.
                5. Planificación fiscal a largo plazo que considere los desafíos ambientales y sociales futuros.

                Solo abordando estos desafíos de manera frontal y honesta, Chile podrá construir una economía verdaderamente resiliente y equitativa para el futuro.

                Fuentes principales: Banco Central de Chile, Instituto Nacional de Estadísticas (INE), Ministerio de Hacienda, Banco Mundial, FMI, CEPAL, OIT
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
    [Output({'type': 'indicator-graph', 'page': 'macroeconomia'}, 'figure'),
     Output({'type': 'indicator-analysis', 'page': 'macroeconomia'}, 'children')],
    [Input({'type': 'indicator-dropdown', 'page': 'macroeconomia'}, 'value')]
)
def update_macroeconomia_content(selected_indicator):
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