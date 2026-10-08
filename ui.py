"""
Smart Grocery Budget Planner - User Interface (Tkinter GUI)
===========================================================
Modern, responsive, and robust desktop GUI built with Python's standard `tkinter` and `ttk`.

Features:
- Live Dashboard cards (Budget, Spent, Remaining, % Used, Top Category, Total Items)
- Real-time Budget Alert Banner (Normal, 80% Warning, 100% Budget Exceeded)
- Add, Edit, Delete, Search grocery items with input validation
- Auto-calculated item totals and live form subtotal preview
- Category-wise spending table and analytics
- Rule-based Smart Shopping Recommendations tab
- Save to JSON & Reset to College Sample Data buttons
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from grocery_manager import CATEGORIES, MEASUREMENT_UNITS


class SmartGroceryApp:
    """
    Main Tkinter Application for the Smart Grocery Budget Planner.
    """

    def __init__(self, root, grocery_manager, data_manager):
        self.root = root
        self.gm = grocery_manager
        self.dm = data_manager

        # Selected item tracking for editing
        self.selected_item_id = None

        # Window configuration
        self.root.title("Smart Grocery Budget Planner - College Mini Project")
        self.root.geometry("1180x760")
        self.root.minsize(1050, 680)

        # Apply Modern Color Theme & Styles
        self._init_theme()

        # Build GUI Components
        self._build_header()
        self._build_alert_banner()
        self._build_kpi_dashboard()
        self._build_main_workspace()
        self._build_status_bar()

        # Initial data load into UI
        self.refresh_ui()

    def _init_theme(self):
        """Initializes ttk styling, color schemes, and fonts."""
        self.colors = {
            "bg": "#F8FAFC",          # Slate 50 (App background)
            "card_bg": "#FFFFFF",     # White (Card backgrounds)
            "header_bg": "#0F172A",   # Slate 900 (Header bar)
            "header_text": "#F8FAFC",
            "primary": "#0D9488",     # Teal 600 (Primary action)
            "primary_dark": "#0F766E",
            "accent": "#3B82F6",      # Blue 500
            "danger": "#EF4444",      # Rose 500 (Delete / Alert)
            "warning": "#F59E0B",     # Amber 500 (80% Warning)
            "success": "#10B981",     # Emerald 500 (Within budget)
            "text_main": "#1E293B",   # Slate 800
            "text_muted": "#64748B",  # Slate 500
            "border": "#E2E8F0",      # Slate 200
            "table_alt": "#F8FAFC"
        }

        self.root.configure(bg=self.colors["bg"])

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Fonts
        self.font_title = ("Segoe UI", 16, "bold")
        self.font_subtitle = ("Segoe UI", 9)
        self.font_card_val = ("Segoe UI", 15, "bold")
        self.font_card_lbl = ("Segoe UI", 9, "bold")
        self.font_section = ("Segoe UI", 11, "bold")
        self.font_bold = ("Segoe UI", 10, "bold")
        self.font_normal = ("Segoe UI", 10)
        self.font_small = ("Segoe UI", 9)

        # Style Treeview
        self.style.configure(
            "Custom.Treeview",
            background="#FFFFFF",
            foreground=self.colors["text_main"],
            fieldbackground="#FFFFFF",
            rowheight=28,
            font=self.font_normal,
            borderwidth=1,
            relief="flat"
        )
        self.style.configure(
            "Custom.Treeview.Heading",
            background="#F1F5F9",
            foreground=self.colors["text_main"],
            font=self.font_bold,
            padding=(6, 6),
            relief="flat"
        )
        self.style.map("Custom.Treeview", background=[("selected", "#CCFBF1")], foreground=[("selected", "#0F766E")])

        # Style Progressbar
        self.style.configure(
            "Safe.Horizontal.TProgressbar",
            troughcolor="#E2E8F0",
            background="#10B981"
        )
        self.style.configure(
            "Warning.Horizontal.TProgressbar",
            troughcolor="#E2E8F0",
            background="#F59E0B"
        )
        self.style.configure(
            "Exceeded.Horizontal.TProgressbar",
            troughcolor="#E2E8F0",
            background="#EF4444"
        )

        # Style Notebook Tabs
        self.style.configure("TNotebook", background=self.colors["bg"], tabmargins=[2, 5, 2, 0])
        self.style.configure("TNotebook.Tab", font=self.font_bold, padding=[16, 8], background="#E2E8F0")
        self.style.map("TNotebook.Tab", background=[("selected", "#FFFFFF")], foreground=[("selected", "#0D9488")])

    # ==========================================
    # Top Header
    # ==========================================

    def _build_header(self):
        """Constructs top branding header bar."""
        header_frame = tk.Frame(self.root, bg=self.colors["header_bg"], height=65)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        # Title & Subtitle
        title_box = tk.Frame(header_frame, bg=self.colors["header_bg"])
        title_box.pack(side=tk.LEFT, padx=20, pady=10)

        title_lbl = tk.Label(
            title_box,
            text="🛒 Smart Grocery Budget Planner",
            font=self.font_title,
            fg=self.colors["header_text"],
            bg=self.colors["header_bg"]
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            title_box,
            text="College Mini Project | Real-Time Expense Monitoring & Smart Recommendations",
            font=self.font_subtitle,
            fg="#94A3B8",
            bg=self.colors["header_bg"]
        )
        sub_lbl.pack(anchor="w")

        # Top Action Buttons
        btn_box = tk.Frame(header_frame, bg=self.colors["header_bg"])
        btn_box.pack(side=tk.RIGHT, padx=20, pady=12)

        save_btn = tk.Button(
            btn_box,
            text="💾 Save Data",
            command=self.on_save_data,
            bg="#0D9488",
            fg="white",
            activebackground="#0F766E",
            activeforeground="white",
            font=self.font_bold,
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=6)

        reset_btn = tk.Button(
            btn_box,
            text="🔄 Sample Data",
            command=self.on_reset_sample_data,
            bg="#475569",
            fg="white",
            activebackground="#334155",
            activeforeground="white",
            font=self.font_normal,
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2"
        )
        reset_btn.pack(side=tk.LEFT, padx=6)

    # ==========================================
    # Dynamic Alert Banner
    # ==========================================

    def _build_alert_banner(self):
        """Banner displaying real-time alert (Safe, Warning 80%, Exceeded 100%)."""
        self.banner_frame = tk.Frame(self.root, bg="#ECFDF5", bd=1, relief="solid")
        self.banner_frame.pack(fill=tk.X, padx=16, pady=(10, 6))

        self.banner_lbl = tk.Label(
            self.banner_frame,
            text="✅ Budget status initialized...",
            font=self.font_bold,
            fg="#047857",
            bg="#ECFDF5",
            pady=7
        )
        self.banner_lbl.pack(fill=tk.X)

    # ==========================================
    # KPI Summary Cards Dashboard
    # ==========================================

    def _build_kpi_dashboard(self):
        """Constructs 6 KPI metric cards."""
        kpi_container = tk.Frame(self.root, bg=self.colors["bg"])
        kpi_container.pack(fill=tk.X, padx=16, pady=4)

        for i in range(6):
            kpi_container.columnconfigure(i, weight=1, uniform="kpi")

        # Card 1: Budget
        self.card_budget_val, _ = self._create_kpi_card(kpi_container, 0, "💰 TOTAL BUDGET", "₹0.00", "#1E293B")
        # Card 2: Total Spent
        self.card_spent_val, _ = self._create_kpi_card(kpi_container, 1, "🛒 TOTAL SPENT", "₹0.00", "#2563EB")
        # Card 3: Remaining / Over
        self.card_remain_val, self.card_remain_title = self._create_kpi_card(
            kpi_container, 2, "⚖️ REMAINING BUDGET", "₹0.00", "#059669"
        )
        # Card 4: Used %
        self.card_used_val, _ = self._create_kpi_card(kpi_container, 3, "📊 BUDGET USED %", "0.0%", "#0D9488")
        # Card 5: Highest Category
        self.card_topcat_val, _ = self._create_kpi_card(kpi_container, 4, "🏷️ TOP CATEGORY", "None", "#7C3AED")
        # Card 6: Total Items
        self.card_items_val, _ = self._create_kpi_card(kpi_container, 5, "📦 TOTAL ITEMS", "0 items", "#475569")

        # Mini Progress Bar under KPI Cards
        prog_frame = tk.Frame(self.root, bg=self.colors["bg"])
        prog_frame.pack(fill=tk.X, padx=16, pady=(2, 6))

        self.budget_progressbar = ttk.Progressbar(
            prog_frame,
            orient="horizontal",
            mode="determinate",
            style="Safe.Horizontal.TProgressbar"
        )
        self.budget_progressbar.pack(fill=tk.X)

    def _create_kpi_card(self, parent, col, title, default_val, val_color):
        """Helper to construct a standardized KPI card."""
        card = tk.Frame(
            parent,
            bg=self.colors["card_bg"],
            bd=1,
            relief="solid",
            highlightthickness=0
        )
        card.grid(row=0, column=col, padx=4, pady=4, sticky="nsew")

        lbl_title = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 8, "bold"),
            fg=self.colors["text_muted"],
            bg=self.colors["card_bg"]
        )
        lbl_title.pack(anchor="w", padx=10, pady=(6, 2))

        lbl_val = tk.Label(
            card,
            text=default_val,
            font=self.font_card_val,
            fg=val_color,
            bg=self.colors["card_bg"]
        )
        lbl_val.pack(anchor="w", padx=10, pady=(0, 6))

        return lbl_val, lbl_title

    # ==========================================
    # Main Workspace (Left Inputs, Right Tabs)
    # ==========================================

    def _build_main_workspace(self):
        """Builds two-column workspace."""
        workspace = tk.Frame(self.root, bg=self.colors["bg"])
        workspace.pack(fill=tk.BOTH, expand=True, padx=16, pady=4)

        # Left Column: Inputs & Forms
        left_col = tk.Frame(workspace, bg=self.colors["bg"], width=350)
        left_col.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_col.pack_propagate(False)

        # Right Column: Notebook Tabs
        right_col = tk.Frame(workspace, bg=self.colors["bg"])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_budget_form(left_col)
        self._build_item_form(left_col)
        self._build_notebook_tabs(right_col)

    # ------------------------------------------
    # Budget Input Form (Left Panel)
    # ------------------------------------------

    def _build_budget_form(self, parent):
        """Section for setting/updating total budget."""
        card = tk.Frame(parent, bg=self.colors["card_bg"], bd=1, relief="solid")
        card.pack(fill=tk.X, pady=(0, 10))

        title = tk.Label(
            card,
            text="💵 Set Grocery Budget",
            font=self.font_section,
            fg=self.colors["text_main"],
            bg=self.colors["card_bg"]
        )
        title.pack(anchor="w", padx=12, pady=(10, 6))

        row = tk.Frame(card, bg=self.colors["card_bg"])
        row.pack(fill=tk.X, padx=12, pady=(0, 10))

        tk.Label(
            row,
            text="Budget (₹):",
            font=self.font_normal,
            bg=self.colors["card_bg"]
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.entry_budget = tk.Entry(
            row,
            font=self.font_normal,
            width=12,
            relief="solid",
            bd=1
        )
        self.entry_budget.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        self.entry_budget.insert(0, str(int(self.gm.get_budget())))

        set_btn = tk.Button(
            row,
            text="Set",
            command=self.on_set_budget,
            bg="#0D9488",
            fg="white",
            activebackground="#0F766E",
            activeforeground="white",
            font=self.font_bold,
            relief="flat",
            padx=10,
            cursor="hand2"
        )
        set_btn.pack(side=tk.RIGHT)

    # ------------------------------------------
    # Item Entry / Edit Form (Left Panel)
    # ------------------------------------------

    def _build_item_form(self, parent):
        """Card for adding or modifying grocery items."""
        card = tk.Frame(parent, bg=self.colors["card_bg"], bd=1, relief="solid")
        card.pack(fill=tk.BOTH, expand=True)

        self.form_title_lbl = tk.Label(
            card,
            text="➕ Add Grocery Item",
            font=self.font_section,
            fg=self.colors["text_main"],
            bg=self.colors["card_bg"]
        )
        self.form_title_lbl.pack(anchor="w", padx=12, pady=(10, 4))

        self.edit_indicator_lbl = tk.Label(
            card,
            text="Mode: Adding new item",
            font=self.font_small,
            fg=self.colors["text_muted"],
            bg=self.colors["card_bg"]
        )
        self.edit_indicator_lbl.pack(anchor="w", padx=12, pady=(0, 8))

        form_fields = tk.Frame(card, bg=self.colors["card_bg"])
        form_fields.pack(fill=tk.X, padx=12)

        # Field: Item Name
        tk.Label(form_fields, text="Item Name *", font=self.font_bold, bg=self.colors["card_bg"]).pack(anchor="w", pady=(2, 2))
        self.entry_name = tk.Entry(form_fields, font=self.font_normal, relief="solid", bd=1)
        self.entry_name.pack(fill=tk.X, pady=(0, 6))

        # Field: Category
        tk.Label(form_fields, text="Category *", font=self.font_bold, bg=self.colors["card_bg"]).pack(anchor="w", pady=(2, 2))
        self.combo_category = ttk.Combobox(
            form_fields,
            values=CATEGORIES,
            font=self.font_normal,
            state="readonly"
        )
        self.combo_category.current(0)
        self.combo_category.pack(fill=tk.X, pady=(0, 6))

        # Field: Quantity & Unit (Side by side)
        qty_unit_frame = tk.Frame(form_fields, bg=self.colors["card_bg"])
        qty_unit_frame.pack(fill=tk.X, pady=(2, 6))

        # Quantity
        qty_box = tk.Frame(qty_unit_frame, bg=self.colors["card_bg"])
        qty_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        tk.Label(qty_box, text="Quantity *", font=self.font_bold, bg=self.colors["card_bg"]).pack(anchor="w")
        self.entry_qty = tk.Entry(qty_box, font=self.font_normal, relief="solid", bd=1)
        self.entry_qty.pack(fill=tk.X, pady=(2, 0))
        self.entry_qty.insert(0, "1")
        self.entry_qty.bind("<KeyRelease>", self._update_live_subtotal)

        # Unit
        unit_box = tk.Frame(qty_unit_frame, bg=self.colors["card_bg"])
        unit_box.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))
        tk.Label(unit_box, text="Unit", font=self.font_bold, bg=self.colors["card_bg"]).pack(anchor="w")
        self.combo_unit = ttk.Combobox(
            unit_box,
            values=MEASUREMENT_UNITS,
            font=self.font_normal,
            state="readonly",
            width=8
        )
        self.combo_unit.current(0)
        self.combo_unit.pack(fill=tk.X, pady=(2, 0))

        # Field: Price per unit
        tk.Label(form_fields, text="Price per Unit (₹) *", font=self.font_bold, bg=self.colors["card_bg"]).pack(anchor="w", pady=(2, 2))
        self.entry_price = tk.Entry(form_fields, font=self.font_normal, relief="solid", bd=1)
        self.entry_price.pack(fill=tk.X, pady=(0, 6))
        self.entry_price.bind("<KeyRelease>", self._update_live_subtotal)

        # Real-time subtotal calculation preview
        self.lbl_subtotal_preview = tk.Label(
            card,
            text="Estimated Total: ₹0.00",
            font=self.font_bold,
            fg="#0D9488",
            bg="#F0FDFA",
            pady=4,
            relief="solid",
            bd=1
        )
        self.lbl_subtotal_preview.pack(fill=tk.X, padx=12, pady=6)

        # Action Buttons
        btn_frame = tk.Frame(card, bg=self.colors["card_bg"])
        btn_frame.pack(fill=tk.X, padx=12, pady=(6, 12))

        self.btn_add = tk.Button(
            btn_frame,
            text="➕ Add Item",
            command=self.on_add_item,
            bg="#0D9488",
            fg="white",
            activebackground="#0F766E",
            activeforeground="white",
            font=self.font_bold,
            relief="flat",
            pady=6,
            cursor="hand2"
        )
        self.btn_add.pack(fill=tk.X, pady=(0, 4))

        self.btn_update = tk.Button(
            btn_frame,
            text="✏️ Update Item",
            command=self.on_update_item,
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            font=self.font_bold,
            relief="flat",
            pady=6,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.btn_update.pack(fill=tk.X, pady=(0, 4))

        self.btn_clear = tk.Button(
            btn_frame,
            text="🧹 Clear Form",
            command=self.clear_form,
            bg="#E2E8F0",
            fg=self.colors["text_main"],
            activebackground="#CBD5E1",
            font=self.font_normal,
            relief="flat",
            pady=4,
            cursor="hand2"
        )
        self.btn_clear.pack(fill=tk.X)

    def _update_live_subtotal(self, event=None):
        """Live calculation of Qty x Price in the input form."""
        try:
            qty = float(self.entry_qty.get().strip())
            price = float(self.entry_price.get().strip())
            total = qty * price
            self.lbl_subtotal_preview.config(text=f"Estimated Total: ₹{total:,.2f}")
        except Exception:
            self.lbl_subtotal_preview.config(text="Estimated Total: --")

    # ------------------------------------------
    # Right Side Notebook Tabs
    # ------------------------------------------

    def _build_notebook_tabs(self, parent):
        """Constructs Notebook containing Shopping List, Categories, and Suggestions."""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Shopping List Table
        tab_list = tk.Frame(self.notebook, bg=self.colors["card_bg"])
        self.notebook.add(tab_list, text="📋 Grocery Shopping List")
        self._build_table_tab(tab_list)

        # Tab 2: Category Spending
        tab_categories = tk.Frame(self.notebook, bg=self.colors["card_bg"])
        self.notebook.add(tab_categories, text="📊 Category Breakdown")
        self._build_categories_tab(tab_categories)

        # Tab 3: Smart Suggestions
        tab_suggestions = tk.Frame(self.notebook, bg=self.colors["card_bg"])
        self.notebook.add(tab_suggestions, text="💡 Smart Suggestions")
        self._build_suggestions_tab(tab_suggestions)

    # ------------------------------------------
    # Tab 1: Grocery Table View & Search
    # ------------------------------------------

    def _build_table_tab(self, parent):
        """Constructs table with Search, Treeview, and Action buttons."""
        # Top Search Bar
        search_frame = tk.Frame(parent, bg=self.colors["card_bg"], pady=8, padx=10)
        search_frame.pack(fill=tk.X)

        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=self.font_bold,
            bg=self.colors["card_bg"]
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.entry_search = tk.Entry(
            search_frame,
            font=self.font_normal,
            width=24,
            relief="solid",
            bd=1
        )
        self.entry_search.pack(side=tk.LEFT, padx=(0, 6))
        self.entry_search.bind("<KeyRelease>", lambda e: self.on_search())

        btn_search = tk.Button(
            search_frame,
            text="Search",
            command=self.on_search,
            bg="#0D9488",
            fg="white",
            relief="flat",
            padx=10,
            cursor="hand2"
        )
        btn_search.pack(side=tk.LEFT, padx=2)

        btn_clear_search = tk.Button(
            search_frame,
            text="Clear",
            command=self.on_clear_search,
            bg="#E2E8F0",
            fg=self.colors["text_main"],
            relief="flat",
            padx=8,
            cursor="hand2"
        )
        btn_clear_search.pack(side=tk.LEFT, padx=4)

        # Action Buttons on Right of Search Bar
        self.btn_table_delete = tk.Button(
            search_frame,
            text="🗑️ Delete Item",
            command=self.on_delete_item,
            bg="#EF4444",
            fg="white",
            activebackground="#DC2626",
            activeforeground="white",
            font=self.font_bold,
            relief="flat",
            padx=10,
            cursor="hand2"
        )
        self.btn_table_delete.pack(side=tk.RIGHT, padx=4)

        self.btn_table_edit = tk.Button(
            search_frame,
            text="✏️ Edit Selected",
            command=self.on_select_item_for_edit,
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            font=self.font_bold,
            relief="flat",
            padx=10,
            cursor="hand2"
        )
        self.btn_table_edit.pack(side=tk.RIGHT, padx=4)

        # Table & Scrollbars Container
        tree_container = tk.Frame(parent, bg=self.colors["card_bg"])
        tree_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 6))

        cols = ("id", "name", "category", "quantity", "price", "total")
        self.tree = ttk.Treeview(
            tree_container,
            columns=cols,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        # Headings and column properties
        self.tree.heading("id", text="# ID")
        self.tree.heading("name", text="Item Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("quantity", text="Quantity & Unit")
        self.tree.heading("price", text="Price / Unit (₹)")
        self.tree.heading("total", text="Total Price (₹)")

        self.tree.column("id", width=55, anchor="center")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("category", width=110, anchor="w")
        self.tree.column("quantity", width=110, anchor="center")
        self.tree.column("price", width=110, anchor="e")
        self.tree.column("total", width=120, anchor="e")

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        tree_container.rowconfigure(0, weight=1)
        tree_container.columnconfigure(0, weight=1)

        # Event: Row click selects item
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_row_click)
        self.tree.bind("<Double-1>", lambda e: self.on_select_item_for_edit())

        # Table Footer
        footer = tk.Frame(parent, bg=self.colors["card_bg"], padx=10, pady=4)
        footer.pack(fill=tk.X)

        self.lbl_table_count = tk.Label(
            footer,
            text="Showing 0 items",
            font=self.font_small,
            fg=self.colors["text_muted"],
            bg=self.colors["card_bg"]
        )
        self.lbl_table_count.pack(side=tk.LEFT)

        tk.Label(
            footer,
            text="Tip: Click a row to load it into the edit form. Double-click or click 'Edit Selected'.",
            font=self.font_small,
            fg="#94A3B8",
            bg=self.colors["card_bg"]
        ).pack(side=tk.RIGHT)

    # ------------------------------------------
    # Tab 2: Category Breakdown
    # ------------------------------------------

    def _build_categories_tab(self, parent):
        """Shows category totals, share percentages, and top category."""
        header_box = tk.Frame(parent, bg=self.colors["card_bg"], padx=16, pady=12)
        header_box.pack(fill=tk.X)

        tk.Label(
            header_box,
            text="Category-Wise Expense Breakdown",
            font=self.font_section,
            fg=self.colors["text_main"],
            bg=self.colors["card_bg"]
        ).pack(anchor="w")

        self.lbl_top_category_banner = tk.Label(
            header_box,
            text="Highest Spending Category: None",
            font=self.font_bold,
            fg="#7C3AED",
            bg="#F5F3FF",
            padx=12,
            pady=6,
            relief="solid",
            bd=1
        )
        self.lbl_top_category_banner.pack(anchor="w", pady=(6, 0))

        # Categories Table
        cat_tree_box = tk.Frame(parent, bg=self.colors["card_bg"], padx=16, pady=6)
        cat_tree_box.pack(fill=tk.BOTH, expand=True)

        cols = ("category", "count", "spent", "share")
        self.tree_categories = ttk.Treeview(
            cat_tree_box,
            columns=cols,
            show="headings",
            style="Custom.Treeview",
            height=9
        )

        self.tree_categories.heading("category", text="Category")
        self.tree_categories.heading("count", text="Item Count")
        self.tree_categories.heading("spent", text="Total Spent (₹)")
        self.tree_categories.heading("share", text="Share of Total Spending (%)")

        self.tree_categories.column("category", width=160, anchor="w")
        self.tree_categories.column("count", width=100, anchor="center")
        self.tree_categories.column("spent", width=140, anchor="e")
        self.tree_categories.column("share", width=180, anchor="center")

        self.tree_categories.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------
    # Tab 3: Smart Shopping Suggestions
    # ------------------------------------------

    def _build_suggestions_tab(self, parent):
        """Displays rule-based smart shopping tips."""
        header_box = tk.Frame(parent, bg=self.colors["card_bg"], padx=16, pady=12)
        header_box.pack(fill=tk.X)

        tk.Label(
            header_box,
            text="💡 Smart Shopping Recommendations & Tips",
            font=self.font_section,
            fg=self.colors["text_main"],
            bg=self.colors["card_bg"]
        ).pack(anchor="w")

        tk.Label(
            header_box,
            text="Rule-based insights to help you stick to your grocery budget and save money.",
            font=self.font_small,
            fg=self.colors["text_muted"],
            bg=self.colors["card_bg"]
        ).pack(anchor="w")

        # Scrollable Suggestions List
        self.suggestions_container = tk.Frame(parent, bg=self.colors["card_bg"], padx=16, pady=6)
        self.suggestions_container.pack(fill=tk.BOTH, expand=True)

        self.sugg_canvas = tk.Canvas(self.suggestions_container, bg=self.colors["card_bg"], highlightthickness=0)
        self.sugg_scrollbar = ttk.Scrollbar(self.suggestions_container, orient=tk.VERTICAL, command=self.sugg_canvas.yview)
        self.sugg_scrollable_frame = tk.Frame(self.sugg_canvas, bg=self.colors["card_bg"])

        self.sugg_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.sugg_canvas.configure(scrollregion=self.sugg_canvas.bbox("all"))
        )

        self.sugg_canvas.create_window((0, 0), window=self.sugg_scrollable_frame, anchor="nw")
        self.sugg_canvas.configure(yscrollcommand=self.sugg_scrollbar.set)

        self.sugg_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sugg_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ==========================================
    # Bottom Status Bar
    # ==========================================

    def _build_status_bar(self):
        """Constructs bottom status bar."""
        status_bar = tk.Frame(self.root, bg="#E2E8F0", height=24)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.lbl_status_msg = tk.Label(
            status_bar,
            text="Ready | Data loaded successfully",
            font=self.font_small,
            fg=self.colors["text_muted"],
            bg="#E2E8F0"
        )
        self.lbl_status_msg.pack(side=tk.LEFT, padx=12)

        credit_lbl = tk.Label(
            status_bar,
            text="Smart Grocery Budget Planner • College Subject Project",
            font=self.font_small,
            fg=self.colors["text_muted"],
            bg="#E2E8F0"
        )
        credit_lbl.pack(side=tk.RIGHT, padx=12)

    # ==========================================
    # Event Handlers & User Actions
    # ==========================================

    def on_set_budget(self):
        """Updates total budget with validation."""
        val = self.entry_budget.get().strip()
        success, msg = self.gm.set_budget(val)
        if success:
            self.refresh_ui()
            self.lbl_status_msg.config(text=msg)
            messagebox.showinfo("Budget Updated", msg)
        else:
            messagebox.showerror("Invalid Budget", msg)

    def on_add_item(self):
        """Validates input fields and adds a new grocery item."""
        name = self.entry_name.get().strip()
        cat = self.combo_category.get()
        qty = self.entry_qty.get().strip()
        unit = self.combo_unit.get()
        price = self.entry_price.get().strip()

        success, msg, item = self.gm.add_item(name, cat, qty, price, unit)
        if success:
            self.clear_form()
            self.refresh_ui()
            self.lbl_status_msg.config(text=msg)

            # Auto check budget alert immediately
            status = self.gm.get_budget_status()
            if status["level"] == "EXCEEDED":
                messagebox.showwarning("Budget Exceeded", status["message"])
            elif status["level"] == "WARNING":
                messagebox.showwarning("Budget Warning", status["message"])
        else:
            messagebox.showerror("Validation Error", msg)

    def on_update_item(self):
        """Updates the selected item with values from form."""
        if self.selected_item_id is None:
            messagebox.showwarning("No Selection", "Please select an item from the list to update.")
            return

        name = self.entry_name.get().strip()
        cat = self.combo_category.get()
        qty = self.entry_qty.get().strip()
        unit = self.combo_unit.get()
        price = self.entry_price.get().strip()

        success, msg = self.gm.update_item(self.selected_item_id, name, cat, qty, price, unit)
        if success:
            self.clear_form()
            self.refresh_ui()
            self.lbl_status_msg.config(text=msg)
            messagebox.showinfo("Item Updated", msg)
        else:
            messagebox.showerror("Update Error", msg)

    def on_delete_item(self):
        """Deletes selected item after confirmation."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item in the table to delete.")
            return

        item_values = self.tree.item(selected[0], "values")
        item_id = int(item_values[0])
        item_name = item_values[1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to remove '{item_name}' (ID: {item_id}) from your shopping list?"
        )
        if confirm:
            success, msg = self.gm.delete_item(item_id)
            if success:
                if self.selected_item_id == item_id:
                    self.clear_form()
                self.refresh_ui()
                self.lbl_status_msg.config(text=msg)
            else:
                messagebox.showerror("Error", msg)

    def _on_tree_row_click(self, event):
        """Single click on row loads values into form."""
        selected = self.tree.selection()
        if not selected:
            return
        item_values = self.tree.item(selected[0], "values")
        item_id = int(item_values[0])
        item = self.gm.get_item(item_id)
        if item:
            self.populate_form_with_item(item)

    def on_select_item_for_edit(self):
        """Puts the form into edit mode for selected item."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item in the list to edit.")
            return
        item_values = self.tree.item(selected[0], "values")
        item_id = int(item_values[0])
        item = self.gm.get_item(item_id)
        if item:
            self.populate_form_with_item(item)
            self.entry_name.focus_set()

    def populate_form_with_item(self, item):
        """Populates the input form fields with an item's data."""
        self.selected_item_id = item["id"]
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, item["name"])

        if item["category"] in CATEGORIES:
            self.combo_category.set(item["category"])

        self.entry_qty.delete(0, tk.END)
        self.entry_qty.insert(0, str(item["quantity"]))

        if item.get("unit") in MEASUREMENT_UNITS:
            self.combo_unit.set(item["unit"])

        self.entry_price.delete(0, tk.END)
        self.entry_price.insert(0, str(item["price_per_unit"]))

        self._update_live_subtotal()

        # Update Form Headers & Button State
        self.form_title_lbl.config(text=f"✏️ Edit Item #{item['id']}")
        self.edit_indicator_lbl.config(text=f"Currently Editing: {item['name']} (ID: {item['id']})", fg="#2563EB")
        self.btn_update.config(state=tk.NORMAL)
        self.btn_add.config(state=tk.DISABLED)

    def clear_form(self):
        """Clears all input fields and resets to 'Add Item' mode."""
        self.selected_item_id = None
        self.entry_name.delete(0, tk.END)
        self.combo_category.current(0)
        self.entry_qty.delete(0, tk.END)
        self.entry_qty.insert(0, "1")
        self.combo_unit.current(0)
        self.entry_price.delete(0, tk.END)
        self.lbl_subtotal_preview.config(text="Estimated Total: ₹0.00")

        self.form_title_lbl.config(text="➕ Add Grocery Item")
        self.edit_indicator_lbl.config(text="Mode: Adding new item", fg=self.colors["text_muted"])
        self.btn_update.config(state=tk.DISABLED)
        self.btn_add.config(state=tk.NORMAL)

    def on_search(self):
        """Filters table by search keyword in name or category."""
        keyword = self.entry_search.get().strip()
        matched = self.gm.search_items(keyword)
        self._populate_table(matched)

    def on_clear_search(self):
        """Clears search filter and restores full list."""
        self.entry_search.delete(0, tk.END)
        self._populate_table(self.gm.get_all_items())

    def on_save_data(self):
        """Saves current state to JSON file."""
        success, msg = self.dm.save_data(self.gm.get_budget(), self.gm.get_all_items())
        if success:
            self.lbl_status_msg.config(text=msg)
            messagebox.showinfo("Saved Successfully", msg)
        else:
            messagebox.showerror("Save Error", msg)

    def on_reset_sample_data(self):
        """Resets application data to default sample values."""
        confirm = messagebox.askyesno(
            "Reset Sample Data",
            "Are you sure you want to reset all items and budget to the default college demo sample data?"
        )
        if confirm:
            data, msg = self.dm.reset_to_defaults()
            self.gm.load_from_dict(data)
            self.clear_form()
            self.refresh_ui()
            self.lbl_status_msg.config(text=msg)
            messagebox.showinfo("Sample Data Loaded", msg)

    # ==========================================
    # Full UI Refresh & Data Binding
    # ==========================================

    def refresh_ui(self):
        """Refreshes all cards, alert banners, tables, and suggestions."""
        # 1. Update KPI Cards & Progress Bar
        budget = self.gm.get_budget()
        spent = self.gm.get_total_spent()
        remaining = self.gm.get_remaining_budget()
        over = self.gm.get_over_budget_amount()
        pct = self.gm.get_budget_percentage()
        items = self.gm.get_all_items()
        cat_stats = self.gm.get_category_spending()

        self.card_budget_val.config(text=f"₹{budget:,.2f}")
        self.card_spent_val.config(text=f"₹{spent:,.2f}")

        if remaining >= 0:
            self.card_remain_title.config(text="⚖️ REMAINING BUDGET")
            self.card_remain_val.config(text=f"₹{remaining:,.2f}", fg="#059669")
        else:
            self.card_remain_title.config(text="🚨 OVER BUDGET")
            self.card_remain_val.config(text=f"-₹{over:,.2f}", fg="#DC2626")

        self.card_used_val.config(text=f"{pct:.1f}%")
        if pct >= 100.0:
            self.card_used_val.config(fg="#DC2626")
        elif pct >= 80.0:
            self.card_used_val.config(fg="#D97706")
        else:
            self.card_used_val.config(fg="#0D9488")

        top_cat_text = f"{cat_stats['highest_category']}" if cat_stats['highest_amount'] > 0 else "None"
        self.card_topcat_val.config(text=top_cat_text)
        self.card_items_val.config(text=f"{len(items)} items")

        # Progress bar
        clamped_pct = min(100.0, max(0.0, pct))
        self.budget_progressbar["value"] = clamped_pct
        if pct >= 100.0:
            self.budget_progressbar.configure(style="Exceeded.Horizontal.TProgressbar")
        elif pct >= 80.0:
            self.budget_progressbar.configure(style="Warning.Horizontal.TProgressbar")
        else:
            self.budget_progressbar.configure(style="Safe.Horizontal.TProgressbar")

        # 2. Update Alert Banner
        status = self.gm.get_budget_status()
        if status["level"] == "EXCEEDED":
            self.banner_frame.config(bg="#FEF2F2", highlightbackground="#DC2626")
            self.banner_lbl.config(
                text=status["message"],
                fg="#B91C1C",
                bg="#FEF2F2"
            )
        elif status["level"] == "WARNING":
            self.banner_frame.config(bg="#FFFBEB", highlightbackground="#D97706")
            self.banner_lbl.config(
                text=status["message"],
                fg="#B45309",
                bg="#FFFBEB"
            )
        else:
            self.banner_frame.config(bg="#ECFDF5", highlightbackground="#059669")
            self.banner_lbl.config(
                text=status["message"],
                fg="#047857",
                bg="#ECFDF5"
            )

        # 3. Populate Main Grocery Table
        self._populate_table(items)

        # 4. Populate Categories Tab
        self._populate_categories_tab(cat_stats)

        # 5. Populate Suggestions Tab
        self._populate_suggestions_tab()

    def _populate_table(self, items):
        """Renders items into the main Treeview."""
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        total_table_cost = 0.0
        for idx, item in enumerate(items):
            total_table_cost += item["total_price"]
            row_tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    item["id"],
                    item["name"],
                    item["category"],
                    f"{item['quantity']} {item.get('unit', 'units')}",
                    f"₹{item['price_per_unit']:,.2f}",
                    f"₹{item['total_price']:,.2f}"
                ),
                tags=(row_tag,)
            )

        self.tree.tag_configure("even", background="#FFFFFF")
        self.tree.tag_configure("odd", background="#F8FAFC")

        self.lbl_table_count.config(
            text=f"Showing {len(items)} items | Subtotal: ₹{total_table_cost:,.2f}"
        )

    def _populate_categories_tab(self, cat_stats):
        """Fills category analytics treeview."""
        for row in self.tree_categories.get_children():
            self.tree_categories.delete(row)

        breakdown = cat_stats["breakdown"]
        for cat, data in breakdown.items():
            if data["count"] > 0:
                self.tree_categories.insert(
                    "",
                    tk.END,
                    values=(
                        cat,
                        f"{data['count']} item(s)",
                        f"₹{data['total']:,.2f}",
                        f"{data['percentage']:.1f}%"
                    )
                )

        if cat_stats["highest_amount"] > 0:
            self.lbl_top_category_banner.config(
                text=(
                    f"🏆 Highest Spending Category: {cat_stats['highest_category']} "
                    f"— ₹{cat_stats['highest_amount']:,.2f}"
                )
            )
        else:
            self.lbl_top_category_banner.config(text="Highest Spending Category: None")

    def _populate_suggestions_tab(self):
        """Renders dynamic rule-based suggestions cards."""
        # Clear existing cards
        for widget in self.sugg_scrollable_frame.winfo_children():
            widget.destroy()

        suggestions = self.gm.get_smart_suggestions()
        for sugg in suggestions:
            card_color = "#FFFFFF"
            border_color = "#E2E8F0"
            text_color = "#1E293B"

            if sugg["type"] == "alert":
                card_color = "#FEF2F2"
                border_color = "#FCA5A5"
                text_color = "#991B1B"
            elif sugg["type"] == "warning":
                card_color = "#FFFBEB"
                border_color = "#FCD34D"
                text_color = "#92400E"
            elif sugg["type"] == "success":
                card_color = "#ECFDF5"
                border_color = "#6EE7B7"
                text_color = "#065F46"
            elif sugg["type"] == "info":
                card_color = "#EFF6FF"
                border_color = "#93C5FD"
                text_color = "#1E40AF"

            card = tk.Frame(
                self.sugg_scrollable_frame,
                bg=card_color,
                bd=1,
                relief="solid",
                padx=12,
                pady=10
            )
            card.pack(fill=tk.X, pady=4, padx=4)

            lbl = tk.Label(
                card,
                text=sugg["text"],
                font=self.font_normal,
                fg=text_color,
                bg=card_color,
                wraplength=700,
                justify="left"
            )
            lbl.pack(anchor="w")
