import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px


file_path = 'data/src/Financial Sample.xlsx'
df = pd.read_excel(file_path, engine="openpyxl")

df = df.rename(columns={' Sales': 'Sales'})

app = Dash(__name__)
app.title = "Financial Dashboard"

# Aggregate sales by segment
sales_by_segment = df.groupby('Segment')['Sales'].sum().reset_index()

# create the chart
segment_fig = px.bar(
    sales_by_segment,
    x='Segment',
    y='Sales',
    title='Sales By Segment',
    labels={'Sales': 'Total Sales'},
    color='Segment',
    text='Sales'
)

segment_fig.update_layout(showlegend=False)
segment_fig.update_yaxes(tickformat="$,.2f")

# Update hover and text templates for dollar formatting
segment_fig.update_traces(
    texttemplate='%{text:$,.2f}',  # Format text on bars as currency
    hovertemplate='%{y:$,.2f}'  # Format hover labels as currency
)

# Adding the chart to the Dash layout
app.layout = html.Div([
    html.H1("Financial Dashboard"),
    dcc.Graph(id='sales-by-segment', figure=segment_fig),
])



# Aggregate sales by country
sales_by_country = df.groupby('Country')['Sales'].sum().reset_index()

# Create the chart
country_fig = px.bar(
    sales_by_country,
    x='Country',
    y='Sales',
    title='Sales by Country',
    labels={'Sales': 'Total Sales'},
    color='Country'
)
country_fig.update_layout(showlegend=False)
country_fig.update_yaxes(tickformat="$,.2f")  # Format y-axis as currency

# Update hover and text templates for dollar formatting
country_fig.update_traces(
    texttemplate='%{y:$,.2f}',  # Format text on bars as currency
    hovertemplate='%{y:$,.2f}'  # Format hover labels as currency
)

# Update the layout to include both charts
app.layout = html.Div([
    dcc.Graph(id='sales-by-segment', figure=segment_fig),
    dcc.Graph(id='sales-by-country', figure=country_fig)
])


# Aggregate monthly sales
monthly_sales = df.groupby('Month Name')['Sales'].sum().reindex([
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
]).reset_index()

# Create the line chart
monthly_fig = px.line(
    monthly_sales,
    x='Month Name',
    y='Sales',
    title='Monthly Sales Trend',
    labels={'Sales': 'Total Sales'},
    markers=True
)
monthly_fig.update_yaxes(tickformat="$,.2f")  # Format y-axis as currency

# Update hover template for dollar format in hover
monthly_fig.update_traces(
    hovertemplate='%{y:$,.2f}'  # Format hover labels as currency
)

# Define the layout with all charts
app.layout = html.Div([
    dcc.Graph(id='sales-by-segment', figure=segment_fig),
    dcc.Graph(id='sales-by-country', figure=country_fig),
    dcc.Graph(id='monthly-sales-trend', figure=monthly_fig)
])

# Aggregate yearly sales
yearly_sales = df.groupby('Year')['Sales'].sum().reset_index()

# Create the bar chart
yearly_fig = px.bar(
    yearly_sales,
    x='Year',
    y='Sales',
    title='Yearly Sales Growth',
    labels={'Sales': 'Total Sales'},
    text='Sales'
)
yearly_fig.update_yaxes(tickformat="$,.2f")  # Format y-axis as currency

# Update hover and text templates for dollar formatting
yearly_fig.update_traces(
    texttemplate='%{text:$,.2f}',  # Format text on bars as currency
    hovertemplate='%{y:$,.2f}'     # Format hover labels as currency
)

# Define the layout with all charts
app.layout = html.Div([
    dcc.Graph(id='sales-by-segment', figure=segment_fig),
    dcc.Graph(id='sales-by-country', figure=country_fig),
    dcc.Graph(id='monthly-sales-trend', figure=monthly_fig),
    dcc.Graph(id='yearly-sales-growth', figure=yearly_fig)
])

# Calculate gross sales and profit by segment
segment_sales_profit = df.groupby('Segment')[['Gross Sales', 'Profit']].sum().reset_index()

# Create the stacked bar chart
sales_profit_fig = px.bar(
    segment_sales_profit,
    x='Segment',
    y=['Gross Sales', 'Profit'],
    title='Gross Sales vs. Profit by Segment',
    labels={'value': 'Amount', 'variable': 'Metric'},
    text_auto=True  # Automatically adds values on top of bars
)
sales_profit_fig.update_yaxes(tickformat="$,.2f")  # Format y-axis as currency

# Update text and hover templates for correct currency formatting
sales_profit_fig.update_traces(
    texttemplate='%{value:$,.2f}',  # Use value placeholder to format numbers on bars as currency
    hovertemplate='%{y:$,.2f}'      # Format hover labels as currency
)

# Define the layout with all charts
app.layout = html.Div([
    dcc.Graph(id='sales-by-segment', figure=segment_fig),
    dcc.Graph(id='sales-by-country', figure=country_fig),
    dcc.Graph(id='monthly-sales-trend', figure=monthly_fig),
    dcc.Graph(id='yearly-sales-growth', figure=yearly_fig),
    dcc.Graph(id='sales-profit-comparison', figure=sales_profit_fig)
])

# Create scatter plot for discounts vs. sales
discount_sales_fig = px.scatter(
    df,
    x='Discounts',
    y='Sales',
    title='Discount Impact on Sales',
    labels={'Discounts': 'Discount Amount', 'Sales': 'Sales Amount'},
    trendline='ols'
)
discount_sales_fig.update_yaxes(tickformat="$,.2f")  # Format y-axis as currency

# Update hover template for dollar format in hover labels
discount_sales_fig.update_traces(
    hovertemplate='%{y:$,.2f}'  # Format hover labels for Sales as currency
)

# Define the layout with all charts
app.layout = html.Div([
    dcc.Graph(id='sales-by-segment', figure=segment_fig),
    dcc.Graph(id='sales-by-country', figure=country_fig),
    dcc.Graph(id='monthly-sales-trend', figure=monthly_fig),
    dcc.Graph(id='yearly-sales-growth', figure=yearly_fig),
    dcc.Graph(id='sales-profit-comparison', figure=sales_profit_fig),
    dcc.Graph(id='discount-impact', figure=discount_sales_fig)
])

# Aggregate units sold by product and segment
units_sold = df.groupby(['Product', 'Segment'])['Units Sold'].sum().reset_index()

# Create grouped bar chart
units_sold_fig = px.bar(
    units_sold,
    x='Segment',
    y='Units Sold',
    color='Product',
    barmode='group',
    title='Units Sold by Product and Segment'
)

# Optionally, customize hover labels for clarity
units_sold_fig.update_traces(
    hovertemplate='Product: %{color}<br>Units Sold: %{y}'  # Clarify the product and units sold in hover
)

# Define the layout with all charts
app.layout = html.Div([
    dcc.Graph(id='sales-by-segment', figure=segment_fig),
    dcc.Graph(id='sales-by-country', figure=country_fig),
    dcc.Graph(id='monthly-sales-trend', figure=monthly_fig),
    dcc.Graph(id='yearly-sales-growth', figure=yearly_fig),
    dcc.Graph(id='sales-profit-comparison', figure=sales_profit_fig),
    dcc.Graph(id='discount-impact', figure=discount_sales_fig),
    dcc.Graph(id='units-sold', figure=units_sold_fig)
])

# Aggregate monthly sales by year
monthly_sales_year = df.pivot_table(
    index='Month Name',
    columns='Year',
    values='Sales',
    aggfunc='sum'
).reindex([
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
])

# Create heatmap
month_sales_fig = px.imshow(
    monthly_sales_year,
    title='Sales Distribution by Month',
    labels=dict(x="Year", y="Month", color="Sales Amount")
)
month_sales_fig.update_coloraxes(colorbar_tickformat="$,.2f")  # Format color bar as currency

# Define the layout with all charts
app.layout = html.Div([
    dcc.Graph(id='sales-by-segment', figure=segment_fig),
    dcc.Graph(id='sales-by-country', figure=country_fig),
    dcc.Graph(id='monthly-sales-trend', figure=monthly_fig),
    dcc.Graph(id='yearly-sales-growth', figure=yearly_fig),
    dcc.Graph(id='sales-profit-comparison', figure=sales_profit_fig),
    dcc.Graph(id='discount-impact', figure=discount_sales_fig),
    dcc.Graph(id='units-sold', figure=units_sold_fig),
    dcc.Graph(id='sales-distribution', figure=month_sales_fig)
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)