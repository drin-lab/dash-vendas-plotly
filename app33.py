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



vendas_f = vendas.groupby('Loja')['Faturamento'].agg('sum').reset_index(name='Faturamento total')
bar_graph = px.bar(
data_frame=vendas_f, 
x='Faturamento total',
y = 'Loja',
orientation = 'h',
title = 'Faturamento total por cidade',
text_auto=True,
color = 'Loja', color_discrete_map={'Sao Paulo':'#abb0ca','Salvador':'#e5cbb0','Rio de Janeiro':'#050507','Porto Alegre':'#e02844',
'Fortaleza':'#6d6e8c','Curitiba':'#554f64','Brasilia':'#8cac7f'},
labels = dict( Loja = ""))
bar_graph.update_layout(showlegend=False)





vendas_p = vendas.groupby('Produto')['Faturamento'].agg('sum').reset_index(name='Faturamentot')
bar_fig = px.bar(
data_frame=vendas_p, 
x = 'Produto',
y='Faturamentot',
title = 'Faturamento total por produto',
color = 'Produto',
text_auto=True,
labels = dict(Produto="", Faturamentot="Faturamento"))
bar_fig.update_layout(showlegend=False)


qtd_local = vendas.groupby('Loja')['Quantidade Vendida'].agg('sum').reset_index(name='Quantidade Total')
tree_fig = px.treemap(vendas, path=['Loja'], values='Quantidade Vendida',
                  color='Quantidade Vendida', title="Qtd Vendas por Cidade",
                  color_continuous_scale=[(0, "#dee817"), (0.5, "#c3c595"), (1, "#cac9c2")])
tree_fig.update_coloraxes(showscale=False)



external_stylesheets = [
    {
        "href":"https://fonts.googleapis.com/css2?"
        "family=Lato:wgt@400;700&display=swap",
        "rel":"stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "[Python] Dashboard Vendas"


app.layout = html.Div(
    children=[
        html.Div(
            children =[
            	html.H1(children = "Report Vendas ",
                className="header-title"),
                html.P(children = "Análise do comportamento de vendas e faturamento",
                className="header-description",),],
            	className="header",),
        html.Div(children=[html.H3("Selecione uma cidade"),dcc.Dropdown(id='cidade_dropdown',
            options=[{'label':'Sao Paulo','value':'Sao Paulo'},
                    {'label':'Salvador','value':'Salvador'},
                    {'label':'Rio de Janeiro', 'value':'Rio de Janeiro'},
                    {'label':'Porto Alegre', 'value':'Porto Alegre'},
                    {'label':'Brasilia','value':'Brasilia'},
                    {'label':'Fortaleza','value':'Fortaleza'},
                    {'label':'Curitiba','value':'Curitiba'}],
                    value='Cidade',
                    multi=True,                    
                    className='select_box',)]),        
        html.Div(dcc.Graph(figure=line_graph),
                style={'width':'850px', 'margin':'auto'}),
        html.Div(dcc.Graph(id="tree_fig", figure=tree_fig),
                style={'width':'550px', 'display':'inline-block', 'margin-left':'130px'}),      
        html.Div(dcc.Graph(id="bar_graph", figure=bar_graph),
        		style={'width':'500px','display':'inline-block', 'margin':'auto'}),        
        html.Div(dcc.Graph(id="bar_fig", figure=bar_fig),
                style={'width':'850px', 'margin':'auto'}), 
        ],
        )


@app.callback(
    Output(component_id='bar_fig', component_property='figure'),
    [Input(component_id='cidade_dropdown', component_property='value')])



def update_plot(input_cidade):
    cidade_filter = 'Todas as cidades'
    vendas2 = vendas.copy(deep=True)
    if input_cidade:
        cidade_filter = input_cidade
        vendas2 = vendas2[vendas2['Loja']==cidade_filter]
    vendas_p = vendas2.groupby('Produto')['Faturamento'].agg('sum').reset_index(name='Faturamentot')
    bar_fig = px.bar(
    data_frame=vendas_p, 
    x = 'Produto',
    y='Faturamentot',
    title = 'Faturamento total por produto',
    color = 'Produto',
    text_auto=True,
    labels = dict(Produto="", Faturamentot="Faturamento"))
    bar_fig.update_layout(showlegend=False) 
    return bar_fig

if __name__ == '__main__':
	app.run_server(debug=True)