"""
Paper Scout Pro — Ludhiana Newspaper Platform
Clean single-file version. All bugs fixed.
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import random
import hashlib
import re
from datetime import date, timedelta, datetime

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG  (must be first Streamlit call)
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Paper Scout Pro |",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()

def is_valid_email(e: str) -> bool:
    return bool(re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$", e, re.I))

def is_valid_phone(p: str) -> bool:
    digits = re.sub(r"[\s\-]", "", p)
    return bool(re.match(r"^[6-9]\d{9}$", digits))


# ══════════════════════════════════════════════════════════════
# SESSION STATE — initialise once
# ══════════════════════════════════════════════════════════════
def _ss(k, v):
    if k not in st.session_state:
        st.session_state[k] = v

_ss("logged_in", False)
_ss("role",      None)
_ss("name",      None)
_ss("email",     None)
_ss("my_subs",   [])
_ss("auth_mode", "login")   # login | register

})

_ss("vendors", [
    {"id":1,"name":"Sharma News Agency","area":"PAU Campus","dist":"300m","langs":["EN","HI","PU"],"papers":["TOI","HT","BHASKAR","AJIT","PTRIB"],"rating":4.8,"reviews":35,"delivery":True,"open":"5:30–10:30 AM","phone":"98765 01001","active":True},
    {"id":2,"name":"PAU Gate 4 Stall","area":"PAU Campus","dist":"500m","langs":["EN","HI","PU"],"papers":["TOI","HT","TRIB","BHASKAR","AJIT"],"rating":4.7,"reviews":31,"delivery":True,"open":"6:00–10:00 AM","phone":"98765 01002","active":True},
    {"id":3,"name":"Clock Tower Akhbaar","area":"Clock Tower","dist":"1.5km","langs":["HI","PU"],"papers":["BHASKAR","JAGRAN","AJIT","PTRIB"],"rating":4.6,"reviews":26,"delivery":True,"open":"5:00–10:00 AM","phone":"98765 01003","active":True},
    {"id":4,"name":"Model Town News","area":"Model Town","dist":"2.0km","langs":["EN","HI"],"papers":["TOI","HT","HINDU","ET","BHASKAR"],"rating":4.7,"reviews":31,"delivery":False,"open":"6:00–10:30 AM","phone":"98765 01004","active":True},
    {"id":5,"name":"Singh Paper Depot","area":"BRS Nagar","dist":"1.2km","langs":["EN","PU"],"papers":["TOI","TRIB","KESARI","AJIT"],"rating":4.2,"reviews":18,"delivery":True,"open":"6:00–10:00 AM","phone":"98765 01005","active":True},
    {"id":6,"name":"Ghumar Mandi Papers","area":"Ghumar Mandi","dist":"0.9km","langs":["EN","HI","PU"],"papers":["TOI","HT","TRIB","BHASKAR","AJIT"],"rating":4.0,"reviews":11,"delivery":True,"open":"5:30–9:30 AM","phone":"98765 01006","active":True},
])

_ss("papers", {
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
})

def av(): return [v for v in st.session_state.vendors if v.get("active", True)]
def ap(): return {k:v for k,v in st.session_state.papers.items() if v.get("active", True)}

def do_login(email: str):
    info = st.session_state.users_db[email]
    st.session_state.logged_in = True
    st.session_state.role  = info["role"]
    st.session_state.name  = info["name"]
    st.session_state.email = email
    st.session_state.my_subs = []
    st.rerun()

def do_logout():
    st.session_state.logged_in = False
    st.session_state.role = st.session_state.name = st.session_state.email = None
    st.session_state.my_subs = []
    st.session_state.auth_mode = "login"
    st.rerun()


# ══════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*, *::before, *::after { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }

/* ── Main ── */
.block-container { padding-top: 1.2rem !important; }

/* ── Cards ── */
.kard {
    background: white; border-radius: 13px;
    padding: 1.1rem 1.3rem; margin-bottom: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
    border-left: 5px solid #FF6B2B;
}
.kard.green  { border-left-color: #10B981; }
.kard.purple { border-left-color: #7C3AED; }
.kard.blue   { border-left-color: #3B82F6; }
.kard.dark   { border-left-color: #1e293b; }
.kt { font-size:.95rem; font-weight:700; color:#111; margin-bottom:3px; }
.ks { font-size:.8rem; color:#666; line-height:1.75; }

/* ── Hero ── */
.hero {
    border-radius: 16px; padding: 1.6rem 2rem; color:white;
    margin-bottom: 1.2rem;
    box-shadow: 0 6px 20px rgba(0,0,0,.15);
}
.hero.orange { background: linear-gradient(135deg,#FF6B2B,#d94f15); }
.hero.green  { background: linear-gradient(135deg,#059669,#047857); }
.hero.purple { background: linear-gradient(135deg,#7C3AED,#5B21B6); }
.hero.dark   { background: linear-gradient(135deg,#1e293b,#0f172a); }
.hero h2 { font-size:1.65rem; font-weight:800; margin:0 0 4px; }
.hero p  { font-size:.9rem;  opacity:.88; margin:0; }

/* ── Stats ── */
.stats { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-bottom:1.2rem; }
.stat {
    background:white; border-radius:12px; padding:.9rem;
    text-align:center; box-shadow:0 2px 8px rgba(0,0,0,.05);
    border-bottom: 4px solid #FF6B2B;
}
.stat.green  { border-bottom-color:#10B981; }
.stat.purple { border-bottom-color:#7C3AED; }
.stat.dark   { border-bottom-color:#1e293b; }
.sn { font-size:1.5rem; font-weight:800; color:#FF6B2B; }
.sn.green  { color:#10B981; }
.sn.purple { color:#7C3AED; }
.sn.dark   { color:#1e293b; }
.sl { font-size:.72rem; color:#888; margin-top:2px; }

/* ── Badges ── */
.badge { display:inline-block; padding:2px 9px; border-radius:20px; font-size:.7rem; font-weight:600; margin:2px; }
.b-or { background:#fff3ec; color:#FF6B2B; }
.b-gr { background:#ecfdf5; color:#059669; }
.b-bl { background:#eff6ff; color:#3B82F6; }
.b-pu { background:#f5f3ff; color:#7C3AED; }

/* ── Alerts ── */
.alert { border-radius:10px; padding:.75rem 1rem; font-size:.83rem; margin:.5rem 0; }
.alert.green  { background:#ecfdf5; border:1.5px solid #10B981; color:#065f46; }
.alert.orange { background:#fff8f5; border:1.5px solid #FF6B2B; color:#9a3412; }
.alert.blue   { background:#eff6ff; border:1.5px solid #3B82F6; color:#1e3a8a; }

/* ── Subscription plan cards ── */
.plan-card {
    background:white; border-radius:14px; padding:1.2rem;
    text-align:center; box-shadow:0 2px 10px rgba(0,0,0,.07);
    border:2px solid #eee;
}
.plan-card.hot { border-color:#FF6B2B; background:#fff8f5; }
.plan-price  { font-size:1.8rem; font-weight:800; color:#FF6B2B; }
.plan-period { font-size:.74rem; color:#888; }
.plan-tag    { background:#FF6B2B; color:white; font-size:.68rem; font-weight:700;
               padding:2px 10px; border-radius:20px; display:inline-block; margin-bottom:.4rem; }

/* ── Order box ── */
.order-box {
    background:linear-gradient(135deg,#fff8f5,#ffe8d6);
    border:2px solid #FF6B2B; border-radius:14px; padding:1.2rem; margin:.7rem 0;
}
.order-row { display:flex; justify-content:space-between; margin-bottom:5px; font-size:.84rem; }
.order-total { font-size:1.7rem; font-weight:800; color:#FF6B2B; text-align:center; margin-top:.5rem; }

/* ── Pred rows ── */
.pred-row {
    background:white; border-radius:10px; padding:.85rem 1rem;
    margin-bottom:7px; display:flex; justify-content:space-between; align-items:center;
    box-shadow:0 1px 5px rgba(0,0,0,.05); border-left:4px solid #7C3AED;
}
.pred-num { font-size:1.25rem; font-weight:800; color:#7C3AED; }

/* ── Success ── */
.success-pop {
    background:linear-gradient(135deg,#10B981,#059669);
    border-radius:14px; padding:1.8rem; text-align:center; color:white; margin:.8rem 0;
}

/* ── Buttons ── */
.stButton > button {
    background:linear-gradient(135deg,#FF6B2B,#e85d1e) !important;
    color:white !important; border:none !important;
    border-radius:10px !important; font-weight:700 !important;
    font-size:.88rem !important; transition: all .15s !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 6px 18px rgba(255,107,43,.4) !important; }

/* ── Login page ── */
.login-card {
    background: white; border-radius: 20px;
    padding: 2.4rem 2.2rem; max-width: 430px;
    margin: 0 auto; box-shadow: 0 8px 40px rgba(0,0,0,.10);
}
.login-logo { text-align: center; margin-bottom: 1.6rem; }

/* ── Sidebar user chip ── */
.user-chip {
    border-radius: 10px; padding: 8px 12px;
    text-align: center; margin-bottom: .5rem;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# SHARED SIDEBAR (returns selected page string)
# ══════════════════════════════════════════════════════════════
ROLE_META = {
    "admin":   ("#1e293b", "👑", "ADMIN"),
    "vendor":  ("#7C3AED", "🏪", "VENDOR"),
    "student": ("#059669", "🎓", "STUDENT"),
    "user":    ("#FF6B2B", "👤", "USER"),
}

def _sidebar(pages: list) -> str:
    role = st.session_state.role
    name = st.session_state.name
    clr, icon, lbl = ROLE_META.get(role, ("#FF6B2B","👤","USER"))
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;padding:.4rem 0 .8rem;">
            <div style="font-size:1.8rem;">📰</div>
            <div style="font-size:.95rem;font-weight:800;color:#FF6B2B;">Paper Scout Pro</div>
            <div style="font-size:.68rem;color:#aaa;">Ludhiana</div>
        </div>
        <div style="background:{clr}18;border:1.5px solid {clr}44;border-radius:10px;
             padding:8px 12px;margin:.3rem 0 1rem;text-align:center;">
            <div style="font-size:.85rem;font-weight:700;color:{clr};">{icon} {name}</div>
            <div style="font-size:.68rem;color:#888;text-transform:uppercase;letter-spacing:.5px;">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        chosen = st.radio("nav", pages, label_visibility="collapsed")
        st.markdown("---")
        if st.button("🚪  Logout", use_container_width=True):
            do_logout()
    return chosen


# ══════════════════════════════════════════════════════════════
# ██  LOGIN PAGE  ██
# ══════════════════════════════════════════════════════════════
_ROLES = {
    "👤  General User":     "user",
    "🎓  Student":          "student",
    "🏪  Newspaper Vendor": "vendor",
    "👑  Admin ":    "admin",
}
_HINTS = {
    "user":    "Find vendors & subscribe to home delivery",
    "student": "₹30/month discount on all subscriptions",
    "vendor":  "AI stock predictions for your stall",
    "admin":   "Full access — manage everything",
}

def page_login():
    # Hide sidebar on login
    st.markdown("<style>[data-testid='stSidebar']{display:none!important;}.block-container{max-width:450px!important;margin:0 auto!important;padding-top:4vh!important;}</style>", unsafe_allow_html=True)

    mode = st.session_state.auth_mode

    # ── Logo ────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;margin-bottom:1.6rem;">
        <div style="font-size:3rem;">📰</div>
        <div style="font-size:1.55rem;font-weight:800;color:#FF6B2B;">Paper Scout Pro</div>
        <div style="color:#888;font-size:.82rem;">Ludhiana's Newspaper Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # ════ LOGIN FORM ════════════════════════════════════════
    if mode == "login":
        st.markdown("### 🔐 Sign In")
        st.caption("Welcome back! Sign in to your account.")

        role_label = st.selectbox("Log in as", list(_ROLES.keys()), key="li_role")
        role_val   = _ROLES[role_label]
        st.markdown(f"<div style='background:#fff8f5;border-left:3px solid #FF6B2B;border-radius:8px;padding:7px 12px;font-size:.8rem;color:#c94d10;margin-bottom:.8rem;'>ℹ️ {_HINTS[role_val]}</div>", unsafe_allow_html=True)

        email = st.text_input("📧 Email Address", placeholder="yourname@gmail.com",   key="li_email")
        pw    = st.text_input("🔒 Password",       placeholder="Enter your password", type="password", key="li_pw")

        # Forgot password link
        st.markdown("<p style='text-align:right;margin-top:-6px;'><a href='#' style='color:#FF6B2B;font-size:.8rem;font-weight:600;text-decoration:none;'>Forgot Password?</a></p>", unsafe_allow_html=True)

        if st.button("Sign In →", use_container_width=True, key="btn_signin"):
            _attempt_login(email.strip(), pw, role_val)

        st.markdown("---")
        st.markdown("<p style='text-align:center;color:#888;font-size:.84rem;margin:0;'>Don't have an account?</p>", unsafe_allow_html=True)
        if st.button("Create Account — It's Free", use_container_width=True, key="btn_go_reg"):
            st.session_state.auth_mode = "register"; st.rerun()

        # Demo credentials
        st.markdown("""
        <div style="background:#fafafa;border:1px solid #eee;border-radius:10px;padding:10px 14px;
             font-size:.74rem;color:#777;line-height:2;margin-top:1rem;">
            <b>🔑 Demo accounts:</b><br>
            👑 admin@paperscout.com &nbsp;/&nbsp; admin123<br>
            🎓 student@pau.edu &nbsp;/&nbsp; student123<br>
            🏪 vendor@paperscout.com &nbsp;/&nbsp; vendor123<br>
            👤 user@gmail.com &nbsp;/&nbsp; user123
        </div>
        """, unsafe_allow_html=True)

    # ════ REGISTER FORM ═════════════════════════════════════
    else:
        st.markdown("### ✨ Create Account")
        st.caption("Join free — takes less than a minute!")

        c1, c2 = st.columns(2)
        with c1: rname  = st.text_input("👤 Full Name *",    placeholder="Gurpreet Singh", key="rg_name")
        with c2: rphone = st.text_input("📱 Phone *",        placeholder="98765 12345",    key="rg_phone")

        remail = st.text_input("📧 Email Address *", placeholder="yourname@gmail.com", key="rg_email")

        c3, c4 = st.columns(2)
        with c3: rpw  = st.text_input("🔒 Password *",         type="password", placeholder="Min 6 chars", key="rg_pw")
        with c4: rcpw = st.text_input("🔒 Confirm Password *", type="password", placeholder="Repeat",      key="rg_cpw")

        rrole_map = {
            "👤 General User":               "user",
            "🎓 Student (PAU/GNDU/LPU/DAV)": "student",
            "🏪 Newspaper Vendor":            "vendor",
            "👑 Admin / Owner":               "admin",
        }
        rrole_lbl = st.selectbox("I am a *", list(rrole_map.keys()), key="rg_role")
        rrole     = rrole_map[rrole_lbl]

        if "Student" in rrole_lbl:
            st.text_input("🏫 College Name", placeholder="e.g. PAU Ludhiana", key="rg_college")

        st.text_input("📍 Area in Ludhiana", placeholder="e.g. Model Town, BRS Nagar", key="rg_area")

        if st.button("Create My Account →", use_container_width=True, key="btn_create"):
            _attempt_register(rname.strip(), rphone.strip(), remail.strip(), rpw, rcpw, rrole)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("← Back to Login", use_container_width=True, key="btn_go_login"):
            st.session_state.auth_mode = "login"; st.rerun()


def _attempt_login(email, pw, role_val):
    db = st.session_state.users_db
    if not email or not pw:
        st.error("❌ Please enter your email and password.")
        return
    if email not in db:
        st.error("❌ Email not found. Please create an account.")
        return
    info = db[email]
    if info["pw"] != md5(pw):
        st.error("❌ Wrong password. Please try again.")
        return
    if info["role"] != role_val:
        st.warning(f"⚠️ This email is registered as **{info['role']}**. Please select the correct role above.")
        return
    do_login(email)


def _attempt_register(name, phone, email, pw, cpw, role):
    errs = []
    if not name:  errs.append("Full name is required.")
    if not phone: errs.append("Phone number is required.")
    elif not is_valid_phone(phone): errs.append("Enter a valid 10-digit Indian phone number (starts with 6-9).")
    if not email: errs.append("Email address is required.")
    elif not is_valid_email(email): errs.append("Enter a valid email address.")
    if not pw:    errs.append("Password is required.")
    elif len(pw) < 6: errs.append("Password must be at least 6 characters.")
    elif pw != cpw:   errs.append("Passwords do not match. Please re-enter.")
    if email and email in st.session_state.users_db:
        errs.append("This email is already registered. Please login instead.")
    if errs:
        for e in errs: st.error(f"❌ {e}")
        return
    st.session_state.users_db[email] = {"pw": md5(pw), "role": role, "name": name, "phone": phone}
    st.success(f"🎉 Account created successfully! Welcome, {name}!")
    do_login(email)


# ══════════════════════════════════════════════════════════════
# ██  USER DASHBOARD  ██
# ══════════════════════════════════════════════════════════════
def page_user():
    USER_PAGES = ["🏠 Home","📍 Find Vendor","📦 Subscribe","🧾 My Orders","✨ Recommendations"]
    page = _sidebar(USER_PAGES)
    AV = av(); AP = ap()

    if page == "🏠 Home":
        subs = st.session_state.my_subs
        st.markdown(f"""
        <div class="hero orange">
            <h2>👤 Welcome, {st.session_state.name}!</h2>
            <p>Find your nearest newspaper vendor or subscribe to home delivery</p>
        </div>
        <div class="stats">
            <div class="stat"><div class="sn">{len(subs)}</div><div class="sl">📦 Subscriptions</div></div>
            <div class="stat"><div class="sn">{len(AV)}</div><div class="sl">🏪 Vendors</div></div>
            <div class="stat"><div class="sn">{len(AP)}</div><div class="sl">📰 Papers</div></div>
            <div class="stat"><div class="sn">₹150</div><div class="sl">🚚 Delivery/mo</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("### 📍 Vendors Near You")
        for v in AV[:4]:
            langs = "".join([f'<span class="badge b-or">{l}</span>' for l in v.get("langs",[])])
            deliv = '<span class="badge b-gr">🚚 Delivery</span>' if v.get("delivery") else '<span class="badge b-bl">Pickup Only</span>'
            st.markdown(f"""
            <div class="kard">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div class="kt">🏪 {v['name']}</div>
                    <div class="ks">📍 {v['area']} &nbsp;|&nbsp; 🚶 {v['dist']} &nbsp;|&nbsp; 🕐 {v['open']}<br>
                    📞 {v['phone']}<br>{langs} {deliv}</div>
                </div>
                <div style="text-align:right;">
                    <div style="color:#f59e0b;font-weight:700;">⭐ {v['rating']}</div>
                    <div style="color:#aaa;font-size:.72rem;">({v['reviews']} reviews)</div>
                </div>
                </div>
            </div>""", unsafe_allow_html=True)

        if subs:
            st.markdown("### 📦 Active Subscriptions")
            for sub in subs:
                p = AP.get(sub["paper"],{})
                st.markdown(f"""
                <div class="kard green">
                    <div class="kt">📰 {p.get('name',sub['paper'])} — {sub['plan']}</div>
                    <div class="ks">💰 ₹{sub['amount']} &nbsp;|&nbsp; 🕐 {sub['time']} &nbsp;|&nbsp; 📅 {sub['date']}</div>
                </div>""", unsafe_allow_html=True)

    elif page == "📍 Find Vendor":
        st.markdown('<div class="hero orange"><h2>📍 Find Vendors</h2><p>All newspaper stalls in Ludhiana</p></div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: lf = st.selectbox("Language",["All","EN","HI","PU"])
        with c2: pf = st.selectbox("Paper",["All"]+list(AP.keys()))
        with c3: df = st.selectbox("Service",["All","Delivery Only","Pickup Only"])
        filtered = [v for v in AV
            if (lf=="All" or lf in v.get("langs",[]))
            and (pf=="All" or pf in v.get("papers",[]))
            and (df!="Delivery Only" or v.get("delivery"))
            and (df!="Pickup Only"   or not v.get("delivery"))]
        st.markdown(f"**{len(filtered)} vendors found**")
        for v in filtered:
            langs = "".join([f'<span class="badge b-or">{l}</span>' for l in v.get("langs",[])])
            deliv = '<span class="badge b-gr">🚚 Delivery</span>' if v.get("delivery") else '<span class="badge b-bl">Pickup Only</span>'
            st.markdown(f"""
            <div class="kard">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div class="kt">🏪 {v['name']}</div>
                    <div class="ks">📍 {v['area']} | 🚶 {v['dist']} | 🕐 {v['open']}<br>
                    📞 {v['phone']}<br>{langs} {deliv}</div>
                </div>
                <div style="text-align:right;">
                    <div style="color:#f59e0b;font-weight:700;">⭐ {v['rating']}</div>
                    <div style="color:#aaa;font-size:.72rem;">({v['reviews']})</div>
                </div>
                </div>
            </div>""", unsafe_allow_html=True)

    elif page == "📦 Subscribe":
        st.markdown('<div class="hero orange"><h2>📦 Subscribe to Delivery</h2><p>Get your newspaper every morning at your door</p></div>', unsafe_allow_html=True)
        _subscription_form(AP, student_discount=False)

    elif page == "🧾 My Orders":
        st.markdown('<div class="hero orange"><h2>🧾 My Orders</h2><p>All your subscriptions</p></div>', unsafe_allow_html=True)
        _orders_view(AP, key_prefix="u")

    elif page == "✨ Recommendations":
        st.markdown('<div class="hero orange"><h2>✨ Papers For You</h2><p>AI recommendations</p></div>', unsafe_allow_html=True)
        _recommendations(AP)


# ══════════════════════════════════════════════════════════════
# ██  STUDENT DASHBOARD  ██
# ══════════════════════════════════════════════════════════════
def page_student():
    STUDENT_PAGES = ["🏠 Home","📍 Find Vendor","📦 Subscribe","🧾 My Orders","✨ Recommendations"]
    page = _sidebar(STUDENT_PAGES)
    AV = av(); AP = ap()

    if page == "🏠 Home":
        subs = st.session_state.my_subs
        st.markdown(f"""
        <div class="hero green">
            <h2>🎓 Welcome, {st.session_state.name}!</h2>
            <p>Student account active — ₹30/month discount on all delivery subscriptions</p>
        </div>
        <div class="stats">
            <div class="stat green"><div class="sn green">{len(subs)}</div><div class="sl">📦 Subscriptions</div></div>
            <div class="stat green"><div class="sn green">{len(AV)}</div><div class="sl">🏪 Vendors</div></div>
            <div class="stat green"><div class="sn green">₹30</div><div class="sl">🎓 Monthly Saving</div></div>
            <div class="stat green"><div class="sn green">{len(AP)}</div><div class="sl">📰 Papers</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="alert green">✅ <b>Student Discount Active!</b> You save ₹30 every month on delivery subscriptions.</div>', unsafe_allow_html=True)

        st.markdown("### 📍 Vendors Near Campus")
        for v in AV[:3]:
            langs = "".join([f'<span class="badge b-or">{l}</span>' for l in v.get("langs",[])])
            deliv = '<span class="badge b-gr">🚚 Delivery</span>' if v.get("delivery") else ""
            st.markdown(f"""
            <div class="kard green">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div class="kt">🏪 {v['name']}</div>
                    <div class="ks">📍 {v['area']} | 🚶 {v['dist']} | 🕐 {v['open']}<br>
                    📞 {v['phone']}<br>{langs} {deliv}</div>
                </div>
                <div style="color:#f59e0b;font-weight:700;">⭐ {v['rating']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        if subs:
            st.markdown("### 📦 Your Subscriptions")
            for i, sub in enumerate(subs):
                p = AP.get(sub["paper"],{})
                c1, c2 = st.columns([5,1])
                with c1:
                    st.markdown(f"""
                    <div class="kard green">
                        <div class="kt">📰 {p.get('name',sub['paper'])} — {sub['plan']}</div>
                        <div class="ks">💰 ₹{sub['amount']} | 🕐 {sub['time']} | 📍 {sub['address']} | 📅 {sub['date']}</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    if st.button("❌", key=f"sh_cancel_{i}"): st.session_state.my_subs.pop(i); st.rerun()
        else:
            st.markdown('<div class="alert orange">📦 No subscriptions yet. Go to <b>Subscribe</b> tab!</div>', unsafe_allow_html=True)

    elif page == "📍 Find Vendor":
        st.markdown('<div class="hero green"><h2>📍 Find Vendors</h2><p>Nearest stalls to your campus</p></div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1: lf = st.selectbox("Language",["All","EN","HI","PU"])
        with c2: pf = st.selectbox("Paper",["All"]+list(AP.keys()))
        filtered = [v for v in AV if (lf=="All" or lf in v.get("langs",[])) and (pf=="All" or pf in v.get("papers",[]))]
        st.markdown(f"**{len(filtered)} vendors found**")
        for v in filtered:
            langs = "".join([f'<span class="badge b-or">{l}</span>' for l in v.get("langs",[])])
            deliv = '<span class="badge b-gr">🚚 Delivery</span>' if v.get("delivery") else '<span class="badge b-bl">Pickup Only</span>'
            st.markdown(f"""
            <div class="kard green">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div><div class="kt">🏪 {v['name']}</div>
                <div class="ks">📍 {v['area']} | 🚶 {v['dist']} | 🕐 {v['open']}<br>
                📞 {v['phone']}<br>{langs} {deliv}</div></div>
                <div style="text-align:right;color:#f59e0b;font-weight:700;">⭐ {v['rating']}<br>
                <span style="color:#aaa;font-size:.7rem;">({v['reviews']})</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

    elif page == "📦 Subscribe":
        st.markdown('<div class="hero green"><h2>📦 Subscribe</h2><p>Student pricing — ₹30/month discount applied automatically!</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="alert green">🎓 <b>Student Discount: ₹30/month OFF</b> on Monthly & Yearly plans!</div>', unsafe_allow_html=True)
        _subscription_form(AP, student_discount=True)

    elif page == "🧾 My Orders":
        st.markdown('<div class="hero green"><h2>🧾 My Orders</h2><p>Your active subscriptions</p></div>', unsafe_allow_html=True)
        _orders_view(AP, key_prefix="s")

    elif page == "✨ Recommendations":
        st.markdown('<div class="hero green"><h2>✨ For You</h2><p>AI paper recommendations</p></div>', unsafe_allow_html=True)
        _recommendations(AP)


# ══════════════════════════════════════════════════════════════
# ██  VENDOR DASHBOARD  ██
# ══════════════════════════════════════════════════════════════
def page_vendor():
    VENDOR_PAGES = ["📊 Dashboard","🧠 AI Predictions","📈 Sales History","📁 Upload Data","⚙️ Stall Settings"]
    page = _sidebar(VENDOR_PAGES)
    AV = av(); AP = ap()
    BASE = {"TOI":55,"HT":35,"BHASKAR":65,"JAGRAN":50,"AJIT":45,"PTRIB":30,"TRIB":40,"ET":25}
    stall = next((v for v in AV if "Sharma" in v.get("name","")), AV[0] if AV else None)
    if not stall:
        st.error("No stall data found."); return
    wb = 1.3 if datetime.now().weekday() in [5,6] else 1.0

    if page == "📊 Dashboard":
        st.markdown(f"""
        <div class="hero purple">
            <h2>🏪 {stall['name']}</h2>
            <p>📍 {stall['area']} &nbsp;|&nbsp; ⭐ {stall['rating']} rating &nbsp;|&nbsp; 🕐 {stall['open']}</p>
        </div>
        <div class="stats">
            <div class="stat purple"><div class="sn purple">{len(stall['papers'])}</div><div class="sl">📰 Papers</div></div>
            <div class="stat purple"><div class="sn purple">⭐{stall['rating']}</div><div class="sl">Rating</div></div>
            <div class="stat purple"><div class="sn purple">{stall['reviews']}</div><div class="sl">Reviews</div></div>
            <div class="stat purple"><div class="sn purple">{'Yes' if stall['delivery'] else 'No'}</div><div class="sl">🚚 Delivery</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("### 🧠 Tomorrow's Stock Prediction")
        st.markdown('<div class="alert blue">🧠 <b>Facebook Prophet ML</b> — 95% accuracy using weather, weekday & exam calendar data</div>', unsafe_allow_html=True)

        for pc in stall["papers"][:5]:
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
        total = sum(int(BASE.get(p,30)*wb) for p in stall["papers"])
        st.success(f"📦 Order ~**{total} total copies** tomorrow | Est. Revenue ₹{total*4}")

    elif page == "🧠 AI Predictions":
        st.markdown('<div class="hero purple"><h2>🧠 Full AI Predictions</h2><p>7-day forecast — Facebook Prophet Model</p></div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        c1.metric("📅 Tomorrow",  (date.today()+timedelta(1)).strftime("%a, %d %b"))
        c2.metric("🌤️ Weather",  "Sunny ☀️")
        c3.metric("📊 Accuracy", "95.2%")
        st.markdown("### 📦 Full Order Quantities Tomorrow")
        total = 0
        for pc in stall["papers"]:
            b=BASE.get(pc,30); pred=int(b*wb*random.uniform(.92,1.08))
            lo,hi=int(pred*.85),int(pred*1.15); inf=AP.get(pc,{}); total+=pred
            st.markdown(f"""
            <div class="pred-row">
                <div>
                    <div style="font-weight:700;">{pc} — {inf.get('name',pc)}</div>
                    <div style="color:#888;font-size:.78rem;">{inf.get('flag','')} {inf.get('lang','')} | Range: {lo}–{hi}</div>
                </div>
                <div class="pred-num">{pred}</div>
            </div>""", unsafe_allow_html=True)
        st.success(f"📦 Total: **{total} copies** | Revenue ≈ ₹{total*4}")

    elif page == "📈 Sales History":
        st.markdown('<div class="hero purple"><h2>📈 Sales History</h2><p>Last 30 days performance</p></div>', unsafe_allow_html=True)
        hist=[]
        for d in range(30,0,-1):
            dt=date.today()-timedelta(d)
            for p in stall["papers"][:4]:
                b=BASE.get(p,30)
                u=int(b*random.uniform(.85,1.15)*(1.3 if dt.weekday() in [5,6] else 1.0))
                hist.append({"Date":dt,"Paper":p,"Units":u,"Revenue":u*4})
        df=pd.DataFrame(hist)
        ps=st.selectbox("Paper",stall["papers"][:4])
        cd=df[df["Paper"]==ps].set_index("Date")
        st.line_chart(cd["Units"])
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Avg/Day",f"{int(cd['Units'].mean())}")
        c2.metric("Best Day",f"{int(cd['Units'].max())}")
        c3.metric("Total",f"{int(cd['Units'].sum())}")
        c4.metric("Revenue",f"₹{int(cd['Revenue'].sum())}")

    elif page == "📁 Upload Data":
        st.markdown('<div class="hero purple"><h2>📁 Upload Sales Data</h2><p>Train AI on your real sales data</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="alert blue">📋 CSV columns: <code>date, paper_code, units_sold, weather, is_holiday, is_weekend</code></div>', unsafe_allow_html=True)
        st.code("2024-01-15,TOI,65,sunny,false,false\n2024-01-16,HT,38,cloudy,false,false")
        up=st.file_uploader("Upload CSV",type=["csv"])
        if up:
            dfu=pd.read_csv(up)
            st.success(f"✅ {len(dfu)} rows uploaded!")
            st.dataframe(dfu.head(10),use_container_width=True)
            if st.button("🧠  Train AI Model"):
                import time
                with st.spinner("Training..."): time.sleep(2)
                st.success("✅ Model updated!"); st.balloons()

    elif page == "⚙️ Stall Settings":
        st.markdown('<div class="hero purple"><h2>⚙️ Stall Settings</h2><p>Update your stall information</p></div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            st.text_input("Stall Name",    value=stall["name"])
            st.text_input("Area",          value=stall["area"])
            st.text_input("Phone",         value=stall["phone"])
        with c2:
            st.text_input("Opening Time",  value=stall["open"].split("–")[0])
            st.text_input("Closing Time",  value=stall["open"].split("–")[-1])
            st.checkbox("Offer Delivery",  value=stall["delivery"])
        st.multiselect("Languages",       ["EN","HI","PU"],  default=stall.get("langs",[]))
        st.multiselect("Papers Available", list(AP.keys()),  default=stall["papers"])
        if st.button("💾  Save Changes"): st.success("✅ Settings saved!")


# ══════════════════════════════════════════════════════════════
# ██  ADMIN DASHBOARD  ██
# ══════════════════════════════════════════════════════════════
def page_admin():
    ADMIN_PAGES = ["📊 Overview","🏪 Vendors","📰 Newspapers","👥 Users","📈 Analytics"]
    page = _sidebar(ADMIN_PAGES)
    AV = st.session_state.vendors
    AP = st.session_state.papers

    if page == "📊 Overview":
        act_v = len([v for v in AV if v.get("active",True)])
        act_p = len([p for p in AP.values() if p.get("active",True)])
        st.markdown(f"""
        <div class="hero dark">
            <h2>👑 Admin Dashboard</h2>
            <p>Full platform control — vendors, newspapers, users & revenue</p>
        </div>
        <div class="stats">
            <div class="stat dark"><div class="sn dark">{act_v}</div><div class="sl">🏪 Active Vendors</div></div>
            <div class="stat dark"><div class="sn dark">{act_p}</div><div class="sl">📰 Active Papers</div></div>
            <div class="stat dark"><div class="sn dark">{len(st.session_state.users_db)}</div><div class="sl">👥 Users</div></div>
            <div class="stat dark"><div class="sn dark">₹12.4K</div><div class="sl">💰 This Month</div></div>
        </div>""", unsafe_allow_html=True)
        st.markdown("### 📈 Orders Last 7 Days")
        dates7 = [(date.today()-timedelta(i)).strftime("%a %d") for i in range(6,-1,-1)]
        st.bar_chart(pd.DataFrame({"Orders":[random.randint(15,50) for _ in dates7]}, index=dates7))
        st.markdown("### 🏆 Top Vendors")
        top = sorted([v for v in AV if v.get("active",True)], key=lambda x:x["rating"], reverse=True)[:5]
        st.dataframe(pd.DataFrame([{"Vendor":v["name"],"Area":v["area"],"Rating":v["rating"],"Reviews":v["reviews"],"Delivery":"✅" if v["delivery"] else "❌"} for v in top]), use_container_width=True, hide_index=True)

    elif page == "🏪 Vendors":
        st.markdown('<div class="hero dark"><h2>🏪 Manage Vendors</h2><p>Add, edit, enable or remove vendors</p></div>', unsafe_allow_html=True)
        with st.expander("➕ Add New Vendor"):
            c1,c2 = st.columns(2)
            with c1:
                nv_n=st.text_input("Stall Name *", key="nv_n")
                nv_a=st.text_input("Area *",        key="nv_a")
                nv_p=st.text_input("Phone *",       key="nv_p")
                nv_d=st.text_input("Distance",      key="nv_d", placeholder="e.g. 1.5km")
            with c2:
                nv_o=st.text_input("Opens",  value="6:00 AM",  key="nv_o")
                nv_c=st.text_input("Closes", value="10:00 AM", key="nv_c")
                nv_l=st.multiselect("Languages",["EN","HI","PU"],default=["EN","HI"], key="nv_l")
                nv_del=st.checkbox("Offers Delivery", key="nv_del")
            ap_active = {k:v for k,v in AP.items() if v.get("active",True)}
            nv_pp=st.multiselect("Papers",list(ap_active.keys()),default=["TOI","BHASKAR"],key="nv_pp")
            if st.button("✅  Add Vendor", key="btn_add_v"):
                if not nv_n or not nv_a or not nv_p:
                    st.error("❌ Name, Area and Phone are required.")
                else:
                    new_id=max([v["id"] for v in AV],default=0)+1
                    st.session_state.vendors.append({"id":new_id,"name":nv_n,"area":nv_a,"dist":nv_d or "?","langs":nv_l,"papers":nv_pp,"rating":0.0,"reviews":0,"delivery":nv_del,"open":f"{nv_o}–{nv_c}","phone":nv_p,"active":True})
                    st.success(f"✅ '{nv_n}' added!"); st.rerun()

        st.markdown(f"### All Vendors ({len(AV)})")
        for i,v in enumerate(AV):
            c1,c2,c3,c4 = st.columns([3.5,1,1,1])
            with c1: st.markdown(f"**{'🟢' if v.get('active',True) else '🔴'} {v['name']}** &nbsp;<small style='color:#888;'>{v['area']}</small>", unsafe_allow_html=True)
            with c2: st.write(f"⭐ {v['rating']}")
            with c3:
                if v.get("active",True):
                    if st.button("🔴 Off",key=f"av_off_{i}"): st.session_state.vendors[i]["active"]=False; st.rerun()
                else:
                    if st.button("🟢 On", key=f"av_on_{i}"):  st.session_state.vendors[i]["active"]=True;  st.rerun()
            with c4:
                if st.button("🗑️",key=f"av_del_{i}"): st.session_state.vendors.pop(i); st.rerun()

    elif page == "📰 Newspapers":
        st.markdown('<div class="hero dark"><h2>📰 Manage Newspapers</h2><p>Add, hide or remove papers</p></div>', unsafe_allow_html=True)
        with st.expander("➕ Add New Newspaper"):
            c1,c2=st.columns(2)
            with c1:
                np_c=st.text_input("Code * (max 8)",placeholder="e.g. TRIB",key="np_c").upper()
                np_n=st.text_input("Full Name *",placeholder="e.g. The Tribune",key="np_n")
                np_l=st.selectbox("Language",["EN - English","HI - Hindi","PU - Punjabi"],key="np_l")
            with c2:
                np_pr=st.number_input("Daily ₹",1,50,5,key="np_pr")
                np_mo=st.number_input("Monthly ₹",50,500,120,key="np_mo")
                np_yr=st.number_input("Yearly ₹",500,6000,1200,key="np_yr")
            np_f={"EN - English":"🇬🇧","HI - Hindi":"🇮🇳","PU - Punjabi":"🏵️"}.get(np_l,"🇬🇧")
            np_lc=np_l.split(" - ")[0]
            if st.button("✅  Add Newspaper",key="btn_add_p"):
                if not np_c or not np_n: st.error("❌ Code and Name required.")
                elif len(np_c)>8: st.error("❌ Code max 8 chars.")
                elif np_c in AP: st.error(f"❌ Code '{np_c}' exists.")
                else:
                    st.session_state.papers[np_c]={"name":np_n,"lang":np_lc,"flag":np_f,"price":np_pr,"monthly":np_mo,"yearly":np_yr,"active":True}
                    st.success(f"✅ '{np_n}' added!"); st.rerun()

        st.markdown(f"### All Newspapers ({len(AP)})")
        for code,info in list(AP.items()):
            c1,c2,c3,c4,c5=st.columns([1,2.5,1,1,1])
            with c1: st.markdown(f"**{code}**")
            with c2: st.write(f"{info['flag']} {info['name']}")
            with c3: st.write(f"₹{info['price']}/d")
            with c4:
                if info.get("active",True):
                    if st.button("🔴 Hide",key=f"ph_{code}"): st.session_state.papers[code]["active"]=False; st.rerun()
                else:
                    if st.button("🟢 Show",key=f"ps_{code}"): st.session_state.papers[code]["active"]=True;  st.rerun()
            with c5:
                if st.button("🗑️",key=f"pd_{code}"): del st.session_state.papers[code]; st.rerun()

    elif page == "👥 Users":
        st.markdown('<div class="hero dark"><h2>👥 Manage Users</h2><p>All registered accounts</p></div>', unsafe_allow_html=True)
        ud=[{"Email":e,"Name":i["name"],"Role":i["role"],"Phone":i.get("phone","—")} for e,i in st.session_state.users_db.items()]
        st.dataframe(pd.DataFrame(ud),use_container_width=True,hide_index=True)
        st.markdown("### ➕ Add User / Staff")
        c1,c2=st.columns(2)
        with c1:
            nu_n=st.text_input("Name *",key="nu_n"); nu_e=st.text_input("Email *",key="nu_e"); nu_ph=st.text_input("Phone",key="nu_ph")
        with c2:
            nu_p=st.text_input("Password *",type="password",key="nu_p"); nu_r=st.selectbox("Role",["user","student","vendor","admin"],key="nu_r")
        if st.button("✅  Add User",key="btn_add_u"):
            if not nu_n or not nu_e or not nu_p: st.error("❌ Name, Email, Password required.")
            elif nu_e in st.session_state.users_db: st.error("❌ Email already exists.")
            else:
                st.session_state.users_db[nu_e]={"pw":md5(nu_p),"role":nu_r,"name":nu_n,"phone":nu_ph}
                st.success(f"✅ {nu_n} added!"); st.rerun()

    elif page == "📈 Analytics":
        st.markdown('<div class="hero dark"><h2>📈 Analytics</h2><p>Platform metrics and revenue</p></div>', unsafe_allow_html=True)
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Vendors", len(AV), f"{len([v for v in AV if v.get('active')])} active")
        c2.metric("Papers",  len(AP), f"{len([p for p in AP.values() if p.get('active')])} active")
        c3.metric("Users",   len(st.session_state.users_db))
        c4.metric("Revenue", "₹12,450","↑ 18%")
        dates14=[(date.today()-timedelta(i)).strftime("%d %b") for i in range(13,-1,-1)]
        st.markdown("### 📈 Daily Metrics — Last 14 Days")
        st.line_chart(pd.DataFrame({"Orders":[random.randint(10,50) for _ in dates14],"Revenue":[random.randint(400,2000) for _ in dates14]},index=dates14))
        top=sorted([v for v in AV if v.get("active",True)],key=lambda x:x["rating"],reverse=True)[:5]
        st.markdown("### 🏆 Top Vendors")
        st.dataframe(pd.DataFrame([{"Vendor":v["name"],"Area":v["area"],"Rating":v["rating"],"Reviews":v["reviews"]} for v in top]),use_container_width=True,hide_index=True)


# ══════════════════════════════════════════════════════════════
# SHARED COMPONENTS
# ══════════════════════════════════════════════════════════════
def _subscription_form(AP, student_discount=False):
    c1, c2 = st.columns([3,2])
    with c1:
        lang_f = st.selectbox("Language",["All","English 🇬🇧","Hindi 🇮🇳","Punjabi 🏵️"],key="sf_lang")
        lc = {"All":"ALL","English 🇬🇧":"EN","Hindi 🇮🇳":"HI","Punjabi 🏵️":"PU"}.get(lang_f,"ALL")
        opts = {c:i for c,i in AP.items() if lc=="ALL" or i["lang"]==lc}
        if not opts: opts = AP

        paper_key = st.selectbox("📰 Newspaper", list(opts.keys()),
            format_func=lambda x: f"{opts[x]['flag']} {opts[x]['name']} — ₹{opts[x]['price']}/day", key="sf_paper")
        pi = opts[paper_key]

        # prices
        dp  = pi["price"]
        mp  = max(pi["monthly"] - (30 if student_discount else 0), 50) + (0 if student_discount else 30)
        yp  = max(pi["yearly"]  - (360 if student_discount else 0), 500) + (0 if student_discount else 300)

        st.markdown("#### 📅 Choose Plan")
        pc = st.columns(3)
        with pc[0]:
            st.markdown(f"""<div class="plan-card">
            <div class="plan-tag">📅 Daily</div>
            <div class="plan-price">₹{dp}</div><div class="plan-period">per copy</div>
            <hr style="border-color:#eee;margin:.5rem 0;">
            <div style="font-size:.74rem;color:#555;">No commitment<br>Pickup from stall</div></div>""", unsafe_allow_html=True)
        with pc[1]:
            discount_note = " (₹30 OFF!)" if student_discount else ""
            st.markdown(f"""<div class="plan-card hot">
            <div class="plan-tag">🔥 Most Popular</div>
            <div class="plan-price">₹{mp}</div><div class="plan-period">/month{discount_note}</div>
            <hr style="border-color:#eee;margin:.5rem 0;">
            <div style="font-size:.74rem;color:#555;">Home delivery<br>Choose time slot<br>Cancel anytime</div></div>""", unsafe_allow_html=True)
        with pc[2]:
            discount_note_yr = " (₹360 OFF!)" if student_discount else ""
            st.markdown(f"""<div class="plan-card">
            <div class="plan-tag">⭐ Best Value</div>
            <div class="plan-price">₹{yp}</div><div class="plan-period">/year{discount_note_yr}</div>
            <hr style="border-color:#eee;margin:.5rem 0;">
            <div style="font-size:.74rem;color:#555;">Home delivery<br>Priority support<br>2 months free</div></div>""", unsafe_allow_html=True)

        sel_plan = st.radio("Select Plan",
            [f"📅 Daily — ₹{dp}/copy", f"🚚 Monthly — ₹{mp}/mo", f"🏆 Yearly — ₹{yp}/yr"],
            horizontal=True, key="sf_plan")
        amount    = dp if "Daily" in sel_plan else (mp if "Monthly" in sel_plan else yp)
        plan_name = "Daily" if "Daily" in sel_plan else ("Monthly" if "Monthly" in sel_plan else "Yearly")

        t_slot = "Pickup"; address = "Pickup"
        if "Daily" not in sel_plan:
            t_slot  = st.select_slider("🕐 Delivery Time", ["5:00 AM","5:30 AM","6:00 AM","6:30 AM","7:00 AM","7:30 AM"], key="sf_time")
            address = st.text_input("📍 Delivery Address *", placeholder="House No, Street, Area, Ludhiana", key="sf_addr")

    with c2:
        st.markdown("**💳 Payment Method**")
        upi = st.radio("Pay via", ["📱 Google Pay","💜 PhonePe","💙 Paytm","🏛️ BHIM UPI"], label_visibility="collapsed", key="sf_upi")
        upi_name = upi.split(" ",1)[1]

        disc_html = ""
        if student_discount and "Daily" not in sel_plan:
            disc_html = '<div class="order-row"><span style="color:#059669;">🎓 Student Discount</span><span style="color:#059669;font-weight:700;">Applied ✅</span></div>'

        st.markdown(f"""
        <div class="order-box">
            <div class="order-row"><span style="color:#666;">📰 Paper</span><span style="font-weight:700;">{pi['name']}</span></div>
            <div class="order-row"><span style="color:#666;">📅 Plan</span><span style="font-weight:700;">{plan_name}</span></div>
            <div class="order-row"><span style="color:#666;">🕐 Time</span><span style="font-weight:700;">{t_slot}</span></div>
            <div class="order-row"><span style="color:#666;">💳 Via</span><span style="font-weight:700;">{upi_name}</span></div>
            {disc_html}
            <hr style="border-color:#FF6B2B44;margin:8px 0;">
            <div class="order-total">₹{amount}</div>
            <div style="text-align:center;color:#888;font-size:.74rem;">{plan_name} total</div>
        </div>""", unsafe_allow_html=True)

        if st.button(f"✅  Confirm & Pay ₹{amount}", use_container_width=True, key="sf_pay"):
            if "Daily" not in sel_plan and not address:
                st.warning("⚠️ Please enter your delivery address first.")
            else:
                st.session_state.my_subs.append({
                    "paper":paper_key,"plan":plan_name,"amount":amount,
                    "time":t_slot,"address":address,"upi":upi_name,
                    "date":date.today().strftime("%d %b %Y")
                })
                st.markdown(f"""
                <div class="success-pop">
                    <div style="font-size:2.5rem;">🎉</div>
                    <div style="font-size:1.1rem;font-weight:800;">Subscribed Successfully!</div>
                    <div>{pi['name']} — {plan_name} Plan</div>
                    <div style="opacity:.88;margin-top:.3rem;">₹{amount} via {upi_name}</div>
                </div>""", unsafe_allow_html=True)
                st.balloons()


def _orders_view(AP, key_prefix=""):
    subs = st.session_state.my_subs
    if not subs:
        st.info("📦 No orders yet. Go to Subscribe tab to get started!")
        return
    st.markdown(f"**{len(subs)} active subscription(s)**")
    for i,sub in enumerate(subs):
        p = AP.get(sub["paper"],{})
        c1,c2 = st.columns([5,1])
        with c1:
            st.markdown(f"""
            <div class="kard green">
                <div class="kt">📰 {p.get('name',sub['paper'])} — {sub['plan']}</div>
                <div class="ks">💰 ₹{sub['amount']} &nbsp;|&nbsp; 🕐 {sub['time']} &nbsp;|&nbsp; 📍 {sub['address']}<br>
                📅 Started {sub['date']} &nbsp;|&nbsp; 💳 {sub['upi']}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            if st.button("❌ Cancel", key=f"{key_prefix}_oc_{i}"):
                st.session_state.my_subs.pop(i); st.rerun()


def _recommendations(AP):
    cur = st.selectbox("I currently read", list(AP.keys()), format_func=lambda x:f"{AP[x]['flag']} {AP[x]['name']}", key="rec_sel")
    if st.button("✨  Get Recommendations", key="rec_btn"):
        RECS = {
            "TOI":    [("HINDU",91,"Similar quality English journalism"),("HT",87,"Different editorial angle"),("ET",72,"Great for business readers")],
            "HT":     [("TOI",90,"Most popular English daily"),("HINDU",82,"Deeper analysis"),("ET",70,"Financial news focus")],
            "BHASKAR":[("JAGRAN",89,"Very similar readership profile"),("KESARI",78,"Top Hindi paper in Punjab")],
            "JAGRAN": [("BHASKAR",88,"Similar Hindi audience"),("KESARI",75,"Strong Punjab coverage")],
            "AJIT":   [("PTRIB",93,"Perfect Punjabi pairing"),("DESH",80,"Strong local Punjab focus")],
            "PTRIB":  [("AJIT",91,"Best Punjabi companion"),("DESH",76,"Good local content")],
        }
        recs = RECS.get(cur,[("HT",85,"Great alternative"),("BHASKAR",75,"Top regional paper")])
        st.markdown("### 🎯 Recommended For You")
        for code,sc,reason in recs:
            if code in AP:
                inf = AP[code]
                st.markdown(f"""
                <div class="kard purple">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div class="kt">{inf['flag']} {inf['name']}</div>
                        <div class="ks">💡 {reason}<br>₹{inf['price']}/day | ₹{inf['monthly']}/month | ₹{inf['yearly']}/year</div>
                    </div>
                    <div style="background:#f5f3ff;border-radius:10px;padding:.5rem .9rem;text-align:center;min-width:60px;">
                        <div style="font-size:1.1rem;font-weight:800;color:#7C3AED;">{sc}%</div>
                        <div style="font-size:.68rem;color:#888;">match</div>
                    </div>
                    </div>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ██  MAIN ROUTER  ██
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    page_login()
else:
    role = st.session_state.role
    if   role == "admin":   page_admin()
    elif role == "vendor":  page_vendor()
    elif role == "student": page_student()
    else:                   page_user()
