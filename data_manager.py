"""
Smart Grocery Budget Planner - Data Manager Module
==================================================
Handles saving and loading grocery items and budget settings to/from a JSON file.
Demonstrates:
- File handling (reading/writing files)
- JSON serialization and deserialization
- Exception handling (FileNotFoundError, json.JSONDecodeError, IOError)
- Default sample data initialization
"""

import os
import json

# Default file name for storing grocery information
DEFAULT_DATA_FILE = "grocery_data.json"

# Standard sample data as specified in project requirements
DEFAULT_SAMPLE_DATA = {
    "budget": 5000.0,
    "items": [
        {
            "id": 1,
            "name": "Rice",
            "category": "Grains",
            "quantity": 2.0,
            "unit": "kg",
            "price_per_unit": 70.0,
            "total_price": 140.0
        },
        {
            "id": 2,
            "name": "Milk",
            "category": "Dairy",
            "quantity": 5.0,
            "unit": "units",
            "price_per_unit": 60.0,
            "total_price": 300.0
        },
        {
            "id": 3,
            "name": "Apples",
            "category": "Fruits",
            "quantity": 2.0,
            "unit": "kg",
            "price_per_unit": 120.0,
            "total_price": 240.0
        },
        {
            "id": 4,
            "name": "Vegetables",
            "category": "Vegetables",
            "quantity": 5.0,
            "unit": "units",
            "price_per_unit": 80.0,
            "total_price": 400.0
        },
        {
            "id": 5,
            "name": "Biscuits",
            "category": "Snacks",
            "quantity": 4.0,
            "unit": "packets",
            "price_per_unit": 30.0,
            "total_price": 120.0
        },
        {
            "id": 6,
            "name": "Detergent",
            "category": "Household",
            "quantity": 1.0,
            "unit": "unit",
            "price_per_unit": 250.0,
            "total_price": 250.0
        }
    ]
}


class DataManager:
    """
    Manages persistent storage for the grocery budget application using JSON.
    """

    def __init__(self, filepath=DEFAULT_DATA_FILE):
        """
        Initializes the DataManager with a target JSON file path.
        """
        self.filepath = filepath

    def save_data(self, budget, items):
        """
        Saves the current budget and list of items to the JSON file.

        Parameters:
            budget (float): The grocery budget amount.
            items (list): List of item dictionaries.

        Returns:
            tuple: (bool, str) -> (Success flag, descriptive message)
        """
        data = {
            "budget": float(budget),
            "items": items
        }

        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True, f"Data successfully saved to '{self.filepath}'."
        except PermissionError:
            return False, f"Permission denied while writing to '{self.filepath}'."
        except Exception as e:
            return False, f"Error saving data: {str(e)}"

    def load_data(self):
        """
        Loads budget and grocery items from the JSON file.
        If the file does not exist or is corrupted, initializes with default sample data.

        Returns:
            tuple: (dict, str) -> (Data dictionary with 'budget' and 'items', status message)
        """
        if not os.path.exists(self.filepath):
            # Create the file with sample data if it does not exist yet
            self.save_data(DEFAULT_SAMPLE_DATA["budget"], DEFAULT_SAMPLE_DATA["items"])
            return DEFAULT_SAMPLE_DATA.copy(), "Initial sample data created and loaded."

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Validate loaded data structure
            if not isinstance(data, dict):
                raise ValueError("Root data must be a JSON object/dictionary.")

            budget = float(data.get("budget", 5000.0))
            raw_items = data.get("items", [])

            # Validate and sanitize item records
            valid_items = []
            for idx, item in enumerate(raw_items, start=1):
                if isinstance(item, dict) and "name" in item and "price_per_unit" in item:
                    item_id = int(item.get("id", idx))
                    name = str(item.get("name", "Unknown")).strip()
                    category = str(item.get("category", "Other")).strip()
                    quantity = float(item.get("quantity", 1.0))
                    unit = str(item.get("unit", "units")).strip()
                    price = float(item.get("price_per_unit", 0.0))
                    total = round(quantity * price, 2)

                    valid_items.append({
                        "id": item_id,
                        "name": name,
                        "category": category,
                        "quantity": quantity,
                        "unit": unit,
                        "price_per_unit": price,
                        "total_price": total
                    })

            cleaned_data = {
                "budget": budget,
                "items": valid_items
            }
            return cleaned_data, f"Data successfully loaded from '{self.filepath}'."

        except json.JSONDecodeError:
            # Corrupted JSON handling
            return DEFAULT_SAMPLE_DATA.copy(), "Warning: JSON file corrupted. Loaded default sample data."
        except Exception as e:
            return DEFAULT_SAMPLE_DATA.copy(), f"Warning: Failed to load file ({str(e)}). Loaded default sample data."

    def reset_to_defaults(self):
        """
        Resets data file back to the original college demo sample data.

        Returns:
            tuple: (dict, str)
        """
        self.save_data(DEFAULT_SAMPLE_DATA["budget"], DEFAULT_SAMPLE_DATA["items"])
        return DEFAULT_SAMPLE_DATA.copy(), "Data reset to default college sample values."
