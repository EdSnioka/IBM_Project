# %%
import yfinance as yf
import pandas as pd
import requests
import html5lib
from bs4 import BeautifulSoup
from plotly import graph_objects as go
from plotly.subplots import make_subplots


### GME TICKER
gme = yf.Ticker("GME")

gme_data = gme.history(period="max")
df_gme_data = pd.DataFrame(gme_data)
df_gme_data.reset_index(inplace=True)
print("First 5 rows of gme data", df_gme_data.head())

### GME wbescraping to extract GME Revenue Data

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'

html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html5lib')

gme_data = {"Date":[],"Revenue":[]}

tbody = soup.find_all("tbody")[1]

for row in tbody.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text

    gme_data["Date"].append(date)
    gme_data['Revenue'].append(revenue)
    df_gme = pd.DataFrame(gme_data)

df_gme["Revenue"] = df_gme['Revenue'].str.replace('$', "")
df_gme["Revenue"] = df_gme['Revenue'].str.replace(',', "")
df_gme["Revenue"] = df_gme['Revenue'].str.replace('|', "")


# Execute the following lines to remove  null or empty strings in the Revenue column.

df_gme.dropna(inplace=True)

df_gme = df_gme[df_gme['Revenue'] != ""]

print("tail\n",df_gme['Revenue'].tail(5))


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

make_graph(df_gme_data, df_gme, 'GME')

# %%
