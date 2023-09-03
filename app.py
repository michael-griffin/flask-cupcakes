"""Flask app for Cupcakes"""

import os

from flask import Flask, request, jsonify
from models import connect_db, db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///cupcakes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "shhhh"



connect_db(app)


@app.get('/api/cupcakes')
def show_cupcakes():
    cupcakes = Cupcake.query.all()

    #serialize, then return
    serialized = [cupcake.serialize() for cupcake in cupcakes ]
    return jsonify(cupcakes = serialized)


@app.get('/api/cupcakes/<int:id>')
def show_single_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)

    #serialize, then return
    serialized = cupcake.serialize()
    print(f'\n\n\n serialized cupcake is: {serialized}')
    return jsonify(cupcake = serialized)


@app.post('/api/cupcakes')
def add_cupcake():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image_url = request.json['image_url']

    new_cupcake = Cupcake(flavor = flavor,
                          size = size,
                          rating = rating,
                          image_url = image_url)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialized), 201)
