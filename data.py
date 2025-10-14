import random

from generation import Generation

ingredients = [
                "61c0c5a71d1f82001bdaaa6d",
                "61c0c5a71d1f82001bdaaa6f",
                "61c0c5a71d1f82001bdaaa70",
                "61c0c5a71d1f82001bdaaa71",
                "61c0c5a71d1f82001bdaaa72",
                "61c0c5a71d1f82001bdaaa6e",
                "61c0c5a71d1f82001bdaaa73",
                "61c0c5a71d1f82001bdaaa74",
                "61c0c5a71d1f82001bdaaa6c",
                "61c0c5a71d1f82001bdaaa75",
                "61c0c5a71d1f82001bdaaa76",
                "61c0c5a71d1f82001bdaaa77",
                "61c0c5a71d1f82001bdaaa78",
                "61c0c5a71d1f82001bdaaa79",
                "61c0c5a71d1f82001bdaaa7a",
    ]


class Payloads:

    full_user = {
                "email": Generation.email(),
                "password": Generation.password(),
                "name": Generation.user_name()
        }

    missing_email = {
                "password": Generation.password(),
                "name": Generation.user_name()
        }
    missing_password = {
                "email": Generation.email(),
                "name": Generation.user_name()
        }
    missing_user_name = {
                "email": Generation.email(),
                "password": Generation.password()
        }

    with_ingredients = {
        "ingredients": random.choices(ingredients, k=random.randint(1, len(ingredients)))
    }

    without_ingredients = {
        "ingredients": []
    }

    invalid_hash_ingredients = {
        "ingredients": ["61c0c5a71d1ff82001bdaaa72", "61c0c5a71d1f82001bdaaas76",]
    }



class ExpectedResponses:
    EXISTING_USER = {
                "success": False,
                "message": "User already exists"
                }

    RESPONSE_MISSING_FIELD = {
                "success": False,
                "message": "Email, password and name are required fields"
                }

    INVALID_CREDENTIALS = {
                "success": False,
                "message": "email or password are incorrect"
                }

    SUCCESS_DELETE_USER = {
                "success": True,
                "message": "User successfully removed"
            }

    WITHOUT_INGREDIENTS = {
                "success": False,
                "message": "Ingredient ids must be provided"
            }
