import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl','rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

model = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### Input the data to predict the salary""")
    
    countries = (
        "United States of America",
        "Germany",                               
        "United Kingdom of Great Britain and Northern Ireland",
        "India",
        "Canada",                                                  
        "France",                                                 
        "Poland",                                                   
        "Brazil",                                                   
        "Netherlands",
        "Australia",                                             
        "Spain",                                               
        "Italy",                                                  
        "Sweden",                                                   
        "Switzerland",
        "Austria",
        "Denmark",
        "Norway",                                                    
        "Portugal",                                                  
        "Czech Republic",                                            
        "Belgium",                                                   
        "Israel",                                                    
        "Finland",                                                   
        "New Zealand",
        "Romania",                                              
        "Ukraine",                                                  
        "Russian Federation"
    )

    education = (
        "Bachelor's degree",
        "Less than a Bachelor's", 
        "Master's degree",
        'Post grad'
    )

    country = st.selectbox("Country",countries)
    education = st.selectbox("Education Level",education)
    age = st.slider("Age",15,76,25)
    experience = st.slider("Years of Experience",0,50,3)

    ok = st.button("Calculate Salary")
 
    if ok:
        input = np.array([[age,education,country,experience]])
        input[:,1] = le_education.transform(input[:,1])
        input[:,2] = le_country.transform(input[:,2])
        input = input.astype(float)

        salary = model.predict(input)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}") 