# 1. Importaciones
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from utils import crear_resumen_ejecutivo, crear_seccion_contenido
from sklearn.preprocessing import MinMaxScaler

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
gini_index = [0.51, 0.505, 0.505, 0.495, 0.495, 0.485, 0.48, 0.475, 0.47, 0.465, 0.46, 0.455, 0.45, 0.445]
poverty_rate = [25.3, 22.8, 20.8, 18.7, 17.2, 15.1, 13.7, 12.7, 11.4, 10.8, 10.8, 11.7, 12.5, 11.9]
education_years = [9.7, 9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 11.0]
health_expenditure = [6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1]
crime_rate = [2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3700, 3900, 4100]
victimization_rate = [28.2, 28.8, 29.4, 30.0, 30.6, 31.2, 31.8, 32.4, 33.0, 33.6, 34.2, 33.8, 35.0, 36.2]
migration_rate = [1.3, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1]

df_social = pd.DataFrame({
    'Año': years,
    'Índice de Gini': gini_index,
    'Tasa de Pobreza (%)': poverty_rate,
    'Años de Educación': education_years,
    'Gasto en Salud (% PIB)': health_expenditure,
    'Tasa de Criminalidad (por 100,000 hab.)': crime_rate,
    'Tasa de Victimización (%)': victimization_rate,
    'Tasa de Migración (%)': migration_rate
})

# Nuevos datos simulados para el análisis enriquecido
regiones = ['Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama', 'Coquimbo', 'Valparaíso', 
            'Metropolitana', "O'Higgins", 'Maule', 'Ñuble', 'Biobío', 'Araucanía', 'Los Ríos', 
            'Los Lagos', 'Aysén', 'Magallanes']

np.random.seed(42)

data = {
    'Region': regiones,
    'Indice_Pobreza': np.random.uniform(5, 25, 16),
    'Desempleo': np.random.uniform(5, 15, 16),
    'Deficit_Habitacional': np.random.uniform(10, 30, 16),
    'Acceso_Agua_Potable': np.random.uniform(85, 100, 16),
    'Acceso_Electricidad': np.random.uniform(95, 100, 16),
    'Indice_Vulnerabilidad': np.random.uniform(20, 50, 16),
    'Cobertura_Salud': np.random.uniform(70, 95, 16),
    'Años_Escolaridad': np.random.uniform(9, 12, 16),
    'Ingreso_Medio': np.random.uniform(300000, 800000, 16)
}

df_enriquecido = pd.DataFrame(data)

# Normalización de datos para el gráfico de radar
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df_enriquecido.select_dtypes(include=[np.number])), 
                             columns=df_enriquecido.select_dtypes(include=[np.number]).columns)
df_normalized['Region'] = df_enriquecido['Region']

# 4. Funciones auxiliares
def create_social_indicator_figure(indicator):
    trace = go.Scatter(
        x=df_social['Año'],
        y=df_social[indicator],
        mode='lines+markers',
        name=indicator,
        line=dict(color=colors['primary'], width=2),
        marker=dict(size=8, color=colors['secondary'])
    )
    
    layout = go.Layout(
        title=f'Evolución de {indicator} en Chile',
        xaxis=dict(title='Año'),
        yaxis=dict(title=indicator),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Roboto", size=12, color=colors['text'])
    )
    
    return {'data': [trace], 'layout': layout}

def create_radar_chart(df):
    fig = go.Figure()

    for i, region in enumerate(df['Region']):
        visibility = 'legendonly'
        if region == 'Metropolitana':
            visibility = True

        fig.add_trace(go.Scatterpolar(
            r=df.iloc[i, :-1].values.tolist() + [df.iloc[i, 0]],
            theta=df.columns[:-1].tolist() + [df.columns[0]],
            fill='toself',
            name=region,
            visible=visibility
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Comparación Multidimensional de Indicadores Sociales por Región"
    )
    return fig

def create_correlation_heatmap(df):
    correlation_matrix = df.select_dtypes(include=[np.number]).corr()
    return px.imshow(correlation_matrix, 
                     labels=dict(color="Correlación"),
                     x=correlation_matrix.columns,
                     y=correlation_matrix.columns,
                     color_continuous_scale=["#E5E5E5", "#1C3D5A"],  # Escala de grises a azul oscuro
                     title="Matriz de Correlación entre Indicadores Sociales")

# 5. Definición del layout
def create_layout(app):
    return html.Div([
        html.Div([
            html.H2("Métricas Sociales", className="section-title"),
            crear_resumen_ejecutivo("""
            El análisis de los indicadores sociales de Chile revela una sociedad compleja, 
            con desigualdades persistentes y nuevos desafíos emergentes. Este estudio profundiza en 
            aspectos como vivienda, empleo, acceso a servicios básicos, vulnerabilidad y protección social,
            ofreciendo una visión holística de la realidad social chilena.
            """),
            
            crear_seccion_contenido("Indicadores Sociales Clave", [
                html.P("Seleccione un indicador del menú desplegable para visualizar su evolución y leer un análisis detallado.", className="instructions-text"),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                id={'type': 'social-indicator-dropdown', 'page': 'sociedad'},
                                options=[
                                    {'label': i, 'value': i} for i in df_social.columns if i != 'Año'
                                ],
                                value='Índice de Gini',
                                clearable=False
                            ),
                        ], style={'width': '100%', 'marginBottom': '20px'}),
                        dcc.Graph(
                            id={'type': 'social-indicator-graph', 'page': 'sociedad'},
                            style={'height': '400px', 'width': '100%'}
                        ),
                    ], className="column-left", style={'width': '50%'}),
                    html.Div([
                        html.Div(id={'type': 'social-indicator-analysis', 'page': 'sociedad'}, className="analysis-text")
                    ], className="column-right", style={'width': '50%'}),
                ], className="two-column-layout", style={'display': 'flex', 'justifyContent': 'space-between'}),
            ]),

            crear_seccion_contenido("Análisis Regional de Indicadores Sociales", [
                html.P("Seleccione una o varias regiones en la leyenda para ver los indicadores en detalle", className="instructions-text"),
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id={'type': 'radar-chart', 'page': 'sociedad'},
                            figure=create_radar_chart(df_normalized),
                            style={'height': '400px', 'width': '100%'}
                        )
                    ], className="column-left", style={'width': '50%'}),
                    html.Div([
                        html.H4("Interpretación del Gráfico de Radar", className="subsection-title"),
                        dcc.Markdown("""
                        Este gráfico de radar muestra la comparación multidimensional de indicadores sociales 
                        entre las diferentes regiones de Chile. Cada eje representa un indicador social 
                        normalizado, permitiendo una comparación directa entre regiones. Las áreas más grandes 
                        indican un mejor desempeño general en los indicadores sociales.
                        """, className="analysis-text")
                    ], className="column-right", style={'width': '50%'}),
                ], className="two-column-layout", style={'display': 'flex', 'justifyContent': 'space-between'}),
            ]),

            crear_seccion_contenido("Correlaciones entre Indicadores Sociales", [
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id={'type': 'correlation-heatmap', 'page': 'sociedad'},
                            figure=create_correlation_heatmap(df_enriquecido),
                            style={'height': '400px', 'width': '100%'}
                        )
                    ], className="column-left", style={'width': '50%'}),
                    html.Div([
                        html.H4("Análisis de Correlaciones", className="subsection-title"),
                        dcc.Markdown("""
                        La matriz de correlación revela relaciones importantes entre los diferentes indicadores sociales:
                        
                        - Existe una fuerte correlación negativa entre el Índice de Pobreza y el Acceso a Servicios Básicos,
                          lo que subraya cómo la pobreza se manifiesta en múltiples dimensiones.
                        - La correlación positiva entre Años de Escolaridad e Ingreso Medio refuerza la idea de que la 
                          educación sigue siendo un factor clave en la movilidad social, a pesar de sus deficiencias.
                        - El Déficit Habitacional muestra una correlación significativa con el Índice de Vulnerabilidad,
                          destacando cómo la falta de vivienda adecuada amplifica otras formas de precariedad social.
                        """, className="analysis-text")
                    ], className="column-right", style={'width': '50%'}),
                ], className="two-column-layout", style={'display': 'flex', 'justifyContent': 'space-between'}),
            ]),
        ], className="page-content"),
    ], className="main-container")

# 6. Callbacks
@callback(
    [Output({'type': 'social-indicator-graph', 'page': 'sociedad'}, 'figure'),
     Output({'type': 'social-indicator-analysis', 'page': 'sociedad'}, 'children')],
    [Input({'type': 'social-indicator-dropdown', 'page': 'sociedad'}, 'value')]
)
def update_social_content(selected_indicator):
    if not selected_indicator:
        raise PreventUpdate
    
    fig = create_social_indicator_figure(selected_indicator)
    analysis = interpretaciones[selected_indicator]
    return fig, dcc.Markdown(analysis)

# 7. Interpretaciones para cada indicador
interpretaciones = {
    'Índice de Gini': """
    La evolución del Índice de Gini en Chile refleja la persistencia de la desigualdad económica. 
    A pesar de algunas mejoras, la concentración de la riqueza sigue siendo un desafío fundamental. 
    Esta desigualdad limita la movilidad social y el acceso a oportunidades, afectando el desarrollo 
    sostenible del país.
    """,
    'Tasa de Pobreza (%)': """
    La tasa de pobreza en Chile ha mostrado una tendencia a la baja, pero sigue siendo un problema 
    significativo. Los avances logrados son frágiles y susceptibles a retrocesos ante crisis económicas. 
    Es necesario fortalecer las políticas de protección social y fomento del empleo de calidad.
    """,
    'Años de Educación': """
    El aumento en los años promedio de educación es un avance positivo, pero insuficiente. La calidad 
    de la educación y su desigual distribución siguen siendo problemas críticos. Se requiere una reforma 
    educativa integral que asegure no solo más años de estudio, sino una educación de calidad para todos.
    """,
    'Gasto en Salud (% PIB)': """
    El incremento en el gasto en salud como porcentaje del PIB es una tendencia positiva, pero aún 
    insuficiente. Persisten desigualdades en el acceso y la calidad de los servicios de salud. Es necesario 
    un sistema de salud más equitativo y eficiente que garantice cobertura universal de calidad.
    """,
    'Tasa de Criminalidad (por 100,000 hab.)': """
    El aumento en la tasa de criminalidad es preocupante y refleja problemas sociales más profundos. 
    Se requieren políticas integrales que aborden no solo la seguridad, sino también las causas 
    subyacentes del crimen, como la desigualdad, el desempleo y la falta de oportunidades.
    """,
    'Tasa de Victimización (%)': """
    La tasa de victimización creciente indica una percepción de inseguridad en aumento. Esto afecta 
    la calidad de vida y la cohesión social. Es crucial implementar estrategias de prevención del delito 
    y fortalecer la confianza en las instituciones de seguridad y justicia.
    """,
    'Tasa de Migración (%)': """
    El aumento en la tasa de migración presenta tanto desafíos como oportunidades. Se requieren políticas 
    migratorias integrales que faciliten la integración de los migrantes y aprovechen su potencial 
    contribución al desarrollo del país, mientras se abordan los desafíos asociados a la migración.
    """
}

# 8. Inicialización de callbacks (si es necesario)
def init_callbacks(app):
    pass