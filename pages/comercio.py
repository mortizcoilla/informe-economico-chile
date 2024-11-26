# 1. Importaciones
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import plotly.express as px
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
exports = [71.1, 81.4, 78.1, 76.8, 75.1, 62.0, 60.7, 69.2, 75.2, 69.9, 74.1, 94.7, 98.1, 86.4]
imports = [59.2, 74.7, 80.1, 79.2, 72.3, 62.4, 59.4, 65.1, 74.2, 69.6, 59.0, 84.1, 92.2, 83.1]
trade_balance = [11.9, 6.7, -2.0, -2.4, 2.8, -0.4, 1.3, 4.1, 1.0, 0.3, 15.1, 10.6, 5.9, 3.3]

copper_exports = [40.3, 44.4, 41.9, 40.0, 36.7, 30.3, 28.1, 32.9, 36.0, 33.1, 37.5, 53.4, 51.0, 43.2]
fruit_exports = [4.2, 4.7, 4.9, 5.3, 5.5, 5.2, 5.7, 5.9, 6.1, 6.3, 6.5, 6.8, 7.1, 7.4]
fuel_imports = [10.5, 12.3, 13.1, 12.8, 11.5, 8.9, 8.5, 10.2, 12.5, 11.8, 9.2, 11.5, 13.2, 12.8]
machinery_imports = [15.2, 18.5, 19.8, 19.5, 17.8, 15.6, 14.8, 16.2, 18.5, 17.4, 14.5, 18.2, 20.5, 19.8]

df_trade = pd.DataFrame({
    'Año': years,
    'Exportaciones': exports,
    'Importaciones': imports,
    'Balanza Comercial': trade_balance
})

df_exports = pd.DataFrame({
    'Año': years,
    'Cobre': copper_exports,
    'Frutas': fruit_exports
})

df_imports = pd.DataFrame({
    'Año': years,
    'Combustibles': fuel_imports,
    'Maquinaria': machinery_imports
})

# Configuración del layout para los gráficos
layout_config = dict(
    autosize=True,
    height=400,
    margin=dict(l=50, r=50, b=100, t=100, pad=4),
    paper_bgcolor="white",
    plot_bgcolor="white",
)

# Crear figuras para exportaciones e importaciones
fig_exports = px.area(df_exports, x='Año', y=['Cobre', 'Frutas'],
                      title='Composición de las Exportaciones Chilenas',
                      labels={'value': 'Miles de millones USD', 'variable': 'Producto'},
                      color_discrete_map={
                          'Cobre': colors['primary'],
                          'Frutas': colors['secondary']
                      })
fig_exports.update_layout(**layout_config)

fig_imports = px.area(df_imports, x='Año', y=['Combustibles', 'Maquinaria'],
                      title='Composición de las Importaciones Chilenas',
                      labels={'value': 'Miles de millones USD', 'variable': 'Producto'},
                      color_discrete_map={
                          'Combustibles': colors['primary'],
                          'Maquinaria': colors['secondary']
                      })
fig_imports.update_layout(**layout_config)

# 4. Diccionario con los análisis para cada aspecto del comercio
analisis_comercio = {
    'Balanza Comercial': """
    La balanza comercial positiva de Chile, que alcanzó $3.3 mil millones en 2023, esconde realidades preocupantes:

    - **Dependencia del cobre**: El 50% de las exportaciones siguen siendo cobre, exponiendo la economía a volatilidades extremas. Una caída del 10% en el precio del cobre puede reducir los ingresos fiscales en hasta un 2% del PIB.
    - **Importaciones de alto valor**: Mientras Chile exporta principalmente materias primas, importa bienes de alto valor agregado. El déficit en la balanza comercial de productos tecnológicos aumentó un 15% en la última década.
    - **Vulnerabilidad a shocks externos**: La pandemia de COVID-19 expuso la fragilidad del modelo comercial chileno, con una contracción del 5.8% en las exportaciones en 2020.
    - **Tratados de libre comercio cuestionables**: A pesar de tener acuerdos con economías que representan el 88% del PIB mundial, el valor agregado de las exportaciones chilenas ha disminuido en un 5% en los últimos 20 años.

    Fuentes: Banco Central de Chile, DIRECON, OMC
    """,
    'Exportaciones': """
    Las exportaciones chilenas, valoradas en $86.4 mil millones en 2023, reflejan un modelo económico estancado:

    - **Concentración peligrosa**: El cobre representa el 50% de las exportaciones, seguido por otros productos primarios. Los 10 principales productos de exportación constituyen el 70% del total.
    - **Bajo valor agregado**: Menos del 5% de las exportaciones son productos de alta tecnología, muy por debajo del promedio de la OCDE (15%).
    - **Desaprovechamiento de oportunidades**: A pesar del boom global en tecnologías verdes, Chile exporta litio principalmente como materia prima, perdiendo oportunidades en la cadena de valor de baterías.
    - **Dependencia de mercados**: China, Estados Unidos y Japón representan el 52% de las exportaciones, exponiendo a Chile a riesgos geopolíticos.

    Fuentes: Servicio Nacional de Aduanas, ProChile, CEPAL
    """,
    'Importaciones': """
    Las importaciones de Chile, que alcanzaron $83.1 mil millones en 2023, revelan debilidades estructurales:

    - **Desindustrialización creciente**: El 70% de las importaciones son bienes manufacturados, evidenciando la incapacidad de la industria local para satisfacer la demanda interna.
    - **Dependencia tecnológica**: Las importaciones de productos de alta tecnología aumentaron un 25% en la última década, profundizando la brecha tecnológica.
    - **Vulnerabilidad energética**: A pesar de su potencial en energías renovables, Chile importa el 70% de su energía, principalmente combustibles fósiles.
    - **Impacto en PyMEs**: La entrada masiva de productos importados ha llevado al cierre de 15,000 pequeñas y medianas empresas en el sector manufacturero en los últimos 5 años.

    Fuentes: Banco Central de Chile, Asociación de Importadores de Chile (AICH), Ministerio de Energía
    """
}

# 5. Definición del layout
def create_layout(app):
    return html.Div([
        html.Div([
            crear_resumen_ejecutivo("""
            El análisis del comercio internacional de Chile revela una economía atrapada en un modelo extractivista y dependiente, 
            con una diversificación limitada y una vulnerabilidad crónica a los shocks externos. A pesar de la amplia red de 
            tratados de libre comercio, Chile no ha logrado ascender en las cadenas de valor global, perpetuando su rol como 
            proveedor de materias primas en un mundo que premia cada vez más el conocimiento y la innovación.
            """),
            
            crear_seccion_contenido("Indicadores Clave del Comercio Internacional", [
                html.Div([
                    dcc.Dropdown(
                        id={'type': 'comercio-dropdown', 'page': 'comercio'},
                        options=[
                            {'label': 'Balanza Comercial', 'value': 'Balanza Comercial'},
                            {'label': 'Exportaciones', 'value': 'Exportaciones'},
                            {'label': 'Importaciones', 'value': 'Importaciones'}
                        ],
                        value='Balanza Comercial',
                        clearable=False
                    ),
                ], className="dropdown-container"),
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id={'type': 'comercio-graph', 'page': 'comercio'},
                            style={'height': '400px', 'width': '100%'}
                        ),
                    ], className="column-left", style={'width': '48%'}),
                    html.Div([
                        html.Div(id={'type': 'comercio-analysis', 'page': 'comercio'}, className="analysis-text")
                    ], className="column-right", style={'width': '48%'}),
                ], className="two-column-layout", style={'display': 'flex', 'justifyContent': 'space-between'}),
            ]),

            html.Div([
                html.H3("Composición del Comercio Internacional", className="section-title"),
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id={'type': 'exports-composition-graph', 'page': 'comercio'},
                            figure=fig_exports,
                            style={'height': '400px', 'width': '100%'}
                        )
                    ], className="column-left", style={'width': '48%'}),
                    html.Div([
                        dcc.Graph(
                            id={'type': 'imports-composition-graph', 'page': 'comercio'},
                            figure=fig_imports,
                            style={'height': '400px', 'width': '100%'}
                        )
                    ], className="column-right", style={'width': '48%'})
                ], className="two-column-layout", style={'display': 'flex', 'justifyContent': 'space-between'}),
            ]),

            html.Div([
                html.H3("Nuevo Paradigma Comercial", className="section-title"),
                dcc.Markdown("""
                El análisis del comercio internacional de Chile revela una economía atrapada en un modelo obsoleto y vulnerable:

                1. La dependencia excesiva de las exportaciones de materias primas, especialmente el cobre, expone a Chile a riesgos inaceptables en un mundo volátil.
                2. La falta de diversificación y valor agregado en las exportaciones limita el potencial de crecimiento y desarrollo económico.
                3. La creciente dependencia de importaciones de alto valor agregado profundiza la brecha tecnológica y debilita el tejido industrial nacional.
                4. Los tratados de libre comercio, aunque numerosos, no han logrado impulsar una transformación estructural de la economía chilena.

                Chile necesita urgentemente una nueva estrategia comercial que:
                - Priorice la diversificación de exportaciones hacia productos de mayor valor agregado y contenido tecnológico.
                - Implemente políticas industriales activas para desarrollar capacidades en sectores estratégicos, como energías renovables y tecnologías verdes.
                - Revise y renegocie los tratados comerciales existentes para asegurar beneficios mutuos y proteger sectores estratégicos.
                - Invierta masivamente en I+D y educación para cerrar la brecha tecnológica y ascender en las cadenas de valor globales.

                Sin una transformación radical de su modelo comercial, Chile corre el riesgo de perpetuar su condición de economía periférica, 
                vulnerable a los caprichos de los mercados globales de materias primas e incapaz de generar el valor y los empleos necesarios 
                para un desarrollo sostenible e inclusivo.

                Fuentes principales: Banco Central de Chile, DIRECON, OMC, CEPAL, ProChile
                """, className="conclusion-text", style={'color': colors['text']})
            ], className="conclusion-section")
        ], className="page-content"),
    ], className="main-container")

# 6. Funciones auxiliares
def create_comercio_figure(indicator):
    try:
        trace = go.Scatter(
            x=df_trade['Año'],
            y=df_trade[indicator],
            mode='lines+markers',
            name=indicator,
            line=dict(color=colors['primary'], width=2),
            marker=dict(size=8, color=colors['secondary'])
        )

        layout = go.Layout(
            title=f'{indicator} de Chile (2010-2023)',
            xaxis=dict(title='Año'),
            yaxis=dict(title='Miles de millones USD'),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font=dict(family="Roboto", size=12, color=colors['text'])
        )

        return {'data': [trace], 'layout': layout}
    except Exception as e:
        return go.Figure()  # Figura vacía en caso de error

# 7. Callbacks
@callback(
    [Output({'type': 'comercio-graph', 'page': 'comercio'}, 'figure'),
     Output({'type': 'comercio-analysis', 'page': 'comercio'}, 'children')],
    [Input({'type': 'comercio-dropdown', 'page': 'comercio'}, 'value')]
)
def update_comercio_content(selected_indicator):
    if not selected_indicator:
        raise PreventUpdate

    try:
        fig = create_comercio_figure(selected_indicator)
        analysis = dcc.Markdown(analisis_comercio[selected_indicator])
        return fig, analysis
    except Exception as e:
        return go.Figure(), f"Error: {str(e)}"

# 8. Inicialización de callbacks (si es necesario)
def init_callbacks(app):
    pass