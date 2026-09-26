import streamlit as st
import pandas as pd 
import plotly.express as px 

# 1. Title and Context
st.title("Lebanon Tourism Facilities Analysis")
st.markdown("""
### Data Context
This interactive dashboard analyzes the distribution of tourism infrastructure, dining establishments, and lodging options across towns and districts in Lebanon based on official survey data.
""")

# 2. Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("tourism.csv")

    # Calculate total tourism businesses
    business_cols = [
        "Total number of hotels",
        "Total number of cafes",
        "Total number of restaurants",
        "Total number of guest houses"

    ]
    df[business_cols] = df[business_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
    df["Total Tourism Businesses"] = df[business_cols].sum(axis=1)

    # Clean district column from refArea
    df["District"] = df["refArea"].astype(str).str.split("/").str[-1].str.replace("District.*", "", regex=True).str.replace("_", " ").str.strip()
    return df
df = load_data()
# 3. Linked Interactive Controls (Sidebar)
st.sidebar.header("Filter Options")

# Control 1: Select Districts
district_options = ["All"] + sorted([d for d in df["District"].unique().tolist() if d])
selected_district = st.sidebar.selectbox("Select District", district_options)

# Link options: Filter dataset based on selected District
if selected_district != "All":
    district_df = df[df["District"] == selected_district]
else:
    district_df = df.copy()

#Control 2: Select Town (Options dynamically update based on District)
town_options = ["All"] + sorted(district_df["Town"].unique().tolist())
selected_town = st.sidebar.selectbox("Select Town", town_options)

# Apply final town filter
if selected_town != "All":
    final_df = district_df[df["Town"] == selected_town]
else:
    final_df = district_df.copy()

# 4. Graph 1: Grouped Bar Chart
st.subheader("Tourism Facility Profiles Across Towns")

top10 = final_df.nlargest(10, "Total Tourism Businesses").rename(columns={
    "Total number of hotels": "Hotels",
    "Total number of cafes": "Cafés",
    "Total number of restaurants": "Restaurants",
    "Total number of guest houses": "Guest Houses"
})

fig1 = px.bar(
    top10,
    x="Town",
    y=["Hotels", "Cafés", "Restaurants", "Guest Houses"],
    barmode="group",
    title="Tourism Facility Profiles Across Leading Towns",
    color_discrete_sequence=["#0B1F3A", "#2457A6", "#4EA8DE", "#A9D6E5"]
)
fig1.update_layout(template="plotly_white", font=dict(family="Avenir", size=14), title_x=0.5)
st.plotly_chart(fig1, use_container_width=True)

# 5. Graph 2: Line Chart
st.subheader("Dining and Café Facilities Across Towns")

top15 = final_df.nlargest(15, "Total Tourism Businesses")

fig2 = px.line(
    top15,
    x="Town",
    y=["Total number of cafes", "Total number of restaurants"],
    markers=True,
    title="Dining and Café Facilities Across Towns",
    color_discrete_sequence=["#7F5539", "#E6CCB2"],
)
fig2.update_layout(template="plotly_white", font=dict(family="Avenir", size=14), title_x=0.5)
st.plotly_chart(fig2, use_container_width=True)

# 6. Key Insights
st.markdown("---")
st.subheader("Key Insights")
st.write("**Insight 1 (Hospitality Facilities):** Mina records the highest café count at 100 while Zouk El-Kharab records the highest count at 100. In contrast, Hadath and Nabatiyeh show a balanced profile, with approximately 50 cafés and 50 restaurants each. Guest houses remain very limited across most leading towns, highlighting the dominance of food-service facilities over accommodation.")
st.write("**Insight 2 (Food-Service Patterns):** Mina records 100 cafés compared with 50 restaurants , while Zouk El-Kharab shows the opposite pattern, with about 20 cafés and 100 restauants. This higlights contrasting food-service profiles across leading towns.")

# 7. Design Justifications
st.markdown("---")
st.subheader("Design Justifications")

with st.expander("Design Justification: Linked District & Town Dropdowns"):
    st.write("""
    **User Question Answered:** How do tourism facility profiles change when zooming from a broader administrative district down to a specific local town?

**Why this Widget:** A two-stage cascading dropdown (`st.selectbox`) was selected instead of showing a flat list of hundreds of towns, which would create severe visual clutter and cognitive overload.

**Course Concept Alignment:** This directly applies the course concept of **reducing visual clutter** and **guided drill-down interaction**. Linking the District filter to the Town selector dynamically isolates relevant subsets of data, focusing user attention.
""")

with st.expander("Design Justification: Grouped Bar & Line Charts"):
    st.write("""
**User Question Answered:** Which specific food-service and lodging categories dominate across high-volume tourist towns?

**Why this Visual Layout:** The grouped bar chart compares four facility types side-by-side, making differences between accommodation and food services visible. The line chart tracks two food-service categories across 15 towns, making gaps between café and restaurant activity easy to identify.

**Course Concept Alignment:** This applies the principles of **focusing visual attention** and **providing comparative context**, enabling users to quickly identify pattern variations without unnecessary scrolling.
""")
