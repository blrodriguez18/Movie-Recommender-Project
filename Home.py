import streamlit as st

# st.image('/Users/beatrizrodriguez/Desktop/MoviesRecommend/images/logo.png', width=250)

st.header("Welcome to my :blue[Movie Recommender]! :star:", divider="blue")
st.subheader("Please check the sidebar menu for your desired page.")

st.write("")
st.write("To see some graphs of an exploratory data analysis performed on The Movies Dataset from Kaggle linked")
st.link_button("here", "https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset")
st.write("please go to the :red[_Exploratory Data Analysis_] page.")

st.write("")
st.write("To enter the title of a movie you like and obtain 5 other recommended movies for it, please go to the :red[_Movie Recommender_] page.")

