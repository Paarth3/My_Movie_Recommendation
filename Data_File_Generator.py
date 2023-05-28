import pandas as pd
from ast import literal_eval
import statistics


# Reading and creating the base DataFrame
df1 = pd.read_csv('tmdb_5000_movies.csv')
df2 = pd.read_csv('tmdb_5000_credits.csv')
df1 = df1[['genres', 'keywords', 'title', 'vote_count', 'vote_average']]
df2 = df2[['title', 'cast', 'crew']]
df = df1.merge(df2, on='title')


# Weighted Rating formula
weighted_rating = []
V = df['vote_count'].values.tolist()
R = df['vote_average'].values.tolist()
C = statistics.mean(R)
M = df['vote_count'].quantile(0.9)

for i in range(len(V)):
    weighted_rating.append((V[i]/(V[i] + M))*R[i] + (M/(V[i] + M))*C)


# Creating the Base lists
all_genres_list = df['genres'].apply(literal_eval).values.tolist()
all_keywords_list = df['keywords'].apply(literal_eval).values.tolist()
all_cast_list = df['cast'].apply(literal_eval).values.tolist()
all_crew_list = df['crew'].apply(literal_eval).values.tolist()
all_title_list = list(df['title'].values)


# Cleaning all the Lists
new_list_genres = []
new_list_keywords = []
new_list_cast = []
new_list_directors = []

for movie in all_genres_list:
    new_list_genres.append([temp_dict.get('name') for temp_dict in movie])

for movie in all_keywords_list:
    new_list_keywords.append([temp_dict.get('name') for temp_dict in movie])

for movie in all_cast_list:
    new_list_cast.append([temp_dict.get('name') for temp_dict in movie])

for movie in all_crew_list:
    new_list_directors.append([temp_dict.get(
        'name') for temp_dict in movie if str.lower(temp_dict.get('job')) == 'director'])


# Creating New and Clean DataFrame
my_df = pd.DataFrame()
my_df['Title'] = all_title_list
my_df['Weighted_Rating'] = weighted_rating
my_df['Director(s)'] = new_list_directors
my_df['Cast'] = new_list_cast
my_df['Genres'] = new_list_genres
my_df['Keywords'] = new_list_keywords

my_df.sort_values(by=['Weighted_Rating'], inplace=True, ascending=False)
my_df.insert(loc=0, column="Movie_ID", value=range(len(all_title_list)))

my_df.to_csv('My_Movie_Data.csv', encoding='UTF-8', index=False)
