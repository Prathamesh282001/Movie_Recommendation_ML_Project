from django.shortcuts import render,HttpResponse
import joblib
import pandas as pd
import requests
import pickle

#movie_list = pickle.load(open("./model/movie_list.pkl","rb"))

similarity_score = joblib.load("./model/similarity_score.pkl")
movie_list = pd.read_pickle("./model/movie_list2.pkl")
"""
df = pd.DataFrame(movie_list.title)
print(df) 
print(similarity_score)"""

# Create your views here.
def home(request):
    lst = movie_list.title
    context = {
                "movie_list":lst,
               }
    return render(request,"index.html",context)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster = data["poster_path"]
    poster = "https://image.tmdb.org/t/p/w500/" + poster
    print(poster)
    return poster


# function for showing top 5 recommendation
def recommended_movie_poster(movie_name):
    movie_id = movie_list[movie_list["title"] == movie_name].index[0]
    score = sorted(list(enumerate(similarity_score[movie_id])),reverse=True,key=lambda x:x[1])
    movie_posters = []
    for i in score[0:6]: 
        movie_posters.append(fetch_poster(movie_list.iloc[i[0]]["movie_id"]))

    return movie_posters
 
def recommendation(request): 
    lst = movie_list.title
    
    status = False
    if request.method == "POST":
        movie_name = request.POST.get("search")
        if movie_name:
            poster = recommended_movie_poster(movie_name)
            status = True
        
            context = {
                "poster":poster,
                "movie_list":lst,
                "status":status            }
            return render(request,"index.html",context)

        else:
            context = {
                "movie_list":lst,
                "status":status
            }
            return render(request,"index.html",context)



        



