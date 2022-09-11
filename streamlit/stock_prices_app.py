import pandas as pd
import streamlit as st
from pinotdb import connect
from datetime import datetime
import plotly.express as px
import time

st.set_page_config(layout="wide")

conn = connect(host='ec2-44-204-8-116.compute-1.amazonaws.com', port=9000, path='/sql', scheme='http')


# SET DATES AND AUTO REFRESH
now = datetime.now()
dt_string = now.strftime("%d %B %Y %H:%M:%S")
st.sidebar.write(f"Last update: {dt_string}")

if not "sleep_time" in st.session_state:
    st.session_state.sleep_time = 2

if not "auto_refresh" in st.session_state:
    st.session_state.auto_refresh = True

auto_refresh = st.sidebar.checkbox('Auto Refresh?', st.session_state.auto_refresh)

if auto_refresh:
    number = st.sidebar.number_input('Refresh rate in seconds', value=st.session_state.sleep_time)
    st.session_state.sleep_time = number

st.title("Trade Prices Dashboard")

	
# available US companies
tickers = ("BINANCE:BTCUSDT", "AAPL", "MSFT", "AMZN", "META")

# dropdown menu
dropdown = st.multiselect("Pick a US company or cryptocurrency exchange to visualize", tickers)

# date menu - time window -- NOT NEEDED
start = st.date_input("Start", value = pd.to_datetime("2022-01-01"))
end = st.date_input("End", value = pd.to_datetime("today"))

query = """
    select *
    from stockevents
    order by ts desc
    limit 30;
"""

subtract_time = 24*60

curs = conn.cursor()
curs.execute(query, {"subtract_time": subtract_time})
curs.execute(query)

st.header("Trade prices:")

df_ts = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
df_ts_melt = pd.melt(df_ts, id_vars=["ts"], value_vars=["price"])

st.table(df_ts)

st.table(df_ts_melt)

fig = px.line(df_ts_melt, x='ts', y="value", color='variable', color_discrete_sequence =['blue', 'red', 'green'])
fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40), title="Updating trade values.")
fig.update_yaxes(range=[0, df_ts["price"].max() * 1.1])

st.plotly_chart(fig, use_container_width=True)

if auto_refresh:
    time.sleep(number)
    st.experimental_rerun()