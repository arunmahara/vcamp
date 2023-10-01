import unittest
from unittest.mock import patch, Mock

from django.test import TestCase
from vcamp.apps.user.task.generate_meal import generate_and_save_recipe, generate_and_save_shopping_list

from vcamp.apps.user.models import Recipe, User
from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.services.edenai import EdenAIService
from vcamp.apps.user.task.push_notification import sendPushNotification
from vcamp.apps.user.helpers.models_helper import bulk_create_recipe, create_recipe, get_fcm_token, get_user
from vcamp.apps.user.helpers.generate_dish import generate_meal_plan_form_prompt, generate_recipe_form_prompt, generate_shopping_list_form_prompt


class GenerateAndSaveRecipeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a mock user for testing
        cls.user = User.objects.create(email="testuser@gmail.com")

    @patch("vcamp.apps.user.helpers.models_helper.get_user")  # Mock the get_user function
    @patch("vcamp.apps.user.task.generate_meal.get_preferences")  # Mock the get_preferences function
    @patch("vcamp.apps.user.helpers.generate_dish.generate_recipe_form_prompt")  # Mock the generate_recipe_form_prompt function
    @patch("vcamp.apps.user.services.edenai.EdenAIService.generate_image")  # Mock the generate_image function
    @patch("vcamp.apps.user.helpers.models_helper.create_recipe")  # Mock the create_recipe function
    @patch("vcamp.apps.user.task.generate_meal.notify_user")  # Mock the notify_user function
    def test_generate_and_save_recipe_success(self, mock_notify_user, mock_create_recipe, mock_generate_image, mock_generate_recipe_form_prompt, mock_get_preferences, mock_get_user):
        # Mock the dependencies and their return values
        mock_get_user.return_value = self.user
        mock_get_preferences.return_value = (True, ["preference1"], ["allergy1"], ["dietary_restriction1"])
        mock_generate_recipe_form_prompt.return_value = {
            "recipes": [
                {
                    "name": "Test Recipe",
                    "nutrition": "Nutrition info",
                    "ingredients": ["ingredient1", "ingredient2"],
                    "measurements": ["measurement1", "measurement2"],
                    "process": "Cooking process"
                }
            ]
        }
        mock_generate_image.return_value = "test_image_url"
        
        # Call the function with mock data
        generate_and_save_recipe(user_id=self.user.id, ingredients=["ingredient1", "ingredient2"])
        
        # Assertions
        mock_notify_user.assert_called_with(self.user, "Recipe Is Ready", "Test Recipe", "test_image_url")
        mock_create_recipe.assert_called_with(
            {
                "user_id": self.user.id,
                "name": "Test Recipe",
                "nutrition": "Nutrition info",
                "ingredients": ["ingredient1", "ingredient2"],
                "measurements": ["measurement1", "measurement2"],
                "process": "Cooking process",
                "image_url": "test_image_url",
            }
        )


class GenerateAndSaveShoppingListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a mock user for testing
        cls.user = User.objects.create(email="testuser@gmail.com", week_meal_plan={"ingredients": ["ingredient1", "ingredient2"]})

    @patch("vcamp.apps.user.helpers.models_helper.get_user")  # Mock the get_user function
    @patch("vcamp.apps.user.helpers.generate_dish.generate_shopping_list_form_prompt")  # Mock the generate_recipe_form_prompt function
    @patch("vcamp.apps.user.services.edenai.EdenAIService.generate_image")  # Mock the generate_image function
    @patch("vcamp.apps.user.task.generate_meal.notify_user")  # Mock the get_preferences function
    def test_generate_and_save_shopping_list_success(self, mock_notify_user, mock_generate_image, mock_generate_shopping_list_form_prompt, mock_get_user):
        # Mock the dependencies and their return values
        mock_get_user.return_value = self.user
        mock_generate_shopping_list_form_prompt.return_value = ({
            "ingredient1": {"measurement": "2 gram"},
            "ingredient2": {"measurement": "3 gram"}
        })
        mock_generate_image.return_value = "test_image_url"
        
        # Call the function with mock data
        generate_and_save_shopping_list(user_id=self.user.id)
        
        # Assertions
        self.user.refresh_from_db()
        self.assertEqual(self.user.shopping_list_for_week, {
            "ingredient1": {"image_url": "test_image_url", "measurement": "2 gram"},
            "ingredient2": {"image_url": "test_image_url", "measurement": "2 gram"}
        })
        mock_notify_user.assert_called_with(self.user, "Shopping List Is Ready", "Go to app to view shopping list.")
