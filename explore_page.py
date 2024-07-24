import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == 'Less than 1 year':
        return 0.5
    if x == 'More than 50 years':
        return 55
    return float(x)

def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor's degree"
    if "Master’s degree" in x:
        return "Master's degree"
    if "Professional degree" in x or 'Other doctoral' in x:
        return "Post grad"
    return "Less than a Bachelor's"

st.cache
def load_data():
    salary_df = pd.read_csv('dev_salary_data.csv')
    salary_df = salary_df[['Age' ,'EdLevel', 'YearsCodePro', 'Country','ConvertedCompYearly']]
    salary_df = salary_df.rename({'ConvertedCompYearly':'Salary'},axis=1)
    salary_df = salary_df.dropna()
    age_mapping = {
        '25-34 years old': 30,
        '35-44 years old': 40,
        '18-24 years old': 18,
        '45-54 years old': 50,
        '55-64 years old': 60,
        '65 years or older': 65,
        'Under 18 years old': 18,
        'Prefer not to say': None
    }
    salary_df['Age'] = salary_df['Age'].replace(age_mapping)
    salary_df = salary_df.dropna()
    country_map = shorten_categories(salary_df.Country.value_counts(),400)
    salary_df['Country'] = salary_df['Country'].map(country_map)
    salary_df = salary_df[salary_df['Salary'] <= 1000000]
    salary_df = salary_df[salary_df['Salary'] <= 250000]
    salary_df = salary_df[salary_df['Salary'] >= 10000]
    salary_df = salary_df[salary_df['Country'] != 'Other']
    salary_df['YearsCodePro'] = salary_df['YearsCodePro'].apply(clean_experience)
    salary_df['EdLevel'] = salary_df['EdLevel'].apply(clean_education)

    return salary_df

salary_df = load_data()

def show_explore_page():
    st.title("Explore the Software Developer Salaries")

    st.write("""### Stack Overflow Developer Survey 2023""")

    data = salary_df['Country'].value_counts()

    total = data.sum()
    percentage = data / total * 100

    # Combine countries with less than 2% into 'Other'
    data_clubbed = data.copy()
    data_clubbed[percentage < 2] = 0
    data_clubbed['Others'] = data[percentage < 2].sum()
    data_clubbed = data_clubbed[data_clubbed > 0]

    fig1,ax1 = plt.subplots()
    ax1.pie(data_clubbed, labels=data_clubbed.index,autopct="%1.1f%%",shadow=True,startangle=90,textprops={'fontsize': 8})
    ax1.axis("equal")

    st.write("""### Amount of data from different Countries""")

    st.pyplot(fig1)

    st.write("""### Mean Salary Based on Country""")

    data = salary_df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""### Mean Salary Based on Experience""")
    data = salary_df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

    st.write("""### Mean Salary Based on Age""")
    data = salary_df.groupby(["Age"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

    st.write("""### Mean Salary Based on Degree""")
    data = salary_df.groupby(["EdLevel"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)