import os
import sys
import time
import http.server
import socketserver
import threading
from playwright.sync_api import sync_playwright

ASSETS_DIR = os.path.abspath('presentation_assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

PORT = 8999

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='frontend-redesign/dist', **kwargs)

def start_server():
    server = socketserver.TCPServer(('127.0.0.1', PORT), Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server

def prepare_login_html():
    css_path = os.path.abspath('src/main/resources/static/css/style.css').replace('\\', '/')
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CampusConnect — Admin Authentication</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
    <link rel="stylesheet" href="file:///{css_path}">
    <style>
        body {{
            background-color: #09090b;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 20px;
        }}
        .ambient-mesh {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 20% 25%, rgba(99, 102, 241, 0.18) 0%, transparent 40%),
                        radial-gradient(circle at 80% 75%, rgba(168, 85, 247, 0.15) 0%, transparent 40%),
                        radial-gradient(circle at 50% 50%, rgba(9, 9, 11, 0.95) 0%, #09090b 100%);
            z-index: 0;
        }}
        .login-card {{
            background: rgba(18, 18, 24, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            padding: 2.75rem 2.5rem;
            width: 100%;
            max-width: 440px;
            position: relative;
            z-index: 1;
            box-shadow: 0 25px 60px -12px rgba(0, 0, 0, 0.7), 0 0 30px rgba(99, 102, 241, 0.15);
            color: #fff;
        }}
        .brand-icon {{
            width: 48px; height: 48px;
            background: linear-gradient(135deg, #6366F1, #8B5CF6);
            border-radius: 14px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-size: 24px; font-weight: 800;
            box-shadow: 0 8px 16px rgba(99, 102, 241, 0.35);
        }}
        .form-control {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #fff;
            padding: 0.75rem 1rem;
            border-radius: 12px;
        }}
        .form-control:focus {{
            background: rgba(255, 255, 255, 0.08);
            border-color: #6366F1;
            color: #fff;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
        }}
        .btn-primary {{
            background: linear-gradient(135deg, #6366F1, #4F46E5);
            border: none;
            padding: 0.85rem;
            font-weight: 600;
            border-radius: 12px;
            box-shadow: 0 8px 20px -4px rgba(99, 102, 241, 0.5);
        }}
        .badge-secure {{
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 9999px;
            padding: 0.35rem 0.85rem;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex; align-items: center; gap: 6px;
        }}
    </style>
</head>
<body>
    <div class="ambient-mesh"></div>
    <div class="login-card">
        <div class="text-center mb-4">
            <div class="brand-icon mx-auto mb-3">🎓</div>
            <h2 class="fw-bold fs-4 mb-1">Administrator Sign In</h2>
            <p class="text-secondary small">CampusConnect Administrative Control Plane</p>
            <div class="mt-2">
                <span class="badge-secure"><i class="bi bi-shield-check"></i> BCrypt + Rate-Limited (Bucket4j)</span>
            </div>
        </div>

        <form action="#" method="post">
            <div class="mb-3">
                <label class="form-label small fw-semibold text-secondary">Username</label>
                <input type="text" class="form-control" value="admin" readonly>
            </div>
            <div class="mb-4">
                <label class="form-label small fw-semibold text-secondary">Password</label>
                <input type="password" class="form-control" value="••••••••••••••••" readonly>
            </div>
            <button type="button" class="btn btn-primary w-100 mb-3">Sign In to Admin Console</button>
            <div class="text-center">
                <a href="#" class="text-secondary text-decoration-none small">← Back to Student Event Catalogue</a>
            </div>
        </form>
    </div>
</body>
</html>"""
    path = os.path.abspath('presentation_assets/login_preview.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return path

def main():
    server = start_server()
    time.sleep(1)
    login_html_path = prepare_login_html()

    print("Launching browser with Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Student Catalogue
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(f'http://127.0.0.1:{PORT}')
        page.wait_for_load_state('networkidle')
        page.screenshot(path=os.path.join(ASSETS_DIR, '01_student_catalogue.png'))
        print("Captured: 01_student_catalogue.png")

        # 2. Event Detail (Click on first event card)
        first_card = page.locator('.group.relative.cursor-pointer').first
        if first_card.count() > 0:
            first_card.click()
            page.wait_for_timeout(600)
            page.screenshot(path=os.path.join(ASSETS_DIR, '05_event_detail.png'))
            print("Captured: 05_event_detail.png")
            page.keyboard.press('Escape')
            page.wait_for_timeout(300)

        # 3. Admin Console
        page.click('button:has-text("Admin Console")')
        page.wait_for_timeout(600)
        page.screenshot(path=os.path.join(ASSETS_DIR, '02_admin_dashboard.png'))
        print("Captured: 02_admin_dashboard.png")

        # 4. Create Event Form
        page.click('button:has-text("New Event")')
        page.wait_for_timeout(600)
        page.screenshot(path=os.path.join(ASSETS_DIR, '03_create_event_form.png'))
        print("Captured: 03_create_event_form.png")

        # 5. Admin Login Page
        page_login = browser.new_page(viewport={'width': 1440, 'height': 900})
        page_login.goto(f'file:///{login_html_path.replace("\\\\", "/")}')
        page_login.wait_for_load_state('networkidle')
        page_login.screenshot(path=os.path.join(ASSETS_DIR, '04_admin_login.png'))
        print("Captured: 04_admin_login.png")

        browser.close()

    server.shutdown()
    print("All UI screenshots captured successfully in", ASSETS_DIR)

if __name__ == '__main__':
    main()
