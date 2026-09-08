"""
Generate OpenDesign Figma Capture IR files (.od-figma.json) for CampusConnect redesign.
Complies with open-design/figma-plugin/IR.md specification.
"""
import json
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "captures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return {
        "r": round(int(hex_str[0:2], 16) / 255.0, 3),
        "g": round(int(hex_str[2:4], 16) / 255.0, 3),
        "b": round(int(hex_str[4:6], 16) / 255.0, 3)
    }

# Theme Colors
C_BG_BASE = rgb("#09090B")
C_BG_SURFACE = rgb("#121218")
C_BG_CARD = rgb("#181824")
C_BG_CARD_HOVER = rgb("#222232")
C_BG_ELEVATED = rgb("#262638")
C_BG_INPUT = rgb("#14141E")

C_TEXT_PRIMARY = rgb("#F8FAFC")
C_TEXT_SECONDARY = rgb("#94A3B8")
C_TEXT_MUTED = rgb("#64748B")
C_TEXT_WHITE = rgb("#FFFFFF")

C_PRIMARY = rgb("#6366F1")
C_PRIMARY_HOVER = rgb("#4F46E5")
C_ACCENT = rgb("#F97316")
C_SUCCESS = rgb("#10B981")
C_INFO = rgb("#38BDF8")
C_WARNING = rgb("#F59E0B")
C_DESTRUCTIVE = rgb("#EF4444")

# Category Colors
C_CAT_TECH = rgb("#6366F1")
C_CAT_CULT = rgb("#EC4899")
C_CAT_SPORT = rgb("#10B981")
C_CAT_WORK = rgb("#F59E0B")
C_CAT_SEMINAR = rgb("#06B6D4")

BORDER_SUBTLE = [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}, "opacity": 0.08}]
BORDER_PRIMARY = [{"type": "SOLID", "color": C_PRIMARY, "opacity": 0.5}]
SHADOW_CARD = [{
    "type": "DROP_SHADOW",
    "color": {"r": 0, "g": 0, "b": 0, "a": 0.4},
    "offset": {"x": 0, "y": 4},
    "radius": 16,
    "spread": 0
}]
SHADOW_GLOW = [{
    "type": "DROP_SHADOW",
    "color": {"r": 0.388, "g": 0.4, "b": 0.945, "a": 0.25},
    "offset": {"x": 0, "y": 0},
    "radius": 24,
    "spread": 0
}]

def make_frame(name, x, y, width, height, fills=None, strokes=None, stroke_weight=0, corner_radius=0, effects=None, children=None):
    node = {
        "type": "FRAME",
        "name": name,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "clipsContent": True
    }
    if fills is not None:
        node["fills"] = fills
    if strokes is not None:
        node["strokes"] = strokes
        node["strokeWeight"] = stroke_weight
    if corner_radius > 0:
        node["cornerRadius"] = corner_radius
    if effects is not None:
        node["effects"] = effects
    if children is not None:
        node["children"] = children
    return node

def make_text(name, x, y, width, height, characters, font_size=14, font_style="Regular", color=C_TEXT_PRIMARY, text_align="LEFT", line_height=None):
    node = {
        "type": "TEXT",
        "name": name,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "characters": characters,
        "fontFamily": "Inter",
        "fontStyle": font_style,
        "fontSize": font_size,
        "textAlign": text_align,
        "color": color,
        "opacity": 1
    }
    if line_height:
        node["lineHeight"] = line_height
    return node

def make_badge(name, x, y, width, height, text, bg_color, text_color, radius=999):
    return make_frame(
        name, x, y, width, height,
        fills=[{"type": "SOLID", "color": bg_color, "opacity": 0.16}],
        strokes=[{"type": "SOLID", "color": bg_color, "opacity": 0.35}],
        stroke_weight=1,
        corner_radius=radius,
        children=[
            make_text(text, x + 8, y + (height - 14) // 2, width - 16, 14, text, font_size=11, font_style="Semi Bold", color=text_color, text_align="CENTER")
        ]
    )

def make_sidebar(is_admin=False):
    children = [
        # Brand
        make_badge("BrandLogo", 24, 28, 32, 32, "CC", C_PRIMARY, C_TEXT_WHITE, radius=8),
        make_text("Brand Title", 64, 32, 160, 24, "CampusConnect", font_size=18, font_style="Bold", color=C_TEXT_PRIMARY),
        make_badge("Role Badge", 64, 60, 72, 20, "ADMIN" if is_admin else "STUDENT", C_PRIMARY if is_admin else C_SUCCESS, C_TEXT_PRIMARY)
    ]
    
    # Navigation Items
    nav_items = [
        ("Overview" if is_admin else "All Events", "active"),
        ("Upcoming", "default"),
        ("Ongoing", "default"),
        ("Past Events", "default")
    ]
    if is_admin:
        nav_items.extend([("Analytics", "default"), ("System Health", "default")])
    else:
        nav_items.extend([("Technical", "cat"), ("Cultural", "cat"), ("Sports", "cat"), ("Workshops", "cat")])

    curr_y = 110
    for title, mode in nav_items:
        is_active = (mode == "active")
        bg = [{"type": "SOLID", "color": C_PRIMARY, "opacity": 0.18}] if is_active else None
        border = BORDER_PRIMARY if is_active else None
        text_c = C_TEXT_PRIMARY if is_active else C_TEXT_SECONDARY
        children.append(
            make_frame(f"Nav-{title}", 16, curr_y, 228, 40, fills=bg, strokes=border, stroke_weight=1 if is_active else 0, corner_radius=8, children=[
                make_text(title, 32, curr_y + 11, 180, 18, title, font_size=13, font_style="Semi Bold" if is_active else "Medium", color=text_c)
            ])
        )
        curr_y += 48

    # Sign Out / Profile at bottom
    curr_y = 940
    children.append(
        make_frame("Sidebar-Footer", 16, curr_y, 228, 52, fills=[{"type": "SOLID", "color": C_BG_CARD, "opacity": 0.6}], corner_radius=10, strokes=BORDER_SUBTLE, stroke_weight=1, children=[
            make_text("User Name", 28, curr_y + 10, 120, 16, "Admin User" if is_admin else "Student Explorer", font_size=12, font_style="Semi Bold", color=C_TEXT_PRIMARY),
            make_text("Sign Out", 28, curr_y + 28, 120, 14, "Sign Out →", font_size=11, font_style="Regular", color=C_DESTRUCTIVE)
        ])
    )

    return make_frame(
        "Sidebar", 0, 0, 260, 1024,
        fills=[{"type": "SOLID", "color": C_BG_SURFACE}],
        strokes=BORDER_SUBTLE,
        stroke_weight=1,
        children=children
    )

# 1. STUDENT CATALOGUE CAPTURE
def build_student_catalogue():
    sidebar = make_sidebar(is_admin=False)
    main_children = []

    # Top Search Bar
    main_children.append(
        make_frame("TopBar", 284, 24, 1132, 56, fills=[{"type": "SOLID", "color": C_BG_CARD}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=12, children=[
            make_text("Search Placeholder", 304, 42, 300, 20, "Search events by title, venue, club...", font_size=14, color=C_TEXT_MUTED),
            make_badge("Kbd Shortcut", 620, 40, 48, 24, "⌘K", C_TEXT_MUTED, C_TEXT_SECONDARY),
            make_text("User Greeting", 1300, 42, 100, 20, "Student Explorer", font_size=13, font_style="Medium", color=C_TEXT_PRIMARY, text_align="RIGHT")
        ])
    )

    # Hero Section
    main_children.append(
        make_frame("HeroSection", 284, 100, 1132, 140, fills=[{"type": "SOLID", "color": C_PRIMARY, "opacity": 0.12}], strokes=BORDER_PRIMARY, stroke_weight=1, corner_radius=16, effects=SHADOW_GLOW, children=[
            make_badge("Hero Tag", 308, 120, 110, 22, "SPRING 2026", C_PRIMARY, C_TEXT_PRIMARY),
            make_text("Hero Title", 308, 150, 700, 36, "Discover What's Happening on Campus", font_size=26, font_style="Extra Bold", color=C_TEXT_PRIMARY),
            make_text("Hero Sub", 308, 192, 800, 24, "Explore verified technical hackathons, cultural fests, sports leagues, and speaker series in real time.", font_size=14, color=C_TEXT_SECONDARY)
        ])
    )

    # Smart Recommendation Card
    main_children.append(
        make_frame("RecommendationCard", 284, 260, 1132, 110, fills=[{"type": "SOLID", "color": C_BG_CARD}], strokes=BORDER_PRIMARY, stroke_weight=1, corner_radius=14, effects=SHADOW_CARD, children=[
            make_badge("Match Badge", 308, 278, 128, 22, "98% SMART MATCH", C_ACCENT, C_TEXT_WHITE),
            make_text("Rec Title", 308, 308, 600, 24, "AI & Autonomous Agents Hackathon 2026", font_size=16, font_style="Bold", color=C_TEXT_PRIMARY),
            make_text("Rec Reason", 308, 334, 600, 18, "Recommended based on your interest in Technical & Systems events • Starts in 3 days", font_size=12, color=C_TEXT_MUTED),
            make_frame("Rec CTA", 1260, 295, 136, 40, fills=[{"type": "SOLID", "color": C_PRIMARY}], corner_radius=8, children=[
                make_text("Rec CTA Text", 1272, 307, 112, 16, "Register Interest →", font_size=12, font_style="Bold", color=C_TEXT_WHITE, text_align="CENTER")
            ])
        ])
    )

    # Category Filter Pills
    pills = [("All Events", True), ("Technical", False), ("Cultural", False), ("Sports", False), ("Workshops", False), ("Seminars", False)]
    px = 284
    for label, active in pills:
        bg = C_PRIMARY if active else C_BG_CARD
        tc = C_TEXT_WHITE if active else C_TEXT_SECONDARY
        main_children.append(
            make_frame(f"Pill-{label}", px, 390, 110, 36, fills=[{"type": "SOLID", "color": bg, "opacity": 1 if active else 0.8}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=999, children=[
                make_text(label, px, 400, 110, 16, label, font_size=12, font_style="Semi Bold" if active else "Medium", color=tc, text_align="CENTER")
            ])
        )
        px += 122

    # 3-Column Event Grid (6 Cards)
    events_data = [
        ("AI & Autonomous Agents Hackathon", "Technical", C_CAT_TECH, "Turing Innovation Lab", "Fri, Mar 14 • 10:00 AM", "120/150 registered", "Upcoming", C_SUCCESS),
        ("Spring Symphony & Cultural Gala", "Cultural", C_CAT_CULT, "Grand University Auditorium", "Sat, Mar 15 • 06:30 PM", "340/400 registered", "Upcoming", C_SUCCESS),
        ("Inter-Collegiate Futsal Derby", "Sports", C_CAT_SPORT, "Campus Sports Complex", "Sun, Mar 16 • 04:00 PM", "80/100 registered", "Ongoing", C_INFO),
        ("Production LLM Systems Workshop", "Workshop", C_CAT_WORK, "Computing Lab 4B", "Tue, Mar 18 • 02:00 PM", "45/50 registered", "Upcoming", C_SUCCESS),
        ("Future of Decentralized Identity", "Seminar", C_CAT_SEMINAR, "Faculty Seminar Hall 1", "Thu, Mar 20 • 11:00 AM", "95/120 registered", "Upcoming", C_SUCCESS),
        ("Modern Design Systems Masterclass", "Technical", C_CAT_TECH, "Media Design Studio", "Sat, Mar 22 • 03:00 PM", "60/60 registered (Full)", "Past", C_TEXT_MUTED)
    ]

    grid_x = 284
    grid_y = 446
    card_w = 360
    card_h = 240
    col_gap = 26
    row_gap = 24

    for i, (title, cat, cat_color, venue, dt, cap, status, st_color) in enumerate(events_data):
        row = i // 3
        col = i % 3
        cx = grid_x + col * (card_w + col_gap)
        cy = grid_y + row * (card_h + row_gap)

        card_children = [
            # Top banner color line
            make_frame("CategoryLine", cx, cy, card_w, 4, fills=[{"type": "SOLID", "color": cat_color}]),
            # Badges
            make_badge("CatBadge", cx + 16, cy + 16, 90, 22, cat.upper(), cat_color, C_TEXT_WHITE),
            make_badge("StatusBadge", cx + card_w - 96, cy + 16, 80, 22, status, st_color, C_TEXT_WHITE),
            # Title
            make_text("CardTitle", cx + 16, cy + 48, card_w - 32, 44, title, font_size=15, font_style="Bold", color=C_TEXT_PRIMARY, line_height=20),
            # Meta
            make_text("DateTime", cx + 16, cy + 98, card_w - 32, 18, f"📅  {dt}", font_size=12, color=C_TEXT_SECONDARY),
            make_text("Venue", cx + 16, cy + 120, card_w - 32, 18, f"📍  {venue}", font_size=12, color=C_TEXT_SECONDARY),
            make_text("Capacity", cx + 16, cy + 144, card_w - 32, 18, f"👥  {cap}", font_size=11, color=C_TEXT_MUTED),
            # Action Button
            make_frame("CardAction", cx + 16, cy + 180, card_w - 32, 38, fills=[{"type": "SOLID", "color": C_PRIMARY, "opacity": 0.15}], strokes=BORDER_PRIMARY, stroke_weight=1, corner_radius=8, children=[
                make_text("BtnText", cx + 24, cy + 191, card_w - 48, 16, "View Details & Register →", font_size=12, font_style="Bold", color=C_PRIMARY, text_align="CENTER")
            ])
        ]

        main_children.append(
            make_frame(f"Card-{i+1}", cx, cy, card_w, card_h, fills=[{"type": "SOLID", "color": C_BG_CARD}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=14, effects=SHADOW_CARD, children=card_children)
        )

    # Pagination footer
    main_children.append(
        make_frame("Pagination", 284, 960, 1132, 44, fills=[{"type": "SOLID", "color": C_BG_CARD, "opacity": 0.5}], corner_radius=8, strokes=BORDER_SUBTLE, stroke_weight=1, children=[
            make_text("PageInfo", 304, 974, 200, 16, "Showing 1–6 of 24 Events", font_size=12, color=C_TEXT_MUTED),
            make_badge("Page1", 1320, 970, 32, 24, "1", C_PRIMARY, C_TEXT_WHITE),
            make_badge("Page2", 1360, 970, 32, 24, "2", C_TEXT_MUTED, C_TEXT_SECONDARY)
        ])
    )

    root = make_frame(
        "Student Event Catalogue (Desktop 1440x1024)", 0, 0, 1440, 1024,
        fills=[{"type": "SOLID", "color": C_BG_BASE}],
        children=[sidebar] + main_children
    )

    return {
        "version": 1,
        "source": {
            "url": "https://www.figma.com/design/Q79IEbAIuSFIQlr29Bw7L7/Untitled?node-id=0-1&m=dev",
            "title": "CampusConnect - Student Discovery Catalogue",
            "capturedAt": 1773000000000,
            "viewport": {"width": 1440, "height": 1024},
            "dpr": 2
        },
        "fonts": [
            {"family": "Inter", "styles": ["Regular", "Medium", "Semi Bold", "Bold", "Extra Bold"]}
        ],
        "root": root
    }

# 2. ADMIN CONTROL CENTER CAPTURE
def build_admin_dashboard():
    sidebar = make_sidebar(is_admin=True)
    main_children = []

    # Header Bar
    main_children.append(
        make_frame("AdminTopBar", 284, 24, 1132, 56, fills=[{"type": "SOLID", "color": C_BG_CARD}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=12, children=[
            make_text("AdminHeaderTitle", 304, 40, 300, 24, "Admin Operations & Control Center", font_size=16, font_style="Bold", color=C_TEXT_PRIMARY),
            # Create Event Button
            make_frame("CreateEventBtn", 1120, 32, 140, 40, fills=[{"type": "SOLID", "color": C_PRIMARY}], corner_radius=8, effects=SHADOW_GLOW, children=[
                make_text("CreateEventText", 1130, 44, 120, 16, "+  Create Event", font_size=12, font_style="Bold", color=C_TEXT_WHITE, text_align="CENTER")
            ]),
            # Export CSV Button
            make_frame("ExportBtn", 1270, 32, 130, 40, fills=[{"type": "SOLID", "color": C_BG_ELEVATED}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=8, children=[
                make_text("ExportText", 1280, 44, 110, 16, "Export CSV", font_size=12, font_style="Medium", color=C_TEXT_PRIMARY, text_align="CENTER")
            ])
        ])
    )

    # KPI Stat Cards Row (4 Cards)
    kpis = [
        ("TOTAL PUBLISHED", "24", "+12% this term", C_PRIMARY),
        ("STUDENT REGISTRATIONS", "1,428", "+28% vs last month", C_SUCCESS),
        ("UPCOMING EVENTS", "14", "Next in 2 days", C_INFO),
        ("SYSTEM TELEMETRY", "142 MB", "JVM Heap • 8 Cores", C_WARNING)
    ]
    card_w = 265
    gap = 24
    kx = 284
    for label, val, sub, colr in kpis:
        main_children.append(
            make_frame(f"KPI-{label}", kx, 96, card_w, 110, fills=[{"type": "SOLID", "color": C_BG_CARD}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=14, effects=SHADOW_CARD, children=[
                make_text("KPILabel", kx + 16, 112, card_w - 32, 16, label, font_size=11, font_style="Semi Bold", color=C_TEXT_MUTED),
                make_text("KPIValue", kx + 16, 134, card_w - 32, 32, val, font_size=26, font_style="Extra Bold", color=C_TEXT_PRIMARY),
                make_text("KPISub", kx + 16, 172, card_w - 32, 16, sub, font_size=11, font_style="Medium", color=colr)
            ])
        )
        kx += card_w + gap

    # Analytics Section (2 Cards)
    # 1. Donut / Distribution
    main_children.append(
        make_frame("CategoryDistCard", 284, 222, 540, 220, fills=[{"type": "SOLID", "color": C_BG_CARD}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=14, effects=SHADOW_CARD, children=[
            make_text("CardTitle", 304, 238, 300, 20, "Category Distribution", font_size=14, font_style="Bold", color=C_TEXT_PRIMARY),
            make_text("Legend1", 304, 274, 200, 18, "Technical — 35%", font_size=12, color=C_TEXT_SECONDARY),
            make_text("Legend2", 304, 302, 200, 18, "Cultural — 25%", font_size=12, color=C_TEXT_SECONDARY),
            make_text("Legend3", 304, 330, 200, 18, "Sports — 15%", font_size=12, color=C_TEXT_SECONDARY),
            make_text("Legend4", 304, 358, 200, 18, "Workshops — 15%", font_size=12, color=C_TEXT_SECONDARY),
            make_text("Legend5", 304, 386, 200, 18, "Seminars — 10%", font_size=12, color=C_TEXT_SECONDARY),
            # Mock Chart Circle Graphic
            make_frame("ChartDonut", 640, 260, 150, 150, fills=[{"type": "SOLID", "color": C_PRIMARY, "opacity": 0.2}], strokes=BORDER_PRIMARY, stroke_weight=20, corner_radius=999, children=[
                make_text("TotalCount", 675, 325, 80, 20, "24 Total", font_size=13, font_style="Bold", color=C_TEXT_PRIMARY, text_align="CENTER")
            ])
        ])
    )

    # 2. Registration Velocity Bar Chart
    main_children.append(
        make_frame("VelocityCard", 848, 222, 568, 220, fills=[{"type": "SOLID", "color": C_BG_CARD}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=14, effects=SHADOW_CARD, children=[
            make_text("VelocityTitle", 868, 238, 300, 20, "Recent Registration Velocity", font_size=14, font_style="Bold", color=C_TEXT_PRIMARY),
            make_text("VelocitySub", 868, 260, 300, 16, "Daily engagement over last 7 days", font_size=11, color=C_TEXT_MUTED),
            # Mock Bars
            make_frame("Bar1", 900, 360, 32, 60, fills=[{"type": "SOLID", "color": C_PRIMARY}]),
            make_frame("Bar2", 950, 320, 32, 100, fills=[{"type": "SOLID", "color": C_PRIMARY}]),
            make_frame("Bar3", 1000, 300, 32, 120, fills=[{"type": "SOLID", "color": C_PRIMARY}]),
            make_frame("Bar4", 1050, 280, 32, 140, fills=[{"type": "SOLID", "color": C_PRIMARY}]),
            make_frame("Bar5", 1100, 330, 32, 90, fills=[{"type": "SOLID", "color": C_PRIMARY}]),
            make_frame("Bar6", 1150, 250, 32, 170, fills=[{"type": "SOLID", "color": C_ACCENT}]),
            make_frame("Bar7", 1200, 270, 32, 150, fills=[{"type": "SOLID", "color": C_PRIMARY}]),
            make_text("BarLabels", 895, 426, 350, 16, "Mon   Tue   Wed   Thu   Fri   Sat   Sun", font_size=11, color=C_TEXT_MUTED)
        ])
    )

    # Event Management Table Card
    table_rows = [
        ("AI & Autonomous Agents Hackathon", "Technical", C_CAT_TECH, "Mar 14, 2026", "Turing Innovation Lab", "120/150", "Upcoming", C_SUCCESS),
        ("Spring Symphony & Cultural Gala", "Cultural", C_CAT_CULT, "Mar 15, 2026", "Grand Auditorium", "340/400", "Upcoming", C_SUCCESS),
        ("Inter-Collegiate Futsal Derby", "Sports", C_CAT_SPORT, "Mar 16, 2026", "Campus Sports Complex", "80/100", "Ongoing", C_INFO),
        ("Production LLM Systems Workshop", "Workshop", C_CAT_WORK, "Mar 18, 2026", "Computing Lab 4B", "45/50", "Upcoming", C_SUCCESS),
        ("Future of Decentralized Identity", "Seminar", C_CAT_SEMINAR, "Mar 20, 2026", "Faculty Seminar Hall 1", "95/120", "Upcoming", C_SUCCESS)
    ]

    table_children = [
        make_text("TableSectionTitle", 304, 468, 300, 24, "Event Registry & Lifecycle", font_size=15, font_style="Bold", color=C_TEXT_PRIMARY),
        # Table Header
        make_frame("TableHeader", 304, 502, 1092, 36, fills=[{"type": "SOLID", "color": C_BG_SURFACE}], corner_radius=6, children=[
            make_text("TH-Title", 320, 512, 280, 16, "EVENT TITLE", font_size=11, font_style="Bold", color=C_TEXT_MUTED),
            make_text("TH-Cat", 620, 512, 120, 16, "CATEGORY", font_size=11, font_style="Bold", color=C_TEXT_MUTED),
            make_text("TH-Date", 760, 512, 120, 16, "DATE", font_size=11, font_style="Bold", color=C_TEXT_MUTED),
            make_text("TH-Reg", 900, 512, 100, 16, "ATTENDEES", font_size=11, font_style="Bold", color=C_TEXT_MUTED),
            make_text("TH-Status", 1020, 512, 100, 16, "STATUS", font_size=11, font_style="Bold", color=C_TEXT_MUTED),
            make_text("TH-Actions", 1180, 512, 180, 16, "ACTIONS", font_size=11, font_style="Bold", color=C_TEXT_MUTED)
        ])
    ]

    ry = 546
    for i, (title, cat, cat_c, dt, venue, reg, st, st_c) in enumerate(table_rows):
        table_children.extend([
            make_text(f"RowTitle-{i}", 320, ry + 12, 280, 18, title, font_size=13, font_style="Semi Bold", color=C_TEXT_PRIMARY),
            make_badge(f"RowCat-{i}", 620, ry + 8, 80, 22, cat, cat_c, C_TEXT_WHITE),
            make_text(f"RowDate-{i}", 760, ry + 12, 120, 16, dt, font_size=12, color=C_TEXT_SECONDARY),
            make_text(f"RowReg-{i}", 900, ry + 12, 100, 16, reg, font_size=12, color=C_TEXT_PRIMARY),
            make_badge(f"RowStatus-{i}", 1020, ry + 8, 80, 22, st, st_c, C_TEXT_WHITE),
            # Action Buttons
            make_badge(f"ActEdit-{i}", 1180, ry + 8, 50, 22, "Edit", C_PRIMARY, C_TEXT_WHITE),
            make_badge(f"ActDel-{i}", 1238, ry + 8, 56, 22, "Delete", C_DESTRUCTIVE, C_TEXT_WHITE)
        ])
        ry += 46

    main_children.append(
        make_frame("EventTableCard", 284, 452, 1132, 330, fills=[{"type": "SOLID", "color": C_BG_CARD}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=14, effects=SHADOW_CARD, children=table_children)
    )

    root = make_frame(
        "Admin Control Center (Desktop 1440x1024)", 1600, 0, 1440, 1024,
        fills=[{"type": "SOLID", "color": C_BG_BASE}],
        children=[sidebar] + main_children
    )

    return {
        "version": 1,
        "source": {
            "url": "https://www.figma.com/design/Q79IEbAIuSFIQlr29Bw7L7/Untitled?node-id=0-1&m=dev",
            "title": "CampusConnect - Admin Control Center",
            "capturedAt": 1773000000000,
            "viewport": {"width": 1440, "height": 1024},
            "dpr": 2
        },
        "fonts": [
            {"family": "Inter", "styles": ["Regular", "Medium", "Semi Bold", "Bold", "Extra Bold"]}
        ],
        "root": root
    }

# 3. ADMIN LOGIN VIEW CAPTURE
def build_admin_login():
    card_w = 460
    card_h = 560
    cx = (1440 - card_w) // 2
    cy = (1024 - card_h) // 2

    card_children = [
        make_badge("LoginLogo", cx + 212, cy + 34, 36, 36, "CC", C_PRIMARY, C_TEXT_WHITE, radius=10),
        make_text("LoginTitle", cx + 30, cy + 76, 400, 28, "CampusConnect Admin", font_size=22, font_style="Extra Bold", color=C_TEXT_PRIMARY, text_align="CENTER"),
        make_text("LoginSub", cx + 30, cy + 108, 400, 20, "Enter authorized credentials to access management control plane", font_size=12, color=C_TEXT_MUTED, text_align="CENTER"),
        
        # Security notice badge
        make_frame("SecBadge", cx + 50, cy + 140, 360, 32, fills=[{"type": "SOLID", "color": C_PRIMARY, "opacity": 0.12}], strokes=BORDER_PRIMARY, stroke_weight=1, corner_radius=6, children=[
            make_text("SecText", cx + 60, cy + 148, 340, 16, "Protected via Rate Limiting, BCrypt & Audit Logging", font_size=11, font_style="Medium", color=C_PRIMARY, text_align="CENTER")
        ]),

        # Form Inputs
        make_text("UserLabel", cx + 40, cy + 194, 380, 16, "ADMIN USERNAME", font_size=11, font_style="Bold", color=C_TEXT_MUTED),
        make_frame("UserInputBox", cx + 40, cy + 216, 380, 48, fills=[{"type": "SOLID", "color": C_BG_INPUT}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=8, children=[
            make_text("UserPlaceholder", cx + 54, cy + 231, 350, 18, "admin", font_size=13, color=C_TEXT_PRIMARY)
        ]),

        make_text("PassLabel", cx + 40, cy + 280, 380, 16, "SECURE PASSWORD", font_size=11, font_style="Bold", color=C_TEXT_MUTED),
        make_frame("PassInputBox", cx + 40, cy + 302, 380, 48, fills=[{"type": "SOLID", "color": C_BG_INPUT}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=8, children=[
            make_text("PassPlaceholder", cx + 54, cy + 317, 350, 18, "••••••••••••••••", font_size=14, color=C_TEXT_PRIMARY)
        ]),

        # Submit CTA
        make_frame("LoginBtn", cx + 40, cy + 380, 380, 50, fills=[{"type": "SOLID", "color": C_PRIMARY}], corner_radius=8, effects=SHADOW_GLOW, children=[
            make_text("LoginBtnText", cx + 40, cy + 395, 380, 20, "Sign In to Admin Console →", font_size=14, font_style="Bold", color=C_TEXT_WHITE, text_align="CENTER")
        ]),

        # Back link
        make_text("BackLink", cx + 40, cy + 456, 380, 20, "← Return to Student Event Discovery", font_size=12, font_style="Medium", color=C_TEXT_SECONDARY, text_align="CENTER")
    ]

    card = make_frame(
        "LoginCard", cx, cy, card_w, card_h,
        fills=[{"type": "SOLID", "color": C_BG_CARD}],
        strokes=BORDER_PRIMARY,
        stroke_weight=1,
        corner_radius=20,
        effects=SHADOW_CARD,
        children=card_children
    )

    root = make_frame(
        "Admin Login Screen (Desktop 1440x1024)", 4800, 0, 1440, 1024,
        fills=[{"type": "SOLID", "color": C_BG_BASE}],
        children=[card]
    )

    return {
        "version": 1,
        "source": {
            "url": "https://www.figma.com/design/Q79IEbAIuSFIQlr29Bw7L7/Untitled?node-id=0-1&m=dev",
            "title": "CampusConnect - Admin Login",
            "capturedAt": 1773000000000,
            "viewport": {"width": 1440, "height": 1024},
            "dpr": 2
        },
        "fonts": [
            {"family": "Inter", "styles": ["Regular", "Medium", "Bold", "Extra Bold"]}
        ],
        "root": root
    }

# 4. EVENT DETAIL MODAL CAPTURE
def build_event_detail():
    modal_w = 700
    modal_h = 720
    mx = (1440 - modal_w) // 2
    my = (1024 - modal_h) // 2

    modal_children = [
        # Image header / banner
        make_frame("ModalBanner", mx, my, modal_w, 200, fills=[{"type": "SOLID", "color": C_CAT_TECH, "opacity": 0.25}], children=[
            make_badge("ModalCat", mx + 24, my + 24, 100, 24, "TECHNICAL", C_CAT_TECH, C_TEXT_WHITE),
            make_badge("ModalStatus", mx + modal_w - 110, my + 24, 86, 24, "Upcoming", C_SUCCESS, C_TEXT_WHITE)
        ]),
        
        # Details
        make_text("ModalTitle", mx + 28, my + 224, modal_w - 56, 32, "AI & Autonomous Agents Hackathon 2026", font_size=22, font_style="Extra Bold", color=C_TEXT_PRIMARY),
        make_text("ModalDateTime", mx + 28, my + 268, modal_w - 56, 20, "Friday, March 14, 2026 • 10:00 AM – 06:00 PM EST", font_size=13, font_style="Semi Bold", color=C_PRIMARY),
        make_text("ModalVenue", mx + 28, my + 296, modal_w - 56, 20, "Turing Innovation Hall, Room 301, North Campus", font_size=13, color=C_TEXT_SECONDARY),
        make_text("ModalCapacity", mx + 28, my + 324, modal_w - 56, 20, "Capacity: 120 / 150 Registered (30 spots remaining)", font_size=12, color=C_TEXT_MUTED),

        # Description
        make_text("DescHead", mx + 28, my + 360, modal_w - 56, 20, "About This Event", font_size=14, font_style="Bold", color=C_TEXT_PRIMARY),
        make_text("DescBody", mx + 28, my + 388, modal_w - 56, 120, 
                  "Join top university researchers, students, and engineers for an intensive 24-hour hackathon focused on building autonomous agent pipelines, tool-calling frameworks, and reliable coding copilots. Free mentorship, compute credits, and hardware prizes provided.", 
                  font_size=13, color=C_TEXT_SECONDARY, line_height=22),

        # Action Button: Register External
        make_frame("RegisterCTA", mx + 28, my + 630, 300, 48, fills=[{"type": "SOLID", "color": C_PRIMARY}], corner_radius=8, effects=SHADOW_GLOW, children=[
            make_text("RegCTAText", mx + 40, my + 644, 276, 20, "Register on External Portal ↗", font_size=13, font_style="Bold", color=C_TEXT_WHITE, text_align="CENTER")
        ]),

        # Add to Calendar CTA
        make_frame("CalendarCTA", mx + 344, my + 630, 180, 48, fills=[{"type": "SOLID", "color": C_BG_ELEVATED}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=8, children=[
            make_text("CalText", mx + 354, my + 644, 160, 20, "Add to Calendar", font_size=12, font_style="Medium", color=C_TEXT_PRIMARY, text_align="CENTER")
        ]),

        # Close button
        make_frame("CloseBtn", mx + 538, my + 630, 134, 48, fills=[{"type": "SOLID", "color": C_BG_CARD_HOVER}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=8, children=[
            make_text("CloseText", mx + 548, my + 644, 114, 20, "Close", font_size=12, font_style="Medium", color=C_TEXT_MUTED, text_align="CENTER")
        ])
    ]

    modal = make_frame(
        "EventDetailModal", mx, my, modal_w, modal_h,
        fills=[{"type": "SOLID", "color": C_BG_CARD}],
        strokes=BORDER_PRIMARY,
        stroke_weight=1,
        corner_radius=18,
        effects=SHADOW_CARD,
        children=modal_children
    )

    root = make_frame(
        "Event Detail View (Desktop 1440x1024)", 3200, 0, 1440, 1024,
        fills=[{"type": "SOLID", "color": C_BG_BASE, "opacity": 0.85}],
        children=[modal]
    )

    return {
        "version": 1,
        "source": {
            "url": "https://www.figma.com/design/Q79IEbAIuSFIQlr29Bw7L7/Untitled?node-id=0-1&m=dev",
            "title": "CampusConnect - Event Detail Drawer",
            "capturedAt": 1773000000000,
            "viewport": {"width": 1440, "height": 1024},
            "dpr": 2
        },
        "fonts": [
            {"family": "Inter", "styles": ["Regular", "Medium", "Semi Bold", "Bold", "Extra Bold"]}
        ],
        "root": root
    }

# 5. ERROR FALLBACK CAPTURE
def build_error_view():
    card_w = 480
    card_h = 420
    cx = (1440 - card_w) // 2
    cy = (1024 - card_h) // 2

    card_children = [
        make_badge("ErrorBadge", cx + 185, cy + 32, 110, 24, "ERROR 404", C_DESTRUCTIVE, C_TEXT_WHITE),
        make_text("ErrorTitle", cx + 24, cy + 74, card_w - 48, 30, "Page or Event Not Found", font_size=20, font_style="Bold", color=C_TEXT_PRIMARY, text_align="CENTER"),
        make_text("ErrorSub", cx + 24, cy + 114, card_w - 48, 44, "The event you requested could not be located. It may have expired, been deleted, or the URL might be mistyped.", font_size=13, color=C_TEXT_MUTED, text_align="CENTER", line_height=20),
        
        # Diagnostic box
        make_frame("DiagBox", cx + 36, cy + 176, card_w - 72, 80, fills=[{"type": "SOLID", "color": C_BG_INPUT}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=8, children=[
            make_text("DiagTitle", cx + 50, cy + 190, 360, 16, "SYSTEM DIAGNOSTIC", font_size=10, font_style="Bold", color=C_TEXT_MUTED),
            make_text("DiagCode", cx + 50, cy + 212, 360, 18, "Status: 404 NOT_FOUND • Handler: GlobalExceptionHandler", font_size=11, font_style="Medium", color=C_DESTRUCTIVE)
        ]),

        # Return Home CTA
        make_frame("HomeCTA", cx + 36, cy + 280, card_w - 72, 46, fills=[{"type": "SOLID", "color": C_PRIMARY}], corner_radius=8, children=[
            make_text("HomeCTAText", cx + 36, cy + 294, card_w - 72, 18, "Return to Events Catalogue", font_size=13, font_style="Bold", color=C_TEXT_WHITE, text_align="CENTER")
        ]),

        make_text("SupportLink", cx + 36, cy + 348, card_w - 72, 18, "Need assistance? Contact Campus Support", font_size=12, color=C_TEXT_SECONDARY, text_align="CENTER")
    ]

    card = make_frame(
        "ErrorCard", cx, cy, card_w, card_h,
        fills=[{"type": "SOLID", "color": C_BG_CARD}],
        strokes=BORDER_SUBTLE,
        stroke_weight=1,
        corner_radius=18,
        effects=SHADOW_CARD,
        children=card_children
    )

    root = make_frame(
        "User-Safe Error Fallback (Desktop 1440x1024)", 6400, 0, 1440, 1024,
        fills=[{"type": "SOLID", "color": C_BG_BASE}],
        children=[card]
    )

    return {
        "version": 1,
        "source": {
            "url": "https://www.figma.com/design/Q79IEbAIuSFIQlr29Bw7L7/Untitled?node-id=0-1&m=dev",
            "title": "CampusConnect - User-Safe Error Fallback",
            "capturedAt": 1773000000000,
            "viewport": {"width": 1440, "height": 1024},
            "dpr": 2
        },
        "fonts": [
            {"family": "Inter", "styles": ["Regular", "Medium", "Bold"]}
        ],
        "root": root
    }

# 6. MOBILE STUDENT FEED CAPTURE
def build_mobile_student():
    w = 375
    h = 812
    children = []

    # Mobile Header
    children.append(
        make_frame("MobileHeader", 0, 0, w, 64, fills=[{"type": "SOLID", "color": C_BG_SURFACE}], strokes=BORDER_SUBTLE, stroke_weight=1, children=[
            make_text("Hamburger", 16, 22, 24, 24, "☰", font_size=20, color=C_TEXT_PRIMARY),
            make_text("MobTitle", 52, 22, 160, 22, "CampusConnect", font_size=16, font_style="Bold", color=C_TEXT_PRIMARY),
            make_badge("MobUser", 320, 18, 38, 28, "S", C_PRIMARY, C_TEXT_WHITE)
        ])
    )

    # Search Bar
    children.append(
        make_frame("MobSearch", 16, 80, 343, 44, fills=[{"type": "SOLID", "color": C_BG_CARD}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=22, children=[
            make_text("MobSearchPh", 36, 94, 260, 18, "Search campus events...", font_size=13, color=C_TEXT_MUTED)
        ])
    )

    # Category Chips
    m_pills = [("All", True), ("Tech", False), ("Culture", False), ("Sports", False)]
    mpx = 16
    for lbl, act in m_pills:
        bg = C_PRIMARY if act else C_BG_CARD
        tc = C_TEXT_WHITE if act else C_TEXT_SECONDARY
        children.append(
            make_frame(f"MobPill-{lbl}", mpx, 138, 74, 32, fills=[{"type": "SOLID", "color": bg}], corner_radius=999, children=[
                make_text(lbl, mpx, 145, 74, 16, lbl, font_size=11, font_style="Semi Bold", color=tc, text_align="CENTER")
            ])
        )
        mpx += 84

    # Stacked Cards
    mob_events = [
        ("AI & Autonomous Agents Hackathon", "Technical", C_CAT_TECH, "Mar 14 • 10 AM", "Turing Lab", "120/150"),
        ("Spring Symphony & Gala", "Cultural", C_CAT_CULT, "Mar 15 • 6:30 PM", "Grand Auditorium", "340/400")
    ]
    my = 186
    for title, cat, cat_c, dt, venue, reg in mob_events:
        children.append(
            make_frame(f"MobCard-{cat}", 16, my, 343, 190, fills=[{"type": "SOLID", "color": C_BG_CARD}], strokes=BORDER_SUBTLE, stroke_weight=1, corner_radius=14, children=[
                make_frame("MobCatLine", 16, my, 343, 3, fills=[{"type": "SOLID", "color": cat_c}]),
                make_badge("MobCat", 32, my + 14, 80, 20, cat, cat_c, C_TEXT_WHITE),
                make_text("MobCardTitle", 32, my + 42, 311, 22, title, font_size=14, font_style="Bold", color=C_TEXT_PRIMARY),
                make_text("MobCardDate", 32, my + 72, 311, 18, dt, font_size=11, color=C_TEXT_SECONDARY),
                make_text("MobCardVenue", 32, my + 94, 311, 18, venue, font_size=11, color=C_TEXT_SECONDARY),
                make_frame("MobBtn", 32, my + 130, 311, 38, fills=[{"type": "SOLID", "color": C_PRIMARY}], corner_radius=8, children=[
                    make_text("MobBtnTxt", 32, my + 140, 311, 16, "View Event Details", font_size=12, font_style="Bold", color=C_TEXT_WHITE, text_align="CENTER")
                ])
            ])
        )
        my += 206

    # Bottom Tab Navigation
    children.append(
        make_frame("BottomNav", 0, 748, w, 64, fills=[{"type": "SOLID", "color": C_BG_SURFACE}], strokes=BORDER_SUBTLE, stroke_weight=1, children=[
            make_text("TabHome", 30, 764, 60, 32, "Events", font_size=11, font_style="Bold", color=C_PRIMARY, text_align="CENTER"),
            make_text("TabExplore", 125, 764, 60, 32, "Explore", font_size=11, color=C_TEXT_MUTED, text_align="CENTER"),
            make_text("TabSaved", 220, 764, 60, 32, "Saved", font_size=11, color=C_TEXT_MUTED, text_align="CENTER"),
            make_text("TabProfile", 310, 764, 60, 32, "Profile", font_size=11, color=C_TEXT_MUTED, text_align="CENTER")
        ])
    )

    root = make_frame(
        "Mobile Student View (375x812)", 8000, 0, w, h,
        fills=[{"type": "SOLID", "color": C_BG_BASE}],
        children=children
    )

    return {
        "version": 1,
        "source": {
            "url": "https://www.figma.com/design/Q79IEbAIuSFIQlr29Bw7L7/Untitled?node-id=0-1&m=dev",
            "title": "CampusConnect - Mobile Student View",
            "capturedAt": 1773000000000,
            "viewport": {"width": 375, "height": 812},
            "dpr": 2
        },
        "fonts": [
            {"family": "Inter", "styles": ["Regular", "Medium", "Semi Bold", "Bold"]}
        ],
        "root": root
    }

def main():
    captures = {
        "student-catalogue.od-figma.json": build_student_catalogue(),
        "admin-control-center.od-figma.json": build_admin_dashboard(),
        "admin-login.od-figma.json": build_admin_login(),
        "event-detail-drawer.od-figma.json": build_event_detail(),
        "error-fallback.od-figma.json": build_error_view(),
        "mobile-student-feed.od-figma.json": build_mobile_student()
    }

    presets_dict = {
        "student-dashboard": captures["student-catalogue.od-figma.json"],
        "admin-dashboard": captures["admin-control-center.od-figma.json"],
        "admin-login": captures["admin-login.od-figma.json"],
        "event-detail": captures["event-detail-drawer.od-figma.json"],
        "error-fallback": captures["error-fallback.od-figma.json"],
        "mobile-student": captures["mobile-student-feed.od-figma.json"]
    }

    for filename, data in captures.items():
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Generated {filepath} ({len(json.dumps(data))} bytes)")

    # Also bundle into od-figma-plugin/presets.js and inline into od-figma-plugin/ui.html
    plugin_dir = os.path.join(os.path.dirname(__file__), "od-figma-plugin")
    plugin_presets_path = os.path.join(plugin_dir, "presets.js")
    with open(plugin_presets_path, "w", encoding="utf-8") as f:
        f.write("// Bundled OpenDesign screen captures for CampusConnect Figma plugin\n")
        f.write("window.CAMPUS_CONNECT_PRESETS = ")
        json.dump(presets_dict, f)
        f.write(";\n")
    print(f"Generated {plugin_presets_path} for Figma plugin preset imports")

    # Ensure ui.html is updated with embedded presets
    ui_html_path = os.path.join(plugin_dir, "ui.html")
    presets_json_str = json.dumps(presets_dict)
    ui_html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>CampusConnect OD Importer</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
      margin: 0;
      padding: 16px;
      background: #09090b;
      color: #f8fafc;
      font-size: 13px;
    }}
    .header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
      padding-bottom: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    h2 {{
      margin: 0;
      font-size: 15px;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .badge {{
      font-size: 10px;
      padding: 2px 7px;
      border-radius: 999px;
      background: rgba(99, 102, 241, 0.2);
      color: #a5b4fc;
      border: 1px solid rgba(99, 102, 241, 0.4);
      font-weight: 600;
      text-transform: uppercase;
    }}
    .target-badge {{
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
      font-family: monospace;
    }}
    p.desc {{
      color: #94a3b8;
      line-height: 1.4;
      margin: 0 0 14px;
      font-size: 12px;
    }}
    .btn-import-all {{
      width: 100%;
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #ffffff;
      padding: 12px 14px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 13px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-bottom: 14px;
      box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
      transition: all 0.15s ease;
    }}
    .btn-import-all:hover {{
      background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
    }}
    .section-title {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #64748b;
      margin: 14px 0 8px;
    }}
    .btn-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 14px;
    }}
    button.screen-btn {{
      background: #14141e;
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: #f1f5f9;
      padding: 9px 12px;
      border-radius: 8px;
      text-align: left;
      font-weight: 500;
      font-size: 12px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.15s ease;
    }}
    button.screen-btn:hover {{
      background: #1e1e2d;
      border-color: #6366f1;
      transform: translateY(-1px);
    }}
    button.screen-btn span.meta {{
      font-size: 10px;
      color: #64748b;
      font-family: monospace;
    }}
    .drop-zone {{
      border: 1px dashed rgba(255, 255, 255, 0.15);
      border-radius: 8px;
      padding: 14px;
      text-align: center;
      color: #94a3b8;
      cursor: pointer;
      font-size: 12px;
      transition: all 0.2s;
      background: rgba(255, 255, 255, 0.02);
    }}
    .drop-zone:hover {{
      border-color: #6366f1;
      color: #ffffff;
      background: rgba(99, 102, 241, 0.05);
    }}
    .status {{
      font-size: 12px;
      padding: 8px 12px;
      border-radius: 6px;
      display: none;
      margin-top: 12px;
    }}
    .status.success {{
      display: block;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .status.error {{
      display: block;
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}
  </style>
</head>
<body>
  <div class="header">
    <h2>CampusConnect <span class="badge">OpenDesign</span></h2>
    <span class="target-badge">node-id=0:1</span>
  </div>
  <p class="desc">Direct vector import engine for Figma dev mode. Generates full layout frames, typography styles, and auto-layouts.</p>

  <button class="btn-import-all" onclick="importAllScreens()">
    <span>🌟 Import Complete Canvas (All 6 Screens)</span>
  </button>

  <div class="section-title">Individual Screen Presets</div>
  <div class="btn-group">
    <button class="screen-btn" onclick="importPreset('student-dashboard')">
      <span>Student Event Catalogue</span>
      <span class="meta">1440×1024 • X: 0</span>
    </button>
    <button class="screen-btn" onclick="importPreset('admin-dashboard')">
      <span>Admin Control Center</span>
      <span class="meta">1440×1024 • X: 1600</span>
    </button>
    <button class="screen-btn" onclick="importPreset('event-detail')">
      <span>Event Detail Drawer</span>
      <span class="meta">1440×1024 • X: 3200</span>
    </button>
    <button class="screen-btn" onclick="importPreset('admin-login')">
      <span>Admin Secure Login</span>
      <span class="meta">1440×1024 • X: 4800</span>
    </button>
    <button class="screen-btn" onclick="importPreset('error-fallback')">
      <span>Diagnostic Error Fallback</span>
      <span class="meta">1440×1024 • X: 6400</span>
    </button>
    <button class="screen-btn" onclick="importPreset('mobile-student')">
      <span>Mobile Student Feed</span>
      <span class="meta">375×812 • X: 8000</span>
    </button>
  </div>

  <div class="drop-zone" id="dropZone">
    Drop custom <code>.od-figma.json</code> capture file or click to browse
    <input type="file" id="fileInput" accept=".json,.od-figma.json" style="display: none;" />
  </div>

  <div id="status" class="status"></div>

  <script>
window.CAMPUS_CONNECT_PRESETS = {presets_json_str};
  </script>
  <script>
    const statusEl = document.getElementById('status');
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');

    function importPreset(key) {{
      if (window.CAMPUS_CONNECT_PRESETS && window.CAMPUS_CONNECT_PRESETS[key]) {{
        sendImport(window.CAMPUS_CONNECT_PRESETS[key]);
      }} else {{
        showStatus('Preset \"' + key + '\" not found', 'error');
      }}
    }}

    function importAllScreens() {{
      if (window.CAMPUS_CONNECT_PRESETS) {{
        showStatus('Building all 6 screens across Canvas node 0:1...', 'success');
        parent.postMessage({{ pluginMessage: {{ type: 'import-all', screens: window.CAMPUS_CONNECT_PRESETS }} }}, '*');
      }} else {{
        showStatus('Preset data not available', 'error');
      }}
    }}

    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => {{ e.preventDefault(); dropZone.style.borderColor = '#6366f1'; }});
    dropZone.addEventListener('dragleave', () => {{ dropZone.style.borderColor = 'rgba(255, 255, 255, 0.15)'; }});
    dropZone.addEventListener('drop', (e) => {{
      e.preventDefault();
      dropZone.style.borderColor = 'rgba(255, 255, 255, 0.15)';
      if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    }});
    fileInput.addEventListener('change', (e) => {{
      if (e.target.files.length) handleFile(e.target.files[0]);
    }});

    function handleFile(file) {{
      const reader = new FileReader();
      reader.onload = (evt) => {{
        try {{
          const ir = JSON.parse(evt.target.result);
          sendImport(ir);
        }} catch (err) {{
          showStatus('Failed to parse JSON file', 'error');
        }}
      }};
      reader.readAsText(file);
    }}

    function sendImport(ir) {{
      showStatus('Building Figma layers for ' + ((ir.source && ir.source.title) || 'screen') + '...', 'success');
      parent.postMessage({{ pluginMessage: {{ type: 'import', ir }} }}, '*');
    }}

    function showStatus(msg, type) {{
      statusEl.textContent = msg;
      statusEl.className = 'status ' + type;
    }}

    window.onmessage = (event) => {{
      const msg = event.data.pluginMessage;
      if (!msg) return;
      if (msg.type === 'done') {{
        showStatus('Successfully imported ' + msg.name, 'success');
      }} else if (msg.type === 'error') {{
        showStatus('Error: ' + msg.message, 'error');
      }}
    }};
  </script>
</body>
</html>
"""
    with open(ui_html_path, "w", encoding="utf-8") as f:
        f.write(ui_html_content)
    print(f"Generated {ui_html_path} with embedded presets for zero-setup execution")

if __name__ == "__main__":
    main()
