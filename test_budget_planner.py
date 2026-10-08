"""
Automated Test Suite for Smart Grocery Budget Planner
======================================================
Tests all requirements, demo scenarios, calculations, alerts,
and error handling edge cases.
"""

import os
import unittest
from grocery_manager import GroceryManager, CATEGORIES
from data_manager import DataManager, DEFAULT_SAMPLE_DATA


class TestSmartGroceryPlanner(unittest.TestCase):
    def setUp(self):
        """Set up a fresh manager before each test."""
        self.test_file = "test_grocery_data.json"
        self.dm = DataManager(filepath=self.test_file)
        self.gm = GroceryManager(initial_budget=5000.0)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_budget_setting(self):
        """Test setting valid and invalid budgets."""
        success, msg = self.gm.set_budget(6000.0)
        self.assertTrue(success)
        self.assertEqual(self.gm.get_budget(), 6000.0)

        # Invalid: Negative budget
        success, msg = self.gm.set_budget(-500)
        self.assertFalse(success)
        self.assertEqual(self.gm.get_budget(), 6000.0)

        # Invalid: Non-numeric
        success, msg = self.gm.set_budget("abc")
        self.assertFalse(success)

    def test_add_items_and_calculations(self):
        """Test adding items and automatic quantity * price calculation."""
        success, msg, item = self.gm.add_item("Rice", "Grains", 2, 70, "kg")
        self.assertTrue(success)
        self.assertEqual(item["total_price"], 140.0)

        success, msg, item = self.gm.add_item("Milk", "Dairy", 5, 60, "units")
        self.assertTrue(success)
        self.assertEqual(item["total_price"], 300.0)

        self.assertEqual(self.gm.get_total_spent(), 440.0)
        self.assertEqual(self.gm.get_remaining_budget(), 4560.0)
        self.assertEqual(self.gm.get_over_budget_amount(), 0.0)

    def test_data_validation(self):
        """Test invalid inputs rejection."""
        # Empty name
        success, msg, _ = self.gm.add_item("", "Dairy", 2, 50)
        self.assertFalse(success)
        self.assertIn("cannot be empty", msg)

        # Negative quantity
        success, msg, _ = self.gm.add_item("Bread", "Grains", -2, 40)
        self.assertFalse(success)
        self.assertIn("greater than zero", msg)

        # Negative price
        success, msg, _ = self.gm.add_item("Bread", "Grains", 2, -40)
        self.assertFalse(success)
        self.assertIn("greater than zero", msg)

        # Non-numeric quantity
        success, msg, _ = self.gm.add_item("Bread", "Grains", "two", 40)
        self.assertFalse(success)

    def test_update_and_delete_item(self):
        """Test updating and deleting grocery items."""
        _, _, item = self.gm.add_item("Apple", "Fruits", 1, 100)
        item_id = item["id"]

        # Update quantity from 1 to 3
        success, msg = self.gm.update_item(item_id, "Apple", "Fruits", 3, 100)
        self.assertTrue(success)
        updated = self.gm.get_item(item_id)
        self.assertEqual(updated["total_price"], 300.0)

        # Delete item
        success, msg = self.gm.delete_item(item_id)
        self.assertTrue(success)
        self.assertIsNone(self.gm.get_item(item_id))

        # Delete non-existent item
        success, msg = self.gm.delete_item(999)
        self.assertFalse(success)

    def test_budget_warning_and_exceeded_alerts(self):
        """Test 80% warning and 100% exceeded alert thresholds."""
        self.gm.set_budget(1000.0)

        # Under 80%: Spend 700 (70%)
        self.gm.add_item("Item1", "Grains", 7, 100)
        status = self.gm.get_budget_status()
        self.assertEqual(status["level"], "SAFE")
        self.assertEqual(status["percentage"], 70.0)

        # Cross 80%: Spend another 150 (Total 850 -> 85%)
        self.gm.add_item("Item2", "Snacks", 3, 50)
        status = self.gm.get_budget_status()
        self.assertEqual(status["level"], "WARNING")
        self.assertEqual(status["percentage"], 85.0)

        # Cross 100%: Spend another 200 (Total 1050 -> 105%)
        self.gm.add_item("Item3", "Dairy", 2, 100)
        status = self.gm.get_budget_status()
        self.assertEqual(status["level"], "EXCEEDED")
        self.assertEqual(status["over_budget"], 50.0)

    def test_category_breakdown_and_highest(self):
        """Test grouping by category and identifying highest spending category."""
        self.gm.add_item("Rice", "Grains", 2, 70)       # 140
        self.gm.add_item("Milk", "Dairy", 5, 60)        # 300
        self.gm.add_item("Cheese", "Dairy", 2, 200)     # 400 (Total Dairy = 700)
        self.gm.add_item("Apples", "Fruits", 2, 120)    # 240

        cat_stats = self.gm.get_category_spending()
        self.assertEqual(cat_stats["highest_category"], "Dairy")
        self.assertEqual(cat_stats["highest_amount"], 700.0)

    def test_smart_suggestions(self):
        """Test rule-based suggestions engine."""
        self.gm.set_budget(1000.0)
        self.gm.add_item("Expensive TV Snack", "Snacks", 10, 100)  # 1000 spent (100%)
        suggestions = self.gm.get_smart_suggestions()
        self.assertTrue(len(suggestions) > 0)
        # Check that recommendations mention budget threshold or non-essentials
        texts = " ".join(s["text"] for s in suggestions)
        self.assertTrue("Budget" in texts or "Category" in texts or "Snacks" in texts)

    def test_save_and_load_persistence(self):
        """Test complete save to file and load from file."""
        self.gm.set_budget(3500.0)
        self.gm.add_item("Test Bread", "Grains", 2, 45, "units")

        # Save data
        saved, msg = self.dm.save_data(self.gm.get_budget(), self.gm.get_all_items())
        self.assertTrue(saved)
        self.assertTrue(os.path.exists(self.test_file))

        # Reopen and load
        loaded_data, load_msg = self.dm.load_data()
        new_gm = GroceryManager()
        new_gm.load_from_dict(loaded_data)

        self.assertEqual(new_gm.get_budget(), 3500.0)
        self.assertEqual(len(new_gm.get_all_items()), 1)
        self.assertEqual(new_gm.get_all_items()[0]["name"], "Test Bread")
        self.assertEqual(new_gm.get_total_spent(), 90.0)


if __name__ == "__main__":
    unittest.main()
