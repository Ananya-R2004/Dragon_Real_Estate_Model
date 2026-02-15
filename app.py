# Import the necessary Dash libraries and components
import dash
from dash import Dash, dcc, html, dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import numpy as np
from dash.dependencies import Input, Output, State

# Load the data from the CSV file
df = pd.read_csv('Predicted_Data.csv')
# Convert 'CHAS' to string for proper filtering
df['CHAS'] = df['CHAS'].astype(str)

# The filter options for RAD are discrete, so we should handle them differently.
rad_options = [{'label': str(i), 'value': str(i)} for i in sorted(df['RAD'].unique())]

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# --- App Layout ---
app.layout = dbc.Container(
    fluid=True,
    children=[
        
        html.Div(
            style={"backgroundColor": "#2c3e50", "color": "white", "padding": "2rem"},
            children=[
                dbc.Row([
                    dbc.Col(
                        
                        html.Img(src="/assets/logo.png", style={"width": "120px", "borderRadius": "50%"}),
                        width="auto",
                        className="d-flex align-items-center"
                    ),
                    dbc.Col(
                        html.Div([
                            html.H1("Dragon Real Estate Analysis", className="display-4"),
                            html.P("Unlocking insights from real estate data to predict home values and neighborhood trends.", className="lead"),
                        ]),
                        className="ms-3 text-start"
                    )
                ], className="d-flex justify-content-start align-items-center"),
            ]
        ),
        html.Div(className="mt-2 text-center text-muted", children=[
            html.Span("Data Updated: 2025-08-07"),
            html.Span(" | "),
            html.Span("Data Source: Dragon Real Estate Analysis data")
        ]),

        # Filters and Data Cards Section
        dbc.Row(className='mt-4', children=[
            # Filters Column (on the left)
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4('Filters', className='card-title'),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col(html.Label('Crime Rate (CRIM)'), width=6),
                            dbc.Col(html.Label('Predicted Price Range ($1000s)'), width=6)
                        ]),
                        dbc.Row([
                            dbc.Col(dcc.RangeSlider(id='crime-rate-slider', min=df['CRIM'].min(), max=df['CRIM'].max(), value=[df['CRIM'].min(), df['CRIM'].max()], tooltip={"placement": "bottom", "always_visible": True}), width=6),
                            dbc.Col(dcc.RangeSlider(id='price-range-slider', min=df['PredictedPrice'].min(), max=df['PredictedPrice'].max(), value=[df['PredictedPrice'].min(), df['PredictedPrice'].max()], tooltip={"placement": "bottom", "always_visible": True}), width=6)
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(html.Label('Average Rooms (RM)'), width=6),
                            dbc.Col(html.Label('Lower Status Population (%) (LSTAT)'), width=6)
                        ]),
                        dbc.Row([
                            dbc.Col(dcc.RangeSlider(id='rooms-slider', min=df['RM'].min(), max=df['RM'].max(), value=[df['RM'].min(), df['RM'].max()], tooltip={"placement": "bottom", "always_visible": True}), width=6),
                            dbc.Col(dcc.RangeSlider(id='lstat-slider', min=df['LSTAT'].min(), max=df['LSTAT'].max(), value=[df['LSTAT'].min(), df['LSTAT'].max()], tooltip={"placement": "bottom", "always_visible": True}), width=6)
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(html.Label('Property Tax Rate (TAX)'), width=6),
                            dbc.Col(html.Label('Nitric Oxide Concentration (NOX)'), width=6)
                        ]),
                        dbc.Row([
                            dbc.Col(dcc.RangeSlider(id='tax-slider', min=df['TAX'].min(), max=df['TAX'].max(), value=[df['TAX'].min(), df['TAX'].max()], tooltip={"placement": "bottom", "always_visible": True}), width=6),
                            dbc.Col(dcc.RangeSlider(id='nox-slider', min=df['NOX'].min(), max=df['NOX'].max(), value=[df['NOX'].min(), df['NOX'].max()], tooltip={"placement": "bottom", "always_visible": True}), width=6)
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(html.Label('Pupil-Teacher Ratio (PTRATIO)'), width=6),
                            dbc.Col(html.Label('Residential Land Zoning (ZN)'), width=6)
                        ]),
                        dbc.Row([
                            dbc.Col(dcc.RangeSlider(id='ptratio-slider', min=df['PTRATIO'].min(), max=df['PTRATIO'].max(), value=[df['PTRATIO'].min(), df['PTRATIO'].max()], tooltip={"placement": "bottom", "always_visible": True}), width=6),
                            dbc.Col(dcc.RangeSlider(id='zn-slider', min=df['ZN'].min(), max=df['ZN'].max(), value=[df['ZN'].min(), df['ZN'].max()], tooltip={"placement": "bottom", "always_visible": True}), width=6)
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(html.Label('Charles River Proximity (CHAS)'), width=6),
                            dbc.Col(html.Label('Radial Highway Accessibility (RAD)'), width=6)
                        ]),
                        dbc.Row([
                            dbc.Col(dcc.Checklist(id='chas-checklist', options=[{'label': 'Yes (1)', 'value': '1'}, {'label': 'No (0)', 'value': '0'}], value=['0', '1'], inline=True), width=6),
                            dbc.Col(dcc.Dropdown(id='rad-dropdown', options=rad_options, value=[str(i) for i in sorted(df['RAD'].unique())], multi=True), width=6)
                        ]),
                    ])
                ), md=4
            ),

            # Data Cards Column
            dbc.Col(
                html.Div(children=[
                    # First row of data cards
                    dbc.Row(className='g-2', children=[
                        dbc.Col(dbc.Card(dbc.CardBody([html.H5('Total Properties'), html.H2(id='total-properties')]))),
                        dbc.Col(dbc.Card(dbc.CardBody([html.H5('Average Price ($1000s)'), html.H2(id='avg-price')]))),
                        dbc.Col(dbc.Card(dbc.CardBody([html.H5('Maximum Price ($1000s)'), html.H2(id='max-price')]))),
                        dbc.Col(dbc.Card(dbc.CardBody([html.H5('Minimum Price ($1000s)'), html.H2(id='min-price')]))),
                        dbc.Col(dbc.Card(dbc.CardBody([html.H5('Average Rooms'), html.H2(id='avg-rooms')]))),
                    ]),
                    # Second row of data cards
                    dbc.Row(className='g-2 mt-2', children=[
                        dbc.Col(dbc.Card(dbc.CardBody([html.H5('Avg Distance'), html.H2(id='avg-dis')]))),
                        dbc.Col(dbc.Card(dbc.CardBody([html.H5('Avg Tax Rate'), html.H2(id='avg-tax')]))),
                        dbc.Col(dbc.Card(dbc.CardBody([html.H5('Avg Pupil-Teacher Ratio'), html.H2(id='avg-ptratio')]))),
                        dbc.Col(dbc.Card(dbc.CardBody([html.H5('Avg NOX'), html.H2(id='avg-nox')]))),
                    ]),
                    # New row for the AI card
                    dbc.Row(className='g-2 mt-2', children=[
                        dbc.Col(
                            dbc.Card(dbc.CardBody([
                                html.H5('Model Details', style={'color':'#6c757d'}, className="fw-bold"),
                                html.P('Built by Ananya R', style={'fontSize': '0.8em'}),
                                html.P('Model: Dragon Real Estate Predictor', style={'fontSize': '0.8em'}),
                                html.Hr(),
                                html.P('Accurate. Transparent. Explainable.', style={'fontSize': '0.75em'}),
                                html.P('Not just predictions -clarity backed by data science.', style={'fontSize': '0.75em'}),
                                html.P('Developed with precision by Ananya R.', style={'fontSize': '0.75em'}),
                                html.P('Transforming patterns into property insights.', style={'fontSize': '0.75em'}),
                                html.P('Every feature counts. Every value tells a story.', style={'fontSize': '0.75em'}),
                            ]), className="h-100 align-self-center shadow-sm"),
                        ),
                    ]),
                ]), md=8
            )
        ]),

        # Charts Section
        dbc.Row(className='mt-4', children=[
            dbc.Col(dcc.Graph(id='price-vs-rooms-scatter'), md=6),
            dbc.Col(dcc.Graph(id='crime-rate-histogram'), md=6),
        ]),
        dbc.Row(className='mt-4', children=[
            dbc.Col(dcc.Graph(id='correlation-heatmap'), width=12),
        ]),
        dbc.Row(className='mt-4', children=[
            dbc.Col(dcc.Graph(id='neighborhood-boxplot'), md=6),
            dbc.Col(dcc.Graph(id='price-vs-distance-line'), md=6),
        ]),
        dbc.Row(className='mt-4', children=[
            dbc.Col(dcc.Graph(id='age-vs-price-scatter'), md=6),
            dbc.Col(dcc.Graph(id='predicted-price-bubble'), md=6)
        ]),
        dbc.Row(className='mt-4', children=[
            dbc.Col(dcc.Graph(id='price-distribution-histogram'), width=12),
        ]),

        # Data Table Section
        dbc.Row(className='mt-4', children=[
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H2('Data Table View'),
                        # Use dash_ag_grid instead of the basic dash_table for better features
                        dag.AgGrid(
                            id="data_table_grid",
                            columnDefs=[],
                            rowData=[],
                            dashGridOptions={
                                "pagination": True,
                                "paginationPageSize": 10,
                                "domLayout": "normal",
                                "defaultColDef": {
                                    "sortable": True,
                                    "filter": True,
                                    "resizable": True,
                                    "floatingFilter": True
                                }
                            },
                            style={'height': 400}
                        )
                    ])
                ),
                width=12
            )
        ])
    ]
)

# --- App Callbacks ---
@app.callback(
    [Output('price-vs-rooms-scatter', 'figure'),
     Output('crime-rate-histogram', 'figure'),
     Output('correlation-heatmap', 'figure'),
     Output('neighborhood-boxplot', 'figure'),
     Output('price-vs-distance-line', 'figure'),
     Output('age-vs-price-scatter', 'figure'),
     Output('predicted-price-bubble', 'figure'),
     Output('price-distribution-histogram', 'figure'),
     Output('data_table_grid', 'columnDefs'),
     Output('data_table_grid', 'rowData'),
     Output('total-properties', 'children'),
     Output('avg-price', 'children'),
     Output('max-price', 'children'),
     Output('min-price', 'children'),
     Output('avg-rooms', 'children'),
     # Outputs for the second row of data cards
     Output('avg-dis', 'children'),
     Output('avg-tax', 'children'),
     Output('avg-ptratio', 'children'),
     Output('avg-nox', 'children')],
    [Input('crime-rate-slider', 'value'),
     Input('price-range-slider', 'value'),
     Input('rooms-slider', 'value'),
     Input('lstat-slider', 'value'),
     Input('chas-checklist', 'value'),
     Input('tax-slider', 'value'),
     Input('nox-slider', 'value'),
     Input('ptratio-slider', 'value'),
     Input('zn-slider', 'value'),
     Input('rad-dropdown', 'value')]
)
def update_dashboard(crime_range, price_range, rooms_range, lstat_range, chas_values, tax_range, nox_range, ptratio_range, zn_range, rad_values):
    # Start with the full dataframe
    filtered_df = df

    # Apply range filters
    filtered_df = filtered_df[
        (filtered_df['CRIM'] >= crime_range[0]) & (filtered_df['CRIM'] <= crime_range[1]) &
        (filtered_df['PredictedPrice'] >= price_range[0]) & (filtered_df['PredictedPrice'] <= price_range[1]) &
        (filtered_df['RM'] >= rooms_range[0]) & (filtered_df['RM'] <= rooms_range[1]) &
        (filtered_df['LSTAT'] >= lstat_range[0]) & (filtered_df['LSTAT'] <= lstat_range[1]) &
        (filtered_df['TAX'] >= tax_range[0]) & (filtered_df['TAX'] <= tax_range[1]) &
        (filtered_df['NOX'] >= nox_range[0]) & (filtered_df['NOX'] <= nox_range[1]) &
        (filtered_df['PTRATIO'] >= ptratio_range[0]) & (filtered_df['PTRATIO'] <= ptratio_range[1]) &
        (filtered_df['ZN'] >= zn_range[0]) & (filtered_df['ZN'] <= zn_range[1])
    ]

    # Apply checklist and dropdown filters only if they are not empty
    if chas_values:
        filtered_df = filtered_df[filtered_df['CHAS'].isin(chas_values)]

    if rad_values:
        filtered_df = filtered_df[filtered_df['RAD'].astype(str).isin(rad_values)]

    # Update Data Cards (handles empty dataframe gracefully)
    if not filtered_df.empty:
        total_properties = len(filtered_df)
        avg_price = f"${filtered_df['PredictedPrice'].mean():.2f}K"
        max_price = f"${filtered_df['PredictedPrice'].max():.2f}K"
        min_price = f"${filtered_df['PredictedPrice'].min():.2f}K"
        avg_rooms = f"{filtered_df['RM'].mean():.2f}"
        # New metrics
        avg_dis = f"{filtered_df['DIS'].mean():.2f}"
        avg_tax = f"{filtered_df['TAX'].mean():.2f}"
        avg_ptratio = f"{filtered_df['PTRATIO'].mean():.2f}"
        avg_nox = f"{filtered_df['NOX'].mean():.3f}"
    else:
        total_properties = 0
        avg_price = "$0.00K"
        max_price = "$0.00K"
        min_price = "$0.00K"
        avg_rooms = "0.00"
        # New metrics
        avg_dis = "0.00"
        avg_tax = "0.00"
        avg_ptratio = "0.00"
        avg_nox = "0.000"

    # Generate figures for each chart (Plotly handles empty dataframes gracefully)
    fig1 = px.scatter(filtered_df, x='RM', y='PredictedPrice', title='Predicted Price vs. Average Rooms')
    fig2 = px.histogram(filtered_df, x='CRIM', title='Crime Rate Distribution')

    # Heatmap requires at least 2 dimensions to correlate
    if len(filtered_df.columns) > 1 and not filtered_df.empty:
        corr_matrix = filtered_df.select_dtypes(include=['number']).corr()
        fig3 = px.imshow(corr_matrix, text_auto=True, title='Correlation Heatmap')
    else:
        fig3 = {}

    fig4 = px.box(filtered_df, y='PredictedPrice', x='CHAS', color='CHAS', title='Neighborhood characteristics boxplot (Price by Charles River Proximity)')
    fig5 = px.line(filtered_df, x='DIS', y='PredictedPrice', title='Predicted Prices by Distance to Employment Centers')
    fig6 = px.scatter(filtered_df, x='AGE', y='PredictedPrice', title='Housing Age vs. Predicted Price')
    fig7 = px.scatter(
        filtered_df,
        x='DIS',
        y='PredictedPrice',
        size='RM',
        color='TAX',
        hover_name='INDUS',
        title='Predicted Price Bubble Chart'
    )
    fig8 = px.histogram(filtered_df, x='PredictedPrice', nbins=50, title='Predicted Price Distribution')

    # Prepare data for Ag-Grid
    column_defs = [{"field": col} for col in filtered_df.columns]
    row_data = filtered_df.to_dict('records')

    # Return all outputs
    return (
        fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8,
        column_defs, row_data,
        total_properties,
        avg_price,
        max_price,
        min_price,
        avg_rooms,
        # Return the new metrics
        avg_dis,
        avg_tax,
        avg_ptratio,
        avg_nox
    )

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)

