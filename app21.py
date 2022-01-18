from dash import Dash
from dash import dcc
from dash import html

import plotly.express as px
import pandas as pd
vendas = pd.read_csv('vendas.csv')

vendasg=vendas.groupby(['Mes_Vendas','Loja'])['Faturamento'].agg('sum').reset_index(name='Faturamento total')
line_graph = px.line(
data_frame = vendasg, 
title = 'Faturamento total por Mês/Loja',
x = 'Mes_Vendas',
y= 'Faturamento total', 
color = 'Loja')
vendas_f = vendas.groupby('Loja')['Faturamento'].agg('sum').reset_index(name='Faturamento total')
bar_graph = px.bar(
data_frame=vendas_f, 
x='Faturamento total',
y = 'Loja',
orientation = 'h',
title = 'Faturamento total por cidade',
color = 'Loja', color_discrete_map={'Sao Paulo':'#abb0ca','Salvador':'#e5cbb0','Rio de Janeiro':'#050507','Porto Alegre':'#e02844',
'Fortaleza':'#6d6e8c','Curitiba':'#554f64','Brasilia':'#8cac7f'})





external_stylesheets = [
    {
        "href":"https://fonts.googleapis.com/css2?"
        "family=Lato:wgt@400;700&display=swap",
        "rel":"stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Análise ação PETR4: preços ações Petrobrás"


app.layout = html.Div(
    children=[
        html.Div(
            children =[
            	html.H1(children = "Evolução de valores PETR4 (2018/2020)",
                className="header-title"),
                html.P(children = "Análise do comportamento do preço das ações PETR4 entre 2018 e 2020",
                className="header-description",),],
            	className="header",
        ),
        html.Div(
            children=[
                html.Div(children=dcc.Graph(
                            id="line_graph",                            
                            figure=line_graph),
                			className="card",), 
            		],
            className="wrapper",
        ),
        html.Div(dcc.Graph(id="bar_graph", figure=bar_graph),
        		style={'width':'750px','margin':'auto'}),
        html.Span(children=["Este ano as maiores vendas vieram de Brasília"])],
        style={"text-align":"center", "font-size":15})       





if __name__ == '__main__':
	app.run_server(debug=True)
	









