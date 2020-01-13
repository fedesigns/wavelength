import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import csv
import time
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas

# Muse data
timestamps = []
dt_object = []
alpha_consciousness = []
focused_concentration = []
calm_relaxation = []
overthinking = []
distraction_vulnerability = []
engagement = []
impulse_control = []
under_arousal = []


# RescueTime data - requesting directly from the API as it provides historical data

#RT_df = pandas.read_csv("https://www.rescuetime.com/anapi/data?key=B63kQQhCfdXEaQLHbKVTt3x55woxyhk2kjabQ3BU&format=csv&pv=interval&rs=minute&rk=efficiency&rb=2020-01-06&re=2020-02-05")
#productivity_dt = RT_df['Date']
#interval_time = RT_df['Time Spent (seconds)'].astype(float)
#productivity = (RT_df['Efficiency (percent)'].astype(float))*interval_time/30000

productivity_dt = []
interval_time = []
productivity = []

with open("Data/productivity.csv", "r", newline='') as csvfile1:
	RTreader = csv.reader(csvfile1, delimiter=',')
	for row in RTreader:
		dt = row[0]
		productivity_dt.append(dt)
		int_time = float(row[1])
		interval_time.append(int_time)
		prod = float(row[4])*int_time/30000
		productivity.append(prod)


# List of Neurofeedback metrics
metrics = [timestamps, dt_object, alpha_consciousness, focused_concentration, calm_relaxation, \
	overthinking, distraction_vulnerability, engagement, \
	impulse_control, under_arousal]

#getting data for the historical graph
with open("Data/Neurofeedback.csv", "r", newline='') as csvfile2:
	datareader = csv.reader(csvfile2, delimiter=',')
	for row in datareader:
		#skipping noisy artefacts
		if float(row[2]) <= 1.3 and float(row[2]) >= -0.5 \
			and float(row[3])<= 1 and float(row[3]) >= -1 \
			and float(row[4])<= 3 and float(row[4]) >= 0 \
			and float(row[5])<= 1.5 and float(row[5]) >= -1 \
			and float(row[7])<= 1.2 and float(row[7]) >= -1 :
			for i in range(2):
				value = row[i]
				metrics[i].append(value)
			
			# scaling data for comparability
			value2 = float(row[2])
			metrics[2].append(value2)
			value3 = (float(row[3])+0.5) 
			metrics[3].append(value3)
			value4 = (float(row[4])-1)/3 
			metrics[4].append(value4)
			value5 = (float(row[5])+0.5)
			metrics[5].append(value5)
			value7 = (float(row[7])+0.5)/1.5
			metrics[7].append(value7)
			

print(dt_object[-1])
#print(timestamps)



print(len(timestamps))
print(len(alpha_consciousness))
print(len(focused_concentration))
'''

values = np.asarray(alpha_consciousness)
values = values.reshape((len(values), 1))
# train the normalization
scaler = MinMaxScaler(feature_range=(0, 1))
scaler = scaler.fit(values)
normalised_consciousness = scaler.transform(values)

values2 = np.asarray(focused_concentration)
values2 = values2.reshape((len(values), 1))
# train the normalization
scaler2 = MinMaxScaler(feature_range=(0, 1))
scaler2 = scaler2.fit(values2)
normalised_concentration = scaler2.transform(values2)

values3 = np.asarray(calm_relaxation)
values3 = values3.reshape((len(values), 1))
# train the normalization
scaler3 = MinMaxScaler(feature_range=(0, 1))
scaler3 = scaler3.fit(values)
normalised_relaxation = scaler3.transform(values3)


values4 = np.asarray(engagement)
values4 = values4.reshape((len(values4), 1))
# train the normalization
scaler4 = MinMaxScaler(feature_range=(0, 1))
scaler4 = scaler4.fit(values4)
normalised_engagement = scaler4.transform(values4)


values5 = np.asarray(overthinking)
values5 = values5.reshape((len(values), 1))
# train the normalization
scaler5 = MinMaxScaler(feature_range=(0, 1))
scaler5 = scaler.fit(values5)
normalised_overthinking = scaler5.transform(values5)
'''



'''
values = np.asarray(focused_concentration)
focused_concentration = values.reshape(1, len(values))

values = np.asarray(calm_relaxation)
calm_relaxation = values.reshape(len(values),1)

values = np.asarray(engagement)
engagement = values.reshape(len(values),1)

values = np.asarray(overthinking)
overthinking = values.reshape(len(values),1)
'''

X = deque(maxlen=30)


dt_object_live = []
productivity_dt_live = []


#app = dash.Dash(__name__)

alpha_consciousness_live = [3]
focused_concentration_live = [3]
calm_relaxation_live = [3]
engagement_live = [3]
overthinking_live = [3]
productivity_live = [3]

data_dict = {'Alpha Consciousness': alpha_consciousness_live,
'Focused Concentration': focused_concentration_live,
'Calm Relaxation': calm_relaxation_live,
'Task Engagament': engagement_live,
'Overactive stress': overthinking_live,
'Laptop Productivity': productivity_live
}

def update_live_values(dt_object_live,alpha_consciousness_live,focused_concentration_live,calm_relaxation_live,overthinking_live,engagement_live,productivity_dt_live,productivity_live, X):
	df = pandas.read_csv("Data/Neurofeedback.csv")
	last_dt_object = df['2020-01-07 17:22:56.287579'].iloc[-1]
	last_consciousness_value = df['-0.7024792791694109'].iloc[-1]
	last_focus_value = df['4.935525575893768'].iloc[-1]
	last_relaxation_value = df['0.2705343652631265'].iloc[-1]
	last_overthinking_value = df['1.0509194520195624'].iloc[-1]
	last_engagement_value = df['0.32101251009833437'].iloc[-1]


	dt_object_live.append(last_dt_object)
	X.append(last_dt_object)

	# Filtering out noisy artefacts
	if float(last_consciousness_value) <= 2 and float(last_consciousness_value) >= -2:
		alpha_consciousness_live.append(float(last_consciousness_value)+3)
	else:
		alpha_consciousness_live.append(alpha_consciousness_live[-1])

	if float(last_focus_value) <= 2 and float(last_focus_value) >= -2:
		focused_concentration_live.append(float(last_focus_value)+3)
	else:
		focused_concentration_live.append(focused_concentration_live[-1])
	
	if float(last_relaxation_value) <= 2 and float(last_relaxation_value) >= -2:
		calm_relaxation_live.append(float(last_relaxation_value)+3)
	else:
		calm_relaxation_live.append(calm_relaxation_live[-1])

	if float(last_overthinking_value) <= 2 and float(last_overthinking_value) >= -2:
		overthinking_live.append(float(last_overthinking_value)+3)
	else:
		overthinking_live.append(overthinking_live[-1])

	if float(last_engagement_value) <= 2 and float(last_engagement_value) >= -2:
		engagement_live.append(float(last_engagement_value)+3)
	else:
		engagement_live.append(engagement_live[-1])

	# Getting the last productivity value from RescueTime
	#RT_df = pandas.read_csv("https://www.rescuetime.com/anapi/data?key=B63kQQhCfdXEaQLHbKVTt3x55woxyhk2kjabQ3BU&format=csv&pv=interval&rs=minute&rk=efficiency&rb=2020-01-06&re=2020-02-05")
	#productivity_dt_live = RT_df['Date'].iloc[-1]
	#interval_time_live = RT_df['Time Spent (seconds)'].iloc[-1].astype(float)
	#productivity_live = (RT_df['Efficiency (percent)'].iloc[-1].astype(float))*interval_time/15000

	return dt_object_live,alpha_consciousness_live,focused_concentration_live,calm_relaxation_live,overthinking_live,engagement_live,productivity_dt_live,productivity_live, X

dt_object_live,alpha_consciousness_live,focused_concentration_live,calm_relaxation_live,overthinking_live,engagement_live,productivity_dt_live,productivity_live, X = \
update_live_values(dt_object_live,alpha_consciousness_live,focused_concentration_live,calm_relaxation_live,overthinking_live,engagement_live,productivity_dt_live,productivity_live,X)

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']

app = dash.Dash('wavelength',
                external_scripts=external_js,
                external_stylesheets=external_css)

app.layout = html.Div([
	html.Div([
		html.H1('wavelength'
			, style={'color': '#2077B4','marginBottom': 0, 'marginTop': 50, 'marginLeft': 0}),
        html.H4('a neurofeedback-based productivity platform',
                style={'float': 'left'},
                       ),
        ]),

    dcc.Dropdown(id='focus-state-metric',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Alpha Consciousness','Focused Concentration','Calm Relaxation'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=3000,
        n_intervals = 0),
	#dcc.Graph(id='focused-concentration', animate=True),
		# CSS framework for responsive front-end layout
	

	dcc.Graph(id='fixed-graph',
		figure = {
			'data' : [
				{'x':dt_object, 'y':alpha_consciousness, 'type':'scatter', 'name':'Alpha Consciousness'},
				{'x':dt_object, 'y':focused_concentration, 'type':'scatter', 'name':'Focused Concentration'},
				{'x':dt_object, 'y':calm_relaxation, 'type':'scatter', 'name':'Calm relaxation'},
			#	{'x':dt_object, 'y':distraction_vulnerability, 'type':'scatter', 'name':'Distraction vulnerability'},
			#	{'x':dt_object, 'y':impulse_control, 'type':'scatter', 'name':'Impulse control'},
			#	{'x':dt_object, 'y':under_arousal, 'type':'scatter', 'name':'Under-arousal'},
				{'x':dt_object, 'y':engagement, 'type':'scatter', 'name':'Task engagement'},
				{'x':dt_object, 'y':overthinking, 'type':'scatter', 'name':'Overactive stress'},
				{'x':productivity_dt, 'y':productivity, 'type':'scatter', 'name':'Laptop work productivity'},
				],
			'layout' : {
				'title':'Historical Data',
				}
			}),
	], className="container",style={'width':'80%','margin-left':120,'margin-right':80,'max-width':50000})
	

'''
@app.callback(Output('focused-concentration', 'figure'),
		[Input('graph-update', 'n_intervals')])
'''

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('focus-state-metric', 'value'),
    dash.dependencies.Input('graph-update', 'n_intervals')],
    )
    

def update_graph(data_names, n):
    graphs = []
    update_live_values(dt_object_live,alpha_consciousness_live,focused_concentration_live,calm_relaxation_live,overthinking_live,engagement_live,productivity_dt_live,productivity_live,X)

    #responsive interface 
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'

    for data_name in data_names:


        data = go.Scatter(
            x=list(X),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            #fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                        yaxis=dict(range=[0.5,5.5]),
                                                        margin={'l':30,'r':30,'t':130,'b':80},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs
'''
def update_graph_scatter(n):
	#X.append(X[-1]+1)
	#Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
	df = pandas.read_csv("Data/Neurofeedback.csv")

	#with open("Data/Neurofeedback.csv", "r", newline='') as csvfile2:
	#	livereader = list(csv.reader(csvfile2, delimiter=','))
		#for row in datareader:
			#skipping noisy artefacts
		#if float(livereader[-1][2]) <= 1.3 and float(livereader[-1][2]) >= -0.5 \
		#	and float(livereader[-1][3])<= 2 and float(livereader[-1][3]) >= -2 \
		#	and float(livereader[-1][4])<= 3 and float(livereader[-1][4]) >= -3 \
		#	and float(livereader[-1][5])<= 2 and float(livereader[-1][5]) >= -2 \
		#	and float(livereader[-1][7])<= 1.2 and float(livereader[-1][7]) >= -1:
			#only appending the last values to the graph's data to only visualise the current session and reduce loading time	
	last_dt_object = df['2020-01-07 17:22:56.287579'].iloc[-1]
	last_focus_value = df['4.935525575893768'].iloc[-1]
	print(last_dt_object)
	print(last_focus_value)
	dt_object_live.append(last_dt_object)

	if float(last_focus_value) <= 2 and float(last_focus_value) >= -2:
		focused_concentration_live.append(last_focus_value)
	else:
		focused_concentration_live.append(focused_concentration_live[-1])

		#if last reading is noisy, grab value from 1 second ago
		#focused_concentration_live.append(df['4.935525575893768'].iloc[-10])


	#setting a rolling deque time window for visualisation
	X.append(last_dt_object)

	data = go.Scatter(
			x=dt_object_live,
			y=focused_concentration_live,
			name='Scatter',
			mode= 'lines+markers'
			)

	return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
												yaxis=dict(range=[min(focused_concentration_live),max(focused_concentration_live)]),
												)}
'''

# running the application
if __name__ == '__main__':
	app.run_server(debug=True)

