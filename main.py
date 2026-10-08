"""
Smart Grocery Budget Planner - Main Application Entry Point
============================================================
Launches the Smart Grocery Budget Planner application.
By default, launches the modern Tkinter Graphical User Interface (GUI).
Can also be launched in terminal mode using the `--cli` argument.

Usage:
    python main.py        -> Starts Tkinter Desktop GUI
    python main.py --cli  -> Starts Command Line Interface (CLI)
"""

import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import tkinter as tk
from tkinter import messagebox

from grocery_manager import GroceryManager
from data_manager import DataManager
from ui import SmartGroceryApp
from cli import run_cli


def launch_gui():
    """Initializes data managers and starts the Tkinter event loop."""
    data_mgr = DataManager()
    data, status_msg = data_mgr.load_data()

    grocery_mgr = GroceryManager()
    grocery_mgr.load_from_dict(data)

    root = tk.Tk()

    # Optional: Set window icon or styling fallback
    try:
        root.iconbitmap(default="")
    except Exception:
        pass

    app = SmartGroceryApp(root, grocery_mgr, data_mgr)

    # Handle graceful window closure
    def on_close():
        # Automatically save current data on closing
        data_mgr.save_data(grocery_mgr.get_budget(), grocery_mgr.get_all_items())
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


def main():
    """Main routing function."""
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--cli", "-c", "cli"):
        # Terminal Mode
        run_cli()
    else:
        # Default Tkinter GUI Mode
        try:
            launch_gui()
        except tk.TclError as e:
            # Fallback if display server is not available
            print(f"[Notice] Tkinter GUI initialization failed ({e}). Falling back to CLI mode...")
            run_cli()


if __name__ == "__main__":
    main()
