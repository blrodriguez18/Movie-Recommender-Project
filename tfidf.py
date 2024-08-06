import pickle
import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD


# @st.cache
def load_data(file_path):
    return pd.read_csv(file_path)


# @st.cache(allow_output_mutation=True)
def process_data(movies1):
    list_of_lists = []
    for i in range(len(movies1)):
        small_list = []
        for col in ["genres", "keywords", "director", "cast", "spoken_languages"]:
            new = ast.literal_eval(movies1.loc[i, col])
            for item in new:
                small_list.append(item)
        new2 = movies1.loc[i, "overview"].split()
        for item2 in new2:
            small_list.append(item2)
        list_of_lists.append(small_list)

    movies1['combined'] = list_of_lists
    return movies1

def convert_to_string(text):
    if isinstance(text, list):
        return ' '.join(text)
    return text

# @st.cache(allow_output_mutation=True)
def create_tfidf_matrix(movies1):
    movies1['combined'] = movies1['combined'].apply(convert_to_string)
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies1['combined'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x))

    svd = TruncatedSVD(n_components=11)
    tfidf_reduced = svd.fit_transform(tfidf_matrix)

    return tfidf_reduced, tfidf.get_feature_names_out()


# @st.cache
def calculate_cosine_similarity(tfidf_reduced):
    return cosine_similarity(tfidf_reduced)


movies1 = load_data("/Users/beatrizrodriguez/Desktop/MoviesRecommend/movies1.csv")
movies1 = process_data(movies1)
tfidf_reduced, feature_names = create_tfidf_matrix(movies1)
cosine_sim_reduced_dim = calculate_cosine_similarity(tfidf_reduced)

with open('cosine_sim.pkl', 'wb') as file:
    pickle.dump(cosine_sim_reduced_dim, file)

# Save the processed dataframe
movies1.to_csv('processed_movies.csv', index=False)