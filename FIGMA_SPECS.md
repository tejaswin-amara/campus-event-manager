# Figma Design Specification & Dev Mode Handoff

> **Figma File Target:** [CampusConnect Untitled Canvas](https://www.figma.com/design/Q79IEbAIuSFIQlr29Bw7L7/Untitled?node-id=0-1&m=dev)  
> **Node ID:** `0:1` (Root Canvas)  
> **Design Framework:** OpenDesign (`nexu-io/open-design`) & UI/UX Pro Max (`nextlevelbuilder/ui-ux-pro-max-skill`)  
> **Captures Generated:** 6 OpenDesign IR Captures (`figma/captures/*.od-figma.json`)

---

## 1. How to Import the Redesign into Figma

Figma files cannot be generated directly as proprietary binary `.fig` files from CLI. Instead, OpenDesign uses the **OD Figma Plugin** architecture (`figma/od-figma-plugin/`) which parses `.od-figma.json` and programmatically generates native Figma layers, text, styles, and frames using the official Figma Plugin API.

### 3-Step Import Instructions:

1. **Open the Figma File in Figma Desktop:**
   - Navigate to [https://www.figma.com/design/Q79IEbAIuSFIQlr29Bw7L7/Untitled?node-id=0-1&m=dev](https://www.figma.com/design/Q79IEbAIuSFIQlr29Bw7L7/Untitled?node-id=0-1&m=dev).
2. **Load the Development Plugin:**
   - In Figma Desktop, click the Main Menu (top left) → **Plugins** → **Development** → **Import plugin from manifest…**
   - Select `figma/od-figma-plugin/manifest.json` from this repository.
3. **Generate Screens:**
   - In Figma, run **Plugins** → **Development** → **CampusConnect - OpenDesign Figma Importer**.
   - Select any screen (e.g. **Student Event Catalogue**, **Admin Control Center**, **Admin Secure Login**, **Event Detail Modal**, **Mobile Student View**), or drop any file from `figma/captures/`.
   - The plugin instantly builds the editable vector frames, typography, auto-layouts, and color styles right onto node `0:1`!

---

## 2. Master Canvas Architecture (Node 0:1)

```
Node 0:1 (Root Canvas)
├── Frame: "Student Event Catalogue (Desktop 1440x1024)" [X: 0, Y: 0]
│   ├── Frame: "Sidebar" [260x1024, Fill: #121218, Border: rgba(255,255,255,0.08)]
│   │   ├── Brand (Logo + "CampusConnect" + Role Badge)
│   │   ├── Navigation List (All Events, Upcoming, Ongoing, Past, Categories)
│   │   └── User Footer (Avatar + Name + Sign Out)
│   ├── Frame: "TopBar" [1132x56, Fill: #181824, Border: rgba(255,255,255,0.08)]
│   │   ├── Search Input Box ("Search events by title, venue, club...")
│   │   └── Keyboard Shortcut Badge ("⌘K")
│   ├── Frame: "HeroSection" [1132x140, Fill: rgba(99,102,241,0.12), Border: rgba(99,102,241,0.5)]
│   │   ├── Hero Badge ("SPRING 2026")
│   │   ├── Headline ("Discover What's Happening on Campus")
│   │   └── Subtitle ("Explore verified technical hackathons, cultural fests...")
│   ├── Frame: "RecommendationCard" [1132x110, Match Badge, Reason, Register CTA]
│   ├── Frame: "CategoryFilterPills" [All, Technical, Cultural, Sports, Workshops, Seminars]
│   ├── Frame: "EventGrid" [3 Columns x 2 Rows = 6 Cards]
│   │   ├── Card 1: AI & Autonomous Agents Hackathon (Technical, Indigo #6366F1)
│   │   ├── Card 2: Spring Symphony & Cultural Gala (Cultural, Pink #EC4899)
│   │   ├── Card 3: Inter-Collegiate Futsal Derby (Sports, Green #10B981)
│   │   ├── Card 4: Production LLM Systems Workshop (Workshop, Amber #F59E0B)
│   │   ├── Card 5: Future of Decentralized Identity (Seminar, Cyan #06B6D4)
│   │   └── Card 6: Modern Design Systems Masterclass (Technical, Indigo #6366F1)
│   └── Frame: "PaginationFooter" [1132x44]
│
├── Frame: "Admin Control Center (Desktop 1440x1024)" [X: 1600, Y: 0]
│   ├── Sidebar [260x1024, Admin Mode]
│   ├── AdminTopBar [Overview Header, "+ Create Event", "Export CSV"]
│   ├── KPI Stat Cards Row [4 Cards: Total Events, Registrations, Upcoming, Telemetry]
│   ├── Analytics Grid:
│   │   ├── Category Distribution Donut Chart
│   │   └── Registration Velocity Bar Chart (Last 7 Days)
│   └── Event Management Table [Sortable headers, Status pills, Category tags, Action buttons]
│
├── Frame: "Event Detail Modal (Desktop 1440x1024)" [X: 3200, Y: 0]
│   ├── Dimmed Backdrop [Opacity: 0.85]
│   └── Centered Modal Card [700x720, Corner Radius: 18px]
│       ├── Banner Image with Category & Status Chips
│       ├── Title, Date/Time Chip, Venue Pin, Capacity Counter
│       ├── About Description Block
│       └── Action Bar ("Register on External Portal", "Add to Calendar", "Close")
│
├── Frame: "Admin Login Screen (Desktop 1440x1024)" [X: 4800, Y: 0]
│   ├── Atmospheric Ambient Glow Floor
│   └── Floating Glass Card [460x560, Corner Radius: 20px]
│       ├── Security Audit Badge ("Protected via BCrypt & Bucket4j Rate Limiting")
│       ├── Floating Input Fields (Username, Password with toggle)
│       └── "Sign In to Admin Console" CTA
│
├── Frame: "User-Safe Error Fallback (Desktop 1440x1024)" [X: 6400, Y: 0]
│   └── Error Card [480x420, Status 404 / 500, Diagnostic info, Return CTA]
│
└── Frame: "Mobile Student View (375x812)" [X: 8000, Y: 0]
    ├── Mobile Topbar & Search
    ├── Category Carousel
    ├── Vertical Feed Cards
    └── Bottom Navigation Bar
```

---

## 3. Dev Mode Design Tokens

### Color Tokens

```json
{
  "Background / Base": "#09090B",
  "Background / Surface": "#121218",
  "Background / Card": "#181824",
  "Background / Card Hover": "#222232",
  "Border / Subtle": "rgba(255, 255, 255, 0.08)",
  "Border / Focus": "#6366F1",
  "Brand / Primary": "#6366F1",
  "Brand / Accent": "#F97316",
  "Status / Upcoming": "#10B981",
  "Status / Ongoing": "#38BDF8",
  "Status / Past": "#64748B",
  "Status / Destructive": "#EF4444",
  "Text / Primary": "#F8FAFC",
  "Text / Secondary": "#94A3B8",
  "Text / Muted": "#64748B"
}
```

### Typography Hierarchy (Font: Inter)

- **Hero Display:** 26px / Line Height 34px / Extra Bold
- **Section Heading:** 18px / Line Height 26px / Bold
- **Card Title:** 15px / Line Height 20px / Bold
- **Body Regular:** 13px / Line Height 20px / Regular
- **Badge / Micro Label:** 11px / Line Height 14px / Semi Bold

---

## 4. Component Auto-Layout & Constraints

| Component | Layout Direction | Padding (X, Y) | Spacing | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| **Sidebar** | Vertical | 16px, 24px | 8px | Top, Bottom, Left |
| **Topbar** | Horizontal | 20px, 12px | 12px | Left & Right, Top |
| **Event Card** | Vertical | 16px, 16px | 12px | Fixed width (360px), Hug height |
| **Pill Filter** | Horizontal | 16px, 8px | 6px | Hug contents |
| **Stat Card** | Vertical | 16px, 16px | 8px | Fill width (265px) |
| **Table Row** | Horizontal | 16px, 12px | 16px | Fill container width |
