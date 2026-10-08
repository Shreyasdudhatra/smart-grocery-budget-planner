# 🛒 Smart Grocery Budget Planner

A complete, feature-rich Python application for students and home managers to plan grocery shopping, control expenses, track category-wise distribution, and prevent budget overruns with real-time alerts and rule-based recommendations.

Developed as a **College Python Subject Mini-Project** demonstrating clean object-oriented architecture, modular programming, standard GUI creation with `tkinter`/`ttk`, and JSON persistence without external dependencies.

---

## 📌 Table of Contents
1. [Project Title & Overview](#-project-title--overview)
2. [Problem Statement](#-problem-statement)
3. [Project Objective](#-project-objective)
4. [Key Features](#-key-features)
5. [Technologies Used](#-technologies-used)
6. [Python Concepts Demonstrated](#-python-concepts-demonstrated)
7. [Project Structure](#-project-structure)
8. [Installation & How to Run](#-installation--how-to-run)
9. [How the System Works](#-how-the-system-works)
10. [Sample Output & Demo Run](#-sample-output--demo-run)
11. [Data Validation & Error Handling](#-data-validation--error-handling)
12. [Future Scope](#-future-scope)
13. [College Viva Questions & Answers (15+ Questions)](#-college-viva-questions--answers)

---

## 🏷️ Project Title & Overview
**“Smart Grocery Budget Planner”** is a desktop and command-line grocery expense planning tool designed to eliminate the common issue of unexpected overspending during grocery shopping trips.

---

## 🎯 Problem Statement
People frequently exceed their monthly or weekly grocery budget because:
1. They purchase items on impulse without pre-calculating total item costs (`Quantity × Unit Price`).
2. They lack visibility into total expenditure while compiling their shopping list.
3. They do not realize how much individual categories (such as Snacks or Household items) dominate their budget.
4. Conventional paper notes or plain text files do not provide warning alerts when spending nears or crosses fixed financial limits.

---

## 🎯 Project Objective
1. **Budget Enforcement**: Allow users to set a strict spending cap (e.g., ₹5,000) and track expenditure in real time.
2. **Automated Calculations**: Instantly compute individual item totals, overall spent amounts, remaining balance, and budget utilization percentages.
3. **Threshold Alerts**: Visually notify users when spending hits **80% (Warning)** or **100%+ (Budget Exceeded)** with exact overspent figures.
4. **Category Breakdown**: Categorize expenses (Fruits, Vegetables, Dairy, Grains, Snacks, Beverages, Household, Other) and highlight the highest-spending category.
5. **Intelligent Suggestions**: Provide rule-based tips to trim non-essential expenses and identify cost outliers.
6. **Data Persistence**: Automatically save and restore lists using simple, reliable JSON serialization.

---

## 🌟 Key Features

| Feature | Description |
| :--- | :--- |
| **Budget Management** | Set and update weekly or monthly grocery budgets with positive numeric validation. |
| **Grocery Item CRUD** | Add, View, Edit, and Delete items with Name, Category, Quantity, Unit, and Price. |
| **Automatic Calculation** | Live calculation of `Quantity × Unit Price` and total shopping bill. |
| **Live KPI Dashboard** | Real-time cards showing Budget, Spent, Remaining, % Used, Top Category, and Item Count. |
| **Visual Progress Bar** | Dynamic color-coded progress bar (Green < 80%, Amber 80–99%, Red ≥ 100%). |
| **Multi-Stage Alerts** | Clear warning banner at 80% and critical alert when budget is exceeded. |
| **Category Analytics** | Dedicated breakdown table showing item counts, spend totals, and % shares. |
| **Item Search** | Case-insensitive search filter by item name or category. |
| **Rule-Based Advisor** | Flags expensive outlier items, dominant categories (>30%), and suggests trims. |
| **JSON Storage** | Reads and writes to `grocery_data.json` with sample fallback data. |
| **Dual Interface** | Runs as a modern **Tkinter Desktop GUI** or an interactive **Terminal CLI**. |

---

## 🛠️ Technologies Used
- **Language**: Python 3.8+ (Tested on Python 3.14)
- **GUI Framework**: Python Standard Library `tkinter` & `ttk` (No third-party packages required)
- **Data Serialization**: Standard `json` module
- **Testing**: Python Standard Library `unittest`
- **Platform**: Cross-platform (Windows, macOS, Linux)

---

## 📚 Python Concepts Demonstrated
This project was written specifically for a college programming evaluation and highlights key syllabus concepts:

1. **Variables & Data Types**: Strings, Integers, Floats, Booleans.
2. **Data Structures**:
   - `list`: Storing collections of items and categories.
   - `dict`: Representing structured grocery items, breakdown summaries, and status payloads.
3. **Control Structures**:
   - `if / elif / else`: Threshold checks (80%, 100%), input validations.
   - `for` loops: Iterating through items, computing totals, rendering table rows.
   - `while` loops: Interactive command-line menu loop.
4. **Functions & OOP**:
   - Methods with docstrings and type hints.
   - Modular classes: `GroceryManager`, `DataManager`, and `SmartGroceryApp`.
5. **String Formatting**:
   - F-strings with currency formatting (`₹{amount:,.2f}`) and column padding (`{name:<18}`).
6. **File I/O & Exception Handling**:
   - `with open(...)` context managers with UTF-8 encoding.
   - `try-except` blocks catching `ValueError`, `FileNotFoundError`, and `json.JSONDecodeError`.
7. **Unit Testing**:
   - Automated tests using `unittest.TestCase`.

---

## 📁 Project Structure

```text
Smart_Grocery_Budget_Planner/
│
├── main.py                 # Primary entry point (Launches Tkinter GUI or CLI with --cli)
├── server.py               # Lightweight local Web server (Serves Web Frontend & REST API)
├── index.html              # Modern Web Dashboard Interface (HTML5)
├── style.css               # Modern CSS Design System (Custom palette, responsive grid)
├── app.js                  # Client logic (Dual API & localStorage, live calculations)
├── grocery_manager.py      # Core business logic, calculations, alerts, and suggestions
├── data_manager.py         # File persistence handler (JSON reading/writing)
├── ui.py                   # Tkinter GUI implementation with modern design system
├── cli.py                  # Interactive terminal menu interface (for Viva / CLI demo)
├── demo_walkthrough.py     # 14-step automated presentation scenario script
├── test_budget_planner.py  # Unit test suite verifying all logic and edge cases
├── grocery_data.json       # JSON data storage file (Auto-created with sample data)
├── requirements.txt        # Environment and standard library specifications
└── README.md               # Complete project documentation and Viva prep guide
```

---

## 🚀 Installation & How to Run

### Prerequisites
- Python 3.8 or higher installed on your computer.
- No `pip install` commands are needed because all modules belong to Python's standard library.

### 1. Launching the Modern Web Frontend (Browser Dashboard)
To run the web interface connected with the Python backend:
```bash
python server.py
```
*Your default web browser will automatically open [http://localhost:5000](http://localhost:5000).*
You can also open [index.html](file:///c:/Users/SHREYAS/OneDrive/Desktop/groceries%20budget%20planner/index.html) directly in any browser for standalone offline mode.

### 2. Launching the Desktop GUI (Tkinter)
To run the native desktop application:
```bash
python main.py
```

### 3. Launching the Terminal Interface (CLI Mode)
If you prefer the command line or need to demonstrate pure terminal logic for viva:
```bash
python main.py --cli
```
*or directly:*
```bash
python cli.py
```

### 3. Running the Automated 14-Step Viva Demo Script
To demonstrate all 14 project requirements sequentially:
```bash
python demo_walkthrough.py
```

### 4. Running the Automated Unit Test Suite
To verify code correctness and calculations:
```bash
python test_budget_planner.py
```

---

## ⚙️ How the System Works

```mermaid
flowchart TD
    A[Launch Application] --> B[DataManager loads 'grocery_data.json']
    B --> C{File exists & valid?}
    C -- Yes --> D[Load saved Budget & Items]
    C -- No --> E[Load default Sample Data ₹5,000 & 6 items]
    D --> F[Initialize GroceryManager]
    E --> F
    F --> G[Render Tkinter GUI / Terminal CLI]
    G --> H[User Actions: Add / Edit / Delete / Search / Set Budget]
    H --> I[GroceryManager updates item list]
    I --> J[Automatic Calculations: Spent, Remaining, % Used]
    J --> K{Check Budget Level}
    K -- "< 80%" --> L[Level: SAFE (Green Banner)]
    K -- "80% - 99%" --> M[Level: WARNING (Amber Banner)]
    K -- ">= 100%" --> N[Level: EXCEEDED (Red Banner & Overspent ₹)]
    L --> O[Evaluate Rule-Based Suggestions]
    M --> O
    N --> O
    O --> P[Update Dashboard Cards & Table]
    P --> Q[Save changes to 'grocery_data.json']
```

---

## 📊 Sample Output & Demo Run

### 1. Default College Sample Data
The application starts with the standard college sample dataset:

| # ID | Item Name | Category | Quantity & Unit | Price / Unit (₹) | Total Price (₹) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Rice | Grains | 2.0 kg | ₹70.00 | ₹140.00 |
| 2 | Milk | Dairy | 5.0 units | ₹60.00 | ₹300.00 |
| 3 | Apples | Fruits | 2.0 kg | ₹120.00 | ₹240.00 |
| 4 | Vegetables | Vegetables | 5.0 units | ₹80.00 | ₹400.00 |
| 5 | Biscuits | Snacks | 4.0 packets | ₹30.00 | ₹120.00 |
| 6 | Detergent | Household | 1.0 unit | ₹250.00 | ₹250.00 |

- **Sample Budget**: ₹5,000.00
- **Total Spent**: ₹1,450.00
- **Remaining Budget**: ₹3,550.00
- **Budget Used**: 29.0%
- **Status**: Safe / On Track

### 2. Threshold Warning Demo (Spending ≥ 80%)
When the user adds items totaling over ₹4,000:
```text
⚠️ BUDGET WARNING: You have spent ₹4,140.00 (82.8% of ₹5,000.00). Only ₹860.00 remaining!
```

### 3. Budget Exceeded Demo (Spending ≥ 100%)
When total expenses surpass ₹5,000:
```text
🚨 BUDGET EXCEEDED! You have spent ₹5,740.00 (114.8% of ₹5,000.00). You are over budget by ₹740.00!
```

---

## 🛡️ Data Validation & Error Handling
The application protects against crashes through defensive coding:
1. **Empty Item Name**: Rejects submission with *"Item name cannot be empty."*
2. **Non-Numeric Quantity / Price**: Caught by `ValueError` exceptions and rejected.
3. **Negative or Zero Quantity**: Validated with `qty > 0`.
4. **Negative or Zero Price**: Validated with `price > 0`.
5. **Invalid Budget**: Rejects non-numeric or negative budget inputs.
6. **Missing Selection on Edit/Delete**: Prompts the user to select an item first.
7. **Corrupt JSON File**: Gracefully falls back to default sample data instead of crashing.

---

## 🔮 Future Scope
1. **Receipt OCR Scanner**: Extract item details and prices from supermarket paper receipts using computer vision (`pytesseract`).
2. **Barcode Integration**: Add barcode scanner input to automatically populate item name and price.
3. **Multi-Store Price Comparison**: Compare item prices between local vendors and online delivery platforms (Blinkit, Zepto, BigBasket).
4. **Historical Shopping Trends**: Add SQLite database storage with multi-month charts and inflation analysis.
5. **Export to PDF**: Generate printable shopping checklists with checkboxes for market visits.

---

## 🎓 College Viva Questions & Answers

Here are **16 commonly asked questions** during practical exams and project viva presentations, complete with clear, concise answers:

### Q1: What is the main objective of this project?
**Answer:** The objective is to help consumers plan their grocery shopping within a predefined budget. It prevents overspending by calculating item totals automatically, displaying real-time financial metrics, sending threshold alerts (at 80% and 100%), and providing category-wise spending insights.

### Q2: Why did you choose Python for this project?
**Answer:** Python offers clean syntax, built-in support for data structures (lists, dictionaries), easy JSON file handling, and a built-in GUI library (`tkinter`) that allows building desktop apps without external dependencies.

### Q3: What is the architecture or design pattern followed in this project?
**Answer:** The project follows a **Modular Separation of Concerns** similar to the Model-View-Controller (MVC) pattern:
- **Model / Business Logic**: `grocery_manager.py` manages data structures, calculations, and rules.
- **Storage / Persistence**: `data_manager.py` manages file read/write operations.
- **View / Presentation**: `ui.py` (Tkinter GUI) and `cli.py` (Terminal interface) handle user interaction.
- **Controller / Entry Point**: `main.py` coordinates application startup.

### Q4: How is data stored and retained between application sessions?
**Answer:** Data is stored in a structured JSON file called `grocery_data.json`. The `json.dump()` function serializes Python dictionaries into formatted text upon saving, and `json.load()` deserializes it back into Python objects when the program boots up.

### Q5: Why did you use JSON instead of a relational database like MySQL or SQLite?
**Answer:** For a personal grocery budget planner, a JSON file is lightweight, human-readable, requires zero database configuration or server installation, and handles hierarchical data (such as a budget amount paired with a list of item dictionaries) naturally.

### Q6: How does the application calculate individual item costs and total spending?
**Answer:** For each item, the total cost is calculated as:
$$\text{Total Price} = \text{Quantity} \times \text{Price per Unit}$$
The overall spending is calculated using Python's built-in `sum()` function with a generator expression:
```python
total_spent = sum(item["total_price"] for item in self.items)
```

### Q7: How are the budget alert conditions implemented?
**Answer:** The budget usage percentage is computed as `(total_spent / budget) * 100`. Then, an `if-elif-else` control structure evaluates the threshold:
- If `percentage >= 100.0`: The status is marked as **EXCEEDED**, and the over-budget amount (`total_spent - budget`) is highlighted.
- Else if `percentage >= 80.0`: The status is marked as **WARNING**, prompting the user to limit further purchases.
- Else: The status remains **SAFE**.

### Q8: How does the category breakdown feature work?
**Answer:** Expenses are grouped by iterating through the items list and aggregating totals into a dictionary where keys are category names (e.g., Dairy, Grains, Vegetables) and values store the item count, total expenditure, and percentage share of total spending. The maximum category total is tracked using a comparison loop.

### Q9: How do the smart shopping recommendations work?
**Answer:** It is a **rule-based expert recommendation system** using conditional heuristics:
1. If the budget is exceeded or ≥ 80%, it recommends trimming discretionary categories like *Snacks* and *Beverages*.
2. If any single category consumes more than 30% of the entire budget, it flags that category for bulk-buying or alternatives.
3. If an individual item's cost is more than 1.8 times the average item cost, it flags that item as a cost outlier.

### Q10: How do you handle invalid inputs such as negative prices or letters in quantity fields?
**Answer:** We use Python exception handling (`try-except ValueError`) combined with boundary validation. If a user enters non-numeric text or negative numbers, the exception is caught, the operation is blocked, and an informative error message is displayed to the user via `messagebox.showerror()` in the GUI or an error prompt in the CLI.

### Q11: What GUI components from Tkinter and ttk did you use?
**Answer:**
- `tk.Tk`: Main application window and event loop (`mainloop()`).
- `ttk.Treeview`: Multi-column tables for the grocery list and category breakdown.
- `ttk.Progressbar`: Visual indicator of budget consumption.
- `ttk.Notebook`: Tabbed interface organizing the shopping list, categories, and suggestions.
- `ttk.Combobox`: Dropdown selectors for categories and measurement units.
- `tk.Entry` and `tk.Button`: Text input fields and action triggers.
- `messagebox`: Alert dialogs for confirmations and warnings.

### Q12: What is the purpose of the `_next_id` or item ID attribute?
**Answer:** Every grocery item receives a unique integer ID generated incrementally. This unique key allows items to be updated, retrieved, or deleted reliably even if multiple items share similar names.

### Q13: How does the search functionality work?
**Answer:** The `search_items(query)` method converts both the search query and the item names/categories to lowercase using `.lower()`, and checks for substring containment using Python's `in` operator. Matching items are dynamically repopulated in the Treeview table.

### Q14: How does the application ensure UTF-8 encoding compatibility on Windows command prompts?
**Answer:** On Windows terminals with legacy code pages, special currency symbols (like `₹`) can cause a `UnicodeEncodeError`. We resolve this by calling `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` during startup so characters render smoothly on all consoles.

### Q15: How did you test the application for reliability?
**Answer:** We created an automated test suite in `test_budget_planner.py` using Python's `unittest` module. It tests 8 test cases covering budget updates, input validations, calculations, category aggregations, alert thresholds, rule recommendations, and JSON persistence.

### Q16: How could this project be scaled up for commercial use?
**Answer:** For commercial use, we could integrate a cloud database (PostgreSQL/Firebase), add user authentication for multi-family accounts, implement web/mobile interfaces using FastAPI and React/Flutter, and integrate supermarket APIs for real-time item pricing.

---

## 👨‍💻 Author & Academic Attribution
- **Project**: Smart Grocery Budget Planner
- **Subject**: Python Programming Laboratory Mini Project
- **Language**: Python 3
- **Year**: Academic College Project Submission
