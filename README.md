Customer Behavior & Product Perception Analysis

Roti ARIES Survey (SQL + Python)

Project Overview

This project analyzes customer preferences and perceptions of Roti ARIES using survey data from 50 respondents in Malang, Indonesia.

The objective is to transform raw survey data into actionable business insights related to:

* Customer buying behavior
* Product perception
* Pricing sensitivity
* Marketing effectiveness
* Distribution channels

Dataset

The dataset contains aggregated survey responses using a 5-point Likert scale:

* Strongly Agree
* Agree
* Don’t Know
* Disagree
* Strongly Disagree

Each record includes:

* question_id
* question_text
* answer
* count (number of respondents)

Tools & Technologies

* SQL (MySQL / PostgreSQL) → Data aggregation & analysis
* Python (Pandas, Matplotlib) → Data processing & visualization
* Jupyter Notebook → End-to-end workflow

Data Preparation

* Converted survey into structured CSV format
* Standardized categorical responses
* Prepared dataset for aggregation and sentiment analysis

Key Analysis & Insights

Customer Behavior

* Customers primarily purchase for family (100%) and personal use (78%)
* Low demand for events such as parties and ceremonies

Product Strengths

* Soft texture (94%) and freshness (84%) are the strongest drivers
* Brand recognition (82%) and attractive packaging (80%) are highly valued

Consumption Pattern

* Strong positioning as a breakfast substitute (72%)
* Weak relevance for lunch/dinner occasions

Pricing Insight

* Only 38% positive sentiment toward price
    → Indicates high price sensitivity

Marketing Effectiveness

* Word-of-mouth (family & friends) is dominant
* Radio & magazine ads (8%) are ineffective

Distribution Channels

* Mobile bread vendors (98%) are the strongest channel
* Supermarkets show very weak engagement (22%)

SQL Analysis Example

# Customer Behavior Analysis - Bakery Dataset

This repository contains a comprehensive data analysis of consumer purchasing habits, preferences, and behavioral triggers for a bakery business model. The insights generated aim to help stakeholders optimize product offerings, improve marketing strategies, and enhance customer retention.

## 📊 Key Findings & Customer Insights

Understanding why customers choose specific bakery products is critical to predicting demand. The visualization below breaks down the primary consumer behavior drivers and sentiment distributions:

![Customer Purchase Drivers](customer_purchase_drivers.png)

### 🔑 Core Takeaways
* **Primary Behavior Triggers:** Visualizes what factors play the biggest role in converting a browser into a buyer.
* **Sentiment Segmentation:** Breaks down customer alignment from *Strongly Agree* to *Strongly Disagree* to identify strong market fits or friction points.

## 🛠️ Project Structure

```text
customer-behavior-analysis-bakery/
├── data/
│   └── customer_survey.csv       # Raw survey data input
├── notebooks/
│   └── exploratory_analysis.ipynb # Step-by-step data exploration
├── customer_purchase_drivers.png # Saved visualization for dashboard
├── visualize.py                  # Main Python visualization script
└── README.md                     # Project documentation
```

## 🚀 How to Run the Analysis

1. Clone this repository to your local machine.
2. Ensure you have the required dependencies installed:
   ```bash
   pip install pandas matplotlib seaborn
   ```
3. Run the script to regenerate the dashboard visualization:
   ```bash
   python visualize.py
   ```


SELECT 
    question_text,
    SUM(CASE WHEN answer IN ('Strongly Agree','Agree') THEN count ELSE 0 END) AS positive,
    SUM(count) AS total,
    ROUND(
        SUM(CASE WHEN answer IN ('Strongly Agree','Agree') THEN count ELSE 0 END) * 100.0 
        / SUM(count), 2
    ) AS positive_percentage
FROM customer_survey
GROUP BY question_text
ORDER BY positive_percentage DESC;

Python Analysis Example

import pandas as pd
df = pd.read_csv("data/customer_survey.csv")
score_map = {
    "Strongly Agree": 5,
    "Agree": 4,
    "Don't Know": 3,
    "Disagree": 2,
    "Strongly Disagree": 1
}
df["score"] = df["answer"].map(score_map)
def weighted_avg(group):
    return (group["score"] * group["count"]).sum() / group["count"].sum()
result = df.groupby("question_text").apply(weighted_avg)
print(result.sort_values(ascending=False))

Business Recommendations

* Focus marketing on word-of-mouth & local community engagement
* Position product strongly as a breakfast solution
* Improve pricing strategy (bundling or smaller portions)
* Strengthen presence in supermarkets
* Maintain product quality: softness & freshness

Author

* Oktafiandi Wibisono
* Aspiring Data Analyst
* GitHub: https://github.com/oandi2026
* LinkedIn: (add your link)
