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
mining_contribution = [13.5, 14.2, 13.8, 12.5, 11.7, 10.9, 9.8, 10.2, 10.5, 10.8, 11.2, 12.5, 13.1, 12.8]
agriculture_contribution = [3.2, 3.1, 3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.4, 2.5, 2.6, 2.7]
manufacturing_contribution = [11.5, 11.2, 10.9, 10.6, 10.3, 10.0, 9.7, 9.4, 9.1, 8.8, 8.5, 8.9, 9.3, 9.5]
services_contribution = [59.8, 60.3, 60.8, 61.3, 61.8, 62.3, 62.8, 63.3, 63.8, 64.3, 63.5, 62.8, 62.1, 61.4]
construction_contribution = [6.5, 6.7, 6.9, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 7.9, 7.5, 7.1, 6.8]

df = pd.DataFrame({
    'Año': years,
    'Minería (% PIB)': mining_contribution,
    'Agricultura (% PIB)': agriculture_contribution,
    'Manufactura (% PIB)': manufacturing_contribution,
    'Servicios (% PIB)': services_contribution,
    'Construcción (% PIB)': construction_contribution
})

# 4. Diccionario con los análisis para cada sector
analisis_sectores = {
    'Minería (% PIB)': """
    La minería sigue siendo un pilar fundamental de la economía chilena, pero su contribución al PIB fluctúa:
    - **Dependencia del cobre**: El sector minero, dominado por el cobre, representa alrededor del 12.8% del PIB en 2023.
    - **Volatilidad de precios**: La contribución del sector ha oscilado entre 9.8% y 14.2% en la última década, reflejando la volatilidad de los precios de las materias primas.
    - **Desafíos ambientales**: La industria enfrenta crecientes presiones para adoptar prácticas más sostenibles y reducir su huella ambiental.
    - **Innovación necesaria**: Se requiere inversión en tecnología para mantener la competitividad y abordar la disminución de las leyes minerales.
    Fuentes: Consejo Minero, COCHILCO, Banco Central de Chile
    """,
    'Agricultura (% PIB)': """
    El sector agrícola, aunque relativamente pequeño, juega un papel crucial en la economía chilena:
    - **Contribución estable**: La agricultura representa consistentemente alrededor del 2.7% del PIB.
    - **Exportaciones clave**: Chile es un importante exportador de frutas, vinos y productos forestales.
    - **Desafíos climáticos**: El sector enfrenta riesgos crecientes debido al cambio climático y la escasez de agua.
    - **Oportunidades en agricultura de precisión**: La adopción de tecnologías avanzadas podría impulsar la productividad y sostenibilidad del sector.
    Fuentes: ODEPA, Ministerio de Agricultura, FAO
    """,
    'Manufactura (% PIB)': """
    El sector manufacturero de Chile muestra signos de recuperación tras años de declive:
    - **Tendencia a la baja revertida**: Después de caer del 11.5% al 8.5% del PIB, el sector ha mostrado una leve recuperación, alcanzando el 9.5% en 2023.
    - **Desafíos de competitividad**: La industria enfrenta competencia de importaciones de bajo costo y altos costos energéticos.
    - **Oportunidades en valor agregado**: Existe potencial para desarrollar industrias de mayor valor agregado, especialmente en sectores como la tecnología y la biotecnología.
    - **Necesidad de inversión**: Se requiere mayor inversión en I+D y capacitación para impulsar la productividad y la innovación.
    Fuentes: SOFOFA, INE, Ministerio de Economía
    """,
    'Servicios (% PIB)': """
    El sector de servicios domina la economía chilena, pero enfrenta desafíos de productividad:
    - **Sector dominante**: Los servicios representan el 61.4% del PIB en 2023, reflejando la transición de Chile hacia una economía basada en servicios.
    - **Diversidad de subsectores**: Incluye comercio, finanzas, turismo, tecnología de la información y servicios profesionales.
    - **Desafíos de productividad**: Muchos subsectores de servicios muestran baja productividad en comparación con países de la OCDE.
    - **Oportunidades digitales**: La transformación digital ofrece oportunidades para mejorar la eficiencia y expandir los servicios, especialmente en fintech y e-commerce.
    Fuentes: Cámara de Comercio de Santiago, Banco Central de Chile, OCDE
    """,
    'Construcción (% PIB)': """
    El sector de la construcción ha experimentado un crecimiento seguido de una reciente contracción:
    - **Crecimiento y contracción**: La contribución del sector aumentó del 6.5% al 8.3% del PIB, pero ha disminuido al 6.8% en 2023.
    - **Impulsor económico**: La construcción es un importante generador de empleo y tiene efectos multiplicadores en la economía.
    - **Desafíos recientes**: La pandemia y la incertidumbre económica han afectado negativamente al sector.
    - **Oportunidades en infraestructura**: Proyectos de infraestructura pública y la necesidad de viviendas asequibles ofrecen potencial de crecimiento.
    Fuentes: Cámara Chilena de la Construcción, Ministerio de Vivienda y Urbanismo, Banco Central de Chile
    """
}

# 5. Definición del layout
def create_layout(app):
    return html.Div([
        html.Div([
            crear_resumen_ejecutivo("""
            El análisis sectorial de la economía chilena revela una estructura productiva diversa pero con desafíos significativos. 
            Mientras algunos sectores muestran un crecimiento robusto, otros enfrentan obstáculos para su desarrollo y competitividad.
            Este análisis examina los principales sectores económicos, evaluando su desempeño, contribución al PIB y perspectivas futuras.
            """),
            
            crear_seccion_contenido("Contribución Sectorial al PIB", [
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                id={'type': 'sector-dropdown', 'page': 'sectorial'},
                                options=[
                                    {'label': 'Minería', 'value': 'Minería (% PIB)'},
                                    {'label': 'Agricultura', 'value': 'Agricultura (% PIB)'},
                                    {'label': 'Manufactura', 'value': 'Manufactura (% PIB)'},
                                    {'label': 'Servicios', 'value': 'Servicios (% PIB)'},
                                    {'label': 'Construcción', 'value': 'Construcción (% PIB)'}
                                ],
                                value='Minería (% PIB)',
                                clearable=False
                            ),
                        ], style={'width': '100%', 'marginBottom': '20px'}),
                        dcc.Graph(
                            id={'type': 'sector-graph', 'page': 'sectorial'},
                            style={'height': '400px', 'width': '100%'}
                        ),
                    ], className="column-left", style={'width': '50%'}),
                    html.Div([
                        html.Div(id={'type': 'sector-analysis', 'page': 'sectorial'}, className="analysis-text")
                    ], className="column-right", style={'width': '50%'}),
                ], className="two-column-layout", style={'display': 'flex', 'justifyContent': 'space-between'}),
            ]),

            html.Div([
                html.H3("Hacia una Economía más Diversificada y Resiliente", className="section-title"),
                dcc.Markdown("""
                El análisis sectorial de la economía chilena revela tanto fortalezas como vulnerabilidades:

                1. La dependencia continua del sector minero expone la economía a volatilidades globales.
                2. El sector de servicios domina la economía, pero enfrenta desafíos de productividad.
                3. La manufactura muestra signos de recuperación, pero requiere mayor inversión en innovación.
                4. La agricultura, aunque pequeña, es crucial para las exportaciones y enfrenta desafíos climáticos.
                5. La construcción, un importante generador de empleo, ha experimentado una contracción reciente.

                Para construir una economía más resiliente y sostenible, Chile debe:

                - Diversificar su base económica, reduciendo la dependencia de la minería.
                - Invertir en sectores de alto valor agregado, especialmente en manufactura avanzada y servicios tecnológicos.
                - Mejorar la productividad en el sector de servicios a través de la digitalización y la innovación.
                - Adaptar el sector agrícola al cambio climático y promover prácticas sostenibles.
                - Fomentar la innovación y la adopción de tecnologías en todos los sectores.
                - Desarrollar el capital humano para satisfacer las demandas de una economía más diversificada y tecnológica.

                Solo a través de una transformación estructural equilibrada, Chile podrá construir una economía más robusta, 
                equitativa y preparada para los desafíos del siglo XXI.

                Fuentes principales: Banco Central de Chile, Ministerio de Economía, CEPAL, OCDE
                """, className="conclusion-text", style={'color': colors['text']})
            ], className="conclusion-section")
        ], className="page-content"),
    ], className="main-container")

# 6. Funciones auxiliares
def create_sector_figure(sector):
    try:
        trace = go.Scatter(
            x=df['Año'],
            y=df[sector],
            mode='lines+markers',
            name=sector,
            line=dict(color=colors['primary'], width=2),
            marker=dict(size=8, color=colors['secondary'])
        )

        layout = go.Layout(
            title=f'Contribución de {sector} al PIB de Chile (2010-2023)',
            xaxis=dict(
                title='Año',
                tickmode='array',
                tickvals=df['Año'][::2],  # Selecciona cada segundo año
                ticktext=df['Año'][::2].astype(str),
                tickangle=0
            ),
            yaxis=dict(title='Porcentaje del PIB'),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font=dict(family="Roboto", size=12, color=colors['text'])
        )

        return {'data': [trace], 'layout': layout}
    except Exception as e:
        return go.Figure()  # Figura vacía en caso de error

# 7. Callbacks
@callback(
    [Output({'type': 'sector-graph', 'page': 'sectorial'}, 'figure'),
     Output({'type': 'sector-analysis', 'page': 'sectorial'}, 'children')],
    [Input({'type': 'sector-dropdown', 'page': 'sectorial'}, 'value')]
)
def update_sector_content(selected_sector):
    if not selected_sector:
        raise PreventUpdate

    try:
        fig = create_sector_figure(selected_sector)
        analysis = dcc.Markdown(analisis_sectores[selected_sector])
        return fig, analysis
    except Exception as e:
        return go.Figure(), f"Error: {str(e)}"

# 8. Inicialización de callbacks (si es necesario)
def init_callbacks(app):
    pass