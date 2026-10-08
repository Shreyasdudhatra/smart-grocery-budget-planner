/**
 * Smart Grocery Budget Planner - Client Application Logic
 * =======================================================
 * Pure Vanilla JavaScript implementation.
 * Supports dual-mode execution:
 * 1. Synchronized with Python backend via REST API (/api/*) when launched via `python server.py`
 * 2. Standalone execution via localStorage / fallback sample data if opened directly in browser.
 */

// Initial Default Sample Data (Matches project requirements)
const DEFAULT_SAMPLE_DATA = {
  budget: 5000.0,
  items: [
    { id: 1, name: "Rice", category: "Grains", quantity: 2.0, unit: "kg", price_per_unit: 70.0, total_price: 140.0 },
    { id: 2, name: "Milk", category: "Dairy", quantity: 5.0, unit: "units", price_per_unit: 60.0, total_price: 300.0 },
    { id: 3, name: "Apples", category: "Fruits", quantity: 2.0, unit: "kg", price_per_unit: 120.0, total_price: 240.0 },
    { id: 4, name: "Vegetables", category: "Vegetables", quantity: 5.0, unit: "units", price_per_unit: 80.0, total_price: 400.0 },
    { id: 5, name: "Biscuits", category: "Snacks", quantity: 4.0, unit: "packets", price_per_unit: 30.0, total_price: 120.0 },
    { id: 6, name: "Detergent", category: "Household", quantity: 1.0, unit: "unit", price_per_unit: 250.0, total_price: 250.0 }
  ]
};

const CATEGORIES = ["Fruits", "Vegetables", "Dairy", "Grains", "Snacks", "Beverages", "Household", "Other"];

// Global State
let state = {
  budget: 5000.0,
  items: [],
  isApiMode: false,
  deleteTargetId: null
};

// DOM Element References
const elements = {
  // Alert Banner
  alertBanner: document.getElementById("alert-banner"),
  alertIcon: document.getElementById("alert-icon"),
  alertTitle: document.getElementById("alert-title"),
  alertMessage: document.getElementById("alert-message"),
  alertBadge: document.getElementById("alert-badge"),

  // KPIs
  kpiBudget: document.getElementById("kpi-budget"),
  kpiSpent: document.getElementById("kpi-spent"),
  kpiRemainLabel: document.getElementById("kpi-remain-label"),
  kpiRemainIcon: document.getElementById("kpi-remain-icon"),
  kpiRemaining: document.getElementById("kpi-remaining"),
  kpiRemainingSub: document.getElementById("kpi-remaining-sub"),
  kpiPercent: document.getElementById("kpi-percent"),
  kpiProgressBar: document.getElementById("kpi-progress-bar"),
  kpiTopCat: document.getElementById("kpi-top-category"),
  kpiTopCatAmount: document.getElementById("kpi-top-category-amount"),
  kpiItemsCount: document.getElementById("kpi-items-count"),
  kpiItemsAvg: document.getElementById("kpi-items-avg"),

  // Forms
  formBudget: document.getElementById("form-budget"),
  inputBudget: document.getElementById("input-budget"),
  btnQuickBudget: document.getElementById("btn-quick-budget"),

  formItem: document.getElementById("form-item"),
  itemFormTitle: document.getElementById("item-form-title"),
  itemFormMode: document.getElementById("item-form-mode"),
  inputEditId: document.getElementById("input-edit-id"),
  inputItemName: document.getElementById("input-item-name"),
  selectCategory: document.getElementById("select-category"),
  inputQuantity: document.getElementById("input-quantity"),
  selectUnit: document.getElementById("select-unit"),
  inputPrice: document.getElementById("input-price"),
  previewSubtotal: document.getElementById("preview-subtotal"),
  btnSubmitItem: document.getElementById("btn-submit-item"),
  btnClearForm: document.getElementById("btn-clear-form"),
  btnCancelEdit: document.getElementById("btn-cancel-edit"),

  // Table & Search
  tableBody: document.getElementById("table-body"),
  inputSearch: document.getElementById("input-search"),
  btnClearSearch: document.getElementById("btn-clear-search"),
  tableShowingText: document.getElementById("table-showing-text"),
  tableSubtotalVal: document.getElementById("table-subtotal-val"),
  emptyState: document.getElementById("empty-state"),
  tabItemsBadge: document.getElementById("tab-items-badge"),
  tabSuggestionsBadge: document.getElementById("tab-suggestions-badge"),

  // Tabs & Views
  categoryCardsGrid: document.getElementById("category-cards-grid"),
  catTopPill: document.getElementById("cat-top-pill"),
  suggestionsContainer: document.getElementById("suggestions-list-container"),

  // Actions
  btnSave: document.getElementById("btn-save"),
  btnReset: document.getElementById("btn-reset"),
  btnExportCsv: document.getElementById("btn-export-csv"),
  footerDataStatus: document.getElementById("footer-data-status"),

  // Modal
  deleteModal: document.getElementById("delete-modal"),
  deleteModalText: document.getElementById("delete-modal-text"),
  btnConfirmDelete: document.getElementById("btn-confirm-delete"),
  btnCancelDelete: document.getElementById("btn-cancel-delete"),

  // Toasts
  toastContainer: document.getElementById("toast-container")
};

// ==========================================================
// Initialization
// ==========================================================

document.addEventListener("DOMContentLoaded", async () => {
  setupEventListeners();
  await loadInitialData();
});

async function loadInitialData() {
  // Test if Python server API is available
  try {
    const res = await fetch("/api/data", { cache: "no-store" });
    if (res.ok) {
      const data = await res.json();
      state.budget = parseFloat(data.budget) || 5000.0;
      state.items = Array.isArray(data.items) ? data.items : [];
      state.isApiMode = true;
      elements.footerDataStatus.textContent = "Storage: Connected to Python API (grocery_data.json)";
      showToast("Connected to Python backend server.", "success");
      renderAll();
      return;
    }
  } catch (err) {
    // API not reachable, running standalone via file:// or static hosting
  }

  // Fallback: localStorage or default sample data
  const localData = localStorage.getItem("smart_grocery_data");
  if (localData) {
    try {
      const parsed = JSON.parse(localData);
      state.budget = parseFloat(parsed.budget) || 5000.0;
      state.items = parsed.items || [];
      elements.footerDataStatus.textContent = "Storage: Browser LocalStorage (Standalone)";
    } catch (e) {
      resetToDefaultState();
    }
  } else {
    resetToDefaultState();
  }

  renderAll();
}

function resetToDefaultState() {
  state.budget = DEFAULT_SAMPLE_DATA.budget;
  state.items = JSON.parse(JSON.stringify(DEFAULT_SAMPLE_DATA.items));
  saveToLocalStorage();
  elements.footerDataStatus.textContent = "Storage: Browser LocalStorage (Sample Loaded)";
}

function saveToLocalStorage() {
  localStorage.setItem("smart_grocery_data", JSON.stringify({
    budget: state.budget,
    items: state.items
  }));
}

// ==========================================================
// Event Listeners
// ==========================================================

function setupEventListeners() {
  // Tabs Navigation
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const targetPane = document.getElementById(btn.dataset.tab);
      if (targetPane) targetPane.classList.add("active");
    });
  });

  // Budget Forms
  elements.formBudget.addEventListener("submit", handleSetBudget);
  elements.btnQuickBudget.addEventListener("click", () => {
    elements.inputBudget.focus();
    elements.inputBudget.select();
  });

  // Item Form & Inputs
  elements.formItem.addEventListener("submit", handleItemSubmit);
  elements.inputQuantity.addEventListener("input", updateLiveSubtotalPreview);
  elements.inputPrice.addEventListener("input", updateLiveSubtotalPreview);
  elements.btnClearForm.addEventListener("click", clearItemForm);
  elements.btnCancelEdit.addEventListener("click", clearItemForm);

  // Search
  elements.inputSearch.addEventListener("input", handleSearch);
  elements.btnClearSearch.addEventListener("click", () => {
    elements.inputSearch.value = "";
    elements.btnClearSearch.style.display = "none";
    renderTable();
  });

  // Top Actions
  elements.btnSave.addEventListener("click", handleSaveData);
  elements.btnReset.addEventListener("click", handleResetSampleData);
  elements.btnExportCsv.addEventListener("click", handleExportCsv);

  // Modal Actions
  elements.btnCancelDelete.addEventListener("click", closeModal);
  elements.btnConfirmDelete.addEventListener("click", executeDeleteItem);
  elements.deleteModal.addEventListener("click", (e) => {
    if (e.target === elements.deleteModal) closeModal();
  });
}

// ==========================================================
// Business Calculations
// ==========================================================

function calculateTotals() {
  const totalSpent = state.items.reduce((sum, item) => sum + (parseFloat(item.total_price) || 0), 0);
  const remaining = state.budget - totalSpent;
  const overBudget = totalSpent > state.budget ? totalSpent - state.budget : 0;
  const percentUsed = state.budget > 0 ? (totalSpent / state.budget) * 100 : 0;

  // Category Aggregation
  const categories = {};
  CATEGORIES.forEach(c => categories[c] = { total: 0, count: 0, percent: 0 });

  state.items.forEach(item => {
    const cat = item.category || "Other";
    if (!categories[cat]) categories[cat] = { total: 0, count: 0, percent: 0 };
    categories[cat].total += parseFloat(item.total_price) || 0;
    categories[cat].count += 1;
  });

  let topCategory = "None";
  let topCategoryAmount = 0;

  Object.keys(categories).forEach(cat => {
    if (totalSpent > 0) {
      categories[cat].percent = (categories[cat].total / totalSpent) * 100;
    }
    if (categories[cat].total > topCategoryAmount) {
      topCategoryAmount = categories[cat].total;
      topCategory = cat;
    }
  });

  // Alert Level
  let alertLevel = "SAFE";
  if (percentUsed >= 100) alertLevel = "EXCEEDED";
  else if (percentUsed >= 80) alertLevel = "WARNING";

  return {
    totalSpent,
    remaining,
    overBudget,
    percentUsed,
    categories,
    topCategory,
    topCategoryAmount,
    alertLevel
  };
}

// ==========================================================
// Rendering
// ==========================================================

function renderAll() {
  const totals = calculateTotals();
  renderAlertBanner(totals);
  renderKPIs(totals);
  renderTable();
  renderCategoryBreakdown(totals);
  renderSmartSuggestions(totals);
}

function formatCurrency(val) {
  return "₹" + parseFloat(val).toLocaleString("en-IN", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

function renderAlertBanner(totals) {
  const { alertLevel, percentUsed, totalSpent, remaining, overBudget } = totals;
  const banner = elements.alertBanner;

  banner.className = "alert-banner";

  if (alertLevel === "EXCEEDED") {
    banner.classList.add("alert-exceeded");
    elements.alertIcon.textContent = "🚨";
    elements.alertTitle.textContent = "Budget Exceeded!";
    elements.alertMessage.textContent = `You have spent ${formatCurrency(totalSpent)} (${percentUsed.toFixed(1)}% of ${formatCurrency(state.budget)}). You are over budget by ${formatCurrency(overBudget)}!`;
    elements.alertBadge.textContent = "EXCEEDED";
  } else if (alertLevel === "WARNING") {
    banner.classList.add("alert-warning");
    elements.alertIcon.textContent = "⚠️";
    elements.alertTitle.textContent = "Budget Warning (≥ 80% Consumed)";
    elements.alertMessage.textContent = `You have utilized ${percentUsed.toFixed(1)}% of your budget (${formatCurrency(totalSpent)}). Only ${formatCurrency(remaining)} remaining. Watch expenses!`;
    elements.alertBadge.textContent = "WARNING";
  } else {
    banner.classList.add("alert-safe");
    elements.alertIcon.textContent = "✅";
    elements.alertTitle.textContent = "Budget On Track";
    elements.alertMessage.textContent = `You have spent ${formatCurrency(totalSpent)} of ${formatCurrency(state.budget)} (${percentUsed.toFixed(1)}% used). ${formatCurrency(remaining)} remaining.`;
    elements.alertBadge.textContent = "SAFE";
  }
}

function renderKPIs(totals) {
  const { totalSpent, remaining, overBudget, percentUsed, topCategory, topCategoryAmount } = totals;

  elements.kpiBudget.textContent = formatCurrency(state.budget);
  elements.inputBudget.value = state.budget;

  elements.kpiSpent.textContent = formatCurrency(totalSpent);

  if (remaining >= 0) {
    elements.kpiRemainLabel.textContent = "REMAINING BUDGET";
    elements.kpiRemainIcon.textContent = "⚖️";
    elements.kpiRemaining.textContent = formatCurrency(remaining);
    elements.kpiRemaining.className = "kpi-value text-emerald";
    elements.kpiRemainingSub.textContent = "Available balance";
  } else {
    elements.kpiRemainLabel.textContent = "OVER BUDGET";
    elements.kpiRemainIcon.textContent = "🚨";
    elements.kpiRemaining.textContent = "-" + formatCurrency(overBudget);
    elements.kpiRemaining.className = "kpi-value text-danger";
    elements.kpiRemainingSub.textContent = "Exceeded limit!";
  }

  elements.kpiPercent.textContent = percentUsed.toFixed(1) + "%";
  const clampedProgress = Math.min(100, Math.max(0, percentUsed));
  elements.kpiProgressBar.style.width = clampedProgress + "%";
  elements.kpiProgressBar.className = "progress-bar";

  if (percentUsed >= 100) elements.kpiProgressBar.classList.add("exceeded");
  else if (percentUsed >= 80) elements.kpiProgressBar.classList.add("warning");

  elements.kpiTopCat.textContent = topCategoryAmount > 0 ? topCategory : "None";
  elements.kpiTopCatAmount.textContent = topCategoryAmount > 0 ? `${formatCurrency(topCategoryAmount)} spent` : "No expenses yet";

  elements.kpiItemsCount.textContent = `${state.items.length} items`;
  const avg = state.items.length > 0 ? totalSpent / state.items.length : 0;
  elements.kpiItemsAvg.textContent = `Avg: ${formatCurrency(avg)} / item`;

  elements.tabItemsBadge.textContent = state.items.length;
}

function renderTable() {
  const query = elements.inputSearch.value.trim().toLowerCase();
  elements.btnClearSearch.style.display = query ? "block" : "none";

  const filtered = state.items.filter(item => {
    return (item.name || "").toLowerCase().includes(query) ||
           (item.category || "").toLowerCase().includes(query);
  });

  elements.tableBody.innerHTML = "";

  if (filtered.length === 0) {
    elements.emptyState.style.display = "block";
    elements.tableShowingText.textContent = "Showing 0 items";
    elements.tableSubtotalVal.textContent = "₹0.00";
    return;
  }

  elements.emptyState.style.display = "none";
  let subtotal = 0;

  filtered.forEach(item => {
    subtotal += parseFloat(item.total_price) || 0;
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td style="color: #64748b; font-weight: 600;">${item.id}</td>
      <td style="font-weight: 600; color: #0f172a;">${escapeHtml(item.name)}</td>
      <td><span class="cat-pill cat-${item.category}">${item.category}</span></td>
      <td style="color: #475569;">${item.quantity} ${item.unit || "units"}</td>
      <td class="text-right" style="color: #475569;">${formatCurrency(item.price_per_unit)}</td>
      <td class="text-right" style="font-weight: 700; color: #0f172a;">${formatCurrency(item.total_price)}</td>
      <td class="text-center">
        <div class="table-actions">
          <button class="action-btn btn-edit-action" onclick="loadItemForEdit(${item.id})">✏️ Edit</button>
          <button class="action-btn btn-del-action" onclick="openDeleteModal(${item.id})">🗑️ Delete</button>
        </div>
      </td>
    `;
    elements.tableBody.appendChild(tr);
  });

  elements.tableShowingText.textContent = `Showing ${filtered.length} of ${state.items.length} items`;
  elements.tableSubtotalVal.textContent = formatCurrency(subtotal);
}

function renderCategoryBreakdown(totals) {
  const { categories, topCategory, topCategoryAmount } = totals;
  elements.categoryCardsGrid.innerHTML = "";

  if (topCategoryAmount > 0) {
    elements.catTopPill.innerHTML = `🏆 Highest Category: <strong>${topCategory} (${formatCurrency(topCategoryAmount)})</strong>`;
  } else {
    elements.catTopPill.innerHTML = `Highest Category: <strong>None</strong>`;
  }

  CATEGORIES.forEach(cat => {
    const data = categories[cat] || { total: 0, count: 0, percent: 0 };
    const isHighest = (cat === topCategory && topCategoryAmount > 0);

    const card = document.createElement("div");
    card.className = `category-card ${isHighest ? "is-highest" : ""}`;

    card.innerHTML = `
      <div class="category-card-top">
        <span class="cat-name">${cat}</span>
        ${isHighest ? '<span class="cat-badge-highest">Top Spend</span>' : ''}
      </div>
      <div class="category-card-amount">${formatCurrency(data.total)}</div>
      <div class="cat-bar-bg">
        <div class="cat-bar-fill" style="width: ${Math.min(100, data.percent)}%;"></div>
      </div>
      <div class="category-card-bottom">
        <span>${data.count} item(s)</span>
        <span>${data.percent.toFixed(1)}% of spending</span>
      </div>
    `;

    elements.categoryCardsGrid.appendChild(card);
  });
}

function renderSmartSuggestions(totals) {
  const { percentUsed, totalSpent, overBudget, categories } = totals;
  const suggestions = [];

  if (state.items.length === 0) {
    suggestions.push({
      type: "info",
      icon: "ℹ️",
      title: "List Empty",
      text: "Your grocery shopping list is empty. Add items using the left form to see budget analytics and insights."
    });
  } else {
    // Rule 1: Budget Status
    if (percentUsed >= 100) {
      suggestions.push({
        type: "alert",
        icon: "🚨",
        title: "Budget Exceeded",
        text: `You have exceeded your grocery budget by ${formatCurrency(overBudget)}. Cut back on non-essential items immediately.`
      });
    } else if (percentUsed >= 80) {
      suggestions.push({
        type: "warning",
        icon: "⚠️",
        title: "Budget Warning Threshold",
        text: `You have consumed ${percentUsed.toFixed(1)}% of your budget. Restrict additional purchases strictly to essentials.`
      });
    }

    // Rule 2: Non-Essentials Check
    if (percentUsed >= 80) {
      const nonEssentials = state.items.filter(i => ["Snacks", "Beverages", "Other"].includes(i.category));
      if (nonEssentials.length > 0) {
        const nonEssentialCost = nonEssentials.reduce((sum, i) => sum + i.total_price, 0);
        const names = nonEssentials.slice(0, 3).map(i => `'${i.name}' (${formatCurrency(i.total_price)})`).join(", ");
        suggestions.push({
          type: "warning",
          icon: "💡",
          title: "Saving Opportunity (Non-Essentials)",
          text: `Non-essential items (${names}) total ${formatCurrency(nonEssentialCost)}. Trimming these will quickly restore budget safety.`
        });
      }
    }

    // Rule 3: Category Dominance (> 30% of entire budget)
    Object.keys(categories).forEach(cat => {
      const catTotal = categories[cat].total;
      if (catTotal > 0 && state.budget > 0) {
        const catBudgetPct = (catTotal / state.budget) * 100;
        if (catBudgetPct >= 30) {
          suggestions.push({
            type: "info",
            icon: "📊",
            title: `Dominant Category: ${cat}`,
            text: `'${cat}' consumes ${formatCurrency(catTotal)} (${catBudgetPct.toFixed(1)}% of your total budget). Consider bulk purchasing or alternatives.`
          });
        }
      }
    });

    // Rule 4: Cost Outlier Check (> 1.8x average item cost)
    const sorted = [...state.items].sort((a, b) => b.total_price - a.total_price);
    if (sorted.length > 1) {
      const highestItem = sorted[0];
      const avg = totalSpent / state.items.length;
      if (highestItem.total_price >= avg * 1.8) {
        suggestions.push({
          type: "info",
          icon: "💎",
          title: `Cost Outlier: ${highestItem.name}`,
          text: `'${highestItem.name}' is your most expensive item at ${formatCurrency(highestItem.total_price)} (${((highestItem.total_price/totalSpent)*100).toFixed(1)}% of spending). Consider reducing quantity if budget is tight.`
        });
      }
    }

    // Rule 5: Healthy Budget Praise
    if (percentUsed < 60 && state.items.length >= 3) {
      suggestions.push({
        type: "success",
        icon: "✅",
        title: "Healthy Budget Discipline",
        text: `Excellent planning! You have used only ${percentUsed.toFixed(1)}% of your budget with ${formatCurrency(totals.remaining)} still available.`
      });
    }
  }

  // Render cards
  elements.suggestionsContainer.innerHTML = "";
  elements.tabSuggestionsBadge.textContent = suggestions.length;

  suggestions.forEach(sugg => {
    const card = document.createElement("div");
    card.className = `suggestion-card sugg-${sugg.type}`;
    card.innerHTML = `
      <div class="suggestion-icon">${sugg.icon}</div>
      <div class="suggestion-body">
        <div class="suggestion-type">${sugg.title}</div>
        <div class="suggestion-text">${sugg.text}</div>
      </div>
    `;
    elements.suggestionsContainer.appendChild(card);
  });
}

// ==========================================================
// Form Handlers & CRUD Actions
// ==========================================================

async function handleSetBudget(e) {
  e.preventDefault();
  const val = parseFloat(elements.inputBudget.value);
  if (isNaN(val) || val <= 0) {
    showToast("Please enter a valid budget greater than zero.", "error");
    return;
  }

  state.budget = Math.round(val * 100) / 100;

  if (state.isApiMode) {
    try {
      await fetch("/api/budget", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ budget: state.budget })
      });
    } catch (err) {}
  } else {
    saveToLocalStorage();
  }

  renderAll();
  showToast(`Budget set to ${formatCurrency(state.budget)}`, "success");
}

function updateLiveSubtotalPreview() {
  const qty = parseFloat(elements.inputQuantity.value);
  const price = parseFloat(elements.inputPrice.value);
  if (!isNaN(qty) && !isNaN(price) && qty > 0 && price > 0) {
    elements.previewSubtotal.textContent = formatCurrency(qty * price);
  } else {
    elements.previewSubtotal.textContent = "₹0.00";
  }
}

async function handleItemSubmit(e) {
  e.preventDefault();
  const editId = elements.inputEditId.value;
  const name = elements.inputItemName.value.trim();
  const category = elements.selectCategory.value;
  const quantity = parseFloat(elements.inputQuantity.value);
  const unit = elements.selectUnit.value;
  const price = parseFloat(elements.inputPrice.value);

  // Validations
  if (!name) {
    showToast("Item name cannot be empty.", "error");
    return;
  }
  if (isNaN(quantity) || quantity <= 0) {
    showToast("Quantity must be a positive number.", "error");
    return;
  }
  if (isNaN(price) || price <= 0) {
    showToast("Price per unit must be a positive number.", "error");
    return;
  }

  const totalPrice = Math.round(quantity * price * 100) / 100;

  if (editId) {
    // Update existing item
    const id = parseInt(editId, 10);
    const index = state.items.findIndex(i => i.id === id);
    if (index !== -1) {
      state.items[index] = {
        id,
        name,
        category,
        quantity: Math.round(quantity * 100) / 100,
        unit,
        price_per_unit: Math.round(price * 100) / 100,
        total_price: totalPrice
      };

      if (state.isApiMode) {
        try {
          await fetch(`/api/items/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(state.items[index])
          });
        } catch (err) {}
      } else {
        saveToLocalStorage();
      }

      showToast(`Updated '${name}' successfully.`, "success");
    }
  } else {
    // Add new item
    const nextId = state.items.length > 0 ? Math.max(...state.items.map(i => i.id)) + 1 : 1;
    const newItem = {
      id: nextId,
      name,
      category,
      quantity: Math.round(quantity * 100) / 100,
      unit,
      price_per_unit: Math.round(price * 100) / 100,
      total_price: totalPrice
    };

    state.items.push(newItem);

    if (state.isApiMode) {
      try {
        await fetch("/api/items", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(newItem)
        });
      } catch (err) {}
    } else {
      saveToLocalStorage();
    }

    showToast(`Added '${name}' (${formatCurrency(totalPrice)})`, "success");
  }

  clearItemForm();
  renderAll();
}

window.loadItemForEdit = function(id) {
  const item = state.items.find(i => i.id === id);
  if (!item) return;

  elements.inputEditId.value = item.id;
  elements.inputItemName.value = item.name;
  elements.selectCategory.value = item.category;
  elements.inputQuantity.value = item.quantity;
  elements.selectUnit.value = item.unit || "units";
  elements.inputPrice.value = item.price_per_unit;

  elements.itemFormTitle.textContent = `✏️ Edit Item #${item.id}`;
  elements.itemFormMode.textContent = `Currently modifying: ${item.name}`;
  elements.btnSubmitItem.textContent = "💾 Update Item";
  elements.btnCancelEdit.style.display = "inline-block";

  updateLiveSubtotalPreview();
  elements.inputItemName.focus();
};

function clearItemForm() {
  elements.inputEditId.value = "";
  elements.inputItemName.value = "";
  elements.selectCategory.value = "Fruits";
  elements.inputQuantity.value = "1";
  elements.selectUnit.value = "units";
  elements.inputPrice.value = "";
  elements.previewSubtotal.textContent = "₹0.00";

  elements.itemFormTitle.textContent = "➕ Add Grocery Item";
  elements.itemFormMode.textContent = "Mode: Adding new item";
  elements.btnSubmitItem.textContent = "➕ Add Item";
  elements.btnCancelEdit.style.display = "none";
}

window.openDeleteModal = function(id) {
  const item = state.items.find(i => i.id === id);
  if (!item) return;

  state.deleteTargetId = id;
  elements.deleteModalText.textContent = `Are you sure you want to remove '${item.name}' (ID: ${item.id}) costing ${formatCurrency(item.total_price)}?`;
  elements.deleteModal.classList.add("open");
};

function closeModal() {
  elements.deleteModal.classList.remove("open");
  state.deleteTargetId = null;
}

async function executeDeleteItem() {
  if (state.deleteTargetId === null) return;
  const id = state.deleteTargetId;
  const item = state.items.find(i => i.id === id);
  const name = item ? item.name : "Item";

  state.items = state.items.filter(i => i.id !== id);

  if (state.isApiMode) {
    try {
      await fetch(`/api/items/${id}`, { method: "DELETE" });
    } catch (err) {}
  } else {
    saveToLocalStorage();
  }

  if (elements.inputEditId.value == id) {
    clearItemForm();
  }

  closeModal();
  renderAll();
  showToast(`Removed '${name}' from shopping list.`, "info");
}

function handleSearch() {
  renderTable();
}

async function handleSaveData() {
  if (state.isApiMode) {
    try {
      const res = await fetch("/api/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ budget: state.budget, items: state.items })
      });
      const data = await res.json();
      showToast(data.message || "Data saved to grocery_data.json", "success");
      return;
    } catch (e) {}
  }

  saveToLocalStorage();
  showToast("Shopping list saved successfully!", "success");
}

async function handleResetSampleData() {
  const confirmReset = confirm("Reset all grocery items and budget back to standard college demo sample data (₹5,000 & 6 items)?");
  if (!confirmReset) return;

  if (state.isApiMode) {
    try {
      const res = await fetch("/api/reset", { method: "POST" });
      const data = await res.json();
      state.budget = data.budget;
      state.items = data.items;
      clearItemForm();
      renderAll();
      showToast("Data reset to standard college sample values.", "success");
      return;
    } catch (e) {}
  }

  resetToDefaultState();
  clearItemForm();
  renderAll();
  showToast("Data reset to standard college sample values.", "success");
}

function handleExportCsv() {
  if (state.items.length === 0) {
    showToast("Shopping list is empty.", "error");
    return;
  }

  let csv = "ID,Item Name,Category,Quantity,Unit,Price per Unit,Total Price\n";
  state.items.forEach(i => {
    csv += `"${i.id}","${i.name}","${i.category}","${i.quantity}","${i.unit || 'units'}","${i.price_per_unit}","${i.total_price}"\n`;
  });

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Grocery_Shopping_List_${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast("CSV file exported.", "success");
}

// ==========================================================
// Toast Notification
// ==========================================================

function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;

  const iconMap = { success: "✓", error: "✕", info: "ℹ" };
  toast.innerHTML = `<span>${iconMap[type] || "•"}</span> <span>${escapeHtml(message)}</span>`;

  elements.toastContainer.appendChild(toast);
  setTimeout(() => toast.classList.add("show"), 10);

  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 300);
  }, 3500);
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
