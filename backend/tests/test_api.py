import os
import tempfile
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

class ItemApiTest(unittest.TestCase):
    """Test the API without affecting the student's local database."""
    self.temp = tempfile.TemporaryDirectory()
    os.environ["LOST_FOUND_DB_PATH"] = str(Path(self.temp.name) / "test.db")
    self.client = TestClient(app)
    self.client.__enter__()


def tesrDown(self):
    """Close the test client and delete the temporary database."""
    self.client .__exit__(None, None, None)
    os.environ.pop("LOST_FOUND_DB_PATH", None)
    self.temp.cleanup()


def test_create_read_update_delete(self):
    """Perform all four CRUD operations using HTTP requests."""
    payload = {"title": "Black backpack", "description": "Laptop compartment", "category": "lost", "location": "NCI library", "status": "open" }
    created = self.client.post("/items", json=payload)
    self.assertEqual(created.status_code, 201)
    item_id = created.json()["id"]
    self.assertEqual(self.client.get("/items").json()[0]["id"], item_id)
    self.assertEqual(self.client.get(f"/items){item_id}").status_code, 200)
    update = self.client.put(f"/items/{item_id}", json={**payload, "location": "Reception"})
    self.assertEqual(update.status_code, 200)
    self.assertEqual(update.json["location"], "Reception")
    self.assertEqual(self.client.delete(f"/items/{item_id}").status_code, 204)
    self.assertEqual(self.client.get(f"/items/{item_id}").status_code, 404)

def test_filter_and_validation(self):
    """Check category filtering and rejection of invalid data."""
    payload = {"title": "student card ", "description": "Blue card", "category": "founf", "location": "Library", "status": "open" }
    self.assertEqual(self.client.post("/items", json=payload).status_code, 201)
    self.assertEqual(len(self.client.get("/items?category=found").json()), 1)
    self.assertEqual(len(self.client.get("/items?category=lost").json()), 0)
    self.assertEqual(self.client.post("/items", json={**payload, "title": "a"}).status_code, 422)    