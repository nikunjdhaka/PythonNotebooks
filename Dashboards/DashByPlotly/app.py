# Building a full interactive dashboard using the Dash framework by Plotly, which lets users select a country and view:
# A line chart of monthly revenue
# A bar chart of the top 5 months by revenue


import dash # Main framework to create the app
from dash import dcc, html, Input, Output
import plotly.express as px
from data_loader import load_data

# dash.dcc --> Dash Core Components (dropdowns, graphs, sliders)
# dash.html --> HTML Components (divs, headings, labels)
# Input , Output --> Used in callbacks for interactivity (dynamic updates)
# load_data() --> Custom function to load & clean retail dataset (present inside data_loader)

# Load the data
df = load_data()
available_countries = sorted(df['Country'].unique()) # Extracts a sorted list of unique countries for use in the dropdown.

# Initialize the Dash App
app = dash.Dash(__name__) # Creates the Dash app object.
app.title = "Retail Dashboard" # Sets the browser tab title to "Retail Dashboard".

# Define the Layout
app.layout = html.Div([                                                         # Main container
    html.H1("Online Retail Dashboard"),                                         # Adds a title heading
    html.Label("Select a Country"),                                             # Adds label text above the dropdown
    dcc.Dropdown(                                                               # A dropdown menu with all countries (populated dynamically)
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in available_countries],
        # value='United Kingdom',
        value=None,
        style={'width': '300px'}
    ),
    dcc.Graph(id='line-chart'),                                                 # Placeholder for line chart
    dcc.Graph(id='bar-chart'),                                                  # Placeholder for bar chart
])

# The ids (country-dropdown, line-chart, bar-chart) are used to link layout elements with interactivity in the callback.

# Set Up Callback for Interactivity :-
# When a country is selected in the dropdown, this callback will:
# Recalculate monthly and top 5 revenue
# Update the line and bar graphs
@app.callback(
    [Output('line-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('country-dropdown', 'value')]
)

# Plot 1 and Plot 2, should be based on selected country
# plot 1 --> line chart -- monthly revenue
# plot 2 --> bar chart -- Top 5 revenue months

def update_chart(selected_country): # Callback Function to Generate Charts
    filtered_df = df[df['Country'] == selected_country] # Filters the dataset to just the selected country

    # Line Chart - Monthly Revenue
    monthly_rev = filtered_df.groupby('Month')['Revenue'].sum().reset_index()
    line_fig = px.line(monthly_rev, 
                       x='Month', 
                       y='Revenue',
                       title=f'Monthly Revenue in {selected_country}',
                       markers=True)
    line_fig.update_layout(xaxis_tickangle=45)
    
    # Bar Chart - Top 5 Revenue Months
    top_months = monthly_rev.sort_values('Revenue', ascending=False).head(5)
    bar_fig = px.bar(top_months, 
                     x='Month', 
                     y='Revenue',
                     title=f'Top 5 Revenue Months in {selected_country}',
                     text='Revenue')
    bar_fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    return line_fig, bar_fig # returned to be shown in the two dcc.Graph components defined in layout.

# Run server : Run the App - > Launches the Dash server (local browser)
if __name__ == '__main__':
    app.run(debug=True) # debug=True auto reloads when you save code changes