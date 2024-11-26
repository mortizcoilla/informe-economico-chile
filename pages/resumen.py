# 1. Importaciones
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import pandas as pd
from utils import crear_resumen_ejecutivo, crear_seccion_contenido

# 2. Definición de variables globales
df_summary = pd.DataFrame({
    'Año': range(2010, 2024),
    'Índice de Libertad Económica': [78, 77, 76, 75, 73, 72, 70, 68, 66, 64, 62, 60, 58, 56],
    'Crecimiento del PIB (%)': [5.8, 6.1, 5.3, 4.0, 1.8, 2.3, 1.7, 1.2, 3.9, 1.1, -5.8, 11.7, 2.4, 0.2],
    'Poder Adquisitivo (Índice)': [100, 102, 104, 105, 106, 107, 108, 109, 110, 111, 105, 102, 95, 90],
    'Tasa de Criminalidad (por 100,000 hab.)': [2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3700, 3900, 4100],
    'Satisfacción con el Sistema de Salud (%)': [70, 68, 66, 64, 62, 60, 58, 56, 54, 52, 50, 48, 46, 44],
    'Calidad de la Educación (Índice)': [75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62]
})

colors = {
    'primary': '#1C3D5A',
    'secondary': '#3E7CB1',
    'text_primary': '#4A4A4A',
    'background': '#FFFFFF',
}

# 3. Funciones auxiliares
def create_summary_figure(selected_indicator):
    trace = go.Scatter(
        x=df_summary['Año'],
        y=df_summary[selected_indicator],
        mode='lines+markers',
        name=selected_indicator,
        line=dict(color=colors['primary'], width=2),
        marker=dict(size=8, color=colors['secondary'])
    )
    
    layout = go.Layout(
        title=f'Evolución de {selected_indicator} en Chile',
        xaxis=dict(title='Año'),
        yaxis=dict(title=selected_indicator),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Roboto", size=12, color=colors['text_primary'])
    )
    
    return {'data': [trace], 'layout': layout}

interpretaciones = {
    'Índice de Libertad Económica': """
    La caída constante del Índice de Libertad Económica refleja un preocupante aumento de la intervención estatal y regulaciones excesivas. 
    Esta tendencia sofoca la iniciativa privada, reduce la competitividad y frena el crecimiento económico. 
    Es crucial revertir esta tendencia mediante desregulación, reducción de impuestos y protección de derechos de propiedad para estimular la inversión y el emprendimiento.
    """,
    'Crecimiento del PIB (%)': """
    La volatilidad y el bajo crecimiento del PIB evidencian la fragilidad del modelo económico chileno. 
    La dependencia excesiva de materias primas y la falta de diversificación económica limitan el potencial de crecimiento. 
    Se necesitan reformas que fomenten la innovación, reduzcan la burocracia y abran nuevos sectores a la competencia para impulsar un crecimiento sostenido y resiliente.
    """,
    'Poder Adquisitivo (Índice)': """
    La reciente caída del poder adquisitivo es alarmante y refleja políticas económicas fallidas. 
    El aumento de la inflación y la rigidez del mercado laboral erosionan el bienestar de los ciudadanos. 
    Es imperativo implementar políticas que fomenten la flexibilidad laboral, reduzcan la carga impositiva y controlen el gasto público para recuperar el poder adquisitivo.
    """,
    'Tasa de Criminalidad (por 100,000 hab.)': """
    El aumento constante de la criminalidad evidencia el fracaso de las políticas de seguridad estatales. 
    La falta de respeto por la propiedad privada y la ineficacia del sistema judicial socavan la libertad y el desarrollo económico. 
    Se requieren reformas que fortalezcan el estado de derecho, mejoren la eficiencia policial y promuevan la responsabilidad individual para revertir esta tendencia.
    """,
    'Satisfacción con el Sistema de Salud (%)': """
    La caída en la satisfacción con el sistema de salud refleja las deficiencias del modelo centralizado y burocrático. 
    La falta de competencia y opciones limita la calidad y accesibilidad de los servicios. 
    Es necesario introducir mayor competencia en el sector, fomentar la medicina privada y ofrecer opciones de seguro más flexibles para mejorar la calidad y eficiencia.
    """,
    'Calidad de la Educación (Índice)': """
    El declive en la calidad educativa es consecuencia de un sistema rígido y centralizado. 
    La falta de opciones y competencia en educación limita la innovación y adaptabilidad. 
    Se requiere una reforma que fomente la diversidad educativa, introduzca vouchers escolares y reduzca la intervención estatal para mejorar la calidad y relevancia de la educación.
    """
}

# 4. Definición del layout
def create_layout(app):
    return html.Div([
        html.Div([
            crear_resumen_ejecutivo("""
            El presente informe ofrece un análisis exhaustivo de la situación económica y social de Chile, abarcando aspectos cruciales como la macroeconomía,
            los sectores productivos, el comercio internacional, los indicadores sociales y las políticas públicas. El estudio revela un panorama crítico
            que demanda una acción urgente y reformas estructurales profundas. Se hace evidente la necesidad de implementar políticas que impulsen la libertad
            económica y estimulen el crecimiento del PIB, al tiempo que se mejore sustancialmente la calidad y accesibilidad de los sistemas de salud y educación.
            Asimismo, es imperativo reforzar las estrategias de seguridad pública para contrarrestar el aumento de la criminalidad y desarrollar medidas efectivas
            que incrementen el poder adquisitivo de los ciudadanos. Este análisis busca proporcionar una base sólida para la toma de decisiones informadas que
            conduzcan a un Chile más próspero, equitativo y seguro para todos sus habitantes.
            """
            ),
            
            crear_seccion_contenido("Indicadores Clave", [
                html.P("Seleccione un indicador del menú desplegable para visualizar su evolución y leer un análisis detallado.", className="instructions-text"),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                id='indicator-dropdown',
                                options=[{'label': i, 'value': i} for i in df_summary.columns if i != 'Año'],
                                value='Índice de Libertad Económica',
                                clearable=False
                            ),
                        ], style={'width': '100%', 'marginBottom': '20px'}),
                        dcc.Graph(
                            id='summary-graph',
                            style={'height': '400px', 'width': '100%'}
                        ),
                    ], className="column-left", style={'width': '50%'}),
                    html.Div([
                        html.Div(id='interpretation', className="analysis-text")
                    ], className="column-right", style={'width': '50%'}),
                ], className="two-column-layout", style={'display': 'flex', 'justifyContent': 'space-between'}),
            ]),
        ], className="page-content"),
    ], className="main-container")

# 5. Callbacks
@callback(
    [Output('summary-graph', 'figure'),
     Output('interpretation', 'children')],
    [Input('indicator-dropdown', 'value')]
)
def update_graph(selected_indicator):
    if not selected_indicator:
        raise PreventUpdate
    return create_summary_figure(selected_indicator), interpretaciones[selected_indicator]

# 6. Inicialización de callbacks
def init_callbacks(app):
    pass