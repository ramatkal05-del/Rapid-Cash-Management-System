# Rapid Cash - Premium Dark FinTech Dashboard Architecture

## Project Overview
**Rapid Cash** is a money transfer and withdrawal management system built with Django + HTMX + Tailwind CSS. This document outlines the architecture for a premium dark FinTech back-office dashboard.

---

## Technology Stack
- **Backend**: Django 5.0+
- **Frontend**: Tailwind CSS 3.x (CDN for rapid prototyping)
- **Interactivity**: HTMX 1.9+
- **JavaScript**: Minimal vanilla JS for UI helpers
- **Fonts**: Inter (UI), JetBrains Mono (money/IDs)

---

## Design System

### Color Palette
```css
/* Background */
--bg-primary: #07080e      /* Main background */
--bg-surface1: #0d0e18    /* Cards, sidebar */
--bg-surface2: #131421    /* Nested elements */
--bg-surface3: #1a1b2e    /* Hover states */
--bg-border: #252640      /* Borders */

/* Accent Colors */
--accent-primary: #4f8ef7  /* Primary actions */
--accent-success: #00d68f /* Positive values */
--accent-danger: #ff5c7a  /* Errors, negative */
--accent-warning: #ffb347 /* Warnings */
--accent-purple: #a78bfa  /* Special */

/* Text */
--text-primary: #e8eaf6   /* Main text */
--text-secondary: #8b8fa8 /* Secondary text */
--text-muted: #5a5d7a     /* Muted text */
```

### Typography
- **UI Font**: Inter (400, 500, 600, 700)
- **Monospace**: JetBrains Mono (transaction IDs, money values)
- **Scale**: 
  - H1: 2rem (32px)
  - H2: 1.5rem (24px)
  - H3: 1.25rem (20px)
  - Body: 0.875rem (14px)
  - Small: 0.75rem (12px)

---

## Template Organization

```
templates/
├── base.html                    # Main layout with sidebar, topbar
├── login.html                   # Login page (standalone)
│
├── partials/                    # Reusable UI components
│   ├── _sidebar.html           # Navigation sidebar
│   ├── _topbar.html            # Sticky header
│   ├── _kpi_card.html          # Stat card component
│   ├── _data_table.html        # Premium table wrapper
│   ├── _badge.html             # Status badges
│   ├── _modal.html             # Modal shell
│   ├── _toast.html             # Toast notification
│   ├── _pagination.html        # HTMX pagination
│   ├── _filter_bar.html        # Filter controls
│   ├── _empty_state.html       # Empty data state
│   ├── _user_card.html        # User profile card
│   └── _progress.html          # Progress bar
│
├── fragments/                  # HTMX partial templates
│   ├── _kpi_refresh.html       # KPI cards refresh
│   ├── _table_rows.html        # Table body refresh
│   ├── _filter_results.html    # Filtered results
│   ├── _toast_single.html      # Single toast
│   ├── _modal_content.html     # Modal content
│   └── _dropdown_options.html  # Dynamic dropdown
│
├── dashboard/
│   └── index.html              # Main dashboard
│
├── operations/
│   ├── list.html               # Transaction history
│   ├── create.html             # Create operation wizard
│   └── detail.html             # Operation detail
│
├── finance/
│   ├── expenses/
│   │   ├── list.html           # Expense management
│   │   └── create.html         # Create expense
│   ├── commissions/
│   │   └── list.html           # Commission tracking
│   └── reports/
│       ├── index.html          # Reports dashboard
│       └── daily.html          # Daily report
│
├── core/
│   ├── agents/
│   │   └── list.html           # Agent management
│   ├── associates/
│   │   └── list.html           # Associate management
│   ├── investors/
│   │   └── list.html           # Investor management
│   ├── cashboxes/
│   │   └── list.html           # Cashbox monitoring
│   └── exchange/
│       └── rates.html          # Exchange rates
│
└── settings/
    └── index.html              # System settings
```

---

## HTMX Implementation Patterns

### 1. Partial Rendering Strategy
All HTMX responses return HTML fragments, not full pages. Use Django's `render()` with context or create dedicated fragment templates.

```python
# views.py pattern
def operation_list(request):
    if request.htmx:
        template = 'fragments/_table_rows.html'
    else:
        template = 'operations/list.html'
    return render(request, template, {...})
```

### 2. HTMX Trigger Headers
Use custom headers for enhanced UX:
- `HX-Refresh`: Trigger KPI refresh after operations
- `HX-Show-Toast`: Display notification

```python
response = render(request, template, context)
response['HX-Refresh'] = 'true'
return response
```

### 3. Common HTMX Attributes
```html
<!-- Filter with debounce -->
<input hx-get="/operations/" 
       hx-trigger="keyup changed delay:500ms" 
       hx-target="#table-body"
       hx-indicator=".htmx-indicator">

<!-- Load modal content -->
<button hx-get="/modal/form/"
        hx-target="#modal-container"
        hx-swap="innerHTML">

<!-- Pagination -->
<a hx-get="?page=2" 
   hx-target="#table-body"
   hx-swap="innerHTML">
```

---

## Page Specifications

### 1. Login Page
- Standalone dark page
- Gradient background with subtle glow
- Demo account quick-login buttons
- Form validation feedback

### 2. Dashboard
- 4-column KPI cards (total transactions, fees, expenses, profit)
- Recent operations table (last 10)
- Cashbox summary cards
- Quick action buttons
- Auto-refresh KPIs every 30s via HTMX

### 3. Transactions (Operations)
- Advanced filters (type, agent, date range, status)
- Sortable table with monospace transaction IDs
- Row actions (view, cancel)
- Pagination with HTMX
- Real-time fee preview during creation

### 4. Expenses
- Category-based filtering
- Amount totals by category
- Admin-only create action

### 5. Cashboxes
- Card grid layout
- Real-time balance display
- Agent assignment
- Transaction history link

### 6. Users (Agents/Associates/Investors)
- Tab-based navigation
- Role-specific columns
- Commission rate display
- Contract details for partners

### 7. Exchange Rates
- Currency pair table
- Rate history sparklines
- Manual update capability

### 8. Reports
- Period selector (daily/weekly/monthly/quarterly/yearly)
- Export to PDF
- Charts for trends

---

## Role-Based Navigation

### ADMIN
- Full navigation access
- All data visible
- Create/Edit/Delete permissions

### AGENT
- Dashboard
- Operations (own only)
- Cashbox (own only)

### ASSOCIATE
- Dashboard (limited)
- Reports (own contracts)

### INVESTOR
- Dashboard (portfolio view)
- Reports (own returns)

---

## JavaScript Helpers

### Required Functions
```javascript
// Modal management
openModal(title, content, actions)
closeModal()
closeModalOnEscape()

// Notifications  
showToast(message, type)
clearToasts()

// HTMX helpers
htmxRefreshKPIs()
htmxShowIndicator(element)

// Fee calculator preview
calculateFee(amount, currency)

// Date/time utilities
formatCurrency(amount, currency)
formatDate(date, format)
```

---

## Performance Considerations

1. **HTMX Pagination**: Load 25-50 items per page
2. **Debounced Filters**: 300-500ms delay
3. **KPI Refresh**: Every 30s, not on every action
4. **Optimistic Updates**: Show success immediately, revert on error
5. **Lazy Loading**: Images and heavy components

---

## Security Notes

1. CSRF protection via Django's `@csrf_exempt` not used
2. HTMX requests include CSRF token automatically
3. Role-based access control on all views
4. Rate limiting on create/update operations
5. Input validation on all forms

---

## File Naming Conventions

- **Partials**: `_name.html` (underscore prefix)
- **Fragments**: `_name.html` (underscore prefix)
- **Pages**: `name.html` or `name/index.html`
- **Templates**: kebab-case preferred
- **CSS Classes**: Tailwind utilities + custom components

---

## Future Enhancements

1. Real-time WebSocket updates for cashbox balances
2. Charts library (Chart.js or similar)
3. PDF export for all reports
4. Multi-language support
5. Audit log for all operations
6. Two-factor authentication
7. Dark/Light theme toggle
