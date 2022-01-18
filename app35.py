import dash
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly
import plotly.express as px
import pandas as pd
vendas = pd.read_csv('vendas.csv')

vendasg=vendas.groupby(['Mes_Vendas','Loja'])['Faturamento'].agg('sum').reset_index(name='Faturamento total')
line_graph = px.line(
data_frame = vendasg, 
title = 'Faturamento total por Mês/Loja',
x = 'Mes_Vendas',
y= 'Faturamento total', 
color = 'Loja',
labels = dict(Mes_Vendas="Período (Mês)", Loja = "Cidade"))
line_graph.update_xaxes(
    ticktext=["Fevereiro", "Abril", "Junho", "Agosto","Outubro","Dezembro"],
    tickvals=["2", "4", "6", "8","10","12"],
)




qtd_local = vendas.groupby('Loja')['Quantidade Vendida'].agg('sum').reset_index(name='Quantidade Total')
tree_fig = px.treemap(vendas, path=['Loja'], values='Quantidade Vendida',
                  color='Quantidade Vendida', title="Qtd Vendas por Cidade",
                  color_continuous_scale=[(0, "#dee817"), (0.5, "#c3c595"), (1, "#cac9c2")])
tree_fig.update_coloraxes(showscale=False)



external_stylesheets = [{"href":"https://fonts.googleapis.com/css2?"},]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "[Python] Dashboard Vendas"

all = vendas['Produto'].unique()


app.layout = html.Div(
    children=[
        html.Div(
            children =[
            	html.H1(children = "Report Vendas ",
                className="header-title"),
                html.P(children = "Análise do comportamento de vendas e faturamento",
                className="header-description",),],
            	className="header",),
        html.Div(children=[html.H3("Selecione uma cidade"),dcc.Dropdown(id='country_dd',
            options=[{'label':'Sao Paulo','value':'Sao Paulo'},
                    {'label':'Salvador','value':'Salvador'},
                    {'label':'Rio de Janeiro', 'value':'Rio de Janeiro'},
                    {'label':'Porto Alegre', 'value':'Porto Alegre'},
                    {'label':'Brasilia','value':'Brasilia'},
                    {'label':'Fortaleza','value':'Fortaleza'},
                    {'label':'Curitiba','value':'Curitiba'}],
                    value='Loja',                                   
                    style={'border-bottom': '3px dotted gold','width': '268px', 'padding': '5px','font-size': '16px','line-height': 1,
                     'border': 0, 'border-radius': '5px','height': '34px','display':'inline-block','margin':'auto',},
                    )]),
        html.Div(children=[html.H3("Selecione um Produto"),dcc.Dropdown(id='product_dd',
            options=[{'label':x, 'value':x} for x in all] + [{'label': 'Select all', 'value': 'all_values'}], 
                    value='all_values',  
                    style={'border-bottom': '3px dotted gold','width': '268px', 'padding': '5px','font-size': '16px','line-height': 1,
                     'border': 0, 'border-radius': '5px','height': '34px','display':'inline-block','margin':'auto',},
                    )]), 
        html.Br(),           
        html.Div(dcc.Graph(figure=line_graph),
                style={'width':'850px', 'margin':'0 auto'}),
        html.Div(dcc.Graph(id="tree_fig", figure=tree_fig),
                style={'width':'550px', 'display':'inline-block', 'margin-left':'130px'}),      
        html.Div(dcc.Graph(id="major_product"),
        		style={'width':'500px','display':'inline-block', 'margin':'auto'}),       
        html.Div(children=[dcc.Graph(id='major_cat'),],
                style={'width':'850px'}), 
        ],
        )


@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='major_cat', component_property='figure'),
    Input(component_id='country_dd', component_property='value')
)

def update_plot(input_country):
    country_filter = 'All Countries'
    vendasc = vendas.copy(deep=True)
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter]
    ecom_bar_major_cat = vendasc.groupby('Produto')['Faturamento'].agg('sum').reset_index(name='Total')
    bar_fig_produto = px.bar(data_frame=ecom_bar_major_cat, x = 'Produto', y='Total', title = 'Faturamento total por produto', color = 'Produto',
    text_auto=True, labels = dict(Produto="", Total="Faturamento"))
    bar_fig_produto.update_layout(showlegend=False)
    return bar_fig_produto

#segundo
@app.callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='major_product', component_property='figure'),
    Input(component_id='product_dd', component_property='value')
)

def update_plot(input_produto):
    vendasc = vendas.copy(deep=True)
    if input_produto:
        produto_filter = input_produto
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    else:
        input_produto == ['all']
        vendasc = vendas.copy(deep=True)
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



  


if __name__ == '__main__':
	app.run_server(debug=True)



