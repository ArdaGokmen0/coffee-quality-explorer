# ☕ Coffee Quality Explorer

An interactive data exploration dashboard built with Streamlit, using the CQI Arabica Coffee Quality dataset.

## 🎯 Project Goal

This app allows users to explore arabica coffee quality data from around the world — filtering by country, processing method, and quality score to discover patterns and insights.

## 📊 Features

- **Sidebar Filters** — Filter by country, processing method, and quality score range
- **KPI Cards** — Total coffees, average score, highest score, number of countries
- **Quality Distribution** — Histogram of Total Cup Points
- **Country Comparison** — Average score by country (bar chart)
- **Sensory Profile** — Radar chart of flavor attributes (Aroma, Flavor, Acidity, etc.)
- **Defects vs Quality** — Scatter plot of Category Two Defects vs quality score
- **Moisture vs Quality** — Scatter plot of moisture percentage vs quality score
- **Top 10 Coffees** — Highest rated coffees from the filtered selection
- **Raw Data Table** — Full filtered dataset view

## 🗂️ Dataset

- **Source:** CQI Arabica Coffee Quality Dataset (Kaggle)
- **File:** df_arabica_clean.csv
- **Rows:** 207 arabica coffee samples
- **Columns:** 40 features including sensory scores, origin, processing method, defects

## 🚀 How to Run

1. Clone this repository
2. Install dependencies:
3. pip install -r requirements.txt
4. Run the app:
5. streamlit run app.py

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly

## 👤 Author

Made as a learning project — exploring data visualization and Streamlit dashboard development.