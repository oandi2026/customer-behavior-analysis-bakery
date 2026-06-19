# 🥐 Customer Behavior & Product Perception Analysis: Roti ARIES### End-to-End Survey Analytics using SQL & Python.

## 📌 Project OverviewThis project analyzes customer preferences and product perceptions of **Roti ARIES** using survey data collected from 50 respondents in Malang, Indonesia. You can see how this integrates with my wider work on my [oandi2026 GitHub Overview](https://github.com) page.

The main objective is to transform raw survey responses into actionable business insights related to:* **Customer Purchasing Behavior:** Understanding consumer buying habits and triggers.* **Product Perception:** Evaluating the quality, presentation, and characteristics of the product.* **Price Sensitivity:** Assessing consumer acceptance of current pricing structures.* **Marketing Effectiveness:** Identifying which promotional channels drive the most engagement.* **Distribution Channel Performance:** Measuring the efficiency of different sales points.

## 📊 Dataset InformationThe dataset consists of aggregated survey responses measured on a 5-point Likert scale:1. *Strongly Agree*2. *Agree*3. *Don’t Know*4. *Disagree*5. *Strongly Disagree*

Each data entry contains the following schema attributes:
* `question_id`: A unique identifier for each survey question.
* `question_text`: The actual text of the question asked.
* `answer`: The categorical Likert-scale response.
* `count`: The total number of respondents who selected that specific answer.

## 🛠️ Tools & Technologies* **SQL (MySQL / PostgreSQL):** Used for initial data cleaning, transformation, and percentage aggregation.* **Python (Pandas, Matplotlib, Seaborn):** Used for advanced data manipulation, statistical calculations, and data visualization.* **Jupyter Notebook:** Serving as the integrated workspace for the end-to-end analytical workflow.

## 🧹 Data PreparationBefore starting the analysis, the raw survey data went through the following engineering steps:
* Converted raw, unstructured survey responses into a clean `.csv` format.* Standardized categorical string response values for consistency.* Formatted the dataset tables to easily calculate positive response metrics and sentiment trends.

## 🔍 Key Analysis & Insights### 👥 Customer Behavior & Consumption* **Target Audience:** **100%** of customers purchase the bread for family consumption, while **78%** buy it for personal use.* **Breakfast Substitution:** The product has established a very strong market positioning as a breakfast substitute (**72%**).* **Special Occasions:** There is very low purchase intent or relevance for special occasions like parties, ceremonies, lunches, or dinners.

### 🥐 Product Strengths & Perception* **Quality Drivers:** Soft texture (**94%**) and product freshness (**84%**) are the primary catalysts for customer satisfaction.* **Branding:** Brand recognition stands high at **82%**, and the product packaging is perceived as highly attractive by **80%** of respondents.

### 💰 Pricing Insight* **Price Sensitivity:** Only **38%** of respondents expressed positive sentiment toward the current pricing. This indicates a relatively **high price sensitivity** among the consumer base.

### 📣 Marketing & Distribution Channels* **Organic Growth:** Word-of-Mouth (recommendations from family & friends) is by far the most influential marketing channel.* **Traditional Media:** Conventional advertising platforms like radio and magazines are largely ineffective, capturing only an **8%** positive impact.* **Sales Infrastructure:** Mobile bread vendors are the undisputed backbone of distribution, holding a **98%** engagement rate. Conversely, supermarket retail penetration is significantly lagging at **22%**.

## 📊 SQL Query Example*This query aggregates and calculates the exact percentage of positive responses ('Strongly Agree' and 'Agree') for each survey question:*
```sql
SELECT 
    question_text, 
    SUM(CASE WHEN answer IN ('Strongly Agree', 'Agree') THEN count ELSE 0 END) AS positive_count, 
    SUM(count) AS total_count, 
    ROUND(
        SUM(CASE WHEN answer IN ('Strongly Agree', 'Agree') THEN count ELSE 0 END) * 100.0 / SUM(count), 
        2
    ) AS positive_percentage 
FROM customer_survey 
GROUP BY question_text 
ORDER BY positive_percentage DESC;

## 🐍 Python Analysis Example*This script maps the categorical Likert scale to numeric values (1-5) and calculates the Weighted Average Score for each metric:*
```python
import pandas as pd

# Load dataset
df = pd.read_csv("data/customer_survey.csv")

# Map Likert scale categories to numerical weights
score_map = {
    "Strongly Agree": 5, 
    "Agree": 4, 
    "Don't Know": 3, 
    "Disagree": 2, 
    "Strongly Disagree": 1
}
df["score"] = df["answer"].map(score_map)

# Define function to calculate the Weighted Average Score
def weighted_avg(group):
    total_weighted_score = (group["score"] * group["count"]).sum()
    total_respondents = group["count"].sum()
    return total_weighted_score / total_respondents

# Compute scores and sort from highest to lowest
result = df.groupby("question_text").apply(weighted_avg)
print(result.sort_values(ascending=False))

## 💼 Business Recommendations
1. **Community-Focused Marketing:** Direct promotional budgets away from traditional media (radio/magazines) and reallocate them toward word-of-mouth referral programs or localized community marketing.
2. **Double Down on Breakfast Campaigns:** Shape digital marketing narratives around family lifestyle, positioning Roti ARIES as the go-to, fresh morning meal solution.
3. **Optimize Pricing Models:** Introduce promotional bundle deals or launch smaller, more economical portion sizes to counteract the high price sensitivity observed in the market.
4. **Revamp Modern Retail Strategy:** Evaluate the supply chain, product shelf positioning, and profit margins within supermarkets to improve the low performance (**22%**) in modern trade channels.
5. **Protect Core Strengths:** Maintain strict quality control protocols regarding product freshness and softness, as these form your primary *Unique Selling Proposition* (USP).

---## 👨‍💻 Author* **Oktafiandi Wibisono*** *Aspiring Data Analyst*
* **GitHub Profile:** [oandi2026](https://github.com)
