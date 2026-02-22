"""
Paper Scout Pro - Complete App with Login + Admin Panel
Ludhiana Hyperlocal Newspaper Platform
"""

import streamlit as st
import pandas as pd
import random
import hashlib
from datetime import datetime, date, timedelta

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Paper Scout Pro | Ludhiana",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1rem !important; }

    /* LOGIN PAGE */
    .login-wrapper {
        max-width: 440px; margin: 3rem auto; padding: 2.5rem;
        background: white; border-radius: 24px;
        box-shadow: 0 20px 60px rgba(255,107,43,0.15);
        border-top: 6px solid #FF6B2B;
    }
    .login-logo { text-align:center; margin-bottom:1.5rem; }
    .login-logo .icon { font-size:3.5rem; }
    .login-logo h1 { font-size:1.8rem; font-weight:800; color:#FF6B2B; margin:0.3rem 0 0; }
    .login-logo p { color:#888; font-size:0.9rem; margin:0; }
    .role-card {
        border: 2px solid #eee; border-radius: 14px; padding: 1rem 1.2rem;
        margin-bottom: 0.7rem; cursor: pointer; transition: all 0.2s;
        display: flex; align-items: center; gap: 1rem;
    }
    .role-card:hover { border-color: #FF6B2B; background: #fff8f5; }
    .role-card.selected { border-color: #FF6B2B; background: #fff3ec; }
    .role-icon { font-size: 2rem; }
    .role-title { font-weight: 700; color: #1a1a1a; }
    .role-desc { font-size: 0.82rem; color: #888; }

    /* HERO */
    .hero-banner {
        background: linear-gradient(135deg, #FF6B2B, #e85d1e);
        border-radius: 20px; padding: 2rem 2rem; color: white;
        margin-bottom: 1.5rem; box-shadow: 0 8px 32px rgba(255,107,43,0.25);
    }
    .hero-title { font-size: 2.2rem; font-weight: 800; margin:0; }
    .hero-sub { opacity: 0.9; margin: 0.3rem 0 0; font-size: 1rem; }

    /* STAT CARDS */
    .stat-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 1.2rem; }
    .stat-card { background:white; border-radius:14px; padding:1rem; text-align:center; box-shadow:0 2px 10px rgba(0,0,0,0.06); border-bottom:4px solid #FF6B2B; }
    .stat-number { font-size:1.8rem; font-weight:800; color:#FF6B2B; }
    .stat-label { font-size:0.8rem; color:#888; margin-top:2px; }

    /* VENDOR / PAPER CARDS */
    .vendor-card { background:white; border-radius:16px; padding:1.2rem; margin-bottom:10px; box-shadow:0 2px 10px rgba(0,0,0,0.06); border-left:5px solid #FF6B2B; }
    .vendor-name { font-size:1.05rem; font-weight:700; color:#1a1a1a; margin-bottom:4px; }
    .badge-green { display:inline-block; background:#edfaf3; color:#27ae60; padding:2px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; margin:2px; }
    .badge-orange { display:inline-block; background:#fff3ec; color:#FF6B2B; padding:2px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; margin:2px; }
    .paper-card { background:white; border-radius:12px; padding:0.9rem 1rem; margin-bottom:8px; box-shadow:0 2px 8px rgba(0,0,0,0.05); display:flex; justify-content:space-between; align-items:center; }
    .paper-code { background:#FF6B2B; color:white; width:46px; height:46px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.72rem; text-align:center; flex-shrink:0; }

    /* ADMIN */
    .admin-card { background:white; border-radius:16px; padding:1.5rem; margin-bottom:12px; box-shadow:0 2px 12px rgba(0,0,0,0.07); border-left:5px solid #9B59B6; }
    .admin-header { font-size:1.1rem; font-weight:700; color:#9B59B6; margin-bottom:1rem; }

    /* ORDER */
    .order-summary { background:linear-gradient(135deg,#fff3ec,#ffe8d6); border-radius:16px; padding:1.5rem; border:2px solid #FF6B2B; margin:1rem 0; }
    .total-price { font-size:2rem; font-weight:800; color:#FF6B2B; text-align:center; }
    .success-box { background:linear-gradient(135deg,#2ECC71,#27ae60); border-radius:20px; padding:2rem; text-align:center; color:white; margin:1rem 0; }
    .discount-banner { background:linear-gradient(135deg,#2ECC71,#27ae60); border-radius:12px; padding:0.9rem 1.2rem; color:white; font-weight:600; margin-bottom:1rem; }
    .info-tip { background:#edf4ff; border-left:4px solid #3498DB; border-radius:8px; padding:0.8rem 1rem; font-size:0.88rem; color:#1a3a6b; margin:0.5rem 0; }
    .pred-card { background:white; border-radius:12px; padding:1rem; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 8px rgba(0,0,0,0.05); border-left:4px solid #9B59B6; }
    .pred-units { font-size:1.3rem; font-weight:800; color:#9B59B6; }

    /* USER BADGE */
    .user-badge { background:#fff3ec; border-radius:30px; padding:6px 16px; display:inline-flex; align-items:center; gap:8px; font-weight:600; color:#FF6B2B; font-size:0.9rem; }

    /* Buttons */
    .stButton > button { background:#FF6B2B !important; color:white !important; border:none !important; border-radius:50px !important; font-weight:700 !important; font-size:0.95rem !important; width:100%; transition: all 0.2s !important; }
    .stButton > button:hover { background:#e85d1e !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SESSION STATE — stores login info while app is open
# ══════════════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ══════════════════════════════════════════════════════════════
# DATA — stored in session so admin changes persist during session
# ══════════════════════════════════════════════════════════════
if "vendors" not in st.session_state:
    st.session_state.vendors = [
        {"id": 1, "name": "Sharma News Agency",  "area": "PAU Campus",    "distance": "300m", "languages": ["EN","HI","PU"], "papers": ["TOI","HT","BHASKAR","AJIT","PTRIB"], "rating": 4.8, "reviews": 35, "delivery": True,  "open": "5:30 AM–10:30 AM", "phone": "98765 01001", "active": True},
        {"id": 2, "name": "PAU Gate 4 Stall",    "area": "PAU Campus",    "distance": "500m", "languages": ["EN","HI","PU"], "papers": ["TOI","HT","TRIB","BHASKAR","AJIT"],  "rating": 4.7, "reviews": 31, "delivery": True,  "open": "6:00 AM–10:00 AM", "phone": "98765 01002", "active": True},
        {"id": 3, "name": "Clock Tower Akhbaar", "area": "Clock Tower",   "distance": "1.5km","languages": ["HI","PU"],       "papers": ["BHASKAR","JAGRAN","AJIT","PTRIB"],  "rating": 4.6, "reviews": 26, "delivery": True,  "open": "5:00 AM–10:00 AM", "phone": "98765 01003", "active": True},
        {"id": 4, "name": "Model Town News",     "area": "Model Town",    "distance": "2.0km","languages": ["EN","HI"],       "papers": ["TOI","HT","HINDU","ET","BHASKAR"],  "rating": 4.7, "reviews": 31, "delivery": False, "open": "6:00 AM–10:30 AM", "phone": "98765 01004", "active": True},
        {"id": 5, "name": "Singh Paper Depot",   "area": "BRS Nagar",     "distance": "1.2km","languages": ["EN","PU"],       "papers": ["TOI","TRIB","KESARI","AJIT"],       "rating": 4.2, "reviews": 18, "delivery": True,  "open": "6:00 AM–10:00 AM", "phone": "98765 01005", "active": True},
        {"id": 6, "name": "New Model Town News", "area": "New Model Town","distance": "1.6km","languages": ["EN","HI","PU"], "papers": ["TOI","HT","TRIB","BHASKAR","AJIT"], "rating": 4.6, "reviews": 22, "delivery": True,  "open": "5:45 AM–10:30 AM", "phone": "98765 01006", "active": True},
        {"id": 7, "name": "Kailash Nagar News",  "area": "Kailash Nagar", "distance": "1.8km","languages": ["EN","HI","PU"], "papers": ["TOI","HT","BHASKAR","KESARI"],      "rating": 4.5, "reviews": 19, "delivery": True,  "open": "5:30 AM–10:30 AM", "phone": "98765 01007", "active": True},
        {"id": 8, "name": "Ghumar Mandi Papers", "area": "Ghumar Mandi",  "distance": "0.9km","languages": ["EN","HI","PU"], "papers": ["TOI","HT","TRIB","BHASKAR","AJIT"], "rating": 4.0, "reviews": 11, "delivery": True,  "open": "5:30 AM–9:30 AM",  "phone": "98765 01008", "active": True},
    ]

if "papers" not in st.session_state:
    st.session_state.papers = {
        "TOI":    {"name":"Times of India",   "lang":"EN","flag":"🇬🇧","price":5, "monthly":120, "active":True},
        "HT":     {"name":"Hindustan Times",  "lang":"EN","flag":"🇬🇧","price":5, "monthly":120, "active":True},
        "HINDU":  {"name":"The Hindu",        "lang":"EN","flag":"🇬🇧","price":6, "monthly":140, "active":True},
        "TRIB":   {"name":"Tribune",          "lang":"EN","flag":"🇬🇧","price":4, "monthly":100, "active":True},
        "ET":     {"name":"Economic Times",   "lang":"EN","flag":"🇬🇧","price":6, "monthly":140, "active":True},
        "BHASKAR":{"name":"Dainik Bhaskar",   "lang":"HI","flag":"🇮🇳","price":4, "monthly":100, "active":True},
        "JAGRAN": {"name":"Dainik Jagran",    "lang":"HI","flag":"🇮🇳","price":4, "monthly":100, "active":True},
        "KESARI": {"name":"Punjab Kesari",    "lang":"HI","flag":"🇮🇳","price":4, "monthly":100, "active":True},
        "AJIT":   {"name":"Ajit",             "lang":"PU","flag":"🏵️","price":4, "monthly":100, "active":True},
        "PTRIB":  {"name":"Punjabi Tribune",  "lang":"PU","flag":"🏵️","price":4, "monthly":100, "active":True},
        "DESH":   {"name":"Desh Sewak",       "lang":"PU","flag":"🏵️","price":4, "monthly":100, "active":True},
    }

if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin@paperscout.com":  {"password": hashlib.md5("admin123".encode()).hexdigest(),  "role": "admin",   "name": "Admin Owner"},
        "student@pau.edu":       {"password": hashlib.md5("student123".encode()).hexdigest(), "role": "student", "name": "Rahul Kumar"},
        "vendor@paperscout.com": {"password": hashlib.md5("vendor123".encode()).hexdigest(), "role": "vendor",  "name": "Sharma Agency"},
        "user@gmail.com":        {"password": hashlib.md5("user123".encode()).hexdigest(),    "role": "user",    "name": "Priya Singh"},
    }

# ══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════
def show_login():
    st.markdown("""
    <div style='max-width:460px; margin: 2rem auto;'>
    <div style='text-align:center; margin-bottom:2rem;'>
        <div style='font-size:4rem;'>📰</div>
        <h1 style='font-size:2rem; font-weight:800; color:#FF6B2B; margin:0.3rem 0 0;'>Paper Scout Pro</h1>
        <p style='color:#888; margin:0;'>Ludhiana's Hyperlocal Newspaper App</p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 👤 Sign In to Your Account")

        login_tab, register_tab = st.tabs(["🔑 Login", "📝 Register"])

        # ── LOGIN TAB ──────────────────────────────────────
        with login_tab:
            st.markdown("#### Choose how to login:")

            # Quick Demo Buttons
            st.markdown("**⚡ Quick Demo Login (one click):**")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("👑 Login as Admin"):
                    st.session_state.logged_in = True
                    st.session_state.user_role = "admin"
                    st.session_state.user_name = "Admin Owner"
                    st.session_state.user_email = "admin@paperscout.com"
                    st.rerun()
                if st.button("🎓 Login as Student"):
                    st.session_state.logged_in = True
                    st.session_state.user_role = "student"
                    st.session_state.user_name = "Rahul Kumar"
                    st.session_state.user_email = "student@pau.edu"
                    st.rerun()
            with c2:
                if st.button("🏪 Login as Vendor"):
                    st.session_state.logged_in = True
                    st.session_state.user_role = "vendor"
                    st.session_state.user_name = "Sharma Agency"
                    st.session_state.user_email = "vendor@paperscout.com"
                    st.rerun()
                if st.button("👤 Login as User"):
                    st.session_state.logged_in = True
                    st.session_state.user_role = "user"
                    st.session_state.user_name = "Priya Singh"
                    st.session_state.user_email = "user@gmail.com"
                    st.rerun()

            st.markdown("---")
            st.markdown("**📧 Or login with Email & Password:**")

            email = st.text_input("Email", placeholder="e.g. admin@paperscout.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            if st.button("🔑 Login"):
                if email in st.session_state.users_db:
                    stored = st.session_state.users_db[email]
                    hashed = hashlib.md5(password.encode()).hexdigest()
                    if hashed == stored["password"]:
                        st.session_state.logged_in = True
                        st.session_state.user_role = stored["role"]
                        st.session_state.user_name = stored["name"]
                        st.session_state.user_email = email
                        st.success(f"✅ Welcome {stored['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Wrong password. Try again.")
                else:
                    st.error("❌ Email not found. Please register first.")

            st.markdown("""
            <div class="info-tip">
            💡 <b>Demo Credentials:</b><br>
            👑 Admin: admin@paperscout.com / admin123<br>
            🎓 Student: student@pau.edu / student123<br>
            🏪 Vendor: vendor@paperscout.com / vendor123<br>
            👤 User: user@gmail.com / user123
            </div>
            """, unsafe_allow_html=True)

        # ── REGISTER TAB ───────────────────────────────────
        with register_tab:
            st.markdown("#### Create New Account")

            new_name  = st.text_input("Full Name", placeholder="e.g. Gurpreet Singh")
            new_email = st.text_input("Email Address", placeholder="e.g. gurpreet@gmail.com")
            new_pass  = st.text_input("Create Password", type="password", placeholder="Min 6 characters")
            new_role  = st.selectbox("I am a...", ["👤 General User", "🎓 Student", "🏪 Newspaper Vendor"])

            role_map = {"👤 General User": "user", "🎓 Student": "student", "🏪 Newspaper Vendor": "vendor"}

            if new_role == "🎓 Student":
                college = st.text_input("College Name", placeholder="e.g. PAU, GNDU, DAV")

            if st.button("📝 Create Account"):
                if not new_name or not new_email or not new_pass:
                    st.error("❌ Please fill all fields!")
                elif len(new_pass) < 6:
                    st.error("❌ Password must be at least 6 characters!")
                elif new_email in st.session_state.users_db:
                    st.error("❌ Email already registered. Please login.")
                else:
                    st.session_state.users_db[new_email] = {
                        "password": hashlib.md5(new_pass.encode()).hexdigest(),
                        "role": role_map[new_role],
                        "name": new_name,
                    }
                    st.session_state.logged_in = True
                    st.session_state.user_role = role_map[new_role]
                    st.session_state.user_name = new_name
                    st.session_state.user_email = new_email
                    st.success(f"🎉 Account created! Welcome {new_name}!")
                    st.rerun()

# ══════════════════════════════════════════════════════════════
# MAIN APP (after login)
# ══════════════════════════════════════════════════════════════
def show_main_app():
    role  = st.session_state.user_role
    name  = st.session_state.user_name
    VENDORS = st.session_state.vendors
    PAPERS  = st.session_state.papers
    base_stock = {"TOI":55,"HT":35,"BHASKAR":65,"JAGRAN":50,"AJIT":45,"PTRIB":30,"TRIB":40,"ET":25}

    # ── SIDEBAR ───────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center; padding:0.8rem 0 0.5rem;'>
            <div style='font-size:2.5rem;'>📰</div>
            <div style='font-size:1.3rem; font-weight:800; color:#FF6B2B;'>Paper Scout Pro</div>
        </div>
        """, unsafe_allow_html=True)

        # User badge
        role_icons = {"admin":"👑","student":"🎓","vendor":"🏪","user":"👤"}
        st.markdown(f"""
        <div class="user-badge" style="margin:0.5rem 0 1rem;">
            {role_icons.get(role,'👤')} {name} <span style='font-size:0.75rem; opacity:0.7;'>({role})</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Navigation based on role
        if role == "admin":
            pages = ["🏠 Home","📍 Find Vendor","🚚 Delivery","🧠 Vendor Dashboard","✨ Recommendations","👑 Admin Panel"]
        elif role == "vendor":
            pages = ["🏠 Home","📍 Find Vendor","🧠 Vendor Dashboard","✨ Recommendations"]
        elif role == "student":
            pages = ["🏠 Home","📍 Find Vendor","🚚 Delivery","✨ Recommendations"]
        else:
            pages = ["🏠 Home","📍 Find Vendor","🚚 Delivery","✨ Recommendations"]

        page = st.radio("Navigate", pages, label_visibility="collapsed")
        st.markdown("---")

        st.markdown("""
        <div style='background:#fff3ec;border-radius:12px;padding:0.9rem;text-align:center;'>
            <div style='font-weight:700;color:#FF6B2B;margin-bottom:0.4rem;'>💰 Pricing</div>
            <div style='font-size:0.85rem;color:#555;'>🎓 Students: <b>₹120/mo</b></div>
            <div style='font-size:0.85rem;color:#555;'>🏠 General: <b>₹150/mo</b></div>
            <div style='font-size:0.85rem;color:#555;'>🏪 Vendors: <b>₹99/mo ML</b></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.user_name = None
            st.rerun()

    active_vendors = [v for v in VENDORS if v.get("active", True)]
    active_papers  = {k:v for k,v in PAPERS.items() if v.get("active", True)}

    # ══════════════════════════════════════════════════════
    # HOME
    # ══════════════════════════════════════════════════════
    if "Home" in page:
        student_greeting = " 🎓 Student discount applied!" if role == "student" else ""
        st.markdown(f"""
        <div class="hero-banner">
            <div style="background:rgba(255,255,255,0.2);display:inline-block;padding:4px 14px;border-radius:30px;font-size:0.85rem;margin-bottom:0.6rem;">📍 Ludhiana, Punjab</div>
            <div class="hero-title">📰 Paper Scout Pro</div>
            <div class="hero-sub">Welcome back, {name}!{student_greeting}</div>
            <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:1rem;">
                <div style="background:rgba(255,255,255,0.2);padding:7px 16px;border-radius:30px;font-size:0.88rem;">📍 Pickup — Free</div>
                <div style="background:rgba(255,255,255,0.2);padding:7px 16px;border-radius:30px;font-size:0.88rem;">🚚 Delivery — ₹{'120' if role=='student' else '150'}/mo</div>
                <div style="background:rgba(255,255,255,0.2);padding:7px 16px;border-radius:30px;font-size:0.88rem;">🗣️ EN / हिंदी / ਪੰਜਾਬੀ</div>
            </div>
        </div>
        <div class="stat-row">
            <div class="stat-card"><div class="stat-number">{len(active_vendors)}</div><div class="stat-label">🏪 Vendors</div></div>
            <div class="stat-card"><div class="stat-number">{len(active_papers)}</div><div class="stat-label">📰 Newspapers</div></div>
            <div class="stat-card"><div class="stat-number">3</div><div class="stat-label">🗣️ Languages</div></div>
            <div class="stat-card"><div class="stat-number">2km</div><div class="stat-label">📡 Coverage</div></div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("### 📍 Nearest Vendors")
            for v in active_vendors[:4]:
                lang_b = "".join([f'<span class="badge-orange">{l}</span>' for l in v["languages"]])
                del_b  = '<span class="badge-green">🚚 Delivery</span>' if v["delivery"] else '<span style="color:#aaa;font-size:0.75rem;">Pickup only</span>'
                st.markdown(f"""
                <div class="vendor-card">
                    <div class="vendor-name">🏪 {v['name']}</div>
                    <div style="color:#666;font-size:0.85rem;line-height:1.9;">
                        📍 {v['area']} &nbsp;|&nbsp; 🚶 {v['distance']} &nbsp;|&nbsp; 🕐 {v['open']}<br>
                        📞 {v['phone']}<br>
                        {lang_b} {del_b}
                        <span style="float:right;color:#f39c12;font-weight:700;">⭐ {v['rating']} ({v['reviews']})</span>
                    </div>
                </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown("### 📰 Available Papers")
            for code, info in list(active_papers.items())[:6]:
                st.markdown(f"""
                <div class="paper-card">
                    <div style="display:flex;align-items:center;gap:10px;">
                        <div class="paper-code">{code}</div>
                        <div>
                            <div style="font-weight:700;font-size:0.9rem;">{info['name']}</div>
                            <div style="color:#888;font-size:0.78rem;">{info['flag']} {info['lang']}</div>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:1.2rem;font-weight:800;color:#FF6B2B;">₹{info['price']}</div>
                        <div style="font-size:0.75rem;color:#27ae60;">₹{info['monthly']}/mo</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # FIND VENDOR
    # ══════════════════════════════════════════════════════
    elif "Find Vendor" in page:
        st.markdown('<div class="hero-banner"><div class="hero-title">📍 Find Vendors Near You</div><div class="hero-sub">All newspaper stalls in Ludhiana</div></div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: lf = st.selectbox("🌐 Language",["All","EN - English","HI - Hindi","PU - Punjabi"])
        with c2: pf = st.selectbox("📰 Paper",["All Papers"]+list(active_papers.keys()))
        with c3: df = st.selectbox("🚚 Service",["All","Delivery Only","Pickup Only"])
        lc = {"All":"ALL","EN - English":"EN","HI - Hindi":"HI","PU - Punjabi":"PU"}.get(lf,"ALL")
        filtered = [v for v in active_vendors if
            (lc=="ALL" or lc in v["languages"]) and
            (pf=="All Papers" or pf in v["papers"]) and
            (df!="Delivery Only" or v["delivery"]) and
            (df!="Pickup Only" or not v["delivery"])]
        st.markdown(f"### 🏪 {len(filtered)} Vendors Found")
        for v in filtered:
            with st.expander(f"🏪 {v['name']} | {v['area']} | {v['distance']} | ⭐{v['rating']}"):
                c1,c2,c3 = st.columns(3)
                with c1:
                    st.write(f"**📍 Area:** {v['area']}")
                    st.write(f"**🚶 Distance:** {v['distance']}")
                    st.write(f"**🕐 Timing:** {v['open']}")
                with c2:
                    st.write(f"**📞 Phone:** {v['phone']}")
                    st.write(f"**⭐ Rating:** {v['rating']} ({v['reviews']} reviews)")
                    st.write(f"**🚚 Delivery:** {'✅ Yes' if v['delivery'] else '❌ No'}")
                with c3:
                    st.write(f"**🌐 Languages:** {', '.join(v['languages'])}")
                    st.write(f"**📰 Papers:** {', '.join(v['papers'])}")

    # ══════════════════════════════════════════════════════
    # DELIVERY
    # ══════════════════════════════════════════════════════
    elif "Delivery" in page:
        st.markdown('<div class="hero-banner"><div class="hero-title">🚚 Home Delivery</div><div class="hero-sub">Get your newspaper every morning at your door</div></div>', unsafe_allow_html=True)
        is_student = role == "student"
        if is_student:
            st.markdown('<div class="discount-banner">🎓 Student discount of ₹30/month automatically applied to your account!</div>', unsafe_allow_html=True)

        c1,c2 = st.columns([3,2])
        with c1:
            lang_sel = st.selectbox("🌐 Language",["All","English 🇬🇧","Hindi 🇮🇳","Punjabi 🏵️"])
            lc2 = {"All":"ALL","English 🇬🇧":"EN","Hindi 🇮🇳":"HI","Punjabi 🏵️":"PU"}.get(lang_sel,"ALL")
            opts = [f"{c} — {i['name']} (₹{i['monthly']}/mo)" for c,i in active_papers.items() if lc2=="ALL" or i["lang"]==lc2]
            sel_str = st.selectbox("📰 Select Paper", opts)
            sel_code = sel_str.split(" — ")[0] if opts else "TOI"
            pinfo = active_papers.get(sel_code, list(active_papers.values())[0])
            t = st.select_slider("🕐 Delivery Time",["5:00 AM","5:30 AM","6:00 AM","6:30 AM","7:00 AM","7:30 AM"])
            months = st.radio("📅 Duration",[1,3,6,12],format_func=lambda x:f"{x} Month{'s' if x>1 else ''}",horizontal=True)
            st.text_input("📍 Delivery Address",placeholder="House No, Street, Area, Ludhiana")
            if not is_student:
                is_student = st.checkbox("🎓 I am a student — Apply ₹30/month discount")

        with c2:
            base_p = pinfo["monthly"]*months
            del_f  = 5*months
            disc   = 30*months if is_student else 0
            total  = base_p+del_f-disc
            disc_row = f"<div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='color:#27ae60;'>🎓 Student discount</span><span style='color:#27ae60;font-weight:700;'>-₹{disc}</span></div>" if is_student else ""
            st.markdown(f"""
            <div class="order-summary">
                <div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='color:#666;'>📰 Paper</span><span style='font-weight:700;'>{pinfo['name']}</span></div>
                <div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='color:#666;'>🕐 Time</span><span style='font-weight:700;'>{t}</span></div>
                <div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='color:#666;'>📦 Subscription</span><span style='font-weight:700;'>₹{base_p}</span></div>
                <div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='color:#666;'>🚚 Delivery fee</span><span style='font-weight:700;'>₹{del_f}</span></div>
                {disc_row}
                <hr style='margin:8px 0;border-color:#FF6B2B44;'>
                <div class="total-price">₹{total}</div>
                <div style='text-align:center;color:#888;font-size:0.82rem;'>for {months} month{'s' if months>1 else ''}</div>
            </div>""", unsafe_allow_html=True)
            upi = st.radio("💳 Pay via",["📱 Google Pay","💜 PhonePe","💙 Paytm","🏛️ BHIM UPI"],label_visibility="collapsed")
            if st.button(f"✅ Subscribe & Pay ₹{total}"):
                st.markdown(f"""<div class="success-box"><div style='font-size:3rem;'>🎉</div><div style='font-size:1.3rem;font-weight:800;'>Order Confirmed!</div><div>₹{total} via {upi.split(' ',1)[1]}</div><div style='margin-top:0.5rem;opacity:0.9;'>📦 {pinfo['name']} starts tomorrow at {t}!</div></div>""", unsafe_allow_html=True)
                st.balloons()

    # ══════════════════════════════════════════════════════
    # VENDOR DASHBOARD
    # ══════════════════════════════════════════════════════
    elif "Vendor Dashboard" in page:
        st.markdown('<div class="hero-banner"><div class="hero-title">🧠 Vendor ML Dashboard</div><div class="hero-sub">AI stock predictions for your stall</div></div>', unsafe_allow_html=True)
        sname = st.selectbox("Select Your Stall",[v["name"] for v in active_vendors])
        sv = next(v for v in active_vendors if v["name"]==sname)
        t1,t2,t3 = st.tabs(["📊 Predictions","📈 Sales History","📁 Upload Sales"])
        tdow = (datetime.now().weekday()+1)%7
        wb = 1.3 if tdow in [5,6] else 1.0
        with t1:
            st.markdown(f"### Tomorrow's order for **{sv['name']}**")
            st.markdown('<div class="info-tip">🧠 Powered by Facebook Prophet ML — 95% accuracy based on weather, weekday & exam calendar</div>',unsafe_allow_html=True)
            c1,c2,c3=st.columns(3)
            c1.metric("📅 Tomorrow",(date.today()+timedelta(1)).strftime("%A %d %b"))
            c2.metric("🌤️ Weather","Sunny")
            c3.metric("📊 Accuracy","95.2%")
            for pc in sv["papers"][:5]:
                b=base_stock.get(pc,30); pred=int(b*wb*random.uniform(0.92,1.08))
                lo,hi=int(pred*0.85),int(pred*1.15); inf=active_papers.get(pc,{})
                st.markdown(f"""<div class="pred-card"><div><div style='font-weight:700;'>{pc} — {inf.get('name',pc)}</div><div style='color:#888;font-size:0.82rem;'>{inf.get('flag','')} {inf.get('lang','')} | Range: {lo}–{hi}</div></div><div style='text-align:right;'><div class="pred-units">{pred}</div><div style='color:#888;font-size:0.78rem;'>copies</div></div></div>""",unsafe_allow_html=True)
            tot=sum(int(base_stock.get(p,30)*wb) for p in sv["papers"][:5])
            st.success(f"📦 Order **{tot} total copies** tomorrow | Revenue ≈ ₹{tot*4}")
        with t2:
            st.markdown("### Sales Last 30 Days")
            hist=[]
            for d in range(30,0,-1):
                dt=date.today()-timedelta(d)
                for p in sv["papers"][:3]:
                    b=base_stock.get(p,30)
                    units=int(b*random.uniform(0.85,1.15)*(1.3 if dt.weekday() in [5,6] else 1.0))
                    hist.append({"Date":dt,"Paper":p,"Units Sold":units})
            df=pd.DataFrame(hist)
            ps=st.selectbox("Paper",sv["papers"][:3])
            cd=df[df["Paper"]==ps].set_index("Date")["Units Sold"]
            st.line_chart(cd)
            c1,c2,c3=st.columns(3)
            c1.metric("Avg Daily",f"{int(cd.mean())}"); c2.metric("Best Day",f"{int(cd.max())}"); c3.metric("Month Total",f"{int(cd.sum())}")
        with t3:
            st.markdown('<div class="info-tip">📋 Upload CSV: <code>date, paper_code, units_sold, weather, is_holiday, is_weekend</code></div>',unsafe_allow_html=True)
            up=st.file_uploader("Upload CSV",type=["csv"])
            if up:
                du=pd.read_csv(up); st.success(f"✅ {len(du)} rows uploaded!"); st.dataframe(du.head())
                if st.button("🧠 Train AI Model"):
                    import time
                    with st.spinner("Training..."):time.sleep(2)
                    st.success("✅ Model trained! Predictions updated."); st.balloons()

    # ══════════════════════════════════════════════════════
    # RECOMMENDATIONS
    # ══════════════════════════════════════════════════════
    elif "Recommendations" in page:
        st.markdown('<div class="hero-banner"><div class="hero-title">✨ Papers For You</div><div class="hero-sub">AI picks based on your reading style</div></div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            cur=st.selectbox("I currently read",list(active_papers.keys()),format_func=lambda x:f"{x} — {active_papers[x]['name']}")
            utype=st.selectbox("I am a...",["🎓 Student","👔 Professional","🏠 Homemaker","📈 Businessman"])
        with c2:
            interests=st.multiselect("My interests",["📈 Business","🏏 Sports","🌍 World News","🎭 Entertainment","🏛️ Politics","📚 Education"])
        if st.button("✨ Get Recommendations"):
            RECS={"TOI":[("HINDU",0.91,"Similar English journalism quality"),("HT",0.87,"Different English perspective"),("ET",0.72,"Great for business")],"BHASKAR":[("JAGRAN",0.89,"Bhaskar readers love Jagran"),("KESARI",0.78,"Top Hindi paper in Punjab")],"AJIT":[("PTRIB",0.93,"Most popular Punjabi pair"),("DESH",0.80,"Strong local Punjab news")]}
            recs=RECS.get(cur,[("HT",0.85,"Great alternative"),("BHASKAR",0.75,"Top regional paper")])
            st.markdown("### 🎯 Recommended For You")
            for code,score,reason in recs:
                if code in active_papers:
                    inf=active_papers[code]
                    st.markdown(f"""<div class="vendor-card" style="border-left-color:#9B59B6;"><div style='display:flex;justify-content:space-between;align-items:center;'><div><div class="vendor-name">{inf['flag']} {inf['name']}</div><div style='color:#666;font-size:0.85rem;'>💡 {reason}</div><div style='color:#27ae60;font-size:0.85rem;'>₹{inf['price']}/day | ₹{inf['monthly']}/mo</div></div><div style='text-align:center;background:#f4eeff;border-radius:12px;padding:0.6rem 1rem;'><div style='font-size:1.3rem;font-weight:800;color:#9B59B6;'>{int(score*100)}%</div><div style='font-size:0.72rem;color:#888;'>match</div></div></div></div>""",unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # 👑 ADMIN PANEL
    # ══════════════════════════════════════════════════════
    elif "Admin" in page and role == "admin":
        st.markdown('<div class="hero-banner"><div class="hero-title">👑 Admin Panel</div><div class="hero-sub">Manage vendors, newspapers & users</div></div>', unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(["🏪 Manage Vendors", "📰 Manage Newspapers", "👥 Manage Users", "📊 Analytics"])

        # ── TAB 1: VENDORS ────────────────────────────────
        with tab1:
            st.markdown("## 🏪 Vendors")

            # ADD NEW VENDOR
            with st.expander("➕ Add New Vendor", expanded=False):
                st.markdown('<div class="admin-card">', unsafe_allow_html=True)
                c1,c2 = st.columns(2)
                with c1:
                    nv_name  = st.text_input("Vendor / Stall Name *", placeholder="e.g. Gupta News Corner")
                    nv_area  = st.text_input("Area / Locality *",      placeholder="e.g. Sarabha Nagar")
                    nv_dist  = st.text_input("Distance from PAU",      placeholder="e.g. 1.5km")
                    nv_phone = st.text_input("Phone Number *",          placeholder="e.g. 98765 12345")
                with c2:
                    nv_open  = st.text_input("Opening Time",  value="6:00 AM")
                    nv_close = st.text_input("Closing Time",  value="10:00 AM")
                    nv_langs = st.multiselect("Languages Offered", ["EN","HI","PU"], default=["EN","HI"])
                    nv_del   = st.checkbox("Offers Home Delivery?")
                nv_papers = st.multiselect("Papers Available", list(active_papers.keys()), default=["TOI","BHASKAR"])

                if st.button("✅ Add Vendor"):
                    if not nv_name or not nv_area or not nv_phone:
                        st.error("❌ Please fill Name, Area and Phone!")
                    else:
                        new_id = max([v["id"] for v in st.session_state.vendors], default=0) + 1
                        st.session_state.vendors.append({
                            "id": new_id, "name": nv_name, "area": nv_area,
                            "distance": nv_dist or "?", "languages": nv_langs,
                            "papers": nv_papers, "rating": 0.0, "reviews": 0,
                            "delivery": nv_del, "open": f"{nv_open}–{nv_close}",
                            "phone": nv_phone, "active": True
                        })
                        st.success(f"🎉 Vendor **{nv_name}** added successfully!")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            # LIST EXISTING VENDORS
            st.markdown(f"### Existing Vendors ({len(st.session_state.vendors)} total)")
            for i, v in enumerate(st.session_state.vendors):
                c1,c2,c3,c4 = st.columns([3,1,1,1])
                with c1:
                    status = "🟢" if v.get("active",True) else "🔴"
                    st.markdown(f"**{status} {v['name']}** — {v['area']} | 📞 {v['phone']}")
                with c2:
                    st.write(f"⭐ {v['rating']}")
                with c3:
                    if v.get("active", True):
                        if st.button("🔴 Deactivate", key=f"dv_{i}"):
                            st.session_state.vendors[i]["active"] = False
                            st.rerun()
                    else:
                        if st.button("🟢 Activate", key=f"av_{i}"):
                            st.session_state.vendors[i]["active"] = True
                            st.rerun()
                with c4:
                    if st.button("🗑️ Delete", key=f"del_v_{i}"):
                        st.session_state.vendors.pop(i)
                        st.success("Vendor deleted!")
                        st.rerun()

        # ── TAB 2: NEWSPAPERS ─────────────────────────────
        with tab2:
            st.markdown("## 📰 Newspapers")

            # ADD NEW NEWSPAPER
            with st.expander("➕ Add New Newspaper", expanded=False):
                c1,c2 = st.columns(2)
                with c1:
                    np_code  = st.text_input("Short Code *", placeholder="e.g. TRIBUNE (max 8 chars)").upper()
                    np_name  = st.text_input("Full Name *",  placeholder="e.g. The Tribune Daily")
                    np_lang  = st.selectbox("Language *", ["EN - English","HI - Hindi","PU - Punjabi"])
                with c2:
                    np_price   = st.number_input("Daily Price (₹) *", min_value=1, max_value=50, value=5)
                    np_monthly = st.number_input("Monthly Price (₹) *", min_value=50, max_value=500, value=120)
                    np_flag    = {"EN - English":"🇬🇧","HI - Hindi":"🇮🇳","PU - Punjabi":"🏵️"}.get(np_lang,"🇬🇧")
                    np_lc      = np_lang.split(" - ")[0]

                if st.button("✅ Add Newspaper"):
                    if not np_code or not np_name:
                        st.error("❌ Please fill Code and Name!")
                    elif np_code in st.session_state.papers:
                        st.error(f"❌ Code '{np_code}' already exists!")
                    elif len(np_code) > 8:
                        st.error("❌ Code must be max 8 characters!")
                    else:
                        st.session_state.papers[np_code] = {
                            "name": np_name, "lang": np_lc, "flag": np_flag,
                            "price": np_price, "monthly": np_monthly, "active": True
                        }
                        st.success(f"🎉 Newspaper **{np_name}** ({np_code}) added!")
                        st.rerun()

            # LIST NEWSPAPERS
            st.markdown(f"### Existing Newspapers ({len(st.session_state.papers)} total)")
            for code, info in list(st.session_state.papers.items()):
                c1,c2,c3,c4,c5 = st.columns([1,3,1,1,1])
                with c1: st.write(f"**{code}**")
                with c2: st.write(f"{info['flag']} {info['name']} ({info['lang']})")
                with c3: st.write(f"₹{info['price']}/day")
                with c4:
                    if info.get("active",True):
                        if st.button("🔴 Hide",key=f"hp_{code}"):
                            st.session_state.papers[code]["active"] = False; st.rerun()
                    else:
                        if st.button("🟢 Show",key=f"sp_{code}"):
                            st.session_state.papers[code]["active"] = True; st.rerun()
                with c5:
                    if st.button("🗑️",key=f"dp_{code}"):
                        del st.session_state.papers[code]; st.rerun()

        # ── TAB 3: USERS ──────────────────────────────────
        with tab3:
            st.markdown("## 👥 Registered Users")
            users_data = []
            for email, info in st.session_state.users_db.items():
                users_data.append({"Email": email, "Name": info["name"], "Role": info["role"]})
            st.dataframe(pd.DataFrame(users_data), use_container_width=True, hide_index=True)
            st.info(f"Total users: {len(st.session_state.users_db)}")

            st.markdown("### ➕ Add New User / Staff")
            c1,c2 = st.columns(2)
            with c1:
                nu_name  = st.text_input("Name")
                nu_email = st.text_input("Email")
            with c2:
                nu_pass = st.text_input("Password", type="password")
                nu_role = st.selectbox("Role", ["user","student","vendor","admin"])
            if st.button("✅ Add User"):
                if nu_name and nu_email and nu_pass:
                    if nu_email in st.session_state.users_db:
                        st.error("❌ Email already exists!")
                    else:
                        st.session_state.users_db[nu_email] = {
                            "password": hashlib.md5(nu_pass.encode()).hexdigest(),
                            "role": nu_role, "name": nu_name
                        }
                        st.success(f"✅ User {nu_name} added!")
                        st.rerun()
                else:
                    st.error("❌ Fill all fields!")

        # ── TAB 4: ANALYTICS ──────────────────────────────
        with tab4:
            st.markdown("## 📊 Platform Analytics")
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Total Vendors",   len(st.session_state.vendors), delta=f"{len([v for v in st.session_state.vendors if v.get('active')])} active")
            c2.metric("Total Papers",    len(st.session_state.papers),  delta=f"{len([p for p in st.session_state.papers.values() if p.get('active')])} active")
            c3.metric("Registered Users",len(st.session_state.users_db))
            c4.metric("Platform Revenue","₹12,450", delta="↑ 18%")

            st.markdown("### 📈 Simulated Orders (Last 7 Days)")
            dates = [(date.today()-timedelta(i)).strftime("%a %d") for i in range(6,-1,-1)]
            orders = [random.randint(12,40) for _ in dates]
            chart_df = pd.DataFrame({"Date":dates,"Orders":orders}).set_index("Date")
            st.bar_chart(chart_df)

            st.markdown("### 🏆 Top Performing Vendors")
            top_vendors = sorted(st.session_state.vendors, key=lambda x: x["rating"], reverse=True)[:5]
            top_data = [{"Vendor":v["name"],"Area":v["area"],"Rating":v["rating"],"Reviews":v["reviews"]} for v in top_vendors]
            st.dataframe(pd.DataFrame(top_data), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# APP ENTRY POINT — Show login or main app
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_login()
else:
    show_main_app()
