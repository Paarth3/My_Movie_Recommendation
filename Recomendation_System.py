import pandas as pd
import statistics
from ast import literal_eval

genre_point = 12
director_point = 10
cast_point = 5

df = pd.read_csv('My_Movie_Data.csv')

df['Director(s)'] = df['Director(s)'].apply(literal_eval)
df['Cast'] = df['Cast'].apply(literal_eval)
df['Genres'] = df['Genres'].apply(literal_eval)
df['Keywords'] = df['Keywords'].apply(literal_eval)

user_selected_id = int(input("Please Enter Movie ID: "))

movie_liked = df.loc[user_selected_id].values.tolist()
df_list = df.values.tolist()
df_list.remove(movie_liked)

all_scores = []
for movie in df_list:
    movie_score = 0
    movie_score += movie[2]
    for genre in movie[5]:
        if genre in movie_liked[5]:
            movie_score += genre_point

    for actor in movie[4]:
        if actor in movie_liked[4]:
            movie_score += cast_point
   
    if len(movie[3]) == 1:
        if movie[3][0] in movie_liked[3]:
            movie_score += director_point
    else:
        for director in movie[3]:
            if director in movie_liked[3]:
                movie_score += director_point

    all_scores.append(movie_score)



top_10_index = sorted(range(len(all_scores)), key=lambda i: all_scores[i], reverse=True)[:10]
top_10_movies = [df_list[i][1] for i in top_10_index]

print(f"Current Selected Movie is '{movie_liked[1]}'\n")
print("Similar Movies: ")
for index, top_movie in enumerate(top_10_movies):
    print(f"{index+1}. {top_movie}")