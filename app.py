import dash
import numpy as np
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
import pandas as pd

import _data_for_dash as _dd

_dict_inductance = {
    'CV': [0.00156769, 0.00246953, 0.00262631, 0.00286779, 0.00299718,
           0.00289128, 0.00281451, 0.0028337 , 0.00281157, 0.0028023 ],
    'CH': [0.00208073, 0.00274155, 0.00301928, 0.00316398, 0.00333924,
           0.0032438 , 0.00305018, 0.00299117, 0.00295591, 0.00293359],
    'QS': [0.00399917, 0.00613224, 0.00634324, 0.00622694, 0.00633215,
           0.00705117, 0.00820824, 0.00890014, 0.00909269, 0.00905809],
    'current[A]CH-CV': np.arange(0.1,1.1,0.1),
    'current[A]QS': np.arange(0.1,3.0,0.3)}

#DataFrame with Inductances values:
_df = pd.DataFrame.from_dict(_dict_inductance)

#DataFrames list with all steps CV and CH values:
_ch_list, _cv_list = _dd.export_list()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def plot_graph(value=_ch_list, name='CH Coil'):
    fig = make_subplots(rows=5, cols=2,subplot_titles=("Step 0-0.1A", "Step 0-0.2A", "Step 0-0.3A", "Step 0-0.4A", "Step 0-5A",
                                                       "Step 0-0.6A", "Step 0-0.7A", "Step 0-0.8A", "Step 0-0.9A", "Step 0-1A"),
                        specs=[[{"secondary_y": True}, {"secondary_y": True}],
                               [{"secondary_y": True}, {"secondary_y": True}],
                               [{"secondary_y": True}, {"secondary_y": True}],
                               [{"secondary_y": True}, {"secondary_y": True}],
                               [{"secondary_y": True}, {"secondary_y": True}]
                              ])
    _c = 1
    while _c < (len(value)):
        for i in range(1,6):
            for j in range(1,3):
                fig.add_trace(
                    go.Scatter(x=value[_c-1]['time(s)'], y=value[_c-1]['I(A)'], name="0-"+str((_c)/10)+"A I[A]"),
                    row=i, col=j, secondary_y=False)

                fig.add_trace(
                    go.Scatter(x=value[_c-1]['time(s)'], y=value[_c-1]['dI/dt'], name="0-"+str((_c)/10)+"[A/s]"),
                    row=i, col=j, secondary_y=True,
                )
                _c += 1

    # Update xaxis properties
    for i in range(1,6):      #n row
        for j in range(1,3):  #n column
            fig.update_xaxes(title_text="time (s)", row=i, col=j)
            # Update yaxis properties
            fig.update_yaxes(title_text="I [A]",secondary_y=False, row=i, col=j)
            fig.update_yaxes(title_text="dI/dt [A/s]",secondary_y=True, showgrid=False, row=i, col=j)

    # Update title and height
    fig.update_layout(title_text=name+" dI/dt and I versus time for all steps", height=1500)

    return fig

#Layout Dash init
app.layout = html.Div([
    html.H2(children='Inductance Magnet Test with Fast Corrector'),

    dcc.Markdown('''
    #### Model: FC-001 - Correction function: FC1

    
    > - **Magnet under test:** Fast Corrector - FC-001 - CV & CH Coil;

    > - **Power Supply:** CAENels FAST-PS 1020;


    > - **Goal:** Measure the possible inductance variation as a function of the applied current.

    > - **Procedure:** The input current in the coils is varied in continuous steps from 0.1 A amplitude to a maximum nominal setting according to magnetic field requirements.
    With the oscilloscope, we measure the variation of current and voltage in the coils,
    calculate the resistance through the relation between voltage and current over time,
    it is possible to determine the time constant of the RL circuit and this way, calculate the inductance of the coil.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
        'data': [
                {'x': _df['current[A]CH-CV'], 'y': _df['CH'], 'type': 'line', 'name': 'CH'},
                {'x': _df['current[A]CH-CV'], 'y': _df['CV'], 'type': 'line', 'name': 'CV'},
                {'x': _df['current[A]QS'], 'y': _df['QS'], 'type': 'line', 'name': 'QS'}
                ],
            
        'layout': go.Layout(
            title={
                'text':"<b>Inductance as a function of current (L[H] x I[A])</b>",
                'xanchor':'center'
                },
            xaxis={
                'title': 'Current [A]',
                'type':'linear'
                },
            yaxis={
                'title': 'L(H)',
                'type': 'linear'
                }
            )
    }
    ),
    
    dcc.Markdown('''
    Select the coil to view Current I (A) and Derivative dI/dt (A/s) graphs:
    '''),

    dcc.Dropdown(id='cb_induct', 
    options=[
        {'label': 'Inductance (L) CH', 'value': 'CH'},
        {'label': 'Inductance (L) CV', 'value': 'CV'},
        {'label': 'Inductance (L) QS', 'value': 'QS'}
    ],
    value='CH'
    ),
    
    dcc.Graph(figure=plot_graph(), id='my-figure')
    
])

@app.callback(
    dash.dependencies.Output(component_id='my-figure', component_property='figure'),
    [dash.dependencies.Input(component_id='cb_induct', component_property='value')]
    )
def update_graph(value):
    '''prepare figure from value'''
    
    if value == 'CH':
        value = _ch_list
        name = 'CH Coil'
    else:
        value = _cv_list
        name = 'CV Coil'
    
    return plot_graph(value, name)
    


























'''
trace1 = go.Scatter(
x=[0, 1, 2],
y=[10, 11, 12]
)
trace2 = go.Scatter(
    x=[2, 3, 4],
    y=[100, 110, 120],
)
trace3 = go.Scatter(
    x=[3, 4, 5],
    y=[1000, 1100, 1200],
)
fig = make_subplots(rows=3, cols=1, specs=[[{}], [{}], [{}]],
                          shared_xaxes=True, shared_yaxes=True,
                          vertical_spacing=0.001)
fig.append_trace(trace1, 3, 1)
fig.append_trace(trace2, 2, 1)
fig.append_trace(trace3, 1, 1)

fig['layout'].update(height=600, width=600, title='Stacked Subplots with Shared X-Axes')


app.layout = html.Div([
    dcc.Graph(figure=fig, id='my-figure')
])
'''
'''
app.layout = html.Div(children=[
    html.H1(children='Inductance Magnet Test with Fast Corrector'),

    dcc.Graph(
        id='example-graph',
        figure={
        'data': [
                {'x': _df['current[A]'], 'y': _df['CH'], 'type': 'line', 'name': 'CH'},
                {'x': _df['current[A]'], 'y': _df['CV'], 'type': 'line', 'name': 'CV'},
                ],
            
        'layout': go.Layout(
            title={
                'text':"<b>Inductance as a function of current (L[H] x I[A])</b>",
                'xanchor':'center'
                },
            xaxis={
                'title': 'Current [A]',
                'type':'linear'
                },
            yaxis={
                'title': 'L(H)',
                'type': 'linear'
                }
            )
    }
    ),

    dcc.Dropdown(id='cb_induct', 
    options=[
        {'label': 'Inductance (L) CH', 'value': 'CH'},
        {'label': 'Inductance (L) CV', 'value': 'CV'},
        {'label': 'Inductance (L) QS', 'value': 'QS'}
    ],
    multi=True,
    value='MTL'
    )
])
##@app.callback(
##    Output(componen_
##    )
'''
if __name__ == '__main__':
    app.run_server(debug=True)

  
