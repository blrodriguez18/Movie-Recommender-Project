import streamlit as st

pg = st.navigation([st.Page("Home.py"), st.Page("Exploratory Data Analysis.py"), st.Page("Movie Recommender.py"),
                    st.Page("Contact.py")])
pg.run()