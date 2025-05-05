import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Generate a large synthetic dataset
data = {
    'Date': pd.date_range(start='1/1/2021', periods=1000, freq='D'),
    'Sales': [150 + i for i in range(1000)],
    'Region': ['North', 'South', 'East', 'West'] * 250,
    'Product': ['Product A', 'Product B', 'Product C', 'Product D'] * 250
}

df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Advanced Sales Dashboard"),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in df['Region'].unique()],
        value='North',
        multi=False,
        clearable=False
    ),
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': product, 'value': product} for product in df['Product'].unique()],
        value='Product A',
        multi=False,
        clearable=False
    ),
    dcc.Graph(id='sales-line-chart'),
    dcc.Graph(id='sales-bar-chart')
])

# Callback to update the line chart
@app.callback(
    Output('sales-line-chart', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('product-dropdown', 'value')]
)
def update_line_chart(selected_region, selected_product):
    filtered_df = df[(df['Region'] == selected_region) & (df['Product'] == selected_product)]
    fig = px.line(filtered_df, x='Date', y='Sales', title=f'Sales Over Time for {selected_product} in {selected_region}')
    return fig

# Callback to update the bar chart
@app.callback(
    Output('sales-bar-chart', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('product-dropdown', 'value')]
)
def update_bar_chart(selected_region, selected_product):
    filtered_df = df[(df['Region'] == selected_region) & (df['Product'] == selected_product)]
    fig = px.bar(filtered_df, x='Date', y='Sales', title=f'Daily Sales for {selected_product} in {selected_region}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
