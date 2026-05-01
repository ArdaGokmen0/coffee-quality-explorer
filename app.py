import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===== SAYFA AYARI =====
st.set_page_config(layout="wide", page_title="Coffee Quality Explorer")

# ===== BAŞLIK =====
st.title("☕ Coffee Quality Explorer")

# ===== VERİYİ YÜKLE =====
df = pd.read_csv("df_arabica_clean.csv")

# Gereksiz sütunu sil
if "Unnamed: 0" in df.columns:
    df = df.drop("Unnamed: 0", axis=1)

# Boş işleme metodlarını doldur
df["Processing Method"] = df["Processing Method"].fillna("Not Specified")

# ===== SIDEBAR FİLTRELER =====
st.sidebar.header("🔍 Filters")

# Ülke filtresi
countries = sorted(df["Country of Origin"].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=countries,
    default=countries
)

# İşleme metodu filtresi
processing_methods = sorted(df["Processing Method"].dropna().unique())
selected_methods = st.sidebar.multiselect(
    "Select Processing Methods:",
    options=processing_methods,
    default=processing_methods
)

# Puan aralığı slider
st.sidebar.subheader("Score Range")
score_min = float(df["Total Cup Points"].min())
score_max = float(df["Total Cup Points"].max())
selected_range = st.sidebar.slider(
    "Select Total Cup Points Range:",
    min_value=score_min,
    max_value=score_max,
    value=(score_min, score_max),
    step=0.1
)

# ===== FİLTRELEME =====
filtered_df = df[
    (df["Country of Origin"].isin(selected_countries)) &
    (df["Processing Method"].isin(selected_methods)) &
    (df["Total Cup Points"] >= selected_range[0]) &
    (df["Total Cup Points"] <= selected_range[1])
]

# ===== KPI KARTLARI =====
st.write("---")

if len(filtered_df) > 0:
    total_coffees = len(filtered_df)
    avg_score = filtered_df["Total Cup Points"].mean()
    highest_score = filtered_df["Total Cup Points"].max()
    num_countries = filtered_df["Country of Origin"].nunique()
else:
    total_coffees = 0
    avg_score = 0
    highest_score = 0
    num_countries = 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("☕ Total Coffees", total_coffees)
with col2:
    st.metric("⭐ Average Score", f"{avg_score:.2f}")
with col3:
    st.metric("🏆 Highest Score", f"{highest_score:.2f}")
with col4:
    st.metric("🌍 Countries", num_countries)

st.write("---")

# ===== VERİ YOK UYARISI =====
if len(filtered_df) == 0:
    st.warning("⚠️ No data found for the selected filters. Please adjust your selections.")
    st.stop()

# ===== HİSTOGRAM =====
st.subheader("📊 Coffee Quality Distribution")

fig_histogram = px.histogram(
    filtered_df,
    x="Total Cup Points",
    nbins=20,
    title="Distribution of Coffee Quality Scores",
    labels={"Total Cup Points": "Quality Score", "count": "Number of Coffees"},
    color_discrete_sequence=["#8B4513"]
)
fig_histogram.update_layout(bargap=0.05)
st.plotly_chart(fig_histogram, use_container_width=True, key="histogram")

# ===== ÜLKEYE GÖRE ORTALAMA BAR CHART =====
st.subheader("🌍 Average Score by Country")

country_avg = (
    filtered_df.groupby("Country of Origin")["Total Cup Points"]
    .mean()
    .sort_values(ascending=True)  # Yatay grafikte ascending=True → en yüksek üstte
    .reset_index()
)
country_avg.columns = ["Country", "Average Score"]
country_avg["Average Score"] = country_avg["Average Score"].round(2)

fig_bar = px.bar(
    country_avg,
    x="Average Score",
    y="Country",
    orientation="h",
    title="Average Coffee Quality Score by Country",
    labels={"Average Score": "Average Score", "Country": "Country"},
    color="Average Score",
    color_continuous_scale="earth",
    text="Average Score"
)
fig_bar.update_traces(textposition="outside")
fig_bar.update_layout(height=max(400, len(country_avg) * 30))
st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")

# ===== RADAR CHART =====
st.subheader("🎯 Sensory Profile")
st.caption("This radar chart shows the average sensory scores for the coffees matching your current filter selection.")

sensory_cols = ["Aroma", "Flavor", "Aftertaste", "Acidity", "Body", "Balance", "Overall"]

# Sadece datasette olan sütunları al
available_cols = [col for col in sensory_cols if col in filtered_df.columns]
sensory_values = [filtered_df[col].mean() for col in available_cols]

fig_radar = go.Figure(data=go.Scatterpolar(
    r=sensory_values,
    theta=available_cols,
    fill="toself",
    name="Sensory Profile",
    line=dict(color="#8B4513"),
    fillcolor="rgba(139, 69, 19, 0.3)"
))

fig_radar.update_layout(
    polar=dict(
        bgcolor="rgba(0,0,0,0)",
        radialaxis=dict(
            visible=True,
            range=[6.8, 8.8],
            tickfont=dict(size=10),
            gridcolor="gray"
        ),
        angularaxis=dict(gridcolor="gray")
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    title="Average Sensory Profile",
    height=550,
    margin=dict(l=80, r=80, t=80, b=80)
)
st.plotly_chart(fig_radar, use_container_width=True, key="radar_chart")

# Sensory değerlerini tablo olarak göster
sensory_table = pd.DataFrame({
    "Attribute": available_cols,
    "Average Score": [round(v, 3) for v in sensory_values]
})
sensory_table = sensory_table.sort_values("Average Score", ascending=False).reset_index(drop=True)
st.dataframe(sensory_table, use_container_width=True)

# ===== SCATTER PLOT =====
st.subheader("⚠️ Defects vs Quality Score")
st.caption("Using 'Category Two Defects' — minor defects found in the coffee sample. 'Defects' column in the dataset is always 0 and not useful.")

scatter_df = filtered_df.copy()
scatter_df["Category Two Defects"] = pd.to_numeric(scatter_df["Category Two Defects"], errors="coerce")
scatter_df = scatter_df.dropna(subset=["Category Two Defects", "Total Cup Points"])

if len(scatter_df) > 0:
    fig_scatter = px.scatter(
        scatter_df,
        x="Category Two Defects",
        y="Total Cup Points",
        color="Country of Origin",
        title="Relationship between Category Two Defects and Coffee Quality",
        labels={
            "Category Two Defects": "Number of Defects (Category 2)",
            "Total Cup Points": "Quality Score",
            "Country of Origin": "Country"
        },
        hover_data=["Country of Origin", "Category Two Defects", "Total Cup Points", "Variety"]
    )
    fig_scatter.update_traces(marker=dict(size=8, opacity=0.8))
    st.plotly_chart(fig_scatter, use_container_width=True, key="scatter_plot")
else:
    st.warning("No valid defect data available for this filter combination.")
# ===== MOISTURE vs QUALITY =====
st.subheader("💧 Moisture Percentage vs Quality Score")
st.caption("Higher moisture can negatively affect coffee quality and shelf life.")

moisture_df = filtered_df.dropna(subset=["Moisture Percentage", "Total Cup Points"]).copy()
moisture_df = moisture_df[moisture_df["Moisture Percentage"] > 0]

if len(moisture_df) > 0:
    fig_moisture = px.scatter(
        moisture_df,
        x="Moisture Percentage",
        y="Total Cup Points",
        color="Country of Origin",
        title="Moisture Percentage vs Coffee Quality Score",
        labels={
            "Moisture Percentage": "Moisture (%)",
            "Total Cup Points": "Quality Score",
            "Country of Origin": "Country"
        },
        hover_data=["Country of Origin", "Moisture Percentage", "Total Cup Points"]
    )
    fig_moisture.update_traces(marker=dict(size=8, opacity=0.8))
    st.plotly_chart(fig_moisture, use_container_width=True, key="moisture_scatter")
else:
    st.warning("No moisture data available for this filter combination.")
# ===== TOP 10 KAHVELER =====
st.write("---")
st.subheader("🏆 Top 10 Highest Rated Coffees")
st.caption("Based on your current filter selection.")

top10_cols = ["Country of Origin", "Farm Name", "Variety", 
              "Processing Method", "Total Cup Points"]

available_top10 = [c for c in top10_cols if c in filtered_df.columns]

top10 = (
    filtered_df[available_top10]
    .sort_values("Total Cup Points", ascending=False)
    .head(10)
    .reset_index(drop=True)
)
top10.index = top10.index + 1  # 1'den başlasın, 0'dan değil

st.dataframe(top10, use_container_width=True)

# ===== HAM VERİ TABLOSU =====
st.write("---")
with st.expander("📋 Show Raw Data Table"):
    st.dataframe(filtered_df.reset_index(drop=True))