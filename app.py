# 1. Importaciones
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from pages import resumen, macroeconomia, sectorial, comercio, sociedad, politicas
from utils import crear_barra_lateral

# 2. Inicialización de la app
app = Dash(__name__, 
           assets_folder='assets',
           meta_tags=[{"name": "viewport", "content": "width=device-width"}],
           suppress_callback_exceptions=True,
           requests_pathname_prefix='/')


# 3. Definición del layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            crear_barra_lateral(app)
        ], className="sidebar"),
        html.Div([
            html.H2(id="subtitle", className="main-subtitle"),
            html.Div(id='page-content')
        ], className="main-content")
    ], className="app-container")
])

# 4. Callbacks del servidor
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/informe-economico-chile/macroeconomia":
        return macroeconomia.create_layout(app)
    elif pathname == "/informe-economico-chile/sectorial":
        return sectorial.create_layout(app)
    elif pathname == "/informe-economico-chile/comercio":
        return comercio.create_layout(app)
    elif pathname == "/informe-economico-chile/sociedad":
        return sociedad.create_layout(app)
    elif pathname == "/informe-economico-chile/politicas":
        return politicas.create_layout(app)
    elif pathname == "/" or pathname == "/informe-economico-chile/resumen":
        return resumen.create_layout(app)
    else:
        return html.Div("404 - Página no encontrada")

@app.callback(Output('subtitle', 'children'),
              [Input('url', 'pathname')])
def update_subtitle(pathname):
    subtitles = {
        "/informe-economico-chile/resumen": "Chile en Cifras: Un Panorama Económico y Social",
        "/informe-economico-chile/macroeconomia": "Macroeconomía: Entre el Crecimiento y la Estabilidad",
        "/informe-economico-chile/sectorial": "Estructura Ecónomica: Fortalezas y Vulnerabilidades de la Economía Chilena",
        "/informe-economico-chile/comercio": "Comercio Internacional: Oportunidades y Riesgos del Comercio Exterior",
        "/informe-economico-chile/sociedad": "Métricas Sociales: Indicadores de Bienestar y Desigualdad",
        "/informe-economico-chile/politicas": "Políticas Públicas: El Camino hacia un Chile más Próspero y Equitativo",
        "/": "Chile en Cifras: Un Panorama Económico y Social"
    }
    return subtitles.get(pathname, "Chile en Cifras: Un Panorama Económico y Social")

# 5. Inicialización de callbacks de páginas
for page in [macroeconomia, sectorial, comercio, sociedad, politicas]:
    if hasattr(page, 'init_callbacks'):
        page.init_callbacks(app)

if __name__ == "__main__":
    from waitress import serve
    serve(app.server, host="0.0.0.0", port=8080)
