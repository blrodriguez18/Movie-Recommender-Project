import streamlit as st
import pandas as pd
import plotly.express as px
import ast
import plotly.graph_objects as go


# explanation expander

st.header("Here are some EDA graphs made with Plotly: ", divider="red")
st.write("")
st.write("")

movies1 = pd.read_csv("/Users/beatrizrodriguez/Desktop/MoviesRecommend/movies1.csv")


# BAR CHART 1
genre_ct_dict = {}
keys_list = genre_ct_dict.keys()

for i in range(len(movies1)):
  thing = ast.literal_eval(movies1.loc[i, "genres"])
  for item in thing:
    if item in keys_list:
      genre_ct_dict[item] += 1
    else:
      genre_ct_dict[item] = 1

# print(genre_ct_dict)

genre_df = pd.DataFrame.from_dict(genre_ct_dict, orient="index")
genre_df = genre_df.reset_index()
genre_df = genre_df.rename(columns={"index": "Genre", 0: "Count"})
genre_df = genre_df.sort_values(by=["Count"], ascending=False)

# print(genre_df.head())

fig1 = px.bar(genre_df, x="Genre", y="Count", color="Count", title="Genre Count")
# ----------------------------------------------------------------------------------------------


# Pie Graph
country_dict = {}
keys_list_2 = country_dict.keys()

for i in range(len(movies1)):
  thing = ast.literal_eval(movies1.loc[i, "production_countries"])
  for item in thing:
    if item in keys_list_2:
      country_dict[item] += 1
    else:
      country_dict[item] = 1

country_df = pd.DataFrame.from_dict(country_dict, orient="index")
country_df = country_df.reset_index()
country_df = country_df.rename(columns={"index": "Prod_Country", 0: "Count"})
country_df = country_df.sort_values(by=["Count"], ascending=False).reset_index()

i_list = []
sum_count = 0

for i in range(len(country_df)):
  if country_df.loc[i, "Count"] < 700:
    sum_count += country_df.loc[i, "Count"]
    i_list.append(i)

country_df_2 = country_df.iloc[:10, :].drop(columns=["index"])
new_row = pd.DataFrame({'Other': [sum_count]})
country_df_2.loc[len(country_df_2)] = ["Other", sum_count]

fig2 = px.pie(country_df_2, values='Count', names='Prod_Country', title='Movie Production Countries')
# ----------------------------------------------------------------------------------------------

# Decade + Popularity
movies_cut = movies1[movies1["release_date"] != '0']
movies_cut['release_date'] = pd.to_datetime(movies_cut['release_date'])
start_year = movies_cut['release_date'].dt.year.min()
end_year = movies_cut['release_date'].dt.year.max()
end_year = (end_year // 10 + 1) * 10 - 1
bins = list(range(start_year, end_year + 1, 10))
labels = [f'{start}-{start+9}' for start in bins[:-1]]
movies_cut['decade'] = pd.cut(movies_cut['release_date'].dt.year, bins=bins, labels=labels, right=False)
decades = pd.DataFrame(movies_cut['decade'].unique(), columns=['decade'])
decades = decades.sort_values(by=["decade"])

pop_list = []
len_list = []

for date_range in decades["decade"]:
    cut_df = movies_cut[movies_cut['decade'] == date_range]
    cut_df['popularity'] = pd.to_numeric(cut_df['popularity'], errors='coerce')
    pop_avg = cut_df['popularity'].mean()
    pop_list.append(pop_avg)
    len_list.append(len(cut_df))

decades["pop_avg"] = pop_list
decades["count"] = len_list

fig3 = px.bar(decades, x=decades['decade'], y=decades["count"], labels={'x':'Decade Range', 'y':'Number of Movies'})

fig4 = go.Figure(fig3)
fig4.add_trace(go.Scatter(x=decades['decade'], y=decades["pop_avg"], name='Popularity Rating Average per Decade', yaxis='y2'))
fig4.update_layout(yaxis2=dict(title='Popularity Ratings', overlaying='y',side='right'),
                    yaxis=dict(title='Movie Count'),
                   title='Decade + Popularity')
# ----------------------------------------------------------------------------------------------




tab1, tab2, tab3 = st.tabs(["Genre Count", "Movie Production Countries", "Decade + Popularity"])

with tab1:
    st.subheader("Number of Movies Categorized into Each :red[Genre]")
    st.plotly_chart(fig1)
with tab2:
    st.subheader("Percentage of Movies Produced in Each :red[Country] (Top 10)")
    st.plotly_chart(fig2)
with tab3:
    st.subheader("Average :red[Popularity Rating] of Movies in Each :red[Decade]")
    st.plotly_chart(fig4)
