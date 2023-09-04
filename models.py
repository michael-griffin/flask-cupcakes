"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


DEFAULT_IMAGE_URL = "https://tinyurl.com/demo-cupcake"

def connect_db(app): #TODO: add docstring
    app.app_context().push()
    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Cupcake data. defaults to a nice chocolate cupcake it seems.
    flavor, size and rating required"""
    __tablename__ = "cupcakes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    flavor = db.Column(
        db.String(50),
        nullable=False
    )

    size = db.Column(
        db.String(15),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    image_url = db.Column(
        db.String(500),
        nullable=False, #this is ok
        default= DEFAULT_IMAGE_URL
    )

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size" : self.size,
            "rating" : self.rating,
            "image_url" : self.image_url
        }