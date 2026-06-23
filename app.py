import pandas as pd 
import plotly.express as px 
import streamlit as st 

st.title("📊 Bakery Customer Behavior Analysis") 

# 1. Correct URL format for CSV export (using gviz/tq endpoint)
sheet_id = "1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

df = pd.read_csv(url) 

# 2. Clean and convert column names to uppercase
df.columns = [c.strip().upper() for c in df.columns] 

df["ANSWER"] = df["ANSWER"].astype(str).str.strip() 
df["COUNT"] = pd.to_numeric(df["COUNT"], errors="coerce") 
df = df.dropna(subset=["ANSWER", "COUNT"]) 

st.write("DATA LOADED:", df.shape) 

# 3. Filter data based on Sidebar selection
list_question = df["QUESTION TEXT"].unique() 
pilihan_pertanyaan = st.sidebar.selectbox("Select Question:", list_question) 

df_filtered = df[df["QUESTION TEXT"] == pilihan_pertanyaan] 

# 4. Group filtered data 
df_bar = df_filtered.groupby("ANSWER")["COUNT"].sum().reset_index() 
order = ["Strongly Agree", "Agree", "Don't Know", "Disagree", "Strongly Disagree"] 
df_bar["ANSWER"] = pd.Categorical(df_bar["ANSWER"], categories=order, ordered=True) 
df_bar = df_bar.sort_values("ANSWER") 

st.write(f"DATA FOR: {pilihan_pertanyaan}", df_bar) 

# 5. Generate Chart
fig = px.bar( 
    df_bar, 
    x="ANSWER", 
    y="COUNT", 
    text="COUNT", 
    title=f"Distribution of Responses for: {pilihan_pertanyaan}", 
    color="ANSWER", 
    color_discrete_sequence=px.colors.qualitative.Pastel 
) 

fig.update_traces(textposition='inside') 
fig.update_layout(xaxis_title="Responses", yaxis_title="Total Count") 

st.plotly_chart(fig, use_container_width=True)
