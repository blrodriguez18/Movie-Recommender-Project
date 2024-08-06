import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pickle
import ast
import zipfile
import io
import pandas as pd

x = st.text_input("Movie Title")
st.write(f'Looking for recommendations if you like the movie: {x} ...')

zip_file_path1 = 'movies1.csv.zip'
csv_file_name1 = 'movies1.csv'
zip_file_path2 = 'processed_movies.csv.zip'
csv_file_name2 = 'processed_movies.csv'

with zipfile.ZipFile(zip_file_path2, 'r') as z:
    with z.open(csv_file_name2) as f:
        movies1 = pd.read_csv(f)
# movies1 = pd.read_csv('/Users/beatrizrodriguez/Desktop/MoviesRecommend/processed_movies.csv')

if x == '':
    st.write("")
elif x not in list(movies1["original_title"]):
    st.subheader(f"Sorry, {x} is not in the database. Make sure your spelling and punctuation are correct, or try a different movie.")
else:
    # Load the cosine similarity matrix
    with open('/Users/beatrizrodriguez/Desktop/MoviesRecommend/cosine_sim.pkl', 'rb') as file:
        cosine_sim_reduced_dim = pickle.load(file)


    def get_content_based_recommendations(title, num_recommendations=5):
        idx = movies1.index[movies1['original_title'] == title]
        # if not idx.any():
        #     return pd.Series([])

        idx = idx[0]
        sim_scores = list(enumerate(cosine_sim_reduced_dim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations + 1]

        movie_indices = [i[0] for i in sim_scores]
        return movies1['original_title'].iloc[movie_indices]

    def wrap_text(text, width=10):
        words = text.split()
        wrapped_text = ""
        line = ""
        for word in words:
            if len(line) + len(word) <= width:
                line += word + " "
            else:
                wrapped_text += line.strip() + "<br>"
                line = word + " "
        wrapped_text += line.strip()
        return wrapped_text


    def get_web_model(movie_list, title):
        angle = np.linspace(0, 2 * np.pi, len(movie_list), endpoint=False)
        x = np.cos(angle)
        y = np.sin(angle)

        x_central = [0]
        y_central = [0]

        x_all = np.concatenate((x_central, x))
        y_all = np.concatenate((y_central, y))

        edge_x = []
        edge_y = []

        for i in range(len(movie_list)):
            edge_x.append(x_central[0])
            edge_x.append(x[i])
            edge_x.append(None)
            edge_y.append(y_central[0])
            edge_y.append(y[i])
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=4, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_trace = go.Scatter(
            x=x_all, y=y_all,
            mode='markers+text',
            text=[f"<span style='color:black'>{wrap_text(title, 10)}</span>"] +
                 [f"<span style='color:white'>{wrap_text(movie, 10)}</span>" for movie in movie_list],
            textposition='middle center',
            hoverinfo='text',
            marker=dict(size=[120] + [100] * len(movie_list), color=["#ff9c38"] + ["#4d64ff"] * len(movie_list), opacity=1))

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=0, l=0, r=0, t=50),
                            title=dict(
                                text=f'Movie Recommendations if You Like: {title}',
                                x=0.5, y=0.95, xanchor='center', yanchor='top'),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            width=600, height=600,
                            autosize=False))
        return fig

    movie_test = list(get_content_based_recommendations(x, num_recommendations=5))
    # st.write(f"Here is the list: {movie_test}")

    web = get_web_model(movie_test, x)

    st.subheader("Here are :orange[5 movies] recommended for you")
    st.plotly_chart(web)

    def get_stats(title):
        index = movies1.index[movies1['original_title'] == title][0]
        stats_df = pd.DataFrame([{
            "original_title": str(movies1.loc[index, "original_title"]).strip(" ',]['"),
            "director": ", ".join(ast.literal_eval(movies1.loc[index, "director"])),
            "genres": ", ".join(ast.literal_eval(movies1.loc[index, "genres"])),
            # "overview": str(movies1.loc[index, "overview"]).strip(" ',]['"),
            # "cast": ", ".join(ast.literal_eval(movies1.loc[index, "cast"])),
            "spoken_languages": ", ".join(ast.literal_eval(movies1.loc[index, "spoken_languages"])),
            "runtime": str(movies1.loc[index, "runtime"]).strip(" ',]['"),
            "release_date": str(movies1.loc[index, "release_date"]).strip(" ',]['"),
            "adult": str(movies1.loc[index, "adult"]).strip(" ',]['"),
            "popularity": str(movies1.loc[index, "popularity"]).strip(" ',]['"),
            "vote_average": str(movies1.loc[index, "vote_average"]).strip(" ',]['")
        }])

        styled_df = stats_df.style.set_properties(**{
            'text-align': 'left',
            'width': '500'
        })

        return styled_df

    st.subheader(":orange[Learn more] about these movies:")
    st.write("**To view the full contents of a cell, double-click on the desired cell.")
    # item_df = get_stats(movie_test)
    # st.dataframe(item_df)

    for item in movie_test:
        item_df = get_stats(item)
        st.write(f'{item}: ')
        st.dataframe(item_df)
