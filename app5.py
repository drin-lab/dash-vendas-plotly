import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
vendas = pd.read_csv('vendas.csv')
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/fdbe0accd2581a0c505dab4b29ebb66cf72a1803/e-comlogo.png'

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Img(src=logo_link,style={'margin':'30px 0px 0px 0px' }),
    html.H1('Sales breakdowns'),
    html.Div(
    children=[
    html.Div(
        children=[
        html.H2('Controls'),
        html.Br(),
        html.H3('Country Select'),
        # Add a dropdown with identifier
        dcc.Dropdown(id='country_dd',
        # Set the available options with noted labels and values
        options=[
            {'label':'Sao Paulo', 'value':'Sao Paulo'},
            {'label':'Salvador', 'value':'Salvador'},
            {'label':'Brasilia', 'value':'Brasilia'},
            {'label':'Curitiba', 'value':'Curitiba'},
            {'label':'Rio de Janeiro', 'value':'Rio de Janeiro'},
            {'label':'Fortaleza', 'value':'Fortaleza'},
            {'label':'Porto Alegre', 'value':'Porto Alegre'}],
            style={'width':'200px', 'margin':'0 auto'})
        ],
        style={'width':'350px', 'height':'350px', 'display':'inline-block', 'vertical-align':'top', 'border':'1px solid black', 'padding':'20px'}),
    html.Div(children=[
            # Add a graph component with identifier
            dcc.Graph(id='major_cat'),
            html.H2('Major Category', 
            style={ 'border':'2px solid black', 'width':'200px', 'margin':'0 auto'})
            ],
             style={'width':'700px','display':'inline-block'}
             ),
    ])], 
  style={'text-align':'center', 'display':'inline-block', 'width':'100%'}
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
    ecom_bar_major_cat = vendasc.groupby('Produto')['Faturamento'].agg('sum').reset_index(name='Total Sales ($)')
    bar_fig_major_cat = px.bar(
        title=f'Sales in {country_filter}', data_frame=ecom_bar_major_cat, x='Total Sales ($)', y='Produto', color='Produto'
                 )
    return bar_fig_major_cat


if __name__ == '__main__':
    app.run_server(debug=True)