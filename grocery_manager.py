"""
Smart Grocery Budget Planner - Grocery Manager Module
======================================================
Core business logic module implementing budget management, grocery item CRUD operations,
category spending analytics, and rule-based smart shopping recommendations.

Demonstrates core Python concepts:
- Object-Oriented Programming (Class, methods, encapsulation)
- Variables and Data Types (float, int, str, bool, list, dict)
- Control structures (if/elif/else, for loops)
- List and dictionary comprehensions
- Exception handling & data validation
- Formatted string representation
"""

# Supported standard categories
CATEGORIES = [
    "Fruits",
    "Vegetables",
    "Dairy",
    "Grains",
    "Snacks",
    "Beverages",
    "Household",
    "Other"
]

# Supported standard measurement units
MEASUREMENT_UNITS = [
    "units",
    "kg",
    "g",
    "packets",
    "litres",
    "bottles",
    "boxes"
]


class GroceryManager:
    """
    Manages budget settings, grocery items collection, financial calculations,
    and smart shopping recommendations.
    """

    def __init__(self, initial_budget=5000.0):
        """
        Initializes the manager with a budget and an empty list of items.
        """
        self.budget = float(initial_budget)
        self.items = []
        self._next_id = 1

    def set_budget(self, amount):
        """
        Sets a new grocery budget. Validates that the amount is a positive number.

        Parameters:
            amount (float or str): Budget value.

        Returns:
            tuple: (bool, str) -> (Success, message)
        """
        try:
            val = float(amount)
            if val <= 0:
                return False, "Budget must be greater than zero."
            self.budget = round(val, 2)
            return True, f"Budget updated successfully to ₹{self.budget:,.2f}"
        except (ValueError, TypeError):
            return False, "Invalid budget value. Please enter a valid numeric number."

    def get_budget(self):
        """Returns the current budget."""
        return self.budget

    def _generate_next_id(self):
        """Generates an incremental unique ID for new items."""
        if not self.items:
            return 1
        return max(item["id"] for item in self.items) + 1

    def add_item(self, name, category, quantity, price_per_unit, unit="units"):
        """
        Adds a new grocery item to the list with strict validation.

        Parameters:
            name (str): Item name.
            category (str): Category (e.g. Fruits, Vegetables, Dairy, etc.).
            quantity (float or str): Quantity (> 0).
            price_per_unit (float or str): Unit price (> 0).
            unit (str): Unit measurement (kg, units, etc.).

        Returns:
            tuple: (bool, str, dict or None) -> (Success, message, created_item)
        """
        # Validate Item Name
        cleaned_name = str(name).strip() if name else ""
        if not cleaned_name:
            return False, "Item name cannot be empty.", None

        # Validate Category
        cleaned_category = str(category).strip() if category else "Other"
        if cleaned_category not in CATEGORIES:
            cleaned_category = "Other"

        # Validate Unit
        cleaned_unit = str(unit).strip() if unit else "units"

        # Validate Quantity
        try:
            qty = float(quantity)
            if qty <= 0:
                return False, "Quantity must be greater than zero.", None
        except (ValueError, TypeError):
            return False, "Quantity must be a valid positive number.", None

        # Validate Price
        try:
            price = float(price_per_unit)
            if price <= 0:
                return False, "Price per unit must be greater than zero.", None
        except (ValueError, TypeError):
            return False, "Price per unit must be a valid positive number.", None

        # Automatic calculation: total = quantity * price
        total_price = round(qty * price, 2)
        new_id = self._generate_next_id()

        new_item = {
            "id": new_id,
            "name": cleaned_name,
            "category": cleaned_category,
            "quantity": round(qty, 2),
            "unit": cleaned_unit,
            "price_per_unit": round(price, 2),
            "total_price": total_price
        }

        self.items.append(new_item)
        return True, f"Item '{cleaned_name}' added successfully (Total: ₹{total_price:,.2f}).", new_item

    def update_item(self, item_id, name, category, quantity, price_per_unit, unit="units"):
        """
        Updates an existing grocery item by ID.

        Returns:
            tuple: (bool, str) -> (Success, message)
        """
        target_item = self.get_item(item_id)
        if not target_item:
            return False, f"Item with ID {item_id} not found."

        # Validate Item Name
        cleaned_name = str(name).strip() if name else ""
        if not cleaned_name:
            return False, "Item name cannot be empty."

        # Validate Category
        cleaned_category = str(category).strip() if category else "Other"
        if cleaned_category not in CATEGORIES:
            cleaned_category = "Other"

        # Validate Unit
        cleaned_unit = str(unit).strip() if unit else target_item.get("unit", "units")

        # Validate Quantity
        try:
            qty = float(quantity)
            if qty <= 0:
                return False, "Quantity must be greater than zero."
        except (ValueError, TypeError):
            return False, "Quantity must be a valid positive number."

        # Validate Price
        try:
            price = float(price_per_unit)
            if price <= 0:
                return False, "Price per unit must be greater than zero."
        except (ValueError, TypeError):
            return False, "Price per unit must be a valid positive number."

        # Update values and recalculate total
        target_item["name"] = cleaned_name
        target_item["category"] = cleaned_category
        target_item["quantity"] = round(qty, 2)
        target_item["unit"] = cleaned_unit
        target_item["price_per_unit"] = round(price, 2)
        target_item["total_price"] = round(qty * price, 2)

        return True, f"Item '{cleaned_name}' (ID: {item_id}) updated successfully."

    def delete_item(self, item_id):
        """
        Deletes an item from the list by its ID.

        Returns:
            tuple: (bool, str) -> (Success, message)
        """
        for index, item in enumerate(self.items):
            if item["id"] == int(item_id):
                removed = self.items.pop(index)
                return True, f"Item '{removed['name']}' removed from shopping list."
        return False, f"Item with ID {item_id} does not exist."

    def get_item(self, item_id):
        """Finds and returns a single item dictionary by ID, or None if not found."""
        for item in self.items:
            if item["id"] == int(item_id):
                return item
        return None

    def get_all_items(self):
        """Returns a copy of all grocery items."""
        return list(self.items)

    def search_items(self, query):
        """
        Searches items by case-insensitive matching in name or category.

        Parameters:
            query (str): The search term.

        Returns:
            list: List of matching item dictionaries.
        """
        clean_query = str(query).strip().lower()
        if not clean_query:
            return self.get_all_items()

        results = []
        for item in self.items:
            name_match = clean_query in item["name"].lower()
            cat_match = clean_query in item["category"].lower()
            if name_match or cat_match:
                results.append(item)
        return results

    # ==========================================
    # Budget Calculations & Alerts
    # ==========================================

    def get_total_spent(self):
        """Calculates total expense of all items in the list."""
        return round(sum(item["total_price"] for item in self.items), 2)

    def get_remaining_budget(self):
        """Calculates remaining budget (can be negative if over budget)."""
        return round(self.budget - self.get_total_spent(), 2)

    def get_over_budget_amount(self):
        """Calculates over-budget amount (0.0 if within budget)."""
        spent = self.get_total_spent()
        if spent > self.budget:
            return round(spent - self.budget, 2)
        return 0.0

    def get_budget_percentage(self):
        """Calculates percentage of budget used."""
        if self.budget <= 0:
            return 0.0
        return round((self.get_total_spent() / self.budget) * 100, 2)

    def get_budget_status(self):
        """
        Evaluates the current spending against the budget and generates alert state.

        Alert Rules:
        - Spent >= 100%: Status 'EXCEEDED'
        - Spent >= 80%:  Status 'WARNING'
        - Otherwise:     Status 'SAFE'

        Returns:
            dict: {
                'level': 'SAFE' | 'WARNING' | 'EXCEEDED',
                'percentage': float,
                'total_spent': float,
                'remaining': float,
                'over_budget': float,
                'message': str,
                'badge_color': str
            }
        """
        total_spent = self.get_total_spent()
        remaining = self.get_remaining_budget()
        over_budget = self.get_over_budget_amount()
        pct = self.get_budget_percentage()

        if pct >= 100.0:
            level = "EXCEEDED"
            message = (
                f"🚨 BUDGET EXCEEDED! You have spent ₹{total_spent:,.2f} "
                f"({pct:.1f}% of ₹{self.budget:,.2f}). "
                f"You are over budget by ₹{over_budget:,.2f}!"
            )
            badge_color = "#DC2626"  # Red
        elif pct >= 80.0:
            level = "WARNING"
            message = (
                f"⚠️ BUDGET WARNING: You have spent ₹{total_spent:,.2f} "
                f"({pct:.1f}% of ₹{self.budget:,.2f}). "
                f"Only ₹{remaining:,.2f} remaining!"
            )
            badge_color = "#D97706"  # Amber/Orange
        else:
            level = "SAFE"
            message = (
                f"✅ Budget On Track: Spent ₹{total_spent:,.2f} of ₹{self.budget:,.2f} "
                f"({pct:.1f}% used). ₹{remaining:,.2f} remaining."
            )
            badge_color = "#059669"  # Emerald Green

        return {
            "level": level,
            "percentage": pct,
            "total_spent": total_spent,
            "remaining": remaining,
            "over_budget": over_budget,
            "message": message,
            "badge_color": badge_color
        }

    # ==========================================
    # Category Breakdown & Analytics
    # ==========================================

    def get_category_spending(self):
        """
        Groups expenses across all categories, calculates category totals,
        spending percentages, and identifies the highest spending category.

        Returns:
            dict: {
                'breakdown': {category_name: {'total': float, 'count': int, 'percentage': float}},
                'highest_category': str,
                'highest_amount': float
            }
        """
        breakdown = {cat: {"total": 0.0, "count": 0, "percentage": 0.0} for cat in CATEGORIES}
        total_spent = self.get_total_spent()

        for item in self.items:
            cat = item.get("category", "Other")
            if cat not in breakdown:
                breakdown[cat] = {"total": 0.0, "count": 0, "percentage": 0.0}
            breakdown[cat]["total"] = round(breakdown[cat]["total"] + item["total_price"], 2)
            breakdown[cat]["count"] += 1

        # Calculate percentages
        highest_cat = "None"
        highest_amt = 0.0

        for cat, stats in breakdown.items():
            if total_spent > 0:
                stats["percentage"] = round((stats["total"] / total_spent) * 100, 1)
            else:
                stats["percentage"] = 0.0

            if stats["total"] > highest_amt:
                highest_amt = stats["total"]
                highest_cat = cat

        return {
            "breakdown": breakdown,
            "highest_category": highest_cat,
            "highest_amount": highest_amt
        }

    # ==========================================
    # Rule-Based Shopping Suggestions
    # ==========================================

    def get_smart_suggestions(self):
        """
        Generates actionable, rule-based recommendations to help the user
        optimize shopping expenses and avoid budget overruns.

        Rules Implemented:
        1. Over-budget / High spending exhaustion rule -> recommends trimming non-essentials.
        2. Category dominance rule -> flags any category taking > 30% of total budget.
        3. Expensive outlier item rule -> flags individual items consuming > 20% of total budget or > 2x average.
        4. Healthy budget indicator rule.

        Returns:
            list of dict: Each dict has {'type': 'alert'|'warning'|'info'|'success', 'text': str}
        """
        suggestions = []
        total_spent = self.get_total_spent()
        budget = self.budget
        pct = self.get_budget_percentage()
        category_data = self.get_category_spending()

        if not self.items:
            suggestions.append({
                "type": "info",
                "text": "Your shopping list is empty. Add grocery items to see live budget analytics and suggestions."
            })
            return suggestions

        # Rule 1: Budget Thresholds
        if pct >= 100.0:
            over = self.get_over_budget_amount()
            suggestions.append({
                "type": "alert",
                "text": f"🚨 Budget Exceeded: You are over budget by ₹{over:,.2f}. Review and remove or reduce non-essential items immediately."
            })
        elif pct >= 80.0:
            suggestions.append({
                "type": "warning",
                "text": f"⚠️ Budget Alert: You have utilized {pct:.1f}% of your budget. Keep any additional shopping strictly to essentials."
            })

        # Rule 2: Non-essential items check when spending is high (>= 80%)
        if pct >= 80.0:
            non_essential_cats = ["Snacks", "Beverages", "Other"]
            non_essential_items = [
                item for item in self.items if item.get("category") in non_essential_cats
            ]
            if non_essential_items:
                non_essential_cost = sum(item["total_price"] for item in non_essential_items)
                item_names = ", ".join(f"'{i['name']}' (₹{i['total_price']:,.2f})" for i in non_essential_items[:3])
                suggestions.append({
                    "type": "warning",
                    "text": (
                        f"💡 Saving Opportunity: Non-essential items ({item_names}) total ₹{non_essential_cost:,.2f}. "
                        "Removing or lowering these can quickly bring your spending under budget."
                    )
                })

        # Rule 3: Category Dominance Check
        # If any single category consumes > 30% of total budget or > 40% of total spending
        for cat, data in category_data["breakdown"].items():
            if data["total"] > 0:
                cat_budget_pct = (data["total"] / budget * 100) if budget > 0 else 0
                if cat_budget_pct >= 30.0:
                    suggestions.append({
                        "type": "info",
                        "text": (
                            f"📊 Category Notice: '{cat}' accounts for ₹{data['total']:,.2f} "
                            f"({cat_budget_pct:.1f}% of your entire budget). Consider comparing brands or buying in bulk."
                        )
                    })

        # Rule 4: Expensive Outlier Item Check
        # Identify the single most expensive item in terms of total price
        sorted_by_cost = sorted(self.items, key=lambda x: x["total_price"], reverse=True)
        if sorted_by_cost:
            top_item = sorted_by_cost[0]
            avg_item_cost = total_spent / len(self.items) if self.items else 0
            if top_item["total_price"] >= (avg_item_cost * 1.8) and len(self.items) > 1:
                suggestions.append({
                    "type": "info",
                    "text": (
                        f"💎 Cost Outlier: '{top_item['name']}' is your highest single expense at ₹{top_item['total_price']:,.2f} "
                        f"({(top_item['total_price']/total_spent*100):.1f}% of total spending). Check if a smaller quantity suffices."
                    )
                })

        # Rule 5: Healthy Budget Praise
        if pct < 60.0 and len(self.items) >= 3:
            suggestions.append({
                "type": "success",
                "text": f"✅ Great Discipline! You have used only {pct:.1f}% of your budget with ₹{self.get_remaining_budget():,.2f} remaining."
            })

        return suggestions

    # ==========================================
    # State Import/Export Helpers
    # ==========================================

    def load_from_dict(self, data):
        """Loads state from a loaded dictionary."""
        if not isinstance(data, dict):
            return False
        self.budget = float(data.get("budget", 5000.0))
        self.items = list(data.get("items", []))
        return True

    def export_to_dict(self):
        """Exports current state as a dictionary for saving."""
        return {
            "budget": self.budget,
            "items": self.items
        }
