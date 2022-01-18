import dash
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from datetime import date
import calendar
from dash_extensions import Lottie

vendas = pd.read_csv('vendas.csv')


vendasg=vendas.groupby(['Mes_Vendas_Num','Loja'])['Faturamento'].agg('sum').reset_index(name='Faturamento total')
line_graph = px.line(
data_frame = vendasg, 
title = 'Faturamento total por Mês/Loja',
x = 'Mes_Vendas_Num',
y= 'Faturamento total', 
color = 'Loja',
labels = dict(Mes_Vendas="Mês", Loja = "Cidade"))
line_graph.update_xaxes(
    ticktext=["Janeiro","Fevereiro","Marco" ,"Abril","Maio" ,"Junho","Julho", "Agosto","Setembro","Outubro","Novembro","Dezembro"],
    tickvals=[1,2,3, 4,5,6,7, 8,9,10,11,12],)

Faturamentot=vendas['Faturamento'].sum()


external_stylesheets = [
    {
        "href":"https://fonts.googleapis.com/css2?"
        "family=Montserrat:wght@500&display=swap", "rel":"stylesheet",
        
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "[Python] Dashboard Vendas"

app.css.config.serve_locally = True

app.layout = html.Div(
    children=[        
        html.Div(
            children =[
            	html.H1(
                    children = "Report Vendas", className="header-title"
                ),
                html.H4(
                    children ="Análise do comportamento de vendas e faturamento",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Cidade", className="menu-title"),
                        dcc.Dropdown(
                            id='country-dd',
                            options=[{'label':'Sao Paulo','value':'Sao Paulo'},
                                    {'label':'Salvador','value':'Salvador'},
                                    {'label':'Rio de Janeiro', 'value':'Rio de Janeiro'},
                                    {'label':'Porto Alegre', 'value':'Porto Alegre'},
                                    {'label':'Brasilia','value':'Brasilia'},
                                    {'label':'Fortaleza','value':'Fortaleza'},
                                    {'label':'Curitiba','value':'Curitiba'}],                    
                            placeholder="Escolha uma cidade", 
                            clearable=True, 
                            className="dropdown",                                 
                        ),
                    ]
                ),    
                html.Div(
                    children=[
                        html.Div(children="Produto", className="menu-title"),
                        dcc.Dropdown(
                            id='product-dd',
                            options=[{'label':'Casaco','value':'Casaco'},
                                     {'label':'Camiseta','value':'Camiseta'},
                                     {'label':'Sapato', 'value':'Sapato'},
                                     {'label':'Vestido', 'value':'Vestido'},
                                     {'label':'Sandalia','value':'Sandalia'},
                                     {'label':'Saia','value':'Saia'},
                                     {'label':'Bermuda','value':'Bermuda'},  
                                     {'label':'Pulseira', 'value':'Pulseira'},
                                     {'label':'Jaqueta','value':'Jaqueta'},
                                     {'label':'Tenis','value':'Tenis'},
                                     {'label':'Short','value':'Short'},
                                     {'label':'Chinelo','value':'Chinelo'},                            ],                   
                            placeholder="Escolha um produto",
                            clearable=True, 
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Período (Mês)", className="menu-title"),
                        dcc.Dropdown(
                            id="date-dd",
                            options=[{'label':'Janeiro','value':1},
                                     {'label':'Fevereiro','value':2},
                                     {'label':'Marco', 'value':3},
                                     {'label':'Abril', 'value':4},
                                     {'label':'Maio','value':5},
                                     {'label':'Junho','value':6},
                                     {'label':'Julho','value':7},  
                                     {'label':'Agosto', 'value':8},
                                     {'label':'Setembro','value':9},
                                     {'label':'Outubro','value':10},
                                     {'label':'Novembro','value':11},
                                     {'label':'Dezembro','value':12},                            ],                   
                            placeholder="Escolha um Mês",
                            clearable=True, 
                            className="dropdown",
                            value=1,                            
                        ),
                    ]
                ),
            ],
            className="menu",
        ),

        html.Br(),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Faturamento", className="menu-title"),
                        dbc.Card([
                        dbc.CardHeader( ""),
                        dbc.CardBody([
                            html.H4("Total : %{Faturamentot}"),
                            html.H6(id='content-connections1')],
                            style={'textAlign':'center', 'display':'inline-block',},
                        ),
                    ], style={"display":"inline-block","width":"268px"},
                ),],),
                html.Div(
                    children=[
                        html.Div(children="Unidades vendidas", className="menu-title"),
                        dbc.Card([
                        dbc.CardHeader( "", ),
                        dbc.CardBody([
                            html.H4('Connections'),
                            html.H6(id='content-connections2')],
                            style={'textAlign':'center', 'display':'inline-block',},
                        ),
                    ],style={"display":"inline-block", "width":"268px"},
                ),],),
                html.Div(
                    children=[
                        html.Div(children="Média Preço", className="menu-title"),
                        dbc.Card([
                        dbc.CardHeader("",),
                        dbc.CardBody([
                            html.H4('Connections'),
                            html.H6(id='content-connections3')],
                            style={'textAlign':'center', 'display':'inline-block',},
                        ),
                    ],style={"display":"inline-block","width":"268px"},
                ),],),],
                className="menu2",
                ),     

        

        html.Br(),    



        html.Div(
            children =[
                html.Div(
                    children=dcc.Graph(
                        id="line_graph",
                    ),
                    className="card",
        ),           
        html.Div(
            children =dcc.Graph(
                        id="tree_fig",
                    ),
                    className="card",
        ),
        html.Div(
            children =dcc.Graph(
                        id="major-product",
                    ),
                    className="card",
        ), 
        html.Div(
            children =dcc.Graph(
                        id="major-cat",
                    ),
                    className="card",
        ), 
    ],
    className="wrapper",
        ),
    ]
)
        
 
        

#bar_fig_produto
@app.callback(
    Output(component_id='major-cat', component_property='figure'),
    [Input(component_id='country-dd', component_property='value'),
     Input(component_id="date-dd", component_property='value'),]
)

def update_plot(input_country, input_date):
    country_filter = 'Todas Cidades'
    vendasc = vendas.copy(deep=True)
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter]
    if input_date:
        date_filter = input_date
        vendasc = vendasc[vendasc['Mes_Vendas_Num']==date_filter]
    ecom_bar_major_cat = vendasc.groupby('Produto')['Faturamento'].agg('sum').reset_index(name='Total')
    bar_fig_produto = px.bar(data_frame=ecom_bar_major_cat, x = 'Produto', y='Total', title = 'Faturamento total por produto', color = 'Produto',
    text_auto=True, labels = dict(Produto="", Total="Faturamento"))
    bar_fig_produto.update_layout(showlegend=False)
    return bar_fig_produto


#bar_graph_cidade
@app.callback(
    Output(component_id='major-product', component_property='figure'),
    [Input(component_id='product-dd', component_property='value'),
     Input(component_id='date-dd',component_property='value'),]
)

def update_plot(input_produto, input_date):
    produto_filter = 'Todos produtos'
    vendasc = vendas.copy(deep=True)
    if input_produto:
        produto_filter = input_produto
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    if input_date:
        date_filter = input_date
        vendasc = vendasc[vendasc['Mes_Vendas_Num']==input_date]
    vend_bar_major_pdt = vendasc.groupby('Loja')['Faturamento'].agg('sum').reset_index(name='Total')
    bar_graph = px.bar(
    data_frame=vend_bar_major_pdt,  x='Total',  y = 'Loja',
    orientation = 'h',
    title = 'Faturamento total por cidade',
    text_auto=True,
    color = 'Loja', color_discrete_map={'Sao Paulo':'#abb0ca','Salvador':'#e5cbb0','Rio de Janeiro':'#050507','Porto Alegre':'#e02844',
    'Fortaleza':'#6d6e8c','Curitiba':'#554f64','Brasilia':'#8cac7f'},
    labels = dict( Loja = ""))
    bar_graph.update_layout(showlegend=False)
    return bar_graph


#line_graph
@app.callback(
    Output(component_id='line_graph', component_property='figure'),
    [Input(component_id='product-dd', component_property='value'),
     Input(component_id='country-dd', component_property='value')])

def update_plot(input_produto, input_country):
    produto_filter = 'Todos produtos'
    vendasc = vendas.copy(deep=True)
    if input_produto:
        produto_filter = input_produto
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter]
    vendasg=vendasc.groupby(['Mes_Vendas_Num','Loja'])['Faturamento'].agg('sum').reset_index(name='Faturamento total')
    line_graph = px.line(
    data_frame = vendasg, 
    title = 'Faturamento total por Mês/Loja',
    x = 'Mes_Vendas_Num',
    y= 'Faturamento total', 
    color = 'Loja',
    labels = dict(Mes_Vendas_Num="", Faturamento_total= "Faturamento"))
    line_graph.update_xaxes(
    ticktext=["Janeiro","Fevereiro","Marco" ,"Abril","Maio" ,"Junho","Julho", "Agosto","Setembro","Outubro","Novembro","Dezembro"],
    tickvals=[1,2,3,4,5,6,7,8,9,10,11,12],)
    return line_graph

#tree_fig
@app.callback(
    Output(component_id='tree_fig', component_property='figure'),
    [Input(component_id='product-dd', component_property='value'),
     Input(component_id='date-dd',component_property='value'),]
)

def update_plot(input_produto, input_date):    
    vendasc = vendas.copy(deep=True)
    if input_produto:
        produto_filter = input_produto
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    if input_date:
        date_filter = input_date
    vendasc = vendasc[vendasc['Mes_Vendas_Num']==input_date]
    vendasg = vendasc.groupby('Loja')['Quantidade Vendida'].agg('sum').reset_index(name='Total')    
    tree_fig = px.treemap(
    data_frame=vendasg, 
    path=['Loja'], 
    values='Total',
    color='Total',
    title="Unidades vendidas por Cidade",)
    tree_fig.update_coloraxes(showscale=False) 
    tree_fig.update_traces(hovertemplate='Cidade = %{label}<br>Total = %{value}<extra></extra>')
    return tree_fig

 
  





if __name__ == '__main__':
	app.run_server(debug=True)



