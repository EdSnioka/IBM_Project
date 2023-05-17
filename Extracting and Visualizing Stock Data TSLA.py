# %%
import yfinance as yf
import pandas as pd
import requests
import html5lib
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from plotly.subplots import make_subplots


### Working with Tesla Ticker

tesla = yf.Ticker("TSLA")

data = tesla.history(period="max")

tesla_data = pd.DataFrame(data)

tesla_data.reset_index(inplace=True)

#print(tesla_data.head())

###______________________________________

### Webscraping to extract tesla revenue data

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'

html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html5lib')

tesla_revenue = {'Date':[], 'Revenue':[]}

for row in soup.find("tbody").find_all('tr')[1:]:
    col = row.find_all('td')
    date = col[0].text
    revenue = col[1].text

    tesla_revenue['Date'].append(date)
    tesla_revenue['Revenue'].append(revenue)
df_tesla_revenue = pd.DataFrame(tesla_revenue)

# Execute the following line to remove the comma and dollar sign from the Revenue column.

df_tesla_revenue["Revenue"] = df_tesla_revenue['Revenue'].str.replace('$', "")
df_tesla_revenue["Revenue"] = df_tesla_revenue['Revenue'].str.replace(',', "")
df_tesla_revenue["Revenue"] = df_tesla_revenue['Revenue'].str.replace('|', "")


# Execute the following lines to remove an null or empty strings in the Revenue column.

df_tesla_revenue.dropna(inplace=True)

df_tesla_revenue = df_tesla_revenue[df_tesla_revenue['Revenue'] != ""]

### revenue_tesla = df_tesla_revenue['Revenue']

### print(df_tesla_revenue['Revenue'].tail(5))

# df_tesla_revenue['Revenue'] = pd.to_numeric(df_tesla_revenue['Revenue'], errors='coerce')

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
make_graph(tesla_data, df_tesla_revenue,'TSLA')


### Finish Q 5-6 of Extracting and Visualizing Stock Data

    



# %%
