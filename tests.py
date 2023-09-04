import os

os.environ["DATABASE_URL"] = 'postgresql:///cupcakes_test'

from unittest import TestCase

from app import app
from models import db, Cupcake

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image_url": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image_url": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [{
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            cupcake_id = resp.json['cupcake']['id']

            # don't know what ID we'll get, make sure it's an int
            self.assertIsInstance(cupcake_id, int)

            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": cupcake_id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image_url": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)


    def test_patch_cupcake(self):
        """Test updating info of a cupcake already in the database"""
        with app.test_client() as client:
            new_cupcake = {
                "flavor": "vanilla",
                "size" : "small"
            }

            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.patch(url, json=new_cupcake)

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            print(f"\n\n\n\n data is: {data}")
            self.assertEqual(data, {'flavor': 'vanilla', 'id': self.cupcake_id,
                                    'image_url': 'http://test.com/cupcake.jpg',
                                    'rating': 5, 'size': 'small'})



    def test_delete_cupcake(self):
        """Test deletion of the single cupcake in the database"""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.delete(url)

            data = resp.json
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {"deleted": self.cupcake_id})
            self.assertEqual(Cupcake.query.count(), 0)
