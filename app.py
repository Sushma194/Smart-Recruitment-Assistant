import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Smart Recruitment Assistant",
    page_icon="🎯",
    layout="wide"
)

# ==========================
# CUSTOM CSS
# ==========================
st.markdown("""
<style>

/* ===== MAIN BACKGROUND ===== */
.stApp{
background: linear-gradient(
120deg,
#ff512f,
#dd2476,
#7b2ff7,
#00c9ff
);
background-size:400% 400%;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"]{
background: linear-gradient(
180deg,
#141e30,
#243b55
);
}

[data-testid="stSidebar"] *{
color:#ffffff !important;
font-weight:600;
}

/* ===== TITLE ===== */
h1{
text-align:center;
font-size:55px !important;
font-weight:bold;
color:#ffd60a !important;
text-shadow:3px 3px 10px rgba(0,0,0,0.4);
}

/* ===== HEADINGS ===== */
h2,h3{
color:#00f5ff !important;
font-weight:bold;
}

/* ===== METRIC CARDS ===== */
[data-testid="metric-container"]{
background: rgba(255,255,255,0.10);
backdrop-filter: blur(12px);
border-radius:20px;
padding:15px;
border:2px solid rgba(255,255,255,0.2);
box-shadow:0px 8px 25px rgba(0,0,0,0.3);
}

[data-testid="metric-container"] *{
color:#fff !important;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"]{
border-radius:20px;
overflow:hidden;
}

/* ===== BUTTONS ===== */
.stButton > button{
background: linear-gradient(
90deg,
#00c9ff,
#92fe9d
);
color:black;
font-weight:bold;
border:none;
border-radius:15px;
height:3em;
width:100%;
}

.stButton > button:hover{
transform:scale(1.03);
}

/* ===== DOWNLOAD BUTTON ===== */
.stDownloadButton button{
background: linear-gradient(
90deg,
#f7971e,
#ffd200
);
color:black;
font-weight:bold;
border:none;
border-radius:15px;
}

/* ===== SUCCESS ===== */
.stSuccess{
background:rgba(0,255,127,0.2);
border-radius:15px;
}

/* ===== ERROR ===== */
.stError{
background:rgba(255,0,0,0.2);
border-radius:15px;
}

/* ===== INFO ===== */
.stInfo{
background:rgba(0,191,255,0.2);
border-radius:15px;
}

/* ===== INPUT BOX ===== */
.stNumberInput input{
background:#1e293b !important;
color:#00f5ff !important;
}

/* ===== SLIDERS ===== */
.stSlider *{
color:#ffffff !important;
}

/* ===== TABLE TEXT ===== */
table{
font-size:16px !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar{
width:10px;
}

::-webkit-scrollbar-thumb{
background:#00f5ff;
border-radius:10px;
}

</style>
""", unsafe_allow_html=True)
# ==========================
# LOAD MODEL
# ==========================

model = joblib.load("models/recruitment_model.pkl")

# ==========================
# TITLE
# ==========================

st.title("🎯 Smart Recruitment Assistant")

st.markdown(
"""
### AI-Powered Hiring Decision Support System
"""
)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.header("Candidate Information")

candidate_id = st.sidebar.number_input(
    "Candidate ID",
    min_value=1,
    value=1
)

cgpa = st.sidebar.slider(
    "CGPA",
    5.0,
    10.0,
    7.5
)

aptitude = st.sidebar.slider(
    "Aptitude Score",
    0,
    100,
    70
)

technical = st.sidebar.slider(
    "Technical Score",
    0,
    100,
    70
)

communication = st.sidebar.slider(
    "Communication Score",
    0,
    100,
    70
)

certifications = st.sidebar.slider(
    "Certifications",
    0,
    10,
    2
)

internships = st.sidebar.slider(
    "Internships",
    0,
    5,
    1
)

projects = st.sidebar.slider(
    "Projects",
    0,
    10,
    3
)

experience = st.sidebar.slider(
    "Experience",
    0,
    10,
    1
)

interview = st.sidebar.slider(
    "Interview Score",
    0,
    100,
    75
)

# ==========================
# PREDICTION
# ==========================

if st.sidebar.button("Predict Candidate"):

    input_data = [[
        candidate_id,
        cgpa,
        aptitude,
        technical,
        communication,
        certifications,
        internships,
        projects,
        experience,
        interview
    ]]

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    hiring_score = (
        cgpa * 5
        + technical * 0.30
        + communication * 0.20
        + interview * 0.30
        + projects * 2
        + internships * 3
    )

    st.subheader("Prediction Result")

    if prediction == 1:
        st.success("✅ Candidate Likely To Be Selected")
    else:
        st.error("❌ Candidate Likely To Be Rejected")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Hiring Probability",
            f"{probability*100:.2f}%"
        )

    with col2:
        st.metric(
            "Hiring Score",
            round(hiring_score, 2)
        )

    if hiring_score >= 90:
        category = "Excellent"
    elif hiring_score >= 75:
        category = "Strong"
    elif hiring_score >= 60:
        category = "Average"
    else:
        category = "Needs Improvement"

    st.info(f"⭐ Category : {category}")

# ==========================
# LOAD DATASET
# ==========================

df = pd.read_csv("data/recruitment_data.csv")

df["HiringScore"] = (
    df["CGPA"] * 5
    + df["Technical"] * 0.30
    + df["Communication"] * 0.20
    + df["Interview"] * 0.30
    + df["Projects"] * 2
    + df["Internships"] * 3
)
# ==========================
# CANDIDATE RANKING
# ==========================

ranking_df = df.sort_values(
    by="HiringScore",
    ascending=False
).reset_index(drop=True)

ranking_df["Rank"] = ranking_df.index + 1

# ==========================
# SEARCH CANDIDATE
# ==========================

st.header("🔍 Candidate Search")

search_id = st.number_input(
    "Enter Candidate ID",
    min_value=1,
    max_value=int(df["Candidate_ID"].max()),
    value=1
)

candidate_data = df[
    df["Candidate_ID"] == search_id
]

if not candidate_data.empty:

    st.success(f"Candidate {search_id} Found")

    candidate_rank = ranking_df[
        ranking_df["Candidate_ID"] == search_id
    ]

    rank = candidate_rank["Rank"].values[0]

    hiring_score = candidate_data[
        "HiringScore"
    ].values[0]

    status = candidate_data[
        "Selected"
    ].values[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Hiring Score",
            f"{hiring_score:.2f}"
        )

    with col2:
        st.metric(
            "Candidate Rank",
            rank
        )

    with col3:
        if status == 1:
            st.success("Selected")
        else:
            st.error("Rejected")

    st.subheader("Candidate Details")

    st.dataframe(candidate_data)

else:
    st.error("Candidate Not Found")

# ==========================
# KPI DASHBOARD
# ==========================

st.header("📊 Dashboard Overview")

total_candidates = len(df)
selected = int(df["Selected"].sum())
rejected = total_candidates - selected

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Candidates",
        total_candidates
    )

with col2:
    st.metric(
        "Selected",
        selected
    )

with col3:
    st.metric(
        "Rejected",
        rejected
    )

# ==========================
# DATASET
# ==========================

st.header("📋 Recruitment Dataset")

st.dataframe(df.head(20))

# ==========================
# BAR CHART
# ==========================

st.header("📊 Selection Distribution")

selection_counts = df["Selected"].value_counts()

fig = px.bar(
    x=["Selected", "Rejected"],
    y=selection_counts.values,
    color=["Selected", "Rejected"],
    title="Selected vs Rejected Candidates",
    color_discrete_map={
        "Selected": "#00F5D4",   # Cyan
        "Rejected": "#FF006E"    # Pink
    }
)

fig.update_traces(
    marker_line_color="#FEE440",
    marker_line_width=3
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="white",
        size=16
    ),
    title_font=dict(
        size=24,
        color="#FFD60A"
    ),
    xaxis=dict(
        title="Candidate Status",
        showgrid=False
    ),
    yaxis=dict(
        title="Number of Candidates",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.1)"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# PIE CHART
# ==========================

st.header("🥧 Selection Ratio")

fig = px.pie(
    values=selection_counts.values,
    names=["Selected", "Rejected"],
    hole=0.55,
    title="Selection Percentage",
    color=["Selected", "Rejected"],
    color_discrete_map={
        "Selected": "#00F5D4",   # Cyan
        "Rejected": "#FF006E"    # Pink
    }
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label",
    textfont_size=18,
    marker=dict(
        line=dict(
            color="#000000",
            width=2
        )
    )
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="white",
        size=16
    ),
    title_font=dict(
        size=24
    ),
    legend=dict(
        font=dict(size=14)
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# HISTOGRAM
# ==========================

st.header("📈 Hiring Score Distribution")

fig = px.histogram(
    df,
    x="HiringScore",
    nbins=20,
    title="Hiring Score Distribution",
    color_discrete_sequence=["#00F5D4"]  # Cyan
)

fig.update_traces(
    marker_line_color="#FFD60A",
    marker_line_width=2,
    opacity=0.9
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(20,20,20,0.3)",
    font=dict(
        color="#F8F9FA",
        size=16
    ),
    title_font=dict(
        size=24,
        color="#FFD60A"
    ),
    xaxis=dict(
        title="Hiring Score",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.1)"
    ),
    yaxis=dict(
        title="Number of Candidates",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.1)"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# TOP 10 CANDIDATES
# ==========================

st.header("🏆 Top 10 Candidates")

top10 = df.sort_values(
    by="HiringScore",
    ascending=False
).head(10)

st.dataframe(top10)

fig = px.bar(
    top10,
    x="Candidate_ID",
    y="HiringScore",
    color="HiringScore",
    title="Top 10 Candidates"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# CORRELATION HEATMAP
# ==========================

st.header("🔥 Correlation Heatmap")

fig, ax = plt.subplots(
    figsize=(12, 6)
)

sns.heatmap(
    df.corr(numeric_only=True),
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)

# ==========================
# CATEGORY ANALYSIS
# ==========================

st.header("⭐ Candidate Categories")

def get_category(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Strong"

    elif score >= 60:
        return "Average"

    else:
        return "Needs Improvement"

df["Category"] = df["HiringScore"].apply(
    get_category
)

category_counts = df["Category"].value_counts()

fig = px.bar(
    x=category_counts.index,
    y=category_counts.values,
    color=category_counts.index,
    title="Candidate Categories"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# DOWNLOAD DATASET
# ==========================

st.header("⬇ Download Dataset")

csv = df.to_csv(index=False)

st.download_button(
    label="Download Recruitment Dataset",
    data=csv,
    file_name="Recruitment_Data.csv",
    mime="text/csv"
)

st.success("🎉 Smart Recruitment Assistant Loaded Successfully")