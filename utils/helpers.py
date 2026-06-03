import json
import os
from faker import Faker

fake = Faker()


def load_test_data(filename: str) -> dict:
    """Load JSON test data from the test-data folder."""
    path = os.path.join(os.path.dirname(__file__), "..", "test-data", filename)
    with open(path) as f:
        return json.load(f)


def generate_user() -> dict:
    """Generate a random user for data-driven tests."""
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "zip_code": fake.zipcode(),
        "email": fake.email(),
    }
