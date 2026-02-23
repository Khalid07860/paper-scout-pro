"""
Paper Scout Pro — Complete Single File App
Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import random
import hashlib
import re as _re
from datetime import date, timedelta, datetime


# ================================================================
# ── DATA ──
# ================================================================

import streamlit as st
import hashlib


def h(pw: str) -> str:
    return hashlib.md5(pw.encode()).hexdigest()


def init():
    """Initialize all session state once."""
    defaults = {
        "logged_in": False,
        "role": None,
        "name": None,
        "email": None,
        "my_subs": [],          # list of subscription dicts
        "page": "login",        # login | register | phone
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if "users_db" not in st.session_state:
        st.session_state.users_db = {
            "admin@paperscout.com":  {"pw": h("admin123"),   "role": "admin",   "name": "Admin Owner",   "phone": "98765-00000"},
            "student@pau.edu":       {"pw": h("student123"),  "role": "student", "name": "Rahul Kumar",    "phone": "98765-11111"},
            "vendor@paperscout.com": {"pw": h("vendor123"),   "role": "vendor",  "name": "Sharma Agency",  "phone": "98765-01001"},
            "user@gmail.com":        {"pw": h("user123"),     "role": "user",    "name": "Priya Singh",    "phone": "98765-22222"},
        }

    if "vendors" not in st.session_state:
        st.session_state.vendors = [
            {"id":1,"name":"Sharma News Agency","area":"PAU Campus","dist":"300m","langs":["EN","HI","PU"],"papers":["TOI","HT","BHASKAR","AJIT","PTRIB"],"rating":4.8,"reviews":35,"delivery":True,"open":"5:30–10:30 AM","phone":"98765 01001","active":True},
            {"id":2,"name":"PAU Gate 4 Stall","area":"PAU Campus","dist":"500m","langs":["EN","HI","PU"],"papers":["TOI","HT","TRIB","BHASKAR","AJIT"],"rating":4.7,"reviews":31,"delivery":True,"open":"6:00–10:00 AM","phone":"98765 01002","active":True},
            {"id":3,"name":"Clock Tower Akhbaar","area":"Clock Tower","dist":"1.5km","langs":["HI","PU"],"papers":["BHASKAR","JAGRAN","AJIT","PTRIB"],"rating":4.6,"reviews":26,"delivery":True,"open":"5:00–10:00 AM","phone":"98765 01003","active":True},
            {"id":4,"name":"Model Town News","area":"Model Town","dist":"2.0km","langs":["EN","HI"],"papers":["TOI","HT","HINDU","ET","BHASKAR"],"rating":4.7,"reviews":31,"delivery":False,"open":"6:00–10:30 AM","phone":"98765 01004","active":True},
            {"id":5,"name":"Singh Paper Depot","area":"BRS Nagar","dist":"1.2km","langs":["EN","PU"],"papers":["TOI","TRIB","KESARI","AJIT"],"rating":4.2,"reviews":18,"delivery":True,"open":"6:00–10:00 AM","phone":"98765 01005","active":True},
            {"id":6,"name":"Ghumar Mandi Papers","area":"Ghumar Mandi","dist":"0.9km","langs":["EN","HI","PU"],"papers":["TOI","HT","TRIB","BHASKAR","AJIT"],"rating":4.0,"reviews":11,"delivery":True,"open":"5:30–9:30 AM","phone":"98765 01006","active":True},
        ]

    if "papers" not in st.session_state:
        st.session_state.papers = {
            "TOI":    {"name":"Times of India",  "lang":"EN","flag":"🇬🇧","price":5, "monthly":120,"yearly":1200,"active":True},
            "HT":     {"name":"Hindustan Times", "lang":"EN","flag":"🇬🇧","price":5, "monthly":120,"yearly":1200,"active":True},
            "HINDU":  {"name":"The Hindu",       "lang":"EN","flag":"🇬🇧","price":6, "monthly":140,"yearly":1400,"active":True},
            "TRIB":   {"name":"Tribune",         "lang":"EN","flag":"🇬🇧","price":4, "monthly":100,"yearly":1000,"active":True},
            "ET":     {"name":"Economic Times",  "lang":"EN","flag":"🇬🇧","price":6, "monthly":140,"yearly":1400,"active":True},
            "BHASKAR":{"name":"Dainik Bhaskar",  "lang":"HI","flag":"🇮🇳","price":4, "monthly":100,"yearly":1000,"active":True},
            "JAGRAN": {"name":"Dainik Jagran",   "lang":"HI","flag":"🇮🇳","price":4, "monthly":100,"yearly":1000,"active":True},
            "KESARI": {"name":"Punjab Kesari",   "lang":"HI","flag":"🇮🇳","price":4, "monthly":100,"yearly":1000,"active":True},
            "AJIT":   {"name":"Ajit",            "lang":"PU","flag":"🏵️","price":4, "monthly":100,"yearly":1000,"active":True},
            "PTRIB":  {"name":"Punjabi Tribune", "lang":"PU","flag":"🏵️","price":4, "monthly":100,"yearly":1000,"active":True},
            "DESH":   {"name":"Desh Sewak",      "lang":"PU","flag":"🏵️","price":4, "monthly":100,"yearly":1000,"active":True},
        }


def active_vendors():
    return [v for v in st.session_state.vendors if v.get("active", True)]


def active_papers():
    return {k: v for k, v in st.session_state.papers.items() if v.get("active", True)}


def login_user(email: str):
    info = st.session_state.users_db[email]
    st.session_state.logged_in = True
    st.session_state.role  = info["role"]
    st.session_state.name  = info["name"]
    st.session_state.email = email
    st.session_state.my_subs = []
    st.rerun()


def logout():
    for k in ["logged_in","role","name","email","my_subs"]:
        st.session_state[k] = False if k == "logged_in" else ([] if k == "my_subs" else None)
    st.session_state.page = "login"
    st.rerun()

# ================================================================
# ── STYLES ──
# ================================================================

import streamlit as st

def apply():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ── LOGIN ── */
    .lp-wrap {
        min-height: 100vh; display: flex;
        align-items: center; justify-content: center;
        background: #f4f4f5; padding: 2rem 1rem;
    }
    .lp-card {
        background: white; border-radius: 20px;
        padding: 2.4rem 2.2rem; width: 100%; max-width: 420px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.10);
    }
    .lp-logo { text-align: center; margin-bottom: 1.8rem; }
    .lp-logo-icon { font-size: 3rem; display: block; margin-bottom: .4rem; }
    .lp-logo-name { font-size: 1.5rem; font-weight: 800; color: #FF6B2B; }
    .lp-logo-sub  { font-size: .82rem; color: #888; }

    .lp-title { font-size: 1.3rem; font-weight: 700; color: #111; margin-bottom: .3rem; }
    .lp-sub   { font-size: .84rem; color: #888; margin-bottom: 1.4rem; }

    .lp-role-hint {
        background: #fff8f5; border-left: 3px solid #FF6B2B;
        border-radius: 8px; padding: 7px 12px;
        font-size: .8rem; color: #c94d10;
        margin-top: -8px; margin-bottom: 1rem;
    }
    .lp-divider {
        display: flex; align-items: center; gap: 10px;
        color: #ccc; font-size: .78rem; margin: 1rem 0;
    }
    .lp-divider::before, .lp-divider::after {
        content:''; flex:1; height:1px; background:#eee;
    }
    .lp-forgot { text-align: right; font-size: .8rem; margin-top: -6px; margin-bottom: .8rem; }
    .lp-forgot a { color: #FF6B2B; text-decoration: none; font-weight: 600; }
    .lp-switch { text-align: center; font-size: .83rem; color: #888; margin-top: 1rem; }
    .lp-demo-box {
        background: #fafafa; border: 1px solid #eee;
        border-radius: 10px; padding: 10px 14px;
        font-size: .74rem; color: #777; line-height: 1.9;
        margin-top: 1rem;
    }

    /* ── MAIN APP ── */
    .block-container { padding-top: 1rem !important; }

    .hero {
        background: linear-gradient(135deg, #FF6B2B, #d94f15);
        border-radius: 16px; padding: 1.6rem 2rem; color: white;
        margin-bottom: 1.2rem;
        box-shadow: 0 6px 20px rgba(255,107,43,.22);
    }
    .hero h2 { font-size: 1.7rem; font-weight: 800; margin: 0 0 3px; }
    .hero p  { font-size: .92rem; opacity: .9; margin: 0; }

    .hero-vendor  { background: linear-gradient(135deg,#7C3AED,#5B21B6) !important; }
    .hero-admin   { background: linear-gradient(135deg,#1e293b,#334155) !important; }
    .hero-student { background: linear-gradient(135deg,#059669,#047857) !important; }

    .stat-row { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-bottom:1.2rem; }
    .stat-card {
        background:white; border-radius:12px; padding:.9rem;
        text-align:center; box-shadow:0 2px 8px rgba(0,0,0,.05);
        border-bottom:4px solid #FF6B2B;
    }
    .stat-card.vc { border-bottom-color:#7C3AED; }
    .stat-card.ac { border-bottom-color:#1e293b; }
    .stat-card.sc { border-bottom-color:#059669; }
    .stat-num { font-size:1.6rem; font-weight:800; color:#FF6B2B; }
    .stat-num.vc { color:#7C3AED; }
    .stat-num.ac { color:#1e293b; }
    .stat-num.sc { color:#059669; }
    .stat-lbl { font-size:.72rem; color:#888; margin-top:2px; }

    .card {
        background:white; border-radius:12px; padding:1.1rem 1.3rem;
        margin-bottom:10px; box-shadow:0 2px 8px rgba(0,0,0,.05);
        border-left:5px solid #FF6B2B;
    }
    .card.vc  { border-left-color:#7C3AED; }
    .card.gc  { border-left-color:#059669; }
    .card.bc  { border-left-color:#3B82F6; }
    .card-title { font-size:.95rem; font-weight:700; color:#111; margin-bottom:3px; }
    .card-sub   { font-size:.8rem; color:#666; line-height:1.75; }

    .badge { display:inline-block; padding:2px 9px; border-radius:20px; font-size:.7rem; font-weight:600; margin:2px; }
    .b-or  { background:#fff3ec; color:#FF6B2B; }
    .b-gr  { background:#ecfdf5; color:#059669; }
    .b-bl  { background:#eff6ff; color:#3B82F6; }
    .b-pu  { background:#f5f3ff; color:#7C3AED; }

    .alert-g { background:#ecfdf5; border:1.5px solid #10B981; border-radius:10px; padding:.75rem 1rem; color:#065f46; font-size:.83rem; margin:.5rem 0; }
    .alert-o { background:#fff8f5; border:1.5px solid #FF6B2B; border-radius:10px; padding:.75rem 1rem; color:#9a3412; font-size:.83rem; margin:.5rem 0; }
    .alert-b { background:#eff6ff; border:1.5px solid #3B82F6; border-radius:10px; padding:.75rem 1rem; color:#1e3a8a; font-size:.83rem; margin:.5rem 0; }

    .sub-card {
        background:white; border-radius:14px; padding:1.2rem;
        text-align:center; box-shadow:0 2px 10px rgba(0,0,0,.07);
        border:2px solid #eee;
    }
    .sub-card.hot { border-color:#FF6B2B; background:#fff8f5; }
    .sub-price  { font-size:1.8rem; font-weight:800; color:#FF6B2B; }
    .sub-per    { font-size:.75rem; color:#888; }
    .sub-badge  { background:#FF6B2B; color:white; font-size:.68rem; font-weight:700;
                  padding:2px 10px; border-radius:20px; display:inline-block; margin-bottom:.4rem; }

    .order-box {
        background:linear-gradient(135deg,#fff8f5,#ffe8d6);
        border:2px solid #FF6B2B; border-radius:14px; padding:1.2rem; margin:.7rem 0;
    }
    .order-row { display:flex; justify-content:space-between; margin-bottom:5px; font-size:.85rem; }
    .order-total { font-size:1.7rem; font-weight:800; color:#FF6B2B; text-align:center; margin-top:.5rem; }

    .pred-row {
        background:white; border-radius:10px; padding:.85rem 1rem;
        margin-bottom:7px; display:flex; justify-content:space-between; align-items:center;
        box-shadow:0 1px 5px rgba(0,0,0,.05); border-left:4px solid #7C3AED;
    }
    .pred-num { font-size:1.25rem; font-weight:800; color:#7C3AED; }

    .success-box {
        background:linear-gradient(135deg,#10B981,#059669);
        border-radius:14px; padding:1.8rem; text-align:center; color:white; margin:.8rem 0;
    }

    /* Buttons */
    .stButton > button {
        background:linear-gradient(135deg,#FF6B2B,#e85d1e) !important;
        color:white !important; border:none !important;
        border-radius:10px !important; font-weight:700 !important;
        font-size:.88rem !important; width:100%;
        box-shadow:0 3px 10px rgba(255,107,43,.28) !important;
        transition:all .15s !important;
    }
    .stButton > button:hover { transform:translateY(-1px) !important; }

    .user-chip {
        border-radius:10px; padding:8px 12px; text-align:center;
        font-weight:700; font-size:.83rem; margin-bottom:.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ================================================================
# ── LOGIN ──
# ================================================================

import streamlit as st
import hashlib
import re


# ── helpers ──────────────────────────────────────────────────
def valid_email(e):  return re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$", e, re.I)
def valid_phone(p):  return re.match(r"^[6-9]\d{9}$", p.replace(" ","").replace("-",""))


ROLE_MAP = {
    "👑  Admin / Owner":    "admin",
    "🎓  Student":          "student",
    "🏪  Newspaper Vendor": "vendor",
    "👤  General User":     "user",
}
ROLE_HINTS = {
    "admin":   "Full access — manage vendors, papers, users & analytics",
    "student": "Get ₹30/month discount on all subscriptions automatically",
    "vendor":  "Access AI stock predictions for your stall",
    "user":    "Find vendors & subscribe to home delivery",
}
DEMO_CREDS = {
    "admin":   ("admin@paperscout.com",  "admin123"),
    "student": ("student@pau.edu",       "student123"),
    "vendor":  ("vendor@paperscout.com", "vendor123"),
    "user":    ("user@gmail.com",        "user123"),
}


def render_login():
    """Render login/register/phone based on st.session_state.page"""

    # Hide sidebar on login
    st.markdown("<style>[data-testid='stSidebar']{display:none!important;}.block-container{max-width:460px!important;margin:0 auto!important;padding-top:5vh!important;}</style>", unsafe_allow_html=True)

    pg = st.session_state.get("page", "login")

    if   pg == "login":    _login_form()
    elif pg == "register": _register_form()
    elif pg == "phone":    _phone_form()


# ══════════════════════════════════════════════════════════════
#  LOGIN FORM
# ══════════════════════════════════════════════════════════════
def _login_form():
    # Logo
    st.markdown("""
    <div style="text-align:center;margin-bottom:1.8rem;">
        <span style="font-size:3.2rem;">📰</span><br>
        <span style="font-size:1.6rem;font-weight:800;color:#FF6B2B;">Paper Scout Pro</span><br>
        <span style="color:#888;font-size:.83rem;">Ludhiana's Newspaper Platform</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔐 Sign In")
    st.markdown("<p style='color:#888;font-size:.85rem;margin-top:-8px;margin-bottom:1.2rem;'>Welcome back! Please sign in to continue.</p>", unsafe_allow_html=True)

    # Role selector
    role_label = st.selectbox("**Log in as**", list(ROLE_MAP.keys()))
    role_val   = ROLE_MAP[role_label]
    st.markdown(f"<div class='lp-role-hint'>ℹ️ {ROLE_HINTS[role_val]}</div>", unsafe_allow_html=True)

    # Fields
    email = st.text_input("📧 Email ID", placeholder="yourname@gmail.com", key="li_email")
    pw    = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="li_pw")

    # Forgot password
    st.markdown("<div class='lp-forgot'><a href='#'>Forgot Password?</a></div>", unsafe_allow_html=True)

    # Login button
    if st.button("🔑  Sign In", use_container_width=True, key="btn_login"):
        _do_login(email.strip(), pw, role_val)

    # Divider
    st.markdown("<div class='lp-divider'>OR</div>", unsafe_allow_html=True)

    # Social-style quick logins (auto fill correct role)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔴  Continue with Gmail", use_container_width=True, key="btn_gmail"):
            # Gmail → auto-login for selected role (demo mode)
            demo_email, _ = DEMO_CREDS[role_val]
            login_user(demo_email)
    with c2:
        if st.button("📱  Login with OTP", use_container_width=True, key="btn_otp"):
            st.session_state.page = "phone"
            st.rerun()

    # Switch to register
    st.markdown("<div class='lp-switch'>Don't have an account?</div>", unsafe_allow_html=True)
    if st.button("📝  Create Account — It's Free", use_container_width=True, key="btn_to_reg"):
        st.session_state.page = "register"
        st.rerun()

    # Demo box
    st.markdown("""
    <div class='lp-demo-box'>
    <b>🔑 Demo Accounts:</b><br>
    👑 admin@paperscout.com &nbsp; / &nbsp; admin123<br>
    🎓 student@pau.edu &nbsp; / &nbsp; student123<br>
    🏪 vendor@paperscout.com &nbsp; / &nbsp; vendor123<br>
    👤 user@gmail.com &nbsp; / &nbsp; user123
    </div>
    """, unsafe_allow_html=True)


def _do_login(email, pw, expected_role):
    if not email or not pw:
        st.error("❌ Please enter your email and password.")
        return
    db = st.session_state.users_db
    if email not in db:
        st.error("❌ Email not found. Please create an account first.")
        return
    info = db[email]
    if info["pw"] != h(pw):
        st.error("❌ Incorrect password. Try again.")
        return
    if info["role"] != expected_role:
        st.warning(f"⚠️ This email is a **{info['role']}** account. Please select the correct role above.")
        return
    login_user(email)


# ══════════════════════════════════════════════════════════════
#  REGISTER FORM
# ══════════════════════════════════════════════════════════════
def _register_form():
    st.markdown("""
    <div style="text-align:center;margin-bottom:1.4rem;">
        <span style="font-size:2.4rem;">📰</span><br>
        <span style="font-size:1.4rem;font-weight:800;color:#FF6B2B;">Paper Scout Pro</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ Create Your Account")
    st.markdown("<p style='color:#888;font-size:.83rem;margin-top:-8px;margin-bottom:1.2rem;'>Join free — takes less than a minute!</p>", unsafe_allow_html=True)

    # Row 1: Name + Phone
    c1, c2 = st.columns(2)
    with c1: rname  = st.text_input("👤 Full Name *",    placeholder="e.g. Gurpreet Singh", key="rg_name")
    with c2: rphone = st.text_input("📱 Phone Number *", placeholder="98765 12345",          key="rg_phone")

    # Email
    remail = st.text_input("📧 Email Address *", placeholder="yourname@gmail.com", key="rg_email")

    # Passwords
    c3, c4 = st.columns(2)
    with c3: rpw  = st.text_input("🔒 Password *",        type="password", placeholder="Min 6 chars", key="rg_pw")
    with c4: rcpw = st.text_input("🔒 Confirm Password *", type="password", placeholder="Repeat",      key="rg_cpw")

    # Role
    rrole_opts = {
        "👤 General User":               "user",
        "🎓 Student (PAU/GNDU/DAV/LPU)": "student",
        "🏪 Newspaper Vendor":            "vendor",
        "👑 Admin / Owner":               "admin",
    }
    rrole_lbl = st.selectbox("I am a *", list(rrole_opts.keys()), key="rg_role")
    rrole     = rrole_opts[rrole_lbl]

    if "Student" in rrole_lbl:
        st.text_input("🏫 College Name", placeholder="e.g. Punjab Agricultural University", key="rg_college")

    rarea = st.text_input("📍 Area in Ludhiana", placeholder="e.g. BRS Nagar, Model Town, PAU Campus", key="rg_area")

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if st.button("🚀  Create My Account", use_container_width=True, key="btn_register"):
        _do_register(rname.strip(), rphone.strip(), remail.strip(), rpw, rcpw, rrole)

    if st.button("← Back to Login", use_container_width=True, key="btn_back_login"):
        st.session_state.page = "login"
        st.rerun()


def _do_register(name, phone, email, pw, cpw, role):
    # ── Validation ──
    errors = []
    if not name:   errors.append("Full name is required.")
    if not phone:  errors.append("Phone number is required.")
    elif not valid_phone(phone): errors.append("Enter a valid 10-digit Indian phone number.")
    if not email:  errors.append("Email address is required.")
    elif not valid_email(email): errors.append("Enter a valid email address.")
    if not pw:     errors.append("Password is required.")
    elif len(pw) < 6: errors.append("Password must be at least 6 characters.")
    elif pw != cpw:   errors.append("Passwords do not match.")
    if email and email in st.session_state.users_db:
        errors.append("This email is already registered. Please login.")

    if errors:
        for e in errors:
            st.error(f"❌ {e}")
        return

    # ── Save user ──
    st.session_state.users_db[email] = {
        "pw": h(pw), "role": role, "name": name, "phone": phone
    }
    st.success(f"🎉 Account created! Welcome, {name}!")
    # Auto-login
    login_user(email)


# ══════════════════════════════════════════════════════════════
#  PHONE OTP FORM
# ══════════════════════════════════════════════════════════════
def _phone_form():
    st.markdown("""
    <div style="text-align:center;margin-bottom:1.4rem;">
        <span style="font-size:2.4rem;">📱</span><br>
        <span style="font-size:1.4rem;font-weight:800;color:#FF6B2B;">Login with Phone OTP</span><br>
        <span style="color:#888;font-size:.82rem;">Enter your number and verify with OTP</span>
    </div>
    """, unsafe_allow_html=True)

    role_map2 = {"👑 Admin":"admin","🎓 Student":"student","🏪 Vendor":"vendor","👤 User":"user"}
    rl2 = st.selectbox("I am a", list(role_map2.keys()), key="ph_role")
    rs2 = role_map2[rl2]

    phone2 = st.text_input("📱 Phone Number", placeholder="98765 01001", key="ph_num")
    otp    = st.text_input("🔢 OTP (demo: 123456)", type="password", key="ph_otp")

    if st.button("✅  Verify & Login", use_container_width=True, key="btn_verify"):
        if not phone2:
            st.error("❌ Enter your phone number.")
        elif otp != "123456":
            st.error("❌ Wrong OTP. Use 123456 for demo.")
        else:
            # Find matching user by phone or fallback to demo
            matched = None
            for em, info in st.session_state.users_db.items():
                if info.get("phone","").replace(" ","").replace("-","") == phone2.replace(" ","").replace("-",""):
                    matched = em; break
            if not matched:
                matched = DEMO_CREDS[rs2][0]
            login_user(matched)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    if st.button("← Back to Login", use_container_width=True, key="btn_back2"):
        st.session_state.page = "login"
        st.rerun()

# ================================================================
# ── SIDEBAR ──
# ================================================================

import streamlit as st


ROLE_COLORS = {
    "admin":   ("#1e293b", "#94a3b8"),
    "vendor":  ("#7C3AED", "#c4b5fd"),
    "student": ("#059669", "#6ee7b7"),
    "user":    ("#FF6B2B", "#fdba74"),
}
ROLE_ICONS = {"admin":"👑","vendor":"🏪","student":"🎓","user":"👤"}


def render_sidebar(pages: list[str]) -> str:
    role = st.session_state.role
    name = st.session_state.name
    bg, fg = ROLE_COLORS.get(role, ("#FF6B2B","#fdba74"))
    icon = ROLE_ICONS.get(role,"👤")

    with st.sidebar:
        # Logo
        st.markdown(f"""
        <div style="text-align:center;padding:.5rem 0 .8rem;">
            <div style="font-size:2rem;">📰</div>
            <div style="font-size:1rem;font-weight:800;color:#FF6B2B;">Paper Scout Pro</div>
            <div style="font-size:.7rem;color:#aaa;">Ludhiana</div>
        </div>
        <div style="background:{bg}18;border:1.5px solid {bg}44;border-radius:10px;
             padding:8px 12px;margin:.4rem 0 1rem;text-align:center;">
            <div style="font-size:.85rem;font-weight:700;color:{bg};">{icon} {name}</div>
            <div style="font-size:.68rem;color:#888;text-transform:uppercase;letter-spacing:.5px;">{role}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        page = st.radio("Navigation", pages, label_visibility="collapsed")
        st.markdown("---")

        if st.button("🚪  Logout", use_container_width=True):
            logout()

    return page

# ================================================================
# ── DASHBOARD_STUDENT ──
# ================================================================

import streamlit as st
import pandas as pd
from datetime import date, timedelta



PAGES = ["🏠 Dashboard","📍 Find Vendor","📦 Subscribe","🧾 My Orders","✨ Recommendations"]


def show_student():
    page = render_sidebar(PAGES)
    AP = active_papers()
    AV = active_vendors()

    # ── DASHBOARD ───────────────────────────────────────────
    if "Dashboard" in page:
        name = st.session_state.name
        subs = st.session_state.my_subs
        st.markdown(f"""
        <div class="hero hero-student">
            <h2>🎓 Hello, {name}!</h2>
            <p>Student account active — ₹30/month discount on all subscriptions</p>
        </div>
        <div class="stat-row">
            <div class="stat-card sc"><div class="stat-num sc">{len(subs)}</div><div class="stat-lbl">📦 My Subscriptions</div></div>
            <div class="stat-card sc"><div class="stat-num sc">{len(AV)}</div><div class="stat-lbl">🏪 Vendors Nearby</div></div>
            <div class="stat-card sc"><div class="stat-num sc">₹30</div><div class="stat-lbl">🎓 Monthly Saving</div></div>
            <div class="stat-card sc"><div class="stat-num sc">{len(AP)}</div><div class="stat-lbl">📰 Papers</div></div>
        </div>
        <div class="alert-g">✅ <b>Student Discount Active!</b> You save ₹30 every month on any delivery subscription.</div>
        """, unsafe_allow_html=True)

        if subs:
            st.markdown("### 📦 Your Active Subscriptions")
            for i, sub in enumerate(subs):
                p = AP.get(sub["paper"], {})
                c1, c2 = st.columns([5,1])
                with c1:
                    st.markdown(f"""
                    <div class="card gc">
                        <div class="card-title">📰 {p.get('name', sub['paper'])} — {sub['plan']} Plan</div>
                        <div class="card-sub">💰 ₹{sub['amount']} | 🕐 {sub['time']} | 📍 {sub['address']}<br>
                        📅 Started {sub['date']} | 💳 {sub['upi']}</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    if st.button("❌", key=f"sdel_{i}", help="Cancel subscription"):
                        st.session_state.my_subs.pop(i); st.rerun()
        else:
            st.markdown('<div class="alert-o">📦 No subscriptions yet. Go to <b>Subscribe</b> tab to start!</div>', unsafe_allow_html=True)

    # ── FIND VENDOR ─────────────────────────────────────────
    elif "Find Vendor" in page:
        st.markdown('<div class="hero hero-student"><h2>📍 Vendors Near You</h2><p>Find newspaper stalls near your campus</p></div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: lf = st.selectbox("Language",["All","EN","HI","PU"])
        with c2: pf = st.selectbox("Paper",["All"]+list(AP.keys()))
        with c3: df = st.selectbox("Service",["All","Delivery","Pickup Only"])
        filtered = [v for v in AV if
            (lf=="All" or lf in v.get("langs",[]))
            and (pf=="All" or pf in v.get("papers",[]))
            and (df!="Delivery" or v.get("delivery"))
            and (df!="Pickup Only" or not v.get("delivery"))]
        st.markdown(f"**{len(filtered)} vendors found**")
        for v in filtered:
            lb = "".join([f'<span class="badge b-or">{l}</span>' for l in v.get("langs",[])])
            db = '<span class="badge b-gr">🚚 Delivery</span>' if v.get("delivery") else '<span class="badge b-bl">Pickup Only</span>'
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div class="card-title">🏪 {v['name']}</div>
                    <div class="card-sub">📍 {v['area']} | 🚶 {v['dist']} | 🕐 {v['open']}<br>
                    📞 {v['phone']}<br>{lb} {db}</div>
                </div>
                <div style="text-align:right;color:#f59e0b;font-weight:700;">⭐ {v['rating']}<br>
                <span style="color:#aaa;font-size:.72rem;">({v['reviews']})</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── SUBSCRIBE ───────────────────────────────────────────
    elif "Subscribe" in page:
        st.markdown('<div class="hero hero-student"><h2>📦 Subscribe to Delivery</h2><p>Student price — ₹30/month discount applied!</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="alert-g">🎓 <b>Student Discount: ₹30/month OFF</b> automatically applied to monthly & yearly plans!</div>', unsafe_allow_html=True)

        c1, c2 = st.columns([3,2])
        with c1:
            lang_f = st.selectbox("Language", ["All","English 🇬🇧","Hindi 🇮🇳","Punjabi 🏵️"])
            lc = {"All":"ALL","English 🇬🇧":"EN","Hindi 🇮🇳":"HI","Punjabi 🏵️":"PU"}.get(lang_f,"ALL")
            opts = {c:i for c,i in AP.items() if lc=="ALL" or i["lang"]==lc}
            if not opts: opts = AP

            paper_sel = st.selectbox("📰 Choose Newspaper", list(opts.keys()),
                format_func=lambda x: f"{opts[x]['flag']} {opts[x]['name']} — ₹{opts[x]['price']}/day")
            pi = opts[paper_sel]

            # Pricing — student gets ₹30 off monthly/yearly
            dp  = pi["price"]
            mp  = max(pi["monthly"] - 30, 50)   # student monthly
            yp  = max(pi["yearly"]  - 360, 500)  # student yearly

            st.markdown("#### 📅 Choose Your Plan")
            pc = st.columns(3)
            with pc[0]:
                st.markdown(f"""<div class="sub-card">
                <div class="sub-badge">Daily</div>
                <div class="sub-price">₹{dp}</div><div class="sub-per">per copy/day</div>
                <hr style="border-color:#eee;margin:.5rem 0;">
                <div style="font-size:.75rem;color:#666;">No commitment<br>Pickup only<br>Pay daily</div></div>""", unsafe_allow_html=True)
            with pc[1]:
                st.markdown(f"""<div class="sub-card hot">
                <div class="sub-badge">🔥 Most Popular</div>
                <div class="sub-price">₹{mp}</div><div class="sub-per">/month (₹30 OFF!)</div>
                <hr style="border-color:#eee;margin:.5rem 0;">
                <div style="font-size:.75rem;color:#666;">Home delivery<br>Choose your time<br>Cancel anytime</div></div>""", unsafe_allow_html=True)
            with pc[2]:
                st.markdown(f"""<div class="sub-card">
                <div class="sub-badge">Best Value</div>
                <div class="sub-price">₹{yp}</div><div class="sub-per">/year (₹360 OFF!)</div>
                <hr style="border-color:#eee;margin:.5rem 0;">
                <div style="font-size:.75rem;color:#666;">Home delivery<br>Priority support<br>Free on holidays</div></div>""", unsafe_allow_html=True)

            sel_plan = st.radio("Select Plan",
                [f"📅 Daily — ₹{dp}/copy", f"🚚 Monthly — ₹{mp}/month", f"🏆 Yearly — ₹{yp}/year"],
                horizontal=True)
            amount    = dp if "Daily" in sel_plan else (mp if "Monthly" in sel_plan else yp)
            plan_name = "Daily" if "Daily" in sel_plan else ("Monthly" if "Monthly" in sel_plan else "Yearly")

            t_slot = "Pickup"
            address = "Pickup"
            if "Daily" not in sel_plan:
                t_slot  = st.select_slider("🕐 Delivery Time", ["5:00 AM","5:30 AM","6:00 AM","6:30 AM","7:00 AM","7:30 AM"])
                address = st.text_input("📍 Delivery Address *", placeholder="Hostel / House No, Locality, Ludhiana")

        with c2:
            upi = st.radio("💳 Payment Method", ["📱 Google Pay","💜 PhonePe","💙 Paytm","🏛️ BHIM UPI"], label_visibility="collapsed")
            upi_name = upi.split(" ",1)[1]
            disc_row = '<div class="order-row"><span style="color:#059669;">🎓 Student Discount</span><span style="color:#059669;font-weight:700;">Applied ✅</span></div>' if "Daily" not in sel_plan else ""
            st.markdown(f"""
            <div class="order-box">
                <div class="order-row"><span style="color:#666;">📰 Paper</span><span style="font-weight:700;">{pi['name']}</span></div>
                <div class="order-row"><span style="color:#666;">📅 Plan</span><span style="font-weight:700;">{plan_name}</span></div>
                <div class="order-row"><span style="color:#666;">🕐 Time</span><span style="font-weight:700;">{t_slot}</span></div>
                {disc_row}
                <hr style="border-color:#FF6B2B44;margin:8px 0;">
                <div class="order-total">₹{amount}</div>
                <div style="text-align:center;color:#888;font-size:.75rem;">Total for {plan_name} plan</div>
            </div>""", unsafe_allow_html=True)

            if "Daily" not in sel_plan and not address:
                st.warning("⚠️ Please enter delivery address")
            elif st.button(f"✅  Subscribe & Pay ₹{amount}", use_container_width=True, key="s_pay"):
                sub = {"paper":paper_sel,"plan":plan_name,"amount":amount,"time":t_slot,
                       "address":address,"upi":upi_name,"date":date.today().strftime("%d %b %Y")}
                st.session_state.my_subs.append(sub)
                st.markdown(f"""<div class="success-box">
                <div style="font-size:2.5rem;">🎉</div>
                <div style="font-size:1.1rem;font-weight:800;">Subscribed Successfully!</div>
                <div>{pi['name']} — {plan_name} Plan</div>
                <div style="opacity:.9;margin-top:.4rem;">₹{amount} via {upi_name}</div>
                </div>""", unsafe_allow_html=True)
                st.balloons()

    # ── MY ORDERS ───────────────────────────────────────────
    elif "Orders" in page:
        st.markdown('<div class="hero hero-student"><h2>🧾 My Orders</h2><p>All your active subscriptions</p></div>', unsafe_allow_html=True)
        subs = st.session_state.my_subs
        if not subs:
            st.info("📦 No orders yet. Go to Subscribe tab to get started!")
        else:
            st.markdown(f"**{len(subs)} active subscription(s)**")
            for i, sub in enumerate(subs):
                p = AP.get(sub["paper"], {})
                c1, c2 = st.columns([5,1])
                with c1:
                    st.markdown(f"""
                    <div class="card gc">
                        <div class="card-title">📰 {p.get('name',sub['paper'])} — {sub['plan']}</div>
                        <div class="card-sub">💰 ₹{sub['amount']} | 🕐 {sub['time']} | 📍 {sub['address']}<br>
                        📅 {sub['date']} | 💳 {sub['upi']}</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    if st.button("❌ Cancel", key=f"ocan_{i}"):
                        st.session_state.my_subs.pop(i); st.rerun()

    # ── RECOMMENDATIONS ─────────────────────────────────────
    elif "Recommendations" in page:
        st.markdown('<div class="hero hero-student"><h2>✨ Recommended For You</h2><p>AI picks based on your reading style</p></div>', unsafe_allow_html=True)
        cur = st.selectbox("I currently read", list(AP.keys()), format_func=lambda x:f"{AP[x]['flag']} {AP[x]['name']}")
        if st.button("✨  Get AI Recommendations"):
            RECS = {
                "TOI":    [("HINDU",91,"Great English journalism quality"),("HT",87,"Different editorial perspective"),("ET",72,"Best for business students")],
                "BHASKAR":[("JAGRAN",89,"Very similar readership"),("KESARI",78,"Top Hindi paper in Punjab")],
                "AJIT":   [("PTRIB",93,"Perfect Punjabi pairing"),("DESH",80,"Strong local Punjab focus")],
            }
            recs = RECS.get(cur,[("HT",85,"Great alternative"),("BHASKAR",75,"Top regional paper")])
            for code,sc,reason in recs:
                if code in AP:
                    inf = AP[code]
                    st.markdown(f"""
                    <div class="card vc">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div class="card-title">{inf['flag']} {inf['name']}</div>
                            <div class="card-sub">💡 {reason}<br>₹{inf['price']}/day | ₹{max(inf['monthly']-30,50)}/month (student)</div>
                        </div>
                        <div style="background:#f5f3ff;border-radius:10px;padding:.5rem .8rem;text-align:center;">
                            <div style="font-size:1.1rem;font-weight:800;color:#7C3AED;">{sc}%</div>
                            <div style="font-size:.68rem;color:#888;">match</div>
                        </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

# ================================================================
# ── DASHBOARD_USER ──
# ================================================================

import streamlit as st
from datetime import date


PAGES = ["🏠 Dashboard","📍 Find Vendor","📦 Subscribe","🧾 My Orders","✨ Recommendations"]


def show_user():
    page = render_sidebar(PAGES)
    AP = active_papers()
    AV = active_vendors()

    if "Dashboard" in page:
        name = st.session_state.name
        subs = st.session_state.my_subs
        st.markdown(f"""
        <div class="hero">
            <h2>👤 Welcome, {name}!</h2>
            <p>Find vendors nearby or subscribe to home delivery from ₹4/day</p>
        </div>
        <div class="stat-row">
            <div class="stat-card"><div class="stat-num">{len(subs)}</div><div class="stat-lbl">📦 Subscriptions</div></div>
            <div class="stat-card"><div class="stat-num">{len(AV)}</div><div class="stat-lbl">🏪 Vendors</div></div>
            <div class="stat-card"><div class="stat-num">{len(AP)}</div><div class="stat-lbl">📰 Papers</div></div>
            <div class="stat-card"><div class="stat-num">₹150</div><div class="stat-lbl">🚚 Delivery/mo</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("### 📍 Nearest Vendors")
        for v in AV[:3]:
            lb = "".join([f'<span class="badge b-or">{l}</span>' for l in v.get("langs",[])])
            db = '<span class="badge b-gr">🚚 Delivery</span>' if v.get("delivery") else ""
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;">
                <div>
                    <div class="card-title">🏪 {v['name']}</div>
                    <div class="card-sub">📍 {v['area']} | 🚶 {v['dist']} | 🕐 {v['open']}<br>
                    📞 {v['phone']}<br>{lb} {db}</div>
                </div>
                <div style="color:#f59e0b;font-weight:700;">⭐ {v['rating']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        if subs:
            st.markdown("### 📦 Active Subscriptions")
            for sub in subs:
                p = AP.get(sub["paper"],{})
                st.markdown(f"""
                <div class="card gc">
                    <div class="card-title">📰 {p.get('name',sub['paper'])} — {sub['plan']}</div>
                    <div class="card-sub">💰 ₹{sub['amount']} | 🕐 {sub['time']} | 📅 {sub['date']}</div>
                </div>""", unsafe_allow_html=True)

    elif "Find Vendor" in page:
        st.markdown('<div class="hero"><h2>📍 Find Vendors</h2><p>All newspaper stalls in Ludhiana</p></div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1: lf = st.selectbox("Language",["All","EN","HI","PU"])
        with c2: pf = st.selectbox("Paper",["All"]+list(AP.keys()))
        filtered = [v for v in AV if (lf=="All" or lf in v.get("langs",[])) and (pf=="All" or pf in v.get("papers",[]))]
        st.markdown(f"**{len(filtered)} vendors found**")
        for v in filtered:
            lb = "".join([f'<span class="badge b-or">{l}</span>' for l in v.get("langs",[])])
            db = '<span class="badge b-gr">🚚 Delivery</span>' if v.get("delivery") else '<span class="badge b-bl">Pickup Only</span>'
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div class="card-title">🏪 {v['name']}</div>
                    <div class="card-sub">📍 {v['area']} | 🚶 {v['dist']} | 🕐 {v['open']}<br>
                    📞 {v['phone']}<br>{lb} {db}</div>
                </div>
                <div style="text-align:right;color:#f59e0b;font-weight:700;">⭐ {v['rating']}<br>
                <span style="color:#aaa;font-size:.72rem;">({v['reviews']})</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

    elif "Subscribe" in page:
        st.markdown('<div class="hero"><h2>📦 Subscribe to Delivery</h2><p>Get your newspaper every morning at your door</p></div>', unsafe_allow_html=True)
        c1,c2 = st.columns([3,2])
        with c1:
            lang_f = st.selectbox("Language", ["All","English 🇬🇧","Hindi 🇮🇳","Punjabi 🏵️"])
            lc = {"All":"ALL","English 🇬🇧":"EN","Hindi 🇮🇳":"HI","Punjabi 🏵️":"PU"}.get(lang_f,"ALL")
            opts = {c:i for c,i in AP.items() if lc=="ALL" or i["lang"]==lc}
            if not opts: opts = AP

            paper_sel = st.selectbox("📰 Newspaper", list(opts.keys()),
                format_func=lambda x: f"{opts[x]['flag']} {opts[x]['name']} — ₹{opts[x]['price']}/day")
            pi = opts[paper_sel]

            dp = pi["price"]
            mp = pi["monthly"] + 30   # delivery fee included
            yp = pi["yearly"]  + 300

            st.markdown("#### 📅 Choose Plan")
            pc = st.columns(3)
            with pc[0]:
                st.markdown(f"""<div class="sub-card">
                <div class="sub-badge">Daily</div>
                <div class="sub-price">₹{dp}</div><div class="sub-per">per copy</div>
                <hr style="border-color:#eee;margin:.5rem 0;">
                <div style="font-size:.75rem;color:#666;">No commitment<br>Pickup only</div></div>""", unsafe_allow_html=True)
            with pc[1]:
                st.markdown(f"""<div class="sub-card hot">
                <div class="sub-badge">🔥 Popular</div>
                <div class="sub-price">₹{mp}</div><div class="sub-per">/month + delivery</div>
                <hr style="border-color:#eee;margin:.5rem 0;">
                <div style="font-size:.75rem;color:#666;">Home delivery<br>Cancel anytime</div></div>""", unsafe_allow_html=True)
            with pc[2]:
                st.markdown(f"""<div class="sub-card">
                <div class="sub-badge">Best Value</div>
                <div class="sub-price">₹{yp}</div><div class="sub-per">/year</div>
                <hr style="border-color:#eee;margin:.5rem 0;">
                <div style="font-size:.75rem;color:#666;">Home delivery<br>2 months free</div></div>""", unsafe_allow_html=True)

            sel_plan = st.radio("Plan", [f"📅 Daily — ₹{dp}",f"🚚 Monthly — ₹{mp}",f"🏆 Yearly — ₹{yp}"], horizontal=True)
            amount    = dp if "Daily" in sel_plan else (mp if "Monthly" in sel_plan else yp)
            plan_name = "Daily" if "Daily" in sel_plan else ("Monthly" if "Monthly" in sel_plan else "Yearly")

            t_slot = "Pickup"; address = "Pickup"
            if "Daily" not in sel_plan:
                t_slot  = st.select_slider("🕐 Time",["5:00 AM","5:30 AM","6:00 AM","6:30 AM","7:00 AM","7:30 AM"])
                address = st.text_input("📍 Delivery Address *", placeholder="House No, Street, Area, Ludhiana")

        with c2:
            upi = st.radio("💳 Pay via",["📱 Google Pay","💜 PhonePe","💙 Paytm","🏛️ BHIM UPI"], label_visibility="collapsed")
            upi_name = upi.split(" ",1)[1]
            st.markdown(f"""
            <div class="order-box">
                <div class="order-row"><span style="color:#666;">📰</span><span style="font-weight:700;">{pi['name']}</span></div>
                <div class="order-row"><span style="color:#666;">📅 Plan</span><span style="font-weight:700;">{plan_name}</span></div>
                <div class="order-row"><span style="color:#666;">🕐 Time</span><span style="font-weight:700;">{t_slot}</span></div>
                <hr style="border-color:#FF6B2B44;margin:8px 0;">
                <div class="order-total">₹{amount}</div>
                <div style="text-align:center;color:#888;font-size:.75rem;">Total for {plan_name}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"✅  Pay ₹{amount}", use_container_width=True, key="u_pay"):
                if "Daily" not in sel_plan and not address:
                    st.warning("⚠️ Please enter your delivery address.")
                else:
                    st.session_state.my_subs.append({"paper":paper_sel,"plan":plan_name,"amount":amount,
                        "time":t_slot,"address":address,"upi":upi_name,"date":date.today().strftime("%d %b %Y")})
                    st.markdown(f"""<div class="success-box">
                    <div style="font-size:2.5rem;">🎉</div>
                    <div style="font-size:1.1rem;font-weight:800;">Subscribed!</div>
                    <div>{pi['name']} — {plan_name}</div>
                    <div style="opacity:.9;">₹{amount} via {upi_name}</div></div>""", unsafe_allow_html=True)
                    st.balloons()

    elif "Orders" in page:
        st.markdown('<div class="hero"><h2>🧾 My Orders</h2><p>Your subscription history</p></div>', unsafe_allow_html=True)
        subs = st.session_state.my_subs
        if not subs:
            st.info("📦 No orders yet. Subscribe to get started!")
        else:
            for i, sub in enumerate(subs):
                p = AP.get(sub["paper"],{})
                c1,c2 = st.columns([5,1])
                with c1:
                    st.markdown(f"""
                    <div class="card gc">
                        <div class="card-title">📰 {p.get('name',sub['paper'])} — {sub['plan']}</div>
                        <div class="card-sub">💰 ₹{sub['amount']} | 🕐 {sub['time']} | 📍 {sub['address']}<br>
                        📅 {sub['date']} | 💳 {sub['upi']}</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    if st.button("❌", key=f"ucan_{i}"):
                        st.session_state.my_subs.pop(i); st.rerun()

    elif "Recommendations" in page:
        st.markdown('<div class="hero"><h2>✨ Papers For You</h2><p>AI recommendations</p></div>', unsafe_allow_html=True)
        cur = st.selectbox("I read", list(AP.keys()), format_func=lambda x:f"{AP[x]['flag']} {AP[x]['name']}")
        if st.button("✨  Recommend"):
            RECS={"TOI":[("HINDU",91,"Similar quality"),("HT",87,"Different angle")],"BHASKAR":[("JAGRAN",89,"Similar readers"),("KESARI",78,"Top Hindi Punjab")],"AJIT":[("PTRIB",93,"Perfect pair"),("DESH",80,"Local Punjab")]}
            for code,sc,reason in RECS.get(cur,[("HT",85,"Good alternative")]):
                if code in AP:
                    inf=AP[code]
                    st.markdown(f"""<div class="card vc"><div style="display:flex;justify-content:space-between;align-items:center;">
                    <div><div class="card-title">{inf['flag']} {inf['name']}</div>
                    <div class="card-sub">💡 {reason} | ₹{inf['monthly']}/month</div></div>
                    <div style="background:#f5f3ff;border-radius:10px;padding:.5rem .8rem;text-align:center;">
                    <div style="font-size:1.1rem;font-weight:800;color:#7C3AED;">{sc}%</div>
                    <div style="font-size:.68rem;color:#888;">match</div></div>
                    </div></div>""", unsafe_allow_html=True)

# ================================================================
# ── DASHBOARD_VENDOR ──
# ================================================================

import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta, datetime


PAGES = ["📊 My Dashboard","🧠 AI Predictions","📈 Sales History","📁 Upload Sales","⚙️ Stall Settings"]
BASE  = {"TOI":55,"HT":35,"BHASKAR":65,"JAGRAN":50,"AJIT":45,"PTRIB":30,"TRIB":40,"ET":25}


def show_vendor():
    page = render_sidebar(PAGES)
    AP   = active_papers()
    AV   = active_vendors()

    # Use first vendor as demo; in real app, link by user email
    my_stall = next((v for v in AV if "Sharma" in v["name"]), AV[0] if AV else None)
    if not my_stall:
        st.error("No vendor stall found."); return

    wb = 1.3 if datetime.now().weekday() in [5,6] else 1.0   # weekend boost

    # ── DASHBOARD ───────────────────────────────────────────
    if "Dashboard" in page:
        st.markdown(f"""
        <div class="hero hero-vendor">
            <h2>🏪 {my_stall['name']}</h2>
            <p>📍 {my_stall['area']} &nbsp;|&nbsp; ⭐ {my_stall['rating']} &nbsp;|&nbsp; 🕐 {my_stall['open']}</p>
        </div>
        <div class="stat-row">
            <div class="stat-card vc"><div class="stat-num vc">{len(my_stall['papers'])}</div><div class="stat-lbl">📰 Papers</div></div>
            <div class="stat-card vc"><div class="stat-num vc">⭐{my_stall['rating']}</div><div class="stat-lbl">Rating</div></div>
            <div class="stat-card vc"><div class="stat-num vc">{my_stall['reviews']}</div><div class="stat-lbl">Reviews</div></div>
            <div class="stat-card vc"><div class="stat-num vc">{'✅' if my_stall['delivery'] else '❌'}</div><div class="stat-lbl">🚚 Delivery</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("### 🧠 Tomorrow's AI Stock Preview")
        st.markdown('<div class="alert-b">🧠 <b>Facebook Prophet ML</b> — 95% accuracy using weather, weekday & exam calendar</div>', unsafe_allow_html=True)
        for pc in my_stall["papers"][:5]:
            b    = BASE.get(pc, 30)
            pred = int(b * wb * random.uniform(0.92, 1.08))
            inf  = AP.get(pc, {})
            st.markdown(f"""
            <div class="pred-row">
                <div>
                    <div style="font-weight:700;">{pc} — {inf.get('name', pc)}</div>
                    <div style="color:#888;font-size:.78rem;">Range: {int(pred*.85)}–{int(pred*1.15)} copies</div>
                </div>
                <div class="pred-num">{pred}</div>
            </div>""", unsafe_allow_html=True)
        total = sum(int(BASE.get(p,30)*wb) for p in my_stall["papers"])
        st.success(f"📦 **Order ~{total} total copies** | Est. Revenue ₹{total*4}")

    # ── AI PREDICTIONS ──────────────────────────────────────
    elif "AI Predictions" in page:
        st.markdown('<div class="hero hero-vendor"><h2>🧠 Full AI Predictions</h2><p>7-day forecast using Facebook Prophet</p></div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        c1.metric("📅 Tomorrow",  (date.today()+timedelta(1)).strftime("%a, %d %b"))
        c2.metric("🌤️ Weather",  "Sunny ☀️")
        c3.metric("📊 Accuracy", "95.2%")
        st.markdown("### 📦 Order Quantities for Tomorrow")
        total = 0
        for pc in my_stall["papers"]:
            b=BASE.get(pc,30); pred=int(b*wb*random.uniform(.92,1.08))
            lo,hi=int(pred*.85),int(pred*1.15); inf=AP.get(pc,{}); total+=pred
            st.markdown(f"""
            <div class="pred-row">
                <div>
                    <div style="font-weight:700;">{pc} — {inf.get('name',pc)}</div>
                    <div style="color:#888;font-size:.78rem;">{inf.get('flag','')} {inf.get('lang','')} | Safe range: {lo}–{hi}</div>
                </div>
                <div class="pred-num">{pred}</div>
            </div>""", unsafe_allow_html=True)
        st.success(f"📦 Total: **{total} copies** | Revenue ≈ ₹{total*4}")

    # ── SALES HISTORY ───────────────────────────────────────
    elif "Sales History" in page:
        st.markdown('<div class="hero hero-vendor"><h2>📈 Sales History</h2><p>Last 30 days performance</p></div>', unsafe_allow_html=True)
        hist = []
        for d in range(30,0,-1):
            dt = date.today()-timedelta(d)
            for p in my_stall["papers"][:4]:
                b = BASE.get(p,30)
                u = int(b*random.uniform(.85,1.15)*(1.3 if dt.weekday() in [5,6] else 1.0))
                hist.append({"Date":dt,"Paper":p,"Units":u,"Revenue":u*4})
        df = pd.DataFrame(hist)
        ps = st.selectbox("Select Paper", my_stall["papers"][:4])
        cd = df[df["Paper"]==ps].set_index("Date")
        st.line_chart(cd["Units"])
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Avg/Day",    f"{int(cd['Units'].mean())}")
        c2.metric("Best Day",   f"{int(cd['Units'].max())}")
        c3.metric("Month Total",f"{int(cd['Units'].sum())}")
        c4.metric("Revenue",    f"₹{int(cd['Revenue'].sum())}")

    # ── UPLOAD ──────────────────────────────────────────────
    elif "Upload" in page:
        st.markdown('<div class="hero hero-vendor"><h2>📁 Upload Sales Data</h2><p>Train AI on your actual sales</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="alert-b">📋 CSV columns: <code>date, paper_code, units_sold, weather, is_holiday, is_weekend</code></div>', unsafe_allow_html=True)
        st.code("2024-01-15,TOI,65,sunny,false,false\n2024-01-16,HT,38,cloudy,false,false")
        up = st.file_uploader("Upload CSV", type=["csv"])
        if up:
            df_up = pd.read_csv(up)
            st.success(f"✅ {len(df_up)} rows uploaded!")
            st.dataframe(df_up.head(10), use_container_width=True)
            if st.button("🧠  Train AI Model"):
                import time
                with st.spinner("Training Prophet model..."):
                    time.sleep(2)
                st.success("✅ Model trained! Predictions updated."); st.balloons()

    # ── STALL SETTINGS ──────────────────────────────────────
    elif "Settings" in page:
        st.markdown('<div class="hero hero-vendor"><h2>⚙️ Stall Settings</h2><p>Update your stall information</p></div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            st.text_input("Stall Name",   value=my_stall["name"])
            st.text_input("Area",         value=my_stall["area"])
            st.text_input("Phone",        value=my_stall["phone"])
        with c2:
            st.text_input("Opening Time", value=my_stall["open"].split("–")[0])
            st.text_input("Closing Time", value=my_stall["open"].split("–")[-1])
            st.checkbox("Offer Delivery", value=my_stall["delivery"])
        st.multiselect("Languages", ["EN","HI","PU"], default=my_stall.get("langs",[]))
        st.multiselect("Papers Available", list(AP.keys()), default=my_stall["papers"])
        if st.button("💾  Save Changes"):
            st.success("✅ Stall info updated!")

# ================================================================
# ── DASHBOARD_ADMIN ──
# ================================================================

import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta


PAGES = ["📊 Overview","🏪 Vendors","📰 Newspapers","👥 Users","📈 Analytics"]


def show_admin():
    page = render_sidebar(PAGES)
    AV = st.session_state.vendors
    AP = st.session_state.papers

    # ── OVERVIEW ────────────────────────────────────────────
    if "Overview" in page:
        av = len([v for v in AV if v.get("active",True)])
        ap = len([p for p in AP.values() if p.get("active",True)])
        st.markdown(f"""
        <div class="hero hero-admin">
            <h2>👑 Admin Dashboard</h2>
            <p>Complete platform control — vendors, papers, users & analytics</p>
        </div>
        <div class="stat-row">
            <div class="stat-card ac"><div class="stat-num ac">{av}</div><div class="stat-lbl">🏪 Active Vendors</div></div>
            <div class="stat-card ac"><div class="stat-num ac">{ap}</div><div class="stat-lbl">📰 Active Papers</div></div>
            <div class="stat-card ac"><div class="stat-num ac">{len(st.session_state.users_db)}</div><div class="stat-lbl">👥 Users</div></div>
            <div class="stat-card ac"><div class="stat-num ac">₹12.4K</div><div class="stat-lbl">💰 This Month</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("### 📈 Orders — Last 7 Days")
        dates = [(date.today()-timedelta(i)).strftime("%a %d") for i in range(6,-1,-1)]
        st.bar_chart(pd.DataFrame({"Orders":[random.randint(15,50) for _ in dates]},index=dates))

        st.markdown("### 🏆 Top Vendors")
        top = sorted([v for v in AV if v.get("active",True)],key=lambda x:x["rating"],reverse=True)[:5]
        st.dataframe(pd.DataFrame([{"Vendor":v["name"],"Area":v["area"],"Rating":v["rating"],"Reviews":v["reviews"],"Delivery":"✅" if v["delivery"] else "❌"} for v in top]),use_container_width=True,hide_index=True)

    # ── VENDORS ─────────────────────────────────────────────
    elif "Vendors" in page:
        st.markdown('<div class="hero hero-admin"><h2>🏪 Manage Vendors</h2><p>Add, edit, enable or remove vendors</p></div>', unsafe_allow_html=True)

        with st.expander("➕ Add New Vendor", expanded=False):
            c1,c2 = st.columns(2)
            with c1:
                nv_n   = st.text_input("Stall Name *",              key="nv_n")
                nv_a   = st.text_input("Area / Locality *",          key="nv_a")
                nv_p   = st.text_input("Phone Number *",              key="nv_p")
                nv_d   = st.text_input("Distance",   placeholder="e.g. 1.5km", key="nv_d")
            with c2:
                nv_o   = st.text_input("Opening Time", value="6:00 AM",  key="nv_o")
                nv_c   = st.text_input("Closing Time",  value="10:00 AM", key="nv_c")
                nv_l   = st.multiselect("Languages", ["EN","HI","PU"], default=["EN","HI"], key="nv_l")
                nv_del = st.checkbox("Offers Home Delivery", key="nv_del")
            AP_active = {k:v for k,v in AP.items() if v.get("active",True)}
            nv_pp = st.multiselect("Papers Available", list(AP_active.keys()), default=["TOI","BHASKAR"], key="nv_pp")

            if st.button("✅  Add Vendor", key="btn_add_vendor"):
                if not nv_n or not nv_a or not nv_p:
                    st.error("❌ Stall Name, Area and Phone are required.")
                else:
                    new_id = max([v["id"] for v in AV], default=0)+1
                    st.session_state.vendors.append({
                        "id":new_id,"name":nv_n,"area":nv_a,"dist":nv_d or "?",
                        "langs":nv_l,"papers":nv_pp,"rating":0.0,"reviews":0,
                        "delivery":nv_del,"open":f"{nv_o}–{nv_c}","phone":nv_p,"active":True
                    })
                    st.success(f"✅ '{nv_n}' added successfully!"); st.rerun()

        st.markdown(f"### All Vendors ({len(AV)} total)")
        for i,v in enumerate(AV):
            c1,c2,c3,c4,c5 = st.columns([3,1,1,1,1])
            with c1: st.markdown(f"**{'🟢' if v.get('active',True) else '🔴'} {v['name']}** &nbsp; <small style='color:#888;'>{v['area']}</small>",unsafe_allow_html=True)
            with c2: st.write(f"⭐ {v['rating']}")
            with c3: st.write("🚚" if v["delivery"] else "—")
            with c4:
                if v.get("active",True):
                    if st.button("🔴 Off",key=f"voff_{i}"): st.session_state.vendors[i]["active"]=False; st.rerun()
                else:
                    if st.button("🟢 On", key=f"von_{i}"):  st.session_state.vendors[i]["active"]=True;  st.rerun()
            with c5:
                if st.button("🗑️",key=f"vdel_{i}"): st.session_state.vendors.pop(i); st.rerun()

    # ── NEWSPAPERS ──────────────────────────────────────────
    elif "Newspapers" in page:
        st.markdown('<div class="hero hero-admin"><h2>📰 Manage Newspapers</h2><p>Add, hide or remove papers from the platform</p></div>', unsafe_allow_html=True)

        with st.expander("➕ Add New Newspaper", expanded=False):
            c1,c2 = st.columns(2)
            with c1:
                np_c  = st.text_input("Short Code * (max 8)", placeholder="e.g. TRIB", key="np_c").upper()
                np_n  = st.text_input("Full Name *",           placeholder="e.g. The Tribune", key="np_n")
                np_l  = st.selectbox("Language *", ["EN - English","HI - Hindi","PU - Punjabi"], key="np_l")
            with c2:
                np_pr = st.number_input("Daily Price ₹",   min_value=1,  max_value=50,   value=5,    key="np_pr")
                np_mo = st.number_input("Monthly Price ₹", min_value=50, max_value=500,  value=120,  key="np_mo")
                np_yr = st.number_input("Yearly Price ₹",  min_value=500,max_value=6000, value=1200, key="np_yr")
            np_f  = {"EN - English":"🇬🇧","HI - Hindi":"🇮🇳","PU - Punjabi":"🏵️"}.get(np_l,"🇬🇧")
            np_lc = np_l.split(" - ")[0]

            if st.button("✅  Add Newspaper", key="btn_add_paper"):
                if not np_c or not np_n:
                    st.error("❌ Code and Name are required.")
                elif len(np_c) > 8:
                    st.error("❌ Code must be max 8 characters.")
                elif np_c in AP:
                    st.error(f"❌ Code '{np_c}' already exists.")
                else:
                    st.session_state.papers[np_c] = {"name":np_n,"lang":np_lc,"flag":np_f,"price":np_pr,"monthly":np_mo,"yearly":np_yr,"active":True}
                    st.success(f"✅ '{np_n}' added!"); st.rerun()

        st.markdown(f"### All Newspapers ({len(AP)} total)")
        for code,info in list(AP.items()):
            c1,c2,c3,c4,c5,c6 = st.columns([1,2.5,1,1,1,1])
            with c1: st.markdown(f"**{code}**")
            with c2: st.write(f"{info['flag']} {info['name']}")
            with c3: st.write(f"₹{info['price']}/d")
            with c4: st.write(f"₹{info['monthly']}/mo")
            with c5:
                if info.get("active",True):
                    if st.button("🔴 Hide",key=f"phide_{code}"): st.session_state.papers[code]["active"]=False; st.rerun()
                else:
                    if st.button("🟢 Show",key=f"pshow_{code}"): st.session_state.papers[code]["active"]=True;  st.rerun()
            with c6:
                if st.button("🗑️",key=f"pdel_{code}"): del st.session_state.papers[code]; st.rerun()

    # ── USERS ───────────────────────────────────────────────
    elif "Users" in page:
        st.markdown('<div class="hero hero-admin"><h2>👥 Manage Users</h2><p>All registered users and roles</p></div>', unsafe_allow_html=True)
        ud = [{"Email":e,"Name":i["name"],"Role":i["role"],"Phone":i.get("phone","—")} for e,i in st.session_state.users_db.items()]
        st.dataframe(pd.DataFrame(ud),use_container_width=True,hide_index=True)

        st.markdown("### ➕ Add New User / Staff")
        c1,c2 = st.columns(2)
        with c1:
            nu_n  = st.text_input("Full Name *",   key="nu_n")
            nu_e  = st.text_input("Email *",        key="nu_e")
            nu_ph = st.text_input("Phone",          key="nu_ph")
        with c2:
            nu_p  = st.text_input("Password *",    type="password", key="nu_p")
            nu_r  = st.selectbox("Role", ["user","student","vendor","admin"], key="nu_r")
        if st.button("✅  Add User", key="btn_add_user"):
            if not nu_n or not nu_e or not nu_p:
                st.error("❌ Name, Email and Password required.")
            elif nu_e in st.session_state.users_db:
                st.error("❌ Email already registered.")
            else:
                import hashlib
                st.session_state.users_db[nu_e] = {"pw":hashlib.md5(nu_p.encode()).hexdigest(),"role":nu_r,"name":nu_n,"phone":nu_ph}
                st.success(f"✅ {nu_n} added!"); st.rerun()

    # ── ANALYTICS ───────────────────────────────────────────
    elif "Analytics" in page:
        st.markdown('<div class="hero hero-admin"><h2>📈 Platform Analytics</h2><p>Revenue, orders and growth metrics</p></div>', unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Vendors",  len(AV),  f"{len([v for v in AV if v.get('active')])} active")
        c2.metric("Papers",   len(AP),  f"{len([p for p in AP.values() if p.get('active')])} active")
        c3.metric("Users",    len(st.session_state.users_db))
        c4.metric("Revenue",  "₹12,450", "↑ 18%")

        st.markdown("### 📈 Daily Orders — Last 14 Days")
        dates14 = [(date.today()-timedelta(i)).strftime("%d %b") for i in range(13,-1,-1)]
        chart_df = pd.DataFrame({
            "Orders":  [random.randint(10,50) for _ in dates14],
            "Revenue": [random.randint(400,2000) for _ in dates14]
        }, index=dates14)
        st.line_chart(chart_df)

        st.markdown("### 🏆 Top Vendors by Rating")
        top = sorted([v for v in AV if v.get("active",True)],key=lambda x:x["rating"],reverse=True)[:5]
        st.dataframe(pd.DataFrame([{"Vendor":v["name"],"Area":v["area"],"Rating":v["rating"],"Reviews":v["reviews"]} for v in top]),use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════════════
# STREAMLIT ENTRY POINT
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Paper Scout Pro",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

init()
apply()

if not st.session_state.logged_in:
    render_login()
else:
    role = st.session_state.role
    if   role == "admin":   show_admin()
    elif role == "vendor":  show_vendor()
    elif role == "student": show_student()
    else:                   show_user()
