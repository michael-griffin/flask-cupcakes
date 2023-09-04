"""Flask app for Cupcakes"""

import os

from flask import Flask, request, jsonify, render_template, flash
from models import connect_db, db, Cupcake
from forms import AddCupcakeForm

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
    form = AddCupcakeForm()
    return render_template('home.html', form=form)



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


##Handle search?

@app.get('/api/cupcakes/search')
def get_searched_cupcakes():

    search_term = request.args.get('search_term')

    some_cupcakes = Cupcake.query.filter(
        Cupcake.flavor.ilike('%' + search_term + "%")).all()


    #Define a query based on search term
    serialized = [cupcake.serialize() for cupcake in some_cupcakes]
    return jsonify(cupcakes = serialized)