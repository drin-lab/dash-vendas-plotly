# Number statistics & number of accidents each day

html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.H3(id='no_acc', style={'fontWeight': 'bold'}),
            html.Label('Total accidents', style={'paddingTop': '.3rem'}),
        ], className="three columns number-stat-box"),

        html.Div(children=[
            html.H3(id='no_cas', style={'fontWeight': 'bold', 'color': '#f73600'}),
            html.Label('Casualties', style={'paddingTop': '.3rem'}),
        ], className="three columns number-stat-box"),

        html.Div(children=[
            html.H3(id='no_veh', style={'fontWeight': 'bold', 'color': '#00aeef'}),
            html.Label('Total vehicles', style={'paddingTop': '.3rem'}),
        ], className="three columns number-stat-box"),

        html.Div(children=[
            html.H3(id='no_days', style={'fontWeight': 'bold', 'color': '#a0aec0'}),
            html.Label('Number of days', style={'paddingTop': '.3rem'}),
        
        ], className="three columns number-stat-box"),
    ], style={'margin':'1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'flex-wrap': 'wrap'}),

    # Line chart for accidents per day
    html.Div(children=[
        dcc.Graph(id='acc_line_chart')
    ], className="twleve columns", style={'padding':'.3rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white', }),

], className="eight columns", style={'backgroundColor': '#f2f2f2', 'margin': '1rem'})