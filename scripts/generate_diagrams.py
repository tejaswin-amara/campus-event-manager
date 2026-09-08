import os
from playwright.sync_api import sync_playwright

ASSETS_DIR = os.path.abspath('presentation_assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

ARCH_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 30px;
    background: #0b0f19;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    color: #f8fafc;
    width: 1200px;
    height: 650px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    text-align: center;
    margin-bottom: 20px;
  }
  .header h1 {
    margin: 0 0 6px 0;
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.5px;
  }
  .header p {
    margin: 0;
    font-size: 14px;
    color: #94a3b8;
  }
  .grid-container {
    display: grid;
    grid-template-columns: 220px 680px 220px;
    gap: 20px;
    flex: 1;
  }
  .column {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  .card {
    background: #182234;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }
  .card-title {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .card-title.client { color: #60a5fa; }
  .card-title.app { color: #818cf8; }
  .card-title.data { color: #34d399; }
  .card-title.ops { color: #fbbf24; }
  
  .item-box {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 8px;
  }
  .item-box:last-child { margin-bottom: 0; }
  .item-name {
    font-size: 14px;
    font-weight: 600;
    color: #f1f5f9;
  }
  .item-desc {
    font-size: 11px;
    color: #94a3b8;
    margin-top: 2px;
  }
  
  /* Monolith Core */
  .monolith {
    background: rgba(30, 41, 59, 0.6);
    border: 1.5px solid #6366f1;
    border-radius: 14px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    box-shadow: 0 0 25px rgba(99, 102, 241, 0.15);
  }
  .layer {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 10px;
    padding: 12px 14px;
  }
  .layer-title {
    font-size: 12px;
    font-weight: 700;
    color: #a5b4fc;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .layer-chips {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .chip {
    background: #1e293b;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
    color: #e2e8f0;
  }
  .chip.highlight {
    background: rgba(99, 102, 241, 0.2);
    border-color: #6366f1;
    color: #c7d2fe;
  }
  .chip.security {
    background: rgba(239, 68, 68, 0.15);
    border-color: #ef4444;
    color: #fca5a5;
  }
  .chip.db {
    background: rgba(16, 185, 129, 0.15);
    border-color: #10b981;
    color: #6ee7b7;
  }
  
  .flow-arrow {
    text-align: center;
    color: #6366f1;
    font-size: 12px;
    font-weight: 700;
  }
</style>
</head>
<body>
  <div class="header">
    <h1>CampusConnect System Architecture</h1>
    <p>Spring Boot Modular Monolith with Relational Data Tier & Secure Control Plane</p>
  </div>
  
  <div class="grid-container">
    <!-- Left Column: Clients & Gateway -->
    <div class="column">
      <div class="card">
        <div class="card-title client"><span>🌐</span> Client Interfaces</div>
        <div class="item-box">
          <div class="item-name">Student Browser</div>
          <div class="item-desc">Public Event Catalogue, Filters, Recommendations</div>
        </div>
        <div class="item-box">
          <div class="item-name">Admin Console</div>
          <div class="item-desc">RBAC Dashboard, Event Form, CSV Export</div>
        </div>
        <div class="item-box">
          <div class="item-name">Mobile Devices</div>
          <div class="item-desc">Responsive Viewports, PWA Ready, Fast Discovery</div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-title ops"><span>⚙️</span> Operational Plane</div>
        <div class="item-box">
          <div class="item-name">Spring Actuator</div>
          <div class="item-desc">Liveness & Readiness Health Checks</div>
        </div>
        <div class="item-box">
          <div class="item-name">Micrometer & Metrics</div>
          <div class="item-desc">Prometheus Monitoring Scrapes</div>
        </div>
      </div>
    </div>
    
    <!-- Center Column: Spring Boot Monolith -->
    <div class="column">
      <div class="monolith">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div style="font-size: 15px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 8px;">
            <span>🍃</span> SPRING BOOT MODULAR APPLICATION RUNTIME
          </div>
          <span style="font-size: 11px; background: rgba(99,102,241,0.25); color: #c7d2fe; padding: 3px 8px; border-radius: 4px; font-weight: 600;">Java 25 LTS / Spring Boot 4</span>
        </div>
        
        <!-- Layer 1: Presentation & Controllers -->
        <div class="layer">
          <div class="layer-title">Presentation & Web Routing Layer</div>
          <div class="layer-chips">
            <div class="chip">Thymeleaf Engine</div>
            <div class="chip highlight">EventController (Student)</div>
            <div class="chip highlight">AdminController (Admin)</div>
            <div class="chip">OpenAPI / Swagger</div>
          </div>
        </div>
        
        <!-- Layer 2: Security & Protection -->
        <div class="layer">
          <div class="layer-title">Security & Interceptor Boundary</div>
          <div class="layer-chips">
            <div class="chip security">Spring Security (RBAC)</div>
            <div class="chip security">BCrypt Password Hashing</div>
            <div class="chip security">CSRF & Session Defense</div>
            <div class="chip security">Bucket4j Rate Limiter</div>
          </div>
        </div>
        
        <!-- Layer 3: Application Services -->
        <div class="layer">
          <div class="layer-title">Domain & Business Service Layer</div>
          <div class="layer-chips">
            <div class="chip highlight">EventService</div>
            <div class="chip highlight">UserService</div>
            <div class="chip highlight">RecommendationService</div>
            <div class="chip">Pessimistic Lock Mgr</div>
          </div>
        </div>
        
        <!-- Layer 4: Data Access & Repositories -->
        <div class="layer">
          <div class="layer-title">Persistence & Migration Layer</div>
          <div class="layer-chips">
            <div class="chip db">Spring Data JPA (Hibernate)</div>
            <div class="chip db">EventRepository</div>
            <div class="chip db">RegistrationRepository</div>
            <div class="chip db">Flyway V1–V3 Migrations</div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Right Column: Database & External -->
    <div class="column">
      <div class="card">
        <div class="card-title data"><span>🐬</span> Relational Database</div>
        <div class="item-box" style="border-color: rgba(16, 185, 129, 0.4);">
          <div class="item-name" style="color: #6ee7b7;">MySQL 8.4 LTS</div>
          <div class="item-desc">Transactional Source of Truth</div>
        </div>
        <div class="item-box">
          <div class="item-name">users Table</div>
          <div class="item-desc">BCrypt credentials, UK constraints</div>
        </div>
        <div class="item-box">
          <div class="item-name">events Table</div>
          <div class="item-desc">Date/Category Indexes, Image Blobs</div>
        </div>
        <div class="item-box">
          <div class="item-name">registrations Table</div>
          <div class="item-desc">UK(user_id, event_id), FK Cascades</div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-title client"><span>🔗</span> External Integration</div>
        <div class="item-box">
          <div class="item-name">External Forms</div>
          <div class="item-desc">Validated HTTP/S registration links</div>
        </div>
        <div class="item-box">
          <div class="item-name">Docker Host</div>
          <div class="item-desc">Non-root App & Compose Orchestration</div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

ER_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 30px;
    background: #0b0f19;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    color: #f8fafc;
    width: 1200px;
    height: 650px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    text-align: center;
    margin-bottom: 20px;
  }
  .header h1 {
    margin: 0 0 6px 0;
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
  }
  .header p {
    margin: 0;
    font-size: 14px;
    color: #94a3b8;
  }
  .er-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex: 1;
    position: relative;
    padding: 0 20px;
  }
  .entity-card {
    background: #182234;
    border: 1.5px solid #334155;
    border-radius: 12px;
    width: 330px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    overflow: hidden;
  }
  .entity-card.users { border-color: #3b82f6; }
  .entity-card.registrations { border-color: #8b5cf6; width: 340px; }
  .entity-card.events { border-color: #10b981; }
  
  .entity-header {
    padding: 12px 16px;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .users .entity-header { background: #1e3a8a; color: #93c5fd; }
  .registrations .entity-header { background: #4c1d95; color: #c4b5fd; }
  .events .entity-header { background: #064e3b; color: #6ee7b7; }
  
  .entity-body {
    padding: 10px 14px;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12px;
    background: #0f172a;
  }
  .attribute-row {
    display: flex;
    justify-content: space-between;
    padding: 5px 0;
    border-bottom: 1px solid #1e293b;
  }
  .attribute-row:last-child { border-bottom: none; }
  .attr-left { display: flex; gap: 8px; align-items: center; }
  .key-badge {
    font-size: 9px;
    font-weight: 800;
    padding: 2px 5px;
    border-radius: 4px;
  }
  .pk { background: #eab308; color: #000; }
  .fk { background: #ec4899; color: #fff; }
  .uk { background: #06b6d4; color: #000; }
  
  .attr-name { color: #f1f5f9; font-weight: 500; }
  .attr-type { color: #94a3b8; font-size: 11px; }
  
  /* Connector Lines */
  .relation-connector {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #a855f7;
    font-size: 12px;
    font-weight: 700;
    padding: 0 10px;
    text-align: center;
  }
  .connector-line {
    height: 3px;
    width: 60px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    margin: 8px 0;
  }
  .connector-line.reverse {
    background: linear-gradient(90deg, #8b5cf6, #10b981);
  }
  .cardinality {
    background: #1e293b;
    border: 1px solid #475569;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 11px;
    color: #cbd5e1;
  }
</style>
</head>
<body>
  <div class="header">
    <h1>CampusConnect Relational Entity-Relationship (ER) Model</h1>
    <p>3NF Normalized Relational Schema with Referential Integrity & Compound Unique Constraints</p>
  </div>
  
  <div class="er-container">
    <!-- USERS Entity -->
    <div class="entity-card users">
      <div class="entity-header">
        <span>USERS</span>
        <span style="font-size: 10px; font-weight: normal; opacity: 0.9;">1 (One)</span>
      </div>
      <div class="entity-body">
        <div class="attribute-row">
          <div class="attr-left"><span class="key-badge pk">PK</span><span class="attr-name">id</span></div>
          <span class="attr-type">BIGINT AUTO_INC</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="key-badge uk">UK</span><span class="attr-name">username</span></div>
          <span class="attr-type">VARCHAR(50)</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="attr-name" style="padding-left: 28px;">password</span></div>
          <span class="attr-type">VARCHAR(255)</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="attr-name" style="padding-left: 28px;">role</span></div>
          <span class="attr-type">VARCHAR(20)</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="key-badge uk">UK</span><span class="attr-name">email</span></div>
          <span class="attr-type">VARCHAR(254)</span>
        </div>
      </div>
    </div>
    
    <!-- Connector 1 -->
    <div class="relation-connector">
      <div class="cardinality">1 : N</div>
      <div class="connector-line"></div>
      <span style="font-size: 10px; color: #94a3b8;">Creates / Expresses Interest</span>
    </div>
    
    <!-- REGISTRATIONS Associative Entity -->
    <div class="entity-card registrations">
      <div class="entity-header">
        <span>REGISTRATIONS</span>
        <span style="font-size: 10px; font-weight: normal; opacity: 0.9;">N (Many)</span>
      </div>
      <div class="entity-body">
        <div class="attribute-row">
          <div class="attr-left"><span class="key-badge pk">PK</span><span class="attr-name">id</span></div>
          <span class="attr-type">BIGINT AUTO_INC</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="key-badge fk">FK</span><span class="attr-name">user_id</span></div>
          <span class="attr-type">BIGINT NOT NULL</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="key-badge fk">FK</span><span class="attr-name">event_id</span></div>
          <span class="attr-type">BIGINT NOT NULL</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="attr-name" style="padding-left: 28px;">registration_date</span></div>
          <span class="attr-type">DATETIME (NOW)</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="attr-name" style="padding-left: 28px;">status</span></div>
          <span class="attr-type">VARCHAR(20)</span>
        </div>
        <div style="margin-top: 8px; padding-top: 6px; border-top: 1px dashed #334155; font-size: 10px; color: #a5b4fc;">
          🛡️ UNIQUE (user_id, event_id)<br>
          ⚡ INDEX (event_id, status), (user_id, status)
        </div>
      </div>
    </div>
    
    <!-- Connector 2 -->
    <div class="relation-connector">
      <div class="cardinality">N : 1</div>
      <div class="connector-line reverse"></div>
      <span style="font-size: 10px; color: #94a3b8;">Receives Registration</span>
    </div>
    
    <!-- EVENTS Entity -->
    <div class="entity-card events">
      <div class="entity-header">
        <span>EVENTS</span>
        <span style="font-size: 10px; font-weight: normal; opacity: 0.9;">1 (One)</span>
      </div>
      <div class="entity-body">
        <div class="attribute-row">
          <div class="attr-left"><span class="key-badge pk">PK</span><span class="attr-name">id</span></div>
          <span class="attr-type">BIGINT AUTO_INC</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="attr-name" style="padding-left: 28px;">title</span></div>
          <span class="attr-type">VARCHAR(255)</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="attr-name" style="padding-left: 28px;">date_time</span></div>
          <span class="attr-type">DATETIME</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="attr-name" style="padding-left: 28px;">venue</span></div>
          <span class="attr-type">VARCHAR(255)</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="attr-name" style="padding-left: 28px;">category</span></div>
          <span class="attr-type">VARCHAR(50)</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="attr-name" style="padding-left: 28px;">max_capacity</span></div>
          <span class="attr-type">INT CHECK(&gt;0)</span>
        </div>
        <div class="attribute-row">
          <div class="attr-left"><span class="attr-name" style="padding-left: 28px;">image_data</span></div>
          <span class="attr-type">MEDIUMBLOB</span>
        </div>
        <div style="margin-top: 8px; padding-top: 6px; border-top: 1px dashed #334155; font-size: 10px; color: #6ee7b7;">
          ⚡ INDEX (date_time), (category, date_time)
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

def main():
    arch_path = os.path.join(ASSETS_DIR, 'arch_temp.html')
    er_path = os.path.join(ASSETS_DIR, 'er_temp.html')
    
    with open(arch_path, 'w', encoding='utf-8') as f:
        f.write(ARCH_HTML)
    with open(er_path, 'w', encoding='utf-8') as f:
        f.write(ER_HTML)
        
    print("Rendering vector diagrams via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        page = browser.new_page(viewport={'width': 1200, 'height': 650})
        page.goto(f'file:///{arch_path.replace("\\\\", "/")}')
        page.wait_for_load_state('networkidle')
        page.screenshot(path=os.path.join(ASSETS_DIR, 'system_architecture.png'))
        print("Generated: system_architecture.png")
        
        page.goto(f'file:///{er_path.replace("\\\\", "/")}')
        page.wait_for_load_state('networkidle')
        page.screenshot(path=os.path.join(ASSETS_DIR, 'er_diagram.png'))
        print("Generated: er_diagram.png")
        
        browser.close()
        
    if os.path.exists(arch_path): os.remove(arch_path)
    if os.path.exists(er_path): os.remove(er_path)
    print("All diagrams generated successfully!")

if __name__ == '__main__':
    main()
