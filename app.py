import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Bakery Likert Survey Analysis")

url = "https://docs.google.com/spreadsheets/d/1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM/edit?gid=0#gid=0"

try:
    df = pd.read_csv(url)

    likert_order = [
        "Strongly Agree",
        "Agree",
        "Don't Know",
        "Disagree",
        "Strongly Disagree"
    ]
    df['ANSWER'] = pd.Categorical(df['ANSWER'], categories=likert_order, ordered=True)

    df_bar = df.groupby('ANSWER', observed=False)['COUNT'].sum().reset_index()

    fig = px.bar(
        df_bar,
        x="ANSWER",
        y="COUNT",
        color="ANSWER",
        title="Total Distribution of Responses",
        text="COUNT"
    )

    fig.update_layout(
        xaxis_title="Skala Respon",
        yaxis_title="Total Count"
    )
    st.plotly_chart(fig, use_container_width=True)
