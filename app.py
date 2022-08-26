from flask import Flask, render_template, request
import pickle
import requests
import pandas as pd

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
app = Flask(__name__)


def getFilmNames(movies):
    l = []
    for i in movies['title']:
        l.append(i)
    return l

def getEveryThing(movie):
    ind = movies[movies['title'] == movie].index[0]
    l = sorted(list(enumerate(similarity[ind])), reverse=True, key=lambda x: x[1])[1:4]
    recommendations = []
    overviews = []
    posters = []
    homepages = []
    for i in l:
        # recommendations.append(movies.iloc[i[0]].title)
        id_ = movies.iloc[i[0]].id
        movie_data = requests.get(
            f'https://api.themoviedb.org/3/movie/{id_}?api_key=f825c289f80889ef2d85b73b7cd32cca&language=en-US')
        movie_data_js = movie_data.json()
        recommendations.append(movie_data_js['title'])
        overviews.append(movie_data_js['overview'])
        homepages.append(movie_data_js['homepage'])
        posters.append('https://image.tmdb.org/t/p/w500' + movie_data_js['poster_path'])

    return recommendations, overviews, homepages, posters


@app.route('/')
def home():
    l = getFilmNames(movies)
    return render_template('home.html', l=l)


@app.route('/predict', methods=['POST'])
def home_ext():
    l = getFilmNames(movies)
    movie = request.form.get('movie')
    recommendations, overviews, homepages, posters = getEveryThing(movie)
    return render_template('home.html', l=l, recommendations=recommendations,
                           overviews=overviews, homepages=homepages, posters=posters)


if __name__ == '__main__':
    app.run(debug=True)