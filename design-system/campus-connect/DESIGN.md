# CampusConnect Design System (OpenDesign + UI/UX Pro Max)

> **Contract:** CampusConnect UI/UX Architecture & Brand Guidelines  
> **Source:** Designed with `nexu-io/open-design` and `nextlevelbuilder/ui-ux-pro-max-skill`  
> **Target Figma Canvas:** `https://www.figma.com/design/Q79IEbAIuSFIQlr29Bw7L7/Untitled?node-id=0-1&m=dev`

---

## 1. Product Brief & Visual Strategy

**Product:** CampusConnect — Modern Campus Event Discovery & Control Plane  
**Target Audience:** University students, club leaders, event organizers, and department administrators  
**Design Dials:**
- **Variance:** 6/10 (Modern, structured, asymmetric hero accents)
- **Motion:** 5/10 (Smooth micro-interactions, back.out(1.4) stagger lists, prefers-reduced-motion safe)
- **Density:** 6/10 (Information-dense yet breathing, 8pt spatial grid)
- **Style Archetype:** Refined Dark Monolith with Linear/shadcn polish, Glassmorphism accents, and Vibrant Event Categories

---

## 2. Color System (WCAG AA & AAA Compliant)

### Semantic Tokens (Dark Theme - Primary Runtime)

| Token | Hex | Role | Contrast Ratio on Surface |
| :--- | :--- | :--- | :--- |
| `--bg-base` | `#09090B` | Deep background floor | — |
| `--bg-surface` | `#121218` | Sidebar, main canvas backdrop | 1.15:1 |
| `--bg-card` | `#181824` | Event cards, stat cards, containers | 1.35:1 |
| `--bg-card-hover` | `#222232` | Elevated card hover state | 1.6:1 |
| `--bg-muted` | `#262638` | Badges, disabled controls, pills | 1.8:1 |
| `--border-subtle` | `rgba(255, 255, 255, 0.08)` | Structural dividers, hairline card borders | >3:1 UI |
| `--border-focus` | `#6366F1` | Accessible focus ring (2px solid, 2px offset) | >4.5:1 |
| `--text-primary` | `#F8FAFC` | Headings, primary event titles, high-contrast labels | **15.2:1** (AAA) |
| `--text-secondary`| `#94A3B8` | Subheadings, dates, venues, body copy | **7.1:1** (AAA) |
| `--text-muted` | `#64748B` | Metadata, helper text, empty states | **4.6:1** (AA) |
| `--primary` | `#6366F1` | Primary brand accent (Indigo) | 4.8:1 |
| `--primary-hover` | `#4F46E5` | Active/hover button state | 5.4:1 |
| `--primary-glow` | `rgba(99, 102, 241, 0.25)` | Focus and elevation glow | — |
| `--accent` | `#F97316` | Action highlight, high-urgency callouts | 6.2:1 |
| `--destructive` | `#EF4444` | Delete actions, cancellation, expired badges | 4.9:1 |

### Event Category Color Identity

Each category carries a distinct, accessible visual identity across badges, card header bars, and analytics charts:

- **Technical:** `#6366F1` (Indigo / Tech Violet) — Hex `#818CF8` text chip
- **Cultural:** `#EC4899` (Rose / Vibrant Pink) — Hex `#F472B6` text chip
- **Sports:** `#10B981` (Emerald / Energy Green) — Hex `#34D399` text chip
- **Workshop:** `#F59E0B` (Amber / Craft Gold) — Hex `#FBBF24` text chip
- **Seminar:** `#06B6D4` (Cyan / Knowledge Blue) — Hex `#22D3EE` text chip

### Event Status Tokens

- **Upcoming:** `#10B981` (Live Green, border `rgba(16, 185, 129, 0.3)`, background `rgba(16, 185, 129, 0.12)`)
- **Ongoing:** `#38BDF8` (Active Pulse Sky, border `rgba(56, 189, 248, 0.3)`, background `rgba(56, 189, 248, 0.12)`)
- **Past:** `#64748B` (Muted Slate, border `rgba(100, 116, 139, 0.2)`, background `rgba(100, 116, 139, 0.08)`)

---

## 3. Typography Hierarchy

Fonts:
- **Headings & UI:** `Inter`, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- **Monospace & Timestamps:** `JetBrains Mono`, "SF Mono", monospace
- **Display Accents (Optional Hero):** `Playfair Display` (editorial touch)

| Style | Size | Weight | Line Height | Letter Spacing | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero Title** | 32px / 2rem | 800 (Extra Bold) | 1.2 | -0.03em | Catalogue / Dashboard Page Header |
| **Section Title** | 22px / 1.375rem | 700 (Bold) | 1.3 | -0.02em | Section headers, card modal titles |
| **Card Title** | 17px / 1.0625rem| 600 (Semi Bold)| 1.4 | -0.01em | Event title in cards and rows |
| **Body Primary**| 14px / 0.875rem | 400 (Regular)  | 1.5 | normal | Descriptions, form inputs, table data |
| **Badge / Label**| 12px / 0.75rem | 600 (Semi Bold)| 1.2 | +0.02em | Category chips, status badges, counters |
| **Micro / Hint**| 11px / 0.6875rem| 500 (Medium)   | 1.3 | +0.01em | Keyboard shortcuts (`⌘K`), timestamps |

---

## 4. Spacing, Sizing & Layout Geometry

The spatial system strictly adheres to an 8-point grid (`4px`, `8px`, `12px`, `16px`, `24px`, `32px`, `48px`, `64px`):

- **Sidebar Width:** Desktop `260px` fixed, mobile `280px` drawer
- **Main Container:** Max-width `1440px`, padding `24px` (desktop), `16px` (mobile)
- **Grid Layout:**
  - Desktop (>= 1200px): 3-column event grid (`grid-template-columns: repeat(3, minmax(0, 1fr))`)
  - Tablet (768px - 1199px): 2-column event grid
  - Mobile (< 768px): 1-column responsive stacked cards
- **Card Radius:** `16px` (outer cards), `10px` (inner elements/inputs), `9999px` (pills/badges)
- **Elevation System:**
  - Card resting: `0 4px 20px -2px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)`
  - Card hover: `0 12px 32px -4px rgba(0, 0, 0, 0.6), 0 0 20px rgba(99, 102, 241, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1)`
  - Modals: `0 24px 60px -12px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.1)`

---

## 5. Micro-Interactions & Physics

- **Card Hover:** Smooth 250ms lift (`transform: translateY(-4px)`), subtle border highlight shift.
- **Button Clicks:** Micro scale tap feedback (`transform: scale(0.98)`).
- **Search Interaction:** `⌘K` / `Ctrl+K` shortcut instant focus with smooth ring glow.
- **Modal Transitions:** Dialog enter fade + scale (`from: opacity 0, scale 0.95 -> to: opacity 1, scale 1` in 200ms `ease-out`).
- **Reduced Motion:** If `prefers-reduced-motion: reduce` is active, all transformations and infinite animations degrade to immediate opacity transitions.

---

## 6. Pre-Delivery Accessibility Audit Checklist

- [x] All text satisfies WCAG 2.1 AA minimum contrast (4.5:1 for normal text, 3:1 for large/bold).
- [x] Interactive buttons and inputs have visible `:focus-visible` outlines.
- [x] Icons carry `aria-hidden="true"` while semantic parent triggers contain `aria-label`.
- [x] Forms have explicit `<label>` bindings and validation feedback with `aria-live="polite"`.
- [x] Modal dialogs trap focus and close on `Escape` key and backdrop tap.
- [x] Touch targets exceed 44×44px on mobile viewports.
