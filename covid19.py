import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    data = pd.read_csv(url)
    return data

data = load_data()

countries = st.multiselect(
    "Escolha os países", list(data["Country/Region"].unique()), ["Brazil", "US"]
)


filtered_data = data[data["Country/Region"].isin(countries)]
filtered_data = filtered_data.groupby("Country/Region").sum().reset_index()


filtered_data = filtered_data.melt(id_vars=["Country/Region"], var_name="Date", value_name="Confirmed Cases")
filtered_data["Date"] = pd.to_datetime(filtered_data["Date"])


fig = px.bar(
    filtered_data, 
    x="Country/Region", 
    y="Confirmed Cases", 
    color="Country/Region",
    labels={"Confirmed Cases": "Casos Confirmados", "Country/Region": "Países"}
)


fig.update_layout(
    title="Casos Confirmados de COVID-19 por País",
    xaxis_title="Países",
    yaxis_title="Casos Confirmados",
    xaxis={'categoryorder':'total descending'}
)


st.plotly_chart(fig)
