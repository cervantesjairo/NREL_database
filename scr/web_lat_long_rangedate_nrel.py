from data.nrel_database.nrel_variables import NrelVar
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

"""
The code is a Python script that creates a dashboard using Dash, a web application framework for Python. The dashboard allows the user to select one or more NREL (National Renewable Energy Laboratory) variables, specify latitude and longitude, and a date range. Upon clicking the "Ejecutar" (execute) button, the dashboard will generate four graphs using Plotly graph objects, which will display the selected NREL variables for the specified location and date range.

The ui_variables variable is a list of dictionaries containing the names and values of the NREL variables that the user can select from using a dropdown menu. The app.layout variable creates the layout of the dashboard, which consists of a container with a header, four columns, and several rows. The first column contains the dropdown menu for selecting NREL variables, the second and third columns contain input fields for specifying latitude and longitude, and the fourth column contains a date range picker and a button to execute the dashboard. The second container contains four graphs that will display the selected NREL variables upon execution of the dashboard.

The @app.callback decorator specifies the function that will be called upon the button click event. The function takes the number of button clicks and the values of the dropdown menu, latitude, longitude, and date range as inputs. The function uses the values of these inputs to query the NREL database using the NrelVar class and generates four graphs using Plotly graph objects, which are then returned as outputs to the dashboard.
"""
ui_variables = [{'label': 'Global Horizontal Irradiation (GHI)',    'value': 'ghi'},
                {'label': 'Diffuse Horizontal Irradiance (DHI)',    'value': 'dhi'},
                {'label': 'Direct Normal Irradiation (DNI)',        'value': 'dni'},
                {'label': 'Clearsky GHI',         'value': 'clearsky_ghi'},
                {'label': 'Wind Speed',           'value': 'wind_speed'},
                {'label': 'Wind Direction',       'value': 'wind_direccion'},
                {'label': 'Temperature',          'value': 'air_temperature'},
                {'label': 'Precipitable Water',   'value': 'total_precipitable_water'},
                {'label': 'Surface Albedo',       'value': 'surface_albedo'},
                {'label': 'Solar Zenith Angle',   'value': 'solar_zenith_angle'},
                {'label': 'ALL',                  'value': 'ghi,dhi,dni,clearsky_ghi,wind_speed,wind_direction,air_temperature,total_precipitable_water,surface_albedo,solar_zenith_angle'}
                ]


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[

    dbc.Container(children=[
        html.H2('Informacion', style={'text-align': 'center', 'font-size': '2.00em', 'line-height': '100%'}),

        html.H2(),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H3('Variables', style={'text-align': 'center', 'fontSize': '1.25em', 'line-height': '200%'}),
                dcc.Dropdown(
                    id='dropdown_var',
                    options=ui_variables,
                    multi=True,
                    placeholder='Selecciona una o varias opciones'
                ),

            ],)# style={'width': '20%'})
        ]),

        html.H2(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Latitude', style={'text-align': 'center', 'font-size': '1.25em', 'line-height': '200%'}),
                dcc.Input(id='lat', type='number', value='', step=0.01, className='form-control')
            ], style={'width': '50%', 'float': 'left', 'text-align': 'center', 'margin': 'auto', 'padding': '12.5px'}),
            dbc.Col([
                dbc.Label('Longitude', style={'text-align': 'center', 'font-size': '1.25em', 'line-height': '200%'}),
                dcc.Input(id='lon', type='number', value='', step=0.01, className='form-control')
            ], style={'width': '50%', 'float': 'right', 'text-align': 'center', 'margin': 'auto', 'padding': '12.5px'}),
        ]),

        html.H2(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Rango de Fechas',
                          style={'text-align': 'center', 'font-size': '1.25em', 'line-height': '200%'}),  # 'margin': 'auto'}),
                dcc.DatePickerRange(
                    id='date_range',
                    start_date='2020-01-01',
                    end_date='2020-12-31',
                    className='form-control',
                    style={
                        'background-color': 'blue !important',
                        'color': 'blue', 'width': '100%',  'padding': '0px'}    # change font color
                )
            ], style={'width': '100%', 'text-align': 'center', 'padding': '10px'}),
        ]),

        html.H2(),
        dbc.Row([
            dbc.Col([
                html.H2(),
                html.Div([
                    html.Button('Ejecutar', id='ejecutar_solucion', n_clicks=0, className='btn btn-primary',
                                style={'width': '100%', 'fontSize': '1.75em', 'line-height': '200%'},
                                )], style={'text-align': 'center'}),
            ], style={'width': '100%', 'padding': '10px', 'margin-top': '12.5px'}),
        ]),


    ], style={'width': '25%', 'float': 'left', 'margin': 'auto', 'padding': '25px'}),


    html.Div(children=[

        html.H2('NREL variables', style={'text-align': 'center', 'font-size': '2.00em', 'line-height': '100%'}),
        html.Button('Download Data', id='btn', style={'text-align': 'center'}),
        dcc.Download(id="download-dataframe-csv"),

        dcc.Graph(id='result_fig1'),


        dcc.Graph(id='result_fig2'),

        dcc.Graph(id='result_fig3'),

        dcc.Graph(id='result_fig4'),

    ], style={'width': '75%', 'float': 'right', 'margin-top': '25px'}),

])


@app.callback(
    Output('result_fig1', 'figure'),
    Output('result_fig2', 'figure'),
    Output('result_fig3', 'figure'),
    Output('result_fig4', 'figure'),
    Input('ejecutar_solucion', 'n_clicks'),
    State('dropdown_var', 'value'),
    State('lat', 'value'),
    State('lon', 'value'),
    State('date_range', 'start_date'),
    State('date_range', 'end_date')
)


def update_graph(n_clicks, dropdown_var, lat, lon, start_date, end_date):
    global df
    #print(dropdown_var)

    if not n_clicks:
        raise PreventUpdate

    if not dropdown_var or not lat or not lon or not start_date or not end_date:
        return {}, {}

    variables_ui = ','.join(dropdown_var)
    nrel_var = NrelVar(var=variables_ui, lon=lon, lat=lat, period_range_from=start_date, period_range_to=end_date)
    df = nrel_var.data_variables()


    result_fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    if 'clearsky_ghi' in variables_ui:
        result_fig1.add_trace(go.Scatter(x=df.datetime, y=df['clearsky_ghi'], name='Clearsky GHI'), secondary_y=False)
    if 'ghi' in variables_ui:
        result_fig1.add_trace(go.Scatter(x=df.datetime, y=df['ghi'], name='GHI', line=dict(color='red')), secondary_y=False)
    if 'dni' in variables_ui:
        result_fig1.add_trace(go.Scatter(x=df.datetime, y=df['dni'], name='DNI'), secondary_y=False)
    if 'dhi' in variables_ui:
        result_fig1.add_trace(go.Scatter(x=df.datetime, y=df['dhi'], name='DHI'), secondary_y=False)
    result_fig1.update_layout(title={'text': 'Irradiance', 'x': 0.5, 'font': {'size': 20}},
                              xaxis_title='Date Time', yaxis_title='Irradiance [W/m2]',
                              margin=dict(l=50, r=50, t=50, b=50),
                              legend=dict(x=0, y=1, traceorder='normal'))


    result_fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    if 'wind_speed' in variables_ui:
        result_fig2.add_trace(go.Scatter(x=df.datetime, y=df['wind_speed'], name='Speed', line=dict(color='green')), secondary_y=False)
    if 'wind_direction' in variables_ui:
        result_fig2.add_trace(go.Scatter(x=df.datetime, y=df['wind_direction'], name='Direction', line=dict(color='blue')), secondary_y=True)
    result_fig2.update_layout(title={'text': 'Wind Speed and Wind Direction', 'x': 0.5, 'font': {'size': 20}},
                              xaxis_title='Date Time',
                              yaxis_title='Wind Speed [m/s]',
                              yaxis2_title='Wind Wind Direction [~]',
                              margin=dict(l=50, r=50, t=50, b=50),
                              legend=dict(x=0, y=1, traceorder='normal'))


    result_fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    if 'air_temperature' in variables_ui:
        result_fig3.add_trace(go.Scatter(x=df.datetime, y=df['air_temperature'], name='Temp.'), secondary_y=False)
    if 'total_precipitable_water' in variables_ui:
        result_fig3.add_trace(go.Scatter(x=df.datetime, y=df['total_precipitable_water'], name='Water'), secondary_y=True)
    result_fig3.update_layout(title={'text': 'Temperature and Precipitable Water', 'x': 0.5, 'font': {'size': 20}},
                              xaxis_title='Date Time',
                              yaxis_title='Temperature [~C]',
                              yaxis2_title='Precipitable Water [??]',
                              margin=dict(l=50, r=50, t=50, b=50),
                              legend=dict(x=0, y=1, traceorder='normal'))


    result_fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    if 'surface_albedo' in variables_ui:
        result_fig4.add_trace(go.Scatter(x=df.datetime, y=df['surface_albedo'], name='Albedo'), secondary_y=False)
    if 'solar_zenith_angle' in variables_ui:
        result_fig4.add_trace(go.Scatter(x=df.datetime, y=df['solar_zenith_angle'], name='Zenith'), secondary_y=True)
    result_fig4.update_layout(title={'text': 'Surface Albedo and Solar Zenith Angle', 'x': 0.5, 'font': {'size': 20}},
                              xaxis_title='Date Time',
                              yaxis_title='Surface Albedo [??]',
                              yaxis2_title='Solar Zenith Angle [??]',
                              margin=dict(l=50, r=50, t=50, b=50),
                              legend=dict(x=0, y=1, traceorder='normal'))


    return result_fig1, result_fig2, result_fig3, result_fig4


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn", "n_clicks")
)

def download_csv(n_clicks):
    global df
    if not n_clicks:
        raise PreventUpdate
    csv = df.to_csv(index=False, encoding='utf-8')
    return dict(content=csv, filename="data.csv")

if __name__ == '__main__':
    app.run_server(debug=True)


