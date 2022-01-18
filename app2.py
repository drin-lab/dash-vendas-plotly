import dash
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly
import plotly.express as px
import pandas as pd
vendas = pd.read_csv('vendas.csv')


# gráfico de linha
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


# gráfico de treemap
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
app.title = "[Python] Dashboard- Report Vendas"


app.layout = html.Div([
  html.H1('Sales breakdowns'),
  html.Div(
    children=[
    html.Div(
        children=[
        html.H2('Controls'),
        html.Br(),
        html.H3('Country Select'),                                
        dcc.Dropdown(id='cidade_dropdown',
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
        html.Div(children=[
            # Add a graph component with identifier
            dcc.Graph(id='major_cat'),
            html.H2('Major Category', 
            style={ 'border':'2px solid black', 'width':'200px', 'margin':'0 auto'})
            ],
             style={'width':'700px','display':'inline-block'}
             ),       
        html.Div(dcc.Graph(figure=line_graph),
                style={'width':'850px', 'margin':'auto'}),
        html.Div(dcc.Graph(id="tree_fig", figure=tree_fig),
                style={'width':'550px', 'display':'inline-block', 'margin-left':'130px'}),      
        html.Div(dcc.Graph(id="bar_graph", figure=bar_graph),
        		style={'width':'500px','display':'inline-block', 'margin':'auto'}),        
        html.Div([dcc.Graph(id="barfig", figure=barfig)],
                style={'width':'850px', 'margin':'auto'}), 
        ],
        )])

@app.callback(
    Output(component_id='major_cat', component_property='figure'),
    [Input(component_id='cidade_dropdown', component_property='value')])

def update_plot(input_cidade):
    vendas2 = vendas.copy(deep=True)
    if input_cidade:
        cidade_filter = input_cidade
        vendas2 = vendas2[vendas2['Loja']==cidade_filter]
    vendas_p = vendas2.groupby('Produto')['Faturamento'].agg('sum').reset_index(name='Faturamentot')
    barfig = px.bar(
    data_frame=vendas_p, 
    x = 'Produto',
    y='Faturamentot',
    title = 'Faturamento total por produto',
    color = 'Produto',
    text_auto=True,
    labels = dict(Produto="", Faturamentot="Faturamento"))
    barfig.update_layout(showlegend=False) 
    return barfig


if __name__ == '__main__':
	app.run_server(debug=True)



