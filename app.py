import pandas as pd
import plotly.express as px
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="Bakery Consumer Insights Dashboard", layout="wide")
st.title("🍞 Bakery Consumer Insights & Market Basket Analysis")
st.markdown("Interactive dashboard built from survey data and text-mined customer associations.")


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


# =========================
# INSIGHT MAPPING
# =========================
insights = {
    "1a": """Based on the distribution data above, it is evident that personal consumption is the primary driver for most buyers. This trend aligns with observations showing that affordable filled breads—particularly cheese and chocolate buns—are highly favored by consumers. Because these products are both highly sought-after and profitable, increasing their production capacity is strongly recommended to maximize revenue""",
    "1b": """Based on the calculation results above, it can be stated that all respondents consume bread with their families. Consumers eat plain bread in the morning as a rice substitute together, which presents an opportunity for companies to offer plain bread in various variations. Examples include family sizes, oval or rectangular shapes, varying densities, and different toppings or spreads like a sprinkle of sesame seeds, butter, and so on.""",
    "1c": """Respondents also purchase bread to serve to personal guests, ranking fourth after family consumption, personal consumption, and gifting. To increase sales in this segment, the company should offer more visually appealing and presentable products, such as adding decorative toppings like sweets or cherries.""",
    "1d": """The chart shows that many respondents rarely purchase bread for parties. Although the bakery offers custom products such as cakes, low awareness—likely due to limited advertising—reduces demand. Increasing promotion could help customers better recognize these offerings.""",
    "1e": """Almost all consumers do not use bread for ritual purposes, suggesting that bread products are primarily associated with everyday consumption rather than ceremonial use.""",
    "1f": """Consumers also buy bread as souvenirs (gifts). The reason for purchasing bread as a souvenir ranks third, following the reasons for family consumption and personal consumption purposes (buy for myself. To optimize bread sales for both souvenir and personal consumption purposes, the company should enhance the packaging, for example, by using attractive cardboard boxes designed in the shape of miniature houses with a handle hole on the top side.""",
    "1g": """According to the chart, some respondents consume bread as a snack, which represents the fifth reason for purchasing bread.""",
    "1h1": """From the chart above, it can be said that respondents really enjoy eating bread as a substitute for rice in the morning.""",
    "1h2": """Respondents show a low preference for consuming bread as rice substitute during lunch""",
    "1h3": """Respondents dislike consuming bread as a rice substitute during the evening. Furthermore, respondent critique indicates that traditional moist cakes (kue basah) are less palatable in the evening due to a lack of freshness.""",
    "1h4": """Respondents dislike consuming bread as a rice substitute during the night.""",
    "2a" : """Consumers prefer thick plastic packaging. With thick plastic packaging, which effectively prevents product damage and will last longer.""",
    "2b" : """Consumers prefer packaging with various patterns. Therefore, the bread company should increase the wrapping patterns from one type to various types, for example, the color brown for chocolate bread and the color red for white bread.""",
     "2c" : """Consumers prefer packaging with attractive shapes; for that reason, the bread company should use appealing packaging, for example, house-shaped cardboard boxes that have handles.""",
     "3" : """It can be concluded that the bakery has successfully established strong brand recognition among the public.""",
     "4": """"Respondents strongly believe that the bread is always fresh ('fresh from the oven')""",
     "5": """Respondents favor the bread due to its consistent baking quality, being well baked without becoming overcooked or burnt.""",
     "6": """The chart shows that respondents perceive the bread as soft, but in some cases too soft and lacking density, indicating an opportunity to improve texture by increasing firmness.""",
     "7": """Based on the chart, the bread is considered less dense, and this perception is reinforced by consumers’ frequent purchasing experience, allowing them to clearly identify the texture issue.""",
     "8": """Based on the survey findings, the range of bread varieties offered is adequate to satisfy consumer preferences, reflecting strong product diversity.""",
     "9": """Consumers perceive the bread pricing as reasonable, indicating strong price acceptability.""",
    "10a": """Data shows family is the primary awareness driver. This connection directly influences buying habits, specifically for family requests, party catering, and as a main meal substitute.""",
    "10b": """The results indicate that, in addition to other sources, friends also contribute to respondents’ awareness of this bread.""",
    "10c": """Based on the results above, respondents stated that they have never heard radio advertisements for the bread. Therefore, it is recommended that the company promote its products through private radio advertising. This promotion is expected to highlight the product’s uniqueness or differences. Although there may be no significant physical differences, effective promotion can create perceived psychological differences among consumers.""",
    "10d": """Based on the results above, respondents stated that they have never seen bread advertisements in magazines. It is recommended that the company promote its products through magazines and newspapers to increase visibility.""",
"11a": """Based on the results above, respondents generally purchase bread from mobile bread vendor. Therefore, it is recommended that the company support and train its vendors to ensure they provide satisfactory service to consumers.""",
"11b": """The results indicate that respondents sometimes buy bread from shops. Given the company’s strong brand, product quality, variety, affordable pricing, and loyal customers, it is recommended to expand distribution through retail shops to strengthen market reach amid competition.""",
"11c": """Based on the results above, respondents stated that they never purchase bread from supermarkets. It is recommended that the company also utilize supermarkets as a distribution channel.""",
"12": """Based on the results above, the bread is considered easy to obtain. This finding can be linked to question 11.a, where almost all respondents stated that they purchase bread from street vendors.""",    
"13": """Most respondents are loyal customers, with the majority selecting “Strongly Agree” and “Agree,” showing high satisfaction and strong repeat purchase behavior.""",
"14": """From the high number of frequently purchased types of bread, the author concludes that bread is increasingly being consumed as a substitute for rice, especially white bread and filled bread."""
    
}

# 3. Filter data based on Sidebar selection
list_question = df["QUESTION TEXT"].unique()
selected_question = st.sidebar.selectbox("Select Question:", list_question)
df_filtered = df[df["QUESTION TEXT"] == selected_question]

# 4. Group filtered data
df_bar = df_filtered.groupby("ANSWER")["COUNT"].sum().reset_index()
order = ["Strongly Agree", "Agree", "Don't Know", "Disagree", "Strongly Disagree"]
df_bar["ANSWER"] = pd.Categorical(df_bar["ANSWER"], categories=order, ordered=True)
df_bar = df_bar.sort_values("ANSWER")

st.write(f"DATA FOR: {selected_question}", df_bar)

# 5. Generate and Display Chart
fig = px.bar(
    df_bar,
    x="ANSWER",
    y="COUNT",
    text="COUNT",
    title=f"Distribution of Responses for: {selected_question}",
    color="ANSWER",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig.update_traces(textposition='inside')
fig.update_layout(xaxis_title="Responses", yaxis_title="Total Count")
st.plotly_chart(fig, use_container_width=True)

# 6. Display Analysis Insight Automatically (FIXED LOGIC)
selected_insight = None

if not df_filtered.empty and "QUESTION ID" in df_filtered.columns:
    # 1. Look up the actual ID (e.g., '1a') matching the chosen text
    current_id = str(df_filtered["QUESTION ID"].iloc[0]).strip().lower()
    
    # 2. Match the cleaned ID directly against the dictionary keys
    for key, insight_text in insights.items():
        if key.lower().strip() == current_id:
            selected_insight = insight_text
            break

if selected_insight:
    st.subheader("💡 Analysis Insight")
    st.info(selected_insight)
else:
    st.subheader("💡 Analysis Insight")
    st.caption("No specific insight mapped for this question format.")

# --- THE ANALYSIS ENGINE ---
keywords = {
    'Product': ['plain bread', 'white bread', 'filled bread', 'cheese bun', 'chocolate bun', 'cake', 'moist cake'],
    'Occasion': ['morning', 'breakfast', 'snack', 'personal consumption', 'family', 'guest', 'gift', 'souvenir', 'party'],
    'Packaging & Features': ['thick plastic', 'cardboard box', 'house-shaped', 'handle', 'topping', 'spread', 'fresh', 'soft', 'dense'],
    'Channel': ['mobile vendor', 'street vendor', 'shop', 'retail', 'supermarket']
}

connections = []
for code, text in insights.items():
    text_lower = text.lower()
    found_nodes = {}
    for category, words in keywords.items():
        for word in words:
            if word in text_lower:
                found_nodes[word.title()] = category
                
    node_list = list(found_nodes.items())
    for i in range(len(node_list)):
        for j in range(i + 1, len(node_list)):
            node_a, cat_a = node_list[i]
            node_b, cat_b = node_list[j]
            if cat_a != cat_b: 
                connections.append((node_a, node_b))

G = nx.Graph()
G.add_edges_from(connections)

color_map = []
for node in G:
    node_lower = node.lower()
    if any(w in node_lower for w in keywords['Product']): color_map.append('#ff9999')
    elif any(w in node_lower for w in keywords['Occasion']): color_map.append('#99ff99')
    elif any(w in node_lower for w in keywords['Packaging & Features']): color_map.append('#99ccff')
    else: color_map.append('#ffcc99')

# --- DISPLAY LAYOUT (Side-by-Side) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 🕸️ Consumer Insights Association Map")
    fig, ax = plt.subplots(figsize=(10, 7))
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color=color_map, alpha=0.9, ax=ax)
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.6, edge_color='gray', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', ax=ax)
    plt.axis('off')
    st.pyplot(fig)

with col2:
    st.write("### 📋 Executive Business Recommendations")
    st.markdown("""
    **1. The Family Breakfast Bundle**
    * Target: Morning plain bread buyers.
    * Strategy: Cross-sell with spreads and toppings.
    
    **2. Premium Gifting Options**
    * Target: Souvenir and guest-serving segments.
    * Strategy: Introduce house-shaped boxes with handles.
    
    **3. Flavor-Coded Packaging**
    * Target: Chocolate and white bread buyers.
    * Strategy: Transition to thick plastic with specific color accents (brown/red).
    """)

st.write("### 🔍 Raw Association Strength Table")
df_assoc = pd.DataFrame(connections, columns=['Item A', 'Item B'])
df_rules = df_assoc.groupby(['Item A', 'Item B']).size().reset_index(name='Strength Count')
st.dataframe(df_rules.sort_values(by='Strength Count', ascending=False), use_container_width=True)



