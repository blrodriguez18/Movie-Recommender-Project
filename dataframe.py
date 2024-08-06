import pandas as pd
import ast

pd.set_option('display.max_columns', None)

movies = pd.read_csv("/Users/beatrizrodriguez/Desktop/MoviesRecommend/csv/movies_metadata.csv")
keywords = pd.read_csv("/Users/beatrizrodriguez/Desktop/MoviesRecommend/csv/keywords.csv")
credits = pd.read_csv("/Users/beatrizrodriguez/Desktop/MoviesRecommend/csv/credits.csv")

for col in movies.columns:
  movies[col] = movies[col].fillna("0")

def split_dicts(df, col, val):
  big_list = []
  for i in range(len(df)):
    list_of_dicts = ast.literal_eval(df.loc[i, col])
    small_list = []
    if type(list_of_dicts) == list:
      for item in list_of_dicts:
        name = item[val]
        small_list.append(name)
    else:
      small_list.append("None")
    big_list.append(small_list)
  return big_list


genres_fixed = split_dicts(movies, "genres", "name")
movies["genres_fixed"] = genres_fixed
prod_comp_fixed = split_dicts(movies, "production_companies", "name")
movies["prod_comp_fixed"] = prod_comp_fixed
prod_cnt_fixed = split_dicts(movies, "production_countries", "name")
movies["prod_cnt_fixed"] = prod_cnt_fixed
spoke_fixed = split_dicts(movies, "spoken_languages", "name")
movies["spoke_fixed"] = spoke_fixed
kw_fixed = split_dicts(keywords, "keywords", "name")
keywords["kw_fixed"] = kw_fixed
cast_fixed = split_dicts(credits, "cast", "name")
credits["cast_fixed"] = cast_fixed

movies = movies.drop(columns=["genres", "production_companies", "production_countries", "spoken_languages", "belongs_to_collection", "title",
                              "budget", "homepage", "imdb_id", "poster_path", "revenue", "status", "video", "tagline"])

def split_dicts_crew(df, col, val):
  big_list = []
  for i in range(len(df)):
    list_of_dicts = ast.literal_eval(df.loc[i, col])
    small_list = []
    for item in list_of_dicts:
      if item["job"] == "Director":
        name = item[val]
        small_list.append(name)
    big_list.append(small_list)
  return big_list

crew_fixed = split_dicts_crew(credits, "crew", "name")
credits["crew_fixed"] = crew_fixed
keywords = keywords.drop(columns=["keywords"])
credits = credits.drop(columns=["cast", "crew"])

movies["id"] = movies["id"].astype(str)
keywords["id"] = keywords["id"].astype(str)
credits["id"] = credits["id"].astype(str)

movies1 = movies.merge(keywords, how="inner", on="id")
movies1 = movies1.merge(credits, how="inner", on="id")

movies1 = movies1.rename(columns={"genres_fixed": "genres", "prod_comp_fixed": "production_companies", "prod_cnt_fixed": "production_countries",
                        "spoke_fixed": "spoken_languages", "kw_fixed": "keywords", "cast_fixed": "cast", "crew_fixed": "director"})

# list_of_lists = []
# for i in range(len(movies1)):
#     small_list = []
#     for col in ["genres", "keywords", "director", "cast", "spoken_languages"]:
#         new = ast.literal_eval(movies1.loc[i, col])
#         for item in new:
#             small_list.append(item)
#     new2 = movies1.loc[0, "overview"].split()
#     for item2 in new2:
#         small_list.append(item2)
#     list_of_lists.append(small_list)
#
# movies1['combined'] = list_of_lists

movies1.to_csv('/Users/beatrizrodriguez/Desktop/MoviesRecommend/movies1.csv', index=False)
