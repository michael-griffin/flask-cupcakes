"""Flask app for Cupcakes"""

import os

from flask import Flask, request, jsonify, render_template
from models import connect_db, db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///cupcakes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhh"


connect_db(app)


###Part Five: homepage for frontend

@app.get('/')
def show_frontend():
    """Set up a template page for JavaScript to populate"""
    return render_template('home.html')


@app.get('/api/cupcakes')
def show_cupcakes():
    """query database for all cupcakes, return list as JSON"""
    cupcakes = Cupcake.query.all()

    print('\n\n\n\n got to overall list')
    serialized = [cupcake.serialize() for cupcake in cupcakes ]
    return jsonify(cupcakes = serialized)


@app.get('/api/cupcakes/<int:id>')
def show_single_cupcake(id):
    """query database for a single cupcake with id, returns as JSON"""
    cupcake = Cupcake.query.get_or_404(id)


    serialized = cupcake.serialize()
    return jsonify(cupcake = serialized)


@app.post('/api/cupcakes')
def add_cupcake():
    """Adds a cupcake and returns the newly created cupcake as JSON"""
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    #need .get to avoid key error, need OR to change "" responses to None so
    #default can be applied.
    image_url = request.json.get('image_url') or None

    new_cupcake = Cupcake(flavor = flavor,
                          size = size,
                          rating = rating,
                          image_url = image_url)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)





############ PART 3:

@app.patch('/api/cupcakes/<int:id>')
def update_cupcake(id):
    """Updates one or more fields of the cupcake matching id"""
    cupcake = Cupcake.query.get_or_404(id)

    #Create a dictionary: default values are the current ones, but
    #updates whenever it can find that key in the JSON.

    #TODO: is there a way to loop over these? It feels strange
    #that I'm making this 'updated' container rather than simply
    #inserting in the loop, but I can't do cupcake['flavor'] right?
    # keys = ['flavor', 'size', 'rating', 'image_url']
    # updated = cupcake.serialize()

    # for key in keys:
    #     new_value = request.json.get(key)
    #     if new_value:
    #         updated[key] = new_value

    # cupcake.size = updated['flavor']
    # cupcake.size = updated['size']
    # cupcake.rating = updated['rating']
    # cupcake.image_url = updated['image_url']


    #TODO: modify, cupcake.flavor = request.json.get(key, cupcake.flavor)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image_url = request.json.get('image_url', cupcake.image_url)

    db.session.commit()

    return jsonify(cupcake.serialize())



@app.delete('/api/cupcakes/<int:id>')
def delete_cupcake(id):
    """Deletes a cupcake. You monster."""
    Cupcake.query.get_or_404(id)

    Cupcake.query.filter(Cupcake.id == id).delete()
    db.session.commit()

    return jsonify({"deleted": id})