import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Data Area Salary Dashboard", 
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

st.sidebar.header("🔍 Filters")

available_years = sorted(df['ano'].unique())
selected_years = st.sidebar.multiselect("Year", available_years, default=available_years)

available_seniorities = sorted(df['senioridade'].unique())
selected_seniorities = st.sidebar.multiselect("Seniority", available_seniorities, default=available_seniorities)

available_contracts = sorted(df['contrato'].unique())
selected_contracts = st.sidebar.multiselect("Contract Type", available_contracts, default=available_contracts)

available_company_sizes = sorted(df['tamanho_empresa'].unique())
selected_company_sizes = st.sidebar.multiselect("Company Size", available_company_sizes, default=available_company_sizes)

filtered_df = df[
    (df['ano'].isin(selected_years)) &
    (df['senioridade'].isin(selected_seniorities)) &
    (df['contrato'].isin(selected_contracts)) &
    (df['tamanho_empresa'].isin(selected_company_sizes))
]

st.title("🎲 Data Area Salary Analysis Dashboard")
st.markdown("Explore salary data in the data area over recent years. Use the filters on the left to refine your analysis.")

st.subheader("General Metrics (Annual Salary in USD)")

if not filtered_df.empty:
    average_salary = filtered_df['usd'].mean()
    max_salary = filtered_df['usd'].max()
    total_records = filtered_df.shape[0]
    most_common_role = filtered_df["cargo"].mode()[0]
else:
    average_salary, max_salary, total_records, most_common_role = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Salary", f"${average_salary:,.0f}")
col2.metric("Maximum Salary", f"${max_salary:,.0f}")
col3.metric("Total Records", f"{total_records:,}")
col4.metric("Most Common Role", most_common_role)

st.markdown("---")

st.subheader("Charts")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    if not filtered_df.empty:
        top_roles = filtered_df.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        role_chart = px.bar(
            top_roles,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 Roles by Average Salary",
            labels={'usd': 'Average Annual Salary (USD)', 'cargo': ''}
        )
        role_chart.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(role_chart, use_container_width=True)
    else:
        st.warning("No data to display for roles chart.")

with col_chart2:
    if not filtered_df.empty:
        salary_hist_chart = px.histogram(
            filtered_df,
            x='usd',
            nbins=30,
            title="Annual Salary Distribution",
            labels={'usd': 'Salary Range (USD)', 'count': ''}
        )
        salary_hist_chart.update_layout(title_x=0.1)
        st.plotly_chart(salary_hist_chart, use_container_width=True)
    else:
        st.warning("No data to display for salary distribution chart.")

col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    if not filtered_df.empty:
        remote_count = filtered_df['remoto'].value_counts().reset_index()
        remote_count.columns = ['work_type', 'count']
        remote_chart = px.pie(
            remote_count,
            names='work_type',
            values='count',
            title='Proportion of Work Types',
            hole=0.5
        )
        remote_chart.update_traces(textinfo='percent+label')
        remote_chart.update_layout(title_x=0.1)
        st.plotly_chart(remote_chart, use_container_width=True)
    else:
        st.warning("No data to display for work type chart.")

with col_chart4:
    if not filtered_df.empty:
        df_ds = filtered_df[filtered_df['cargo'] == 'Data Scientist']
        avg_ds_country = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        country_chart = px.choropleth(
            avg_ds_country,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Average Data Scientist Salary by Country',
            labels={'usd': 'Average Salary (USD)', 'residencia_iso3': 'Country'}
        )
        country_chart.update_layout(title_x=0.1)
        st.plotly_chart(country_chart, use_container_width=True)
    else:
        st.warning("No data to display for country chart.")

st.subheader("Detailed Data")
st.dataframe(filtered_df)