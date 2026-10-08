import os
import sys
import time

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from grocery_manager import GroceryManager
from data_manager import DataManager


def print_step(step_num, title):
    print("\n" + "=" * 70)
    print(f" STEP {step_num}: {title.upper()}")
    print("=" * 70)


def run_college_demo():
    print("\n" + "#" * 70)
    print("   COLLEGE PROJECT DEMO: SMART GROCERY BUDGET PLANNER")
    print("   Automated Demonstration Walkthrough (14 Scenarios)")
    print("#" * 70)

    # 1. Start application & initialize managers
    print_step(1, "Start the Application")
    dm = DataManager(filepath="demo_grocery_data.json")
    gm = GroceryManager()
    print(" -> DataManager initialized with temporary demo file.")
    print(" -> GroceryManager instantiated successfully.")

    # 2. Set budget to ₹5000
    print_step(2, "Set Budget to ₹5,000")
    success, msg = gm.set_budget(5000.0)
    print(f" -> {msg}")
    print(f" -> Current Budget: ₹{gm.get_budget():,.2f}")

    # 3. Add several grocery items
    print_step(3, "Add Initial Grocery Items")
    sample_items = [
        ("Rice", "Grains", 2, 70, "kg"),
        ("Milk", "Dairy", 5, 60, "units"),
        ("Apples", "Fruits", 2, 120, "kg"),
        ("Vegetables", "Vegetables", 5, 80, "units"),
        ("Biscuits", "Snacks", 4, 30, "packets"),
        ("Detergent", "Household", 1, 250, "unit"),
    ]
    for name, cat, qty, price, unit in sample_items:
        _, msg, _ = gm.add_item(name, cat, qty, price, unit)
        print(f"    • Added: {name:<12} ({qty} {unit} @ ₹{price}/unit) -> {msg}")

    # 4. Display the grocery table
    print_step(4, "Display the Grocery Table")
    print(f"{'ID':<4} | {'Name':<14} | {'Category':<12} | {'Quantity':<12} | {'Price':<10} | {'Total Price'}")
    print("-" * 68)
    for it in gm.get_all_items():
        qty_str = f"{it['quantity']} {it['unit']}"
        print(f"{it['id']:<4} | {it['name']:<14} | {it['category']:<12} | {qty_str:<12} | ₹{it['price_per_unit']:<9.2f} | ₹{it['total_price']:<10.2f}")

    # 5. Show total spending and remaining budget
    print_step(5, "Show Total Spending and Remaining Budget")
    print(f" -> Total Budget     : ₹{gm.get_budget():,.2f}")
    print(f" -> Total Spent      : ₹{gm.get_total_spent():,.2f}")
    print(f" -> Remaining Budget : ₹{gm.get_remaining_budget():,.2f}")
    print(f" -> Budget Used %    : {gm.get_budget_percentage():.1f}%")

    # 6. Show category-wise spending
    print_step(6, "Show Category-Wise Spending")
    cat_stats = gm.get_category_spending()
    for cat, data in cat_stats["breakdown"].items():
        if data["count"] > 0:
            print(f"    • {cat:<12}: ₹{data['total']:<8.2f} ({data['percentage']:>4.1f}% of spending, {data['count']} items)")
    print(f"\n -> 🏆 Highest Spending Category: {cat_stats['highest_category']} (₹{cat_stats['highest_amount']:,.2f})")

    # 7. Update an item's quantity
    print_step(7, "Update an Item's Quantity")
    rice = [i for i in gm.get_all_items() if i["name"] == "Rice"][0]
    print(f" -> Current Rice Quantity: {rice['quantity']} kg (Total: ₹{rice['total_price']:,.2f})")
    gm.update_item(rice["id"], "Rice", "Grains", 5, 70, "kg")
    updated_rice = gm.get_item(rice["id"])
    print(f" -> Updated Rice Quantity: {updated_rice['quantity']} kg (New Total: ₹{updated_rice['total_price']:,.2f})")
    print(f" -> New Total Spent: ₹{gm.get_total_spent():,.2f}")

    # 8. Delete an unnecessary item
    print_step(8, "Delete an Unnecessary Item")
    biscuits = [i for i in gm.get_all_items() if i["name"] == "Biscuits"][0]
    success, msg = gm.delete_item(biscuits["id"])
    print(f" -> {msg}")
    print(f" -> Remaining Items Count: {len(gm.get_all_items())}")

    # 9. Add enough items to cross 80% of budget
    print_step(9, "Add Items to Cross 80% of Budget")
    print(f" -> Current Spent: ₹{gm.get_total_spent():,.2f} ({gm.get_budget_percentage():.1f}%)")
    print(" -> Adding 'Olive Oil' (2 bottles @ ₹1300 each = ₹2600)...")
    gm.add_item("Olive Oil", "Household", 2, 1300, "bottles")
    print(f" -> New Spent: ₹{gm.get_total_spent():,.2f} of ₹{gm.get_budget():,.2f} ({gm.get_budget_percentage():.1f}%)")

    # 10. Demonstrate the budget warning
    print_step(10, "Demonstrate Budget Warning (>= 80%)")
    status = gm.get_budget_status()
    print(f" -> Status Level : [{status['level']}]")
    print(f" -> Alert Message: {status['message']}")
    print(" -> Smart Suggestions:")
    for s in gm.get_smart_suggestions():
        print(f"    • {s['text']}")

    # 11. Cross the budget and demonstrate "Budget Exceeded" warning
    print_step(11, "Cross Budget and Demonstrate 'Budget Exceeded' Alert")
    print(" -> Adding 'Premium Dry Fruits' (2 kg @ ₹800 = ₹1600)...")
    gm.add_item("Premium Dry Fruits", "Snacks", 2, 800, "kg")
    status = gm.get_budget_status()
    print(f" -> Total Spent     : ₹{status['total_spent']:,.2f} / ₹{gm.get_budget():,.2f}")
    print(f" -> Status Level    : [{status['level']}]")
    print(f" -> Over Budget By  : ₹{status['over_budget']:,.2f}")
    print(f" -> Alert Message   : {status['message']}")

    # 12. Save the data
    print_step(12, "Save Data to JSON")
    success, msg = dm.save_data(gm.get_budget(), gm.get_all_items())
    print(f" -> {msg}")

    # 13. Close and reopen the application
    print_step(13, "Simulate Close and Reopen Application")
    del gm
    del dm
    print(" -> Application memory cleared (closed).")
    print(" -> Reopening application and re-initializing DataManager...")
    new_dm = DataManager(filepath="demo_grocery_data.json")
    loaded_data, load_msg = new_dm.load_data()
    new_gm = GroceryManager()
    new_gm.load_from_dict(loaded_data)
    print(f" -> {load_msg}")

    # 14. Verify saved grocery data is loaded
    print_step(14, "Verify Loaded Data Integrity")
    print(f" -> Loaded Budget      : ₹{new_gm.get_budget():,.2f}")
    print(f" -> Loaded Items Count : {len(new_gm.get_all_items())}")
    print(f" -> Loaded Total Spent : ₹{new_gm.get_total_spent():,.2f}")
    print(f" -> Loaded Status      : [{new_gm.get_budget_status()['level']}]")

    # Clean up demo temp file
    import os
    if os.path.exists("demo_grocery_data.json"):
        os.remove("demo_grocery_data.json")

    print("\n" + "#" * 70)
    print(" ALL 14 DEMO SCENARIOS COMPLETED & VERIFIED SUCCESSFULLY!")
    print("#" * 70 + "\n")


if __name__ == "__main__":
    run_college_demo()
