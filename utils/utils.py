# 1. Importaciones
from dash import html, dcc
import pandas as pd

# 2. Componentes principales de la interfaz

def crear_barra_lateral(app):
    return html.Div([
        html.Div([
            html.A(html.Img(src=app.get_asset_url("icons/github.png"), className="social-icon"), href="https://github.com/mortizcoilla", target="_blank"),
            html.A(html.Img(src=app.get_asset_url("icons/linkedin.png"), className="social-icon"), href="https://www.linkedin.com/in/mortizcoilla", target="_blank"),
            html.A(html.Img(src=app.get_asset_url("icons/microsoft.png"), className="social-icon"), href="https://learn.microsoft.com/es-mx/users/mortizcoilla", target="_blank"),
            html.A(html.Img(src=app.get_asset_url("icons/coursera.png"), className="social-icon"), href="https://www.coursera.org/learner/mortizcoilla", target="_blank"),
        ], className="social-links"),
        html.Nav([
            dcc.Link("Resumen", href="/informe-economico-chile/resumen", className="nav-link"),
            dcc.Link("Macroeconomía", href="/informe-economico-chile/macroeconomia", className="nav-link"),
            dcc.Link("Estructura Económica", href="/informe-economico-chile/sectorial", className="nav-link"),
            dcc.Link("Comercio Internacional", href="/informe-economico-chile/comercio", className="nav-link"),
            dcc.Link("Métricas Sociales", href="/informe-economico-chile/sociedad", className="nav-link"),
            dcc.Link("Políticas Públicas", href="/informe-economico-chile/politicas", className="nav-link"),
        ], className="sidebar-nav"),
    ], className="sidebar")

# 3. Funciones auxiliares para la creación de contenido

def crear_tabla_dash(df):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(len(df))
        ])
    ], className="data-table")

def crear_seccion_contenido(titulo, contenido, clase_adicional=""):
    return html.Div([
        html.H2(titulo, className="section-title"),
        html.Div(contenido, className="section-content")
    ], className=f"content-section {clase_adicional}".strip())

def crear_resumen_ejecutivo(texto, contenido_adicional=None):
    contenido = [
        html.P(texto, className="executive-summary-text")
    ]
    if contenido_adicional:
        contenido.extend(contenido_adicional)
    return html.Div(contenido, className="executive-summary-box")

def crear_contenedor_grafico(titulo, grafico, analisis):
    return html.Div([
        html.H3(titulo, className="graph-title"),
        html.P(analisis, className="analysis-text"),
        dcc.Graph(figure=grafico)
    ], className="graph-container")