"""
Smart Grocery Budget Planner - Command Line Interface (CLI)
============================================================
Interactive terminal-based application providing the same complete functionality
as the GUI. Ideal for college viva presentations and demonstrating pure Python
console I/O, control flow, loops, and data structures.

Demonstrates:
- Input/Output functions (input, print)
- while loops, for loops
- if/elif/else conditional logic
- String formatting and alignment
- Try/except blocks for robust error handling
"""

import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from grocery_manager import GroceryManager, CATEGORIES, MEASUREMENT_UNITS
from data_manager import DataManager


def print_header(title):
    """Prints a styled section header in the terminal."""
    print("\n" + "=" * 65)
    print(f" {title}")
    print("=" * 65)


def print_table(items):
    """
    Prints grocery items in a clean ASCII table.
    Demonstrates string formatting, padding, and loop iteration.
    """
    if not items:
        print("\n [!] No grocery items found in your list.")
        return

    print("\n" + "-" * 78)
    print(f"{'ID':<4} | {'Item Name':<18} | {'Category':<12} | {'Quantity':<10} | {'Price (₹)':<11} | {'Total (₹)':<12}")
    print("-" * 78)

    for item in items:
        qty_str = f"{item['quantity']} {item.get('unit', '')}".strip()
        print(
            f"{item['id']:<4} | "
            f"{item['name']:<18} | "
            f"{item['category']:<12} | "
            f"{qty_str:<10} | "
            f"₹{item['price_per_unit']:<10.2f} | "
            f"₹{item['total_price']:<11.2f}"
        )
    print("-" * 78)


def display_budget_summary(gm):
    """Displays comprehensive budget summary, alerts, and analytics."""
    print_header("BUDGET SUMMARY & FINANCIAL STATUS")
    budget = gm.get_budget()
    spent = gm.get_total_spent()
    remaining = gm.get_remaining_budget()
    over = gm.get_over_budget_amount()
    pct = gm.get_budget_percentage()
    status = gm.get_budget_status()

    print(f" • Total Budget        : ₹{budget:,.2f}")
    print(f" • Total Spent         : ₹{spent:,.2f}")
    if remaining >= 0:
        print(f" • Remaining Budget    : ₹{remaining:,.2f}")
    else:
        print(f" • OVER BUDGET BY      : ₹{over:,.2f}  [CRITICAL]")
    print(f" • Budget Consumed     : {pct:.1f}%")
    print(f" • Total Items Count   : {len(gm.get_all_items())} items")
    print("-" * 65)
    print(f" Status Alert: {status['message']}")
    print("-" * 65)


def display_category_breakdown(gm):
    """Displays category-wise spending analysis."""
    print_header("CATEGORY-WISE SPENDING BREAKDOWN")
    cat_data = gm.get_category_spending()
    breakdown = cat_data["breakdown"]

    print(f"{'Category':<16} | {'Items':<8} | {'Spent (₹)':<14} | {'Share (%)':<10}")
    print("-" * 55)

    for cat, data in breakdown.items():
        if data["count"] > 0:
            print(f"{cat:<16} | {data['count']:<8} | ₹{data['total']:<12.2f} | {data['percentage']:<9.1f}%")

    print("-" * 55)
    if cat_data["highest_amount"] > 0:
        print(f" 🏆 Highest Spending Category: {cat_data['highest_category']} (₹{cat_data['highest_amount']:,.2f})")
    else:
        print(" Highest Spending Category: None")


def display_suggestions(gm):
    """Displays rule-based smart recommendations."""
    print_header("SMART SHOPPING RECOMMENDATIONS")
    suggestions = gm.get_smart_suggestions()
    for idx, s in enumerate(suggestions, start=1):
        print(f" [{idx}] {s['text']}")


def run_cli():
    """Main interactive CLI loop."""
    dm = DataManager()
    data, load_msg = dm.load_data()
    gm = GroceryManager()
    gm.load_from_dict(data)

    print("\n" + "*" * 65)
    print("      SMART GROCERY BUDGET PLANNER - TERMINAL EDITION")
    print("             College Subject Python Project")
    print("*" * 65)
    print(f" {load_msg}")

    while True:
        print("\n" + "=" * 65)
        print(" MAIN MENU:")
        print(" [1]  View Grocery Shopping List")
        print(" [2]  Add New Grocery Item")
        print(" [3]  Update Existing Grocery Item")
        print(" [4]  Delete Grocery Item")
        print(" [5]  Search Grocery Item")
        print(" [6]  View Budget Summary & Alerts")
        print(" [7]  View Category-wise Spending")
        print(" [8]  View Smart Shopping Suggestions")
        print(" [9]  Set / Modify Budget")
        print(" [10] Save Data to File")
        print(" [11] Reset to College Sample Data")
        print(" [0]  Exit Application")
        print("=" * 65)

        choice = input("Enter your choice (0-11): ").strip()

        if choice == "1":
            print_header("GROCERY SHOPPING LIST")
            items = gm.get_all_items()
            print_table(items)
            print(f" Total Spent: ₹{gm.get_total_spent():,.2f} / ₹{gm.get_budget():,.2f}")

        elif choice == "2":
            print_header("ADD NEW GROCERY ITEM")
            name = input("Enter Item Name: ").strip()
            if not name:
                print(" [!] Error: Item name cannot be empty.")
                continue

            print("\nAvailable Categories:", ", ".join(CATEGORIES))
            cat = input("Enter Category: ").strip()
            if cat not in CATEGORIES:
                cat = "Other"

            qty_in = input("Enter Quantity: ").strip()
            print("Measurement Units:", ", ".join(MEASUREMENT_UNITS))
            unit = input("Enter Unit (e.g., kg, units, packets) [default: units]: ").strip()
            if not unit:
                unit = "units"

            price_in = input("Enter Price per Unit (₹): ").strip()

            success, msg, item = gm.add_item(name, cat, qty_in, price_in, unit)
            if success:
                print(f"\n [✓] {msg}")
                # Auto check alert
                status = gm.get_budget_status()
                if status["level"] in ("WARNING", "EXCEEDED"):
                    print(f"\n [ALERT] {status['message']}")
            else:
                print(f"\n [!] Error: {msg}")

        elif choice == "3":
            print_header("UPDATE EXISTING GROCERY ITEM")
            items = gm.get_all_items()
            print_table(items)
            if not items:
                continue

            id_in = input("Enter the ID of the item to update: ").strip()
            try:
                item_id = int(id_in)
                item = gm.get_item(item_id)
                if not item:
                    print(f" [!] Item with ID {item_id} not found.")
                    continue
            except ValueError:
                print(" [!] Error: ID must be a valid integer number.")
                continue

            print(f"\nUpdating: {item['name']} (Leave blank to keep current value)")
            new_name = input(f"New Name [{item['name']}]: ").strip() or item['name']
            new_cat = input(f"New Category [{item['category']}]: ").strip() or item['category']
            new_qty = input(f"New Quantity [{item['quantity']}]: ").strip() or str(item['quantity'])
            new_unit = input(f"New Unit [{item.get('unit', 'units')}]: ").strip() or item.get('unit', 'units')
            new_price = input(f"New Price [{item['price_per_unit']}]: ").strip() or str(item['price_per_unit'])

            success, msg = gm.update_item(item_id, new_name, new_cat, new_qty, new_price, new_unit)
            if success:
                print(f"\n [✓] {msg}")
            else:
                print(f"\n [!] Error: {msg}")

        elif choice == "4":
            print_header("DELETE GROCERY ITEM")
            items = gm.get_all_items()
            print_table(items)
            if not items:
                continue

            id_in = input("Enter the ID of the item to remove: ").strip()
            try:
                item_id = int(id_in)
            except ValueError:
                print(" [!] Error: ID must be a valid integer number.")
                continue

            item = gm.get_item(item_id)
            if not item:
                print(f" [!] Item with ID {item_id} does not exist.")
                continue

            confirm = input(f"Are you sure you want to delete '{item['name']}'? (y/n): ").strip().lower()
            if confirm == "y":
                success, msg = gm.delete_item(item_id)
                if success:
                    print(f"\n [✓] {msg}")
                else:
                    print(f"\n [!] Error: {msg}")
            else:
                print(" [i] Deletion cancelled.")

        elif choice == "5":
            print_header("SEARCH GROCERY ITEM")
            keyword = input("Enter search keyword (name or category): ").strip()
            results = gm.search_items(keyword)
            print(f"\nFound {len(results)} matching items:")
            print_table(results)

        elif choice == "6":
            display_budget_summary(gm)

        elif choice == "7":
            display_category_breakdown(gm)

        elif choice == "8":
            display_suggestions(gm)

        elif choice == "9":
            print_header("SET GROCERY BUDGET")
            print(f"Current Budget: ₹{gm.get_budget():,.2f}")
            val = input("Enter new budget amount (₹): ").strip()
            success, msg = gm.set_budget(val)
            if success:
                print(f"\n [✓] {msg}")
            else:
                print(f"\n [!] Error: {msg}")

        elif choice == "10":
            print_header("SAVE DATA")
            success, msg = dm.save_data(gm.get_budget(), gm.get_all_items())
            if success:
                print(f" [✓] {msg}")
            else:
                print(f" [!] {msg}")

        elif choice == "11":
            print_header("RESET TO SAMPLE DATA")
            confirm = input("Reset all items and budget to default sample data? (y/n): ").strip().lower()
            if confirm == "y":
                data, msg = dm.reset_to_defaults()
                gm.load_from_dict(data)
                print(f" [✓] {msg}")
            else:
                print(" [i] Reset cancelled.")

        elif choice == "0":
            # Auto-save before exit prompt
            save_on_exit = input("Do you want to save current changes before exiting? (y/n): ").strip().lower()
            if save_on_exit == "y":
                dm.save_data(gm.get_budget(), gm.get_all_items())
                print(" [✓] Data saved.")
            print("\nThank you for using Smart Grocery Budget Planner! Goodbye.\n")
            sys.exit(0)

        else:
            print(" [!] Invalid option. Please select a valid number from the menu.")


if __name__ == "__main__":
    run_cli()
