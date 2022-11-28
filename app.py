from flask import Flask, request, render_template, redirect, url_for, jsonify, make_response
from werkzeug.exceptions import abort

from forms import MovieForm
from models import movies

app = Flask(__name__)
app.config["SECRET_KEY"] = "nunununnu"

@app.route("/movies/", methods=["GET"])
def movie_details2():
    form = MovieForm()
    return render_template("movies.html", form=form,movies=movies.all())

@app.route("/movies/<int:movie_id>", methods=["GET", "POST"])
def movie_details(movie_id):
    movie = movies.get(movie_id - 1)
    form = MovieForm(data=movie)
    if request.method == "POST":
        if form.validate_on_submit():
            movies.update(movie_id - 1, form.data)
            return redirect(url_for("movies_list_api_v1"))

    return render_template("movie.html", form=form, movie_id=movie_id)


@app.route("/api/v1/movies/", methods=["GET"])
def movies_list_api_v1():
    return jsonify(movies.all())


@app.route("/api/v1/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = movies.get(movie_id)
    if not movie:
        abort(404)
    return jsonify({"movie": movie})


@app.route("/api/v1/movies/", methods=["POST"])
def create_movie():
    if not request.json or 'title' not in request.json:
        abort(400)
    movie = {
        'id': movies.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'plot': request.json.get('plot', ""),
        'score': request.json.get('score', ""),
        'my_score': request.json.get('my_score', ""),
        'watched': request.json.get('watched', False),
        'poster': request.json.get('poster', ""),
    }
    movies.create(movie)
    return jsonify({'movie': movie}), 201



@app.route("/api/v1/movies/<int:movie_id>", methods=['DELETE'])
def delete_movie(movie_id):
    result = movies.delete(movie_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    movie = movies.get(movie_id)
    if not movie:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'plot' in data and not isinstance(data.get('plot'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    movie = {
        'title': data.get('title', movie['title']),
        'plot': data.get('plot', movie['plot']),
        'score': data.get('score', movie['score']),
        'my_score': data.get('my_score', movie['my_score']),
        'watched': data.json.get('watched', movie['watched']),
        'poster': data.json.get('poster', movie["poster"]),
    }
    movies.update(movie_id, movie)
    return jsonify({'movie': movie})


@app.errorhandler(400)
def bad_request():
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)
