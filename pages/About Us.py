import pandas
import streamlit as st
import pandas as pd

st.title('Tips Data Table')
data = pandas.read_csv("tips (1).csv")
st.table(data)
