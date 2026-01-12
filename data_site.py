import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    /* Reduce the gap at the very top of the page */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

background_color = st.config.get_option("theme.secondaryBackgroundColor")
accent_color = st.config.get_option("theme.primaryColor")
text_color = st.config.get_option("theme.textColor")

st.title("Gun Violence vs. Household Income")

num_rows = st.slider("Number of Incidents", 1, 61725, 61725)

data = pd.read_csv("./data/data_with_income.csv")
data['date'] = pd.to_datetime(data['date'])

# filters
states = sorted(data['state'].unique())
states.insert(0, "All States")
num_injured = sorted(data['n_injured'].unique())
num_injured.insert(0, "All")
num_killed = sorted(data['n_killed'].unique())
num_killed.insert(0, "All")

display_data = data.drop(columns=["incident_id", "participant_relationship"])
display_data = data.sample(n=num_rows, random_state=42)
display_data['month'] = display_data['date'].dt.month_name()
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
  st.caption(f"State")
  selected_state = st.multiselect("State", states, label_visibility="collapsed")
with col2:
  st.caption(f"Number of People Killed")
  selected_killed = st.multiselect("Number of People Killed", num_killed, label_visibility="collapsed")
with col3:
  st.caption(f"Number of People Injured")
  selected_injured = st.multiselect("Number of People Injured", num_injured, label_visibility="collapsed")

if selected_state:
  if "All States" not in selected_state:
    display_data = display_data[display_data['state'].isin(selected_state)]
if selected_killed:
  if "All" not in selected_killed:
    display_data = display_data[display_data['n_killed'].isin(selected_killed)]
if selected_injured:
  if "All" not in selected_injured:
    display_data = display_data[display_data['n_injured'].isin(selected_injured)]
total_rows = len(display_data)

st.markdown(f"**Total Rows: {total_rows}**")

# Graph and chart display

fig, ax = plt.subplots()
ax.set_xlim(0, 175000)
ax.set_title("Distribution of Median Income at Incident Locations", fontsize=18, fontweight='bold', color=text_color, pad=20)
ax.hist(display_data['median_income'], bins=30, color=accent_color, edgecolor='black')
fig.set_facecolor(background_color)
ax.set_facecolor(background_color)
ax.set_xlabel('Median Household Income ($)', fontsize=14)
ax.set_ylabel('Number of Incidents', fontsize=14)

# national median
national_median = 61372
ax.axvline(national_median, color='green', linestyle='--', linewidth=2, label=f'US Median Income (${national_median:,})')

# dataset median
dataset_median = display_data['median_income'].median()
ax.axvline(dataset_median, color='red', linestyle='-', linewidth=2, label=f'Incident Site Mean (${dataset_median:,.0f})')
ax.legend()
st.pyplot(fig)

col1, col2 = st.columns([1, 1])

state_counts = display_data['state'].value_counts().head(5)

fig, ax = plt.subplots()
fig.set_facecolor(background_color)
ax.set_title("Incidents by State (Top 5)", fontsize=18, fontweight='bold', pad=20)
ax.set_facecolor(background_color)
ax.pie(
    state_counts, 
    labels=state_counts.index, 
    autopct='%1.1f%%',
    startangle=90,
    colors=plt.cm.Paired.colors,
    textprops={'fontsize': 16, 'color': text_color}
)
ax.axis('equal')
with col1:
  st.pyplot(fig)


month_counts = display_data['month'].value_counts()
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]
existing_months = [m for m in month_order if m in month_counts.index]
month_counts = month_counts.reindex(existing_months)

fig, ax = plt.subplots()
fig.set_facecolor(background_color)
ax.set_facecolor(background_color)

ax.bar(month_counts.index, month_counts.values, color=accent_color, edgecolor=text_color)

ax.set_title("Incidents by Month", fontsize=18, fontweight='bold', color=text_color, pad=20)
ax.set_ylabel("Count", color=text_color)
ax.tick_params(axis='x', rotation=45, colors=text_color)
ax.tick_params(axis='y', colors=text_color)

plt.tight_layout()

with col2:
  st.pyplot(fig)

col1, col2, col3 = st.columns([1, 5, 1])

bins = list(range(0, 200001, 10000))
labels = bins[:-1]

display_data['income_bin'] = pd.cut(display_data['median_income'], bins=bins, labels=labels)
trend_data = display_data.groupby('income_bin', observed=True)['n_killed'].mean().reset_index()

fig, ax = plt.subplots()
fig.set_facecolor(background_color)
ax.set_facecolor(background_color)

ax.plot(
    trend_data['income_bin'], 
    trend_data['n_killed'], 
    color=accent_color, 
    marker='o',
    linestyle='-', 
    linewidth=2,
    markersize=6
)

ax.fill_between(trend_data['income_bin'], trend_data['n_killed'], color=accent_color, alpha=0.2)

ax.set_xlabel("Median Household Income ($)", color=text_color)
ax.set_ylabel("Average Deaths per Incident", color=text_color)
ax.set_title("Average Severity vs. Income Level", color=text_color, fontsize=18, fontweight='bold')
ax.tick_params(colors=text_color)

ticks = list(range(0, 200001, 20000))
ax.set_xticks(ticks)

tick_labels = [f'{int(x/1000)}k' if x != 0 else '0' for x in ticks]
ax.set_xticklabels(tick_labels, color=text_color, fontsize=12)

with col2:
  st.pyplot(fig)