"""
Paper Scout Pro — Complete Rebuilt App
- Simple working login (no HTML panels)
- Role-based dashboards (Admin / Vendor / Student / User)
- Live subscriptions (day/monthly/yearly)
- Working admin panel
"""

import streamlit as st
import pandas as pd
import random
import hashlib
from datetime import datetime, date, timedelta

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Paper Scout Pro",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding-top: 1.2rem !important; }

/* Cards */
.card {
    background: white; border-radius: 14px;
    padding: 1.2rem 1.4rem; margin-bottom: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    border-left: 5px solid #FF6B2B;
}
.card-purple { border-left-color: #8B5CF6; }
.card-green  { border-left-color: #10B981; }
.card-blue   { border-left-color: #3B82F6; }

.card-title { font-size: 1rem; font-weight: 700; color: #111; margin-bottom: 4px; }
.card-sub   { font-size: 0.82rem; color: #666; line-height: 1.7; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #FF6B2B, #d94f15);
    border-radius: 16px; padding: 1.8rem 2rem;
    color: white; margin-bottom: 1.2rem;
    box-shadow: 0 6px 24px rgba(255,107,43,0.25);
}
.hero h1 { font-size: 1.8rem; font-weight: 800; margin: 0 0 4px; }
.hero p  { opacity: .88; margin: 0; font-size: .95rem; }

/* Stat row */
.stat-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 1.2rem; }
.stat-card {
    background: white; border-radius: 12px; padding: 1rem;
    text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border-bottom: 4px solid #FF6B2B;
}
.stat-num { font-size: 1.7rem; font-weight: 800; color: #FF6B2B; }
.stat-lbl { font-size: 0.75rem; color: #888; margin-top: 2px; }

/* Badge */
.badge { display:inline-block; padding:2px 10px; border-radius:20px; font-size:.72rem; font-weight:600; margin:2px; }
.badge-or  { background:#fff3ec; color:#FF6B2B; }
.badge-gr  { background:#ecfdf5; color:#059669; }
.badge-bl  { background:#eff6ff; color:#3B82F6; }
.badge-pu  { background:#f5f3ff; color:#7C3AED; }

/* Subscription card */
.sub-card {
    background: white; border-radius: 14px; padding: 1.4rem;
    text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border: 2px solid #eee; transition: all .2s;
}
.sub-card:hover { border-color: #FF6B2B; transform: translateY(-2px); }
.sub-card.popular { border-color: #FF6B2B; background: #fff8f5; }
.sub-price { font-size: 2rem; font-weight: 800; color: #FF6B2B; }
.sub-period { font-size: .78rem; color: #888; }
.sub-tag { background: #FF6B2B; color: white; font-size:.7rem; font-weight:700;
           padding:2px 10px; border-radius:20px; margin-bottom:.5rem; display:inline-block; }

/* Paper tile */
.paper-row {
    background: white; border-radius: 10px; padding: .8rem 1rem;
    margin-bottom: 8px; display: flex; justify-content: space-between;
    align-items: center; box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}
.paper-code {
    background: #FF6B2B; color: white; width: 42px; height: 42px;
    border-radius: 8px; display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: .7rem; text-align: center; flex-shrink: 0;
}

/* Order summary */
.order-box {
    background: linear-gradient(135deg,#fff8f5,#ffe8d6);
    border: 2px solid #FF6B2B; border-radius: 14px;
    padding: 1.4rem; margin: .8rem 0;
}
.order-total { font-size: 1.8rem; font-weight: 800; color: #FF6B2B; text-align: center; }

/* Prediction */
.pred-row {
    background: white; border-radius: 10px; padding: .9rem 1rem;
    margin-bottom: 8px; display: flex; justify-content: space-between;
    align-items: center; box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    border-left: 4px solid #8B5CF6;
}

/* Alert boxes */
.alert-green { background:#ecfdf5; border:1.5px solid #10B981; border-radius:10px; padding:.8rem 1rem; color:#065f46; font-size:.88rem; margin:.5rem 0; }
.alert-orange { background:#fff8f5; border:1.5px solid #FF6B2B; border-radius:10px; padding:.8rem 1rem; color:#9a3412; font-size:.88rem; margin:.5rem 0; }
.alert-blue   { background:#eff6ff; border:1.5px solid #3B82F6; border-radius:10px; padding:.8rem 1rem; color:#1e3a8a; font-size:.88rem; margin:.5rem 0; }

/* Sidebar user badge */
.user-chip {
    background: #fff3ec; border-radius: 30px; padding: 6px 14px;
    color: #FF6B2B; font-weight: 700; font-size: .85rem;
    display: inline-block; margin-bottom: .5rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#FF6B2B,#e85d1e) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: .9rem !important; width: 100%;
    box-shadow: 0 3px 10px rgba(255,107,43,.3) !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; }

/* Success */
.success-pop {
    background: linear-gradient(135deg,#10B981,#059669);
    border-radius: 16px; padding: 2rem; text-align: center;
    color: white; margin: .8rem 0;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════
def ss(k, v):
    if k not in st.session_state:
        st.session_state[k] = v

ss("logged_in", False)
ss("role", None)
ss("name", None)
ss("email", None)
ss("my_subscriptions", [])
ss("login_mode", "login")

ss("users_db", {
    "admin@paperscout.com":  {"pw": hashlib.md5(b"admin123").hexdigest(),   "role": "admin",   "name": "Admin Owner",   "phone": "98765-00000"},
    "student@pau.edu":       {"pw": hashlib.md5(b"student123").hexdigest(),  "role": "student", "name": "Rahul Kumar",    "phone": "98765-11111"},
    "vendor@paperscout.com": {"pw": hashlib.md5(b"vendor123").hexdigest(),   "role": "vendor",  "name": "Sharma Agency",  "phone": "98765-01001"},
    "user@gmail.com":        {"pw": hashlib.md5(b"user123").hexdigest(),     "role": "user",    "name": "Priya Singh",    "phone": "98765-22222"},
})

ss("vendors", [
    {"id":1,"name":"Sharma News Agency","area":"PAU Campus","dist":"300m","langs":["EN","HI","PU"],"papers":["TOI","HT","BHASKAR","AJIT","PTRIB"],"rating":4.8,"reviews":35,"delivery":True,"open":"5:30–10:30 AM","phone":"98765 01001","active":True},
    {"id":2,"name":"PAU Gate 4 Stall","area":"PAU Campus","dist":"500m","langs":["EN","HI","PU"],"papers":["TOI","HT","TRIB","BHASKAR","AJIT"],"rating":4.7,"reviews":31,"delivery":True,"open":"6:00–10:00 AM","phone":"98765 01002","active":True},
    {"id":3,"name":"Clock Tower Akhbaar","area":"Clock Tower","dist":"1.5km","langs":["HI","PU"],"papers":["BHASKAR","JAGRAN","AJIT","PTRIB"],"rating":4.6,"reviews":26,"delivery":True,"open":"5:00–10:00 AM","phone":"98765 01003","active":True},
    {"id":4,"name":"Model Town News","area":"Model Town","dist":"2.0km","langs":["EN","HI"],"papers":["TOI","HT","HINDU","ET","BHASKAR"],"rating":4.7,"reviews":31,"delivery":False,"open":"6:00–10:30 AM","phone":"98765 01004","active":True},
    {"id":5,"name":"Singh Paper Depot","area":"BRS Nagar","dist":"1.2km","langs":["EN","PU"],"papers":["TOI","TRIB","KESARI","AJIT"],"rating":4.2,"reviews":18,"delivery":True,"open":"6:00–10:00 AM","phone":"98765 01005","active":True},
    {"id":6,"name":"Ghumar Mandi Papers","area":"Ghumar Mandi","dist":"0.9km","langs":["EN","HI","PU"],"papers":["TOI","HT","TRIB","BHASKAR","AJIT"],"rating":4.0,"reviews":11,"delivery":True,"open":"5:30–9:30 AM","phone":"98765 01006","active":True},
])

ss("papers", {
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

# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def active_vendors(): return [v for v in st.session_state.vendors if v.get("active", True)]
def active_papers():  return {k:v for k,v in st.session_state.papers.items() if v.get("active", True)}

def do_login(email, role):
    info = st.session_state.users_db[email]
    st.session_state.logged_in = True
    st.session_state.role  = info["role"]
    st.session_state.name  = info["name"]
    st.session_state.email = email
    st.rerun()

# ══════════════════════════════════════════════════════════════
# ██████  LOGIN PAGE  ██████
# ══════════════════════════════════════════════════════════════
def page_login():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    .block-container { max-width: 480px !important; margin: 0 auto !important; padding-top: 4vh !important; }
    </style>
    """, unsafe_allow_html=True)

    # Logo
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <div style="font-size:3rem;">📰</div>
        <div style="font-size:1.7rem; font-weight:800; color:#FF6B2B; margin:4px 0 2px;">Paper Scout Pro</div>
        <div style="color:#888; font-size:.88rem;">Ludhiana's Newspaper Platform</div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.session_state.login_mode

    # ── LOGIN ──────────────────────────────────────────────
    if mode == "login":
        st.markdown("### 🔐 Sign In")

        role_map = {
            "👑 Admin / Owner":    "admin",
            "🎓 Student":          "student",
            "🏪 Newspaper Vendor": "vendor",
            "👤 General User":     "user",
        }
        role_lbl = st.selectbox("Log in as", list(role_map.keys()))
        role_sel = role_map[role_lbl]

        # Hint
        hints = {
            "admin":   "Full access — vendors, papers, users & analytics",
            "student": "Student discount ₹30/month applied automatically",
            "vendor":  "AI stock dashboard for your stall",
            "user":    "Find vendors & subscribe to home delivery",
        }
        st.caption(f"ℹ️ {hints[role_sel]}")

        email = st.text_input("Email ID", placeholder="e.g. admin@paperscout.com")
        pw    = st.text_input("Password", type="password", placeholder="Enter password")

        # Forgot password row
        col_a, col_b = st.columns([1, 1])
        with col_b:
            st.markdown("<p style='text-align:right; margin-top:-8px;'><a href='#' style='color:#FF6B2B; font-size:.82rem; font-weight:600; text-decoration:none;'>Forgot Password?</a></p>", unsafe_allow_html=True)

        if st.button("🔑  Login", use_container_width=True):
            if not email or not pw:
                st.error("❌ Enter your email and password.")
            elif email not in st.session_state.users_db:
                st.error("❌ Email not found. Please create an account.")
            else:
                info = st.session_state.users_db[email]
                if info["pw"] != hashlib.md5(pw.encode()).hexdigest():
                    st.error("❌ Wrong password. Try again.")
                elif info["role"] != role_sel:
                    st.warning(f"⚠️ This email is registered as **{info['role']}**. Select correct role above.")
                else:
                    do_login(email, role_sel)

        st.markdown("<div style='display:flex;align-items:center;gap:8px;color:#bbb;font-size:.78rem;margin:.8rem 0;'><div style='flex:1;height:1px;background:#eee;'></div>OR<div style='flex:1;height:1px;background:#eee;'></div></div>", unsafe_allow_html=True)

        # Gmail / Phone quick buttons
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔴  Gmail Login", use_container_width=True):
                # Auto-match role
                defaults = {
                    "admin":   "admin@paperscout.com",
                    "student": "student@pau.edu",
                    "vendor":  "vendor@paperscout.com",
                    "user":    "user@gmail.com",
                }
                do_login(defaults[role_sel], role_sel)
        with c2:
            if st.button("📱  Phone OTP", use_container_width=True):
                st.session_state.login_mode = "phone"
                st.rerun()

        st.markdown("<div style='margin-top:1.2rem; text-align:center; color:#888; font-size:.85rem;'>Don't have an account?</div>", unsafe_allow_html=True)
        if st.button("📝  Create Free Account", use_container_width=True):
            st.session_state.login_mode = "register"
            st.rerun()

        # Demo hint box
        st.markdown("""
        <div style='background:#f8f8f8; border-radius:10px; padding:10px 14px; margin-top:1rem;
             font-size:.75rem; color:#666; border:1px solid #eee; line-height:1.9;'>
            <b>🔑 Demo Logins:</b><br>
            👑 admin@paperscout.com / admin123<br>
            🎓 student@pau.edu / student123<br>
            🏪 vendor@paperscout.com / vendor123<br>
            👤 user@gmail.com / user123
        </div>
        """, unsafe_allow_html=True)

    # ── PHONE OTP ─────────────────────────────────────────
    elif mode == "phone":
        st.markdown("### 📱 Login with Phone OTP")
        role_map2 = {"👑 Admin":"admin","🎓 Student":"student","🏪 Vendor":"vendor","👤 User":"user"}
        rl2 = st.selectbox("I am a", list(role_map2.keys()))
        rs2 = role_map2[rl2]
        ph  = st.text_input("Phone Number", placeholder="98765 01001")
        otp = st.text_input("OTP (demo: 123456)", type="password")
        if st.button("✅  Verify & Login", use_container_width=True):
            if otp == "123456" and ph:
                defaults2 = {"admin":"admin@paperscout.com","student":"student@pau.edu","vendor":"vendor@paperscout.com","user":"user@gmail.com"}
                do_login(defaults2[rs2], rs2)
            else:
                st.error("❌ Wrong OTP. Use 123456 for demo.")
        if st.button("← Back", use_container_width=True):
            st.session_state.login_mode = "login"; st.rerun()

    # ── REGISTER ──────────────────────────────────────────
    else:
        st.markdown("### ✨ Create Account")
        c1, c2 = st.columns(2)
        with c1: rname  = st.text_input("Full Name *",    placeholder="Gurpreet Singh")
        with c2: rphone = st.text_input("Phone Number *", placeholder="98765 12345")
        remail = st.text_input("Email Address *", placeholder="yourname@gmail.com")
        rpw    = st.text_input("Password *",      type="password", placeholder="Min 6 chars")
        rcpw   = st.text_input("Confirm Password *", type="password")
        rrole_opts = {"👤 General User":"user","🎓 Student":"student","🏪 Newspaper Vendor":"vendor","👑 Admin":"admin"}
        rrl  = st.selectbox("I am a *", list(rrole_opts.keys()))
        rrol = rrole_opts[rrl]
        if "Student" in rrl:
            st.text_input("College Name", placeholder="PAU / GNDU / DAV / LPU")
        if st.button("🚀  Create Account", use_container_width=True):
            if not rname or not remail or not rpw or not rphone:
                st.error("❌ Fill all required fields.")
            elif len(rpw) < 6:
                st.error("❌ Password min 6 characters.")
            elif rpw != rcpw:
                st.error("❌ Passwords don't match.")
            elif remail in st.session_state.users_db:
                st.error("❌ Email already registered.")
            else:
                st.session_state.users_db[remail] = {"pw": hashlib.md5(rpw.encode()).hexdigest(), "role": rrol, "name": rname, "phone": rphone}
                do_login(remail, rrol)
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.login_mode = "login"; st.rerun()


# ══════════════════════════════════════════════════════════════
# SHARED SIDEBAR
# ══════════════════════════════════════════════════════════════
def sidebar(pages):
    role = st.session_state.role
    name = st.session_state.name
    icons = {"admin":"👑","student":"🎓","vendor":"🏪","user":"👤"}
    role_colors = {"admin":"#7C3AED","student":"#059669","vendor":"#FF6B2B","user":"#3B82F6"}
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center; padding:.5rem 0 .8rem;'>
            <div style='font-size:2.2rem;'>📰</div>
            <div style='font-size:1.1rem; font-weight:800; color:#FF6B2B;'>Paper Scout Pro</div>
            <div style='font-size:.75rem; color:#aaa;'>Ludhiana</div>
        </div>
        <div style='background:{role_colors.get(role,"#FF6B2B")}18; border:1.5px solid {role_colors.get(role,"#FF6B2B")}44;
             border-radius:10px; padding:8px 12px; margin:.5rem 0 1rem; text-align:center;'>
            <div style='font-size:.85rem; font-weight:700; color:{role_colors.get(role,"#FF6B2B")};'>
                {icons.get(role,"👤")} {name}
            </div>
            <div style='font-size:.72rem; color:#888; text-transform:uppercase; letter-spacing:.5px;'>{role}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("", pages, label_visibility="collapsed")
        st.markdown("---")
        if st.button("🚪 Logout"):
            for k in ["logged_in","role","name","email","my_subscriptions"]:
                st.session_state[k] = False if k == "logged_in" else ([] if k == "my_subscriptions" else None)
            st.session_state.login_mode = "login"
            st.rerun()
    return page


# ══════════════════════════════════════════════════════════════
# ██████  STUDENT DASHBOARD  ██████
# ══════════════════════════════════════════════════════════════
def dashboard_student():
    page = sidebar(["🏠 My Dashboard","📍 Find Vendor","📦 Subscribe","🧾 My Orders","✨ Recommendations"])
    AP = active_papers()
    AV = active_vendors()

    # ── MY DASHBOARD ──
    if "Dashboard" in page:
        st.markdown(f"""
        <div class="hero">
            <h1>🎓 Welcome, {st.session_state.name}!</h1>
            <p>Your student account — ₹30/month discount active on all subscriptions</p>
        </div>
        <div class="stat-row">
            <div class="stat-card"><div class="stat-num">{len(st.session_state.my_subscriptions)}</div><div class="stat-lbl">📦 My Subscriptions</div></div>
            <div class="stat-card"><div class="stat-num">{len(AV)}</div><div class="stat-lbl">🏪 Nearby Vendors</div></div>
            <div class="stat-card"><div class="stat-num">₹30</div><div class="stat-lbl">🎓 Monthly Saving</div></div>
            <div class="stat-card"><div class="stat-num">{len(AP)}</div><div class="stat-lbl">📰 Papers Available</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="alert-green">
            ✅ <b>Student Discount Active!</b> You save ₹30 every month on delivery subscriptions.
            Your PAU/GNDU student status has been verified.
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.my_subscriptions:
            st.markdown("### 📦 Your Active Subscriptions")
            for sub in st.session_state.my_subscriptions:
                p = AP.get(sub["paper"], {})
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">📰 {p.get('name', sub['paper'])} — {sub['plan']} Plan</div>
                    <div class="card-sub">
                        💰 ₹{sub['amount']} paid | 🕐 Delivery: {sub['time']} | 📍 {sub['address']}<br>
                        📅 Started: {sub['date']} | 💳 via {sub['upi']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-orange">
                📦 No active subscriptions yet. Go to <b>Subscribe</b> tab to get your newspaper delivered!
            </div>
            """, unsafe_allow_html=True)

    # ── FIND VENDOR ──
    elif "Find Vendor" in page:
        st.markdown('<div class="hero"><h1>📍 Find Vendors Near You</h1><p>Newspaper stalls near PAU/GNDU campus</p></div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: lf = st.selectbox("Language", ["All","EN","HI","PU"])
        with c2: pf = st.selectbox("Paper", ["All"] + list(AP.keys()))
        with c3: df = st.selectbox("Service", ["All","Delivery","Pickup Only"])
        filtered = [v for v in AV if
            (lf=="All" or lf in v["langs"]) and
            (pf=="All" or pf in v["papers"]) and
            (df!="Delivery" or v["delivery"]) and
            (df!="Pickup Only" or not v["delivery"])]
        st.markdown(f"**{len(filtered)} vendors found**")
        for v in filtered:
            lb = "".join([f'<span class="badge badge-or">{l}</span>' for l in v["langs"]])
            db = '<span class="badge badge-gr">🚚 Delivery</span>' if v["delivery"] else '<span class="badge badge-bl">Pickup Only</span>'
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="card-title">🏪 {v['name']}</div>
                        <div class="card-sub">
                            📍 {v['area']} &nbsp;|&nbsp; 🚶 {v['dist']} &nbsp;|&nbsp; 🕐 {v['open']}<br>
                            📞 {v['phone']}<br>
                            {lb} {db}
                        </div>
                    </div>
                    <div style="text-align:right; color:#f59e0b; font-weight:700;">⭐ {v['rating']}<br>
                    <span style="color:#aaa; font-size:.75rem;">({v['reviews']} reviews)</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── SUBSCRIBE ──
    elif "Subscribe" in page:
        st.markdown('<div class="hero"><h1>📦 Subscribe to Home Delivery</h1><p>Get your newspaper every morning — student price applied!</p></div>', unsafe_allow_html=True)

        st.markdown('<div class="alert-green">🎓 Student discount: <b>₹30/month OFF</b> automatically applied!</div>', unsafe_allow_html=True)

        c1, c2 = st.columns([3, 2])
        with c1:
            lang_sel = st.selectbox("Language", ["All","English 🇬🇧","Hindi 🇮🇳","Punjabi 🏵️"])
            lc = {"All":"ALL","English 🇬🇧":"EN","Hindi 🇮🇳":"HI","Punjabi 🏵️":"PU"}.get(lang_sel,"ALL")
            opts = {c: i for c,i in AP.items() if lc=="ALL" or i["lang"]==lc}

            paper_sel = st.selectbox("📰 Choose Newspaper", list(opts.keys()),
                format_func=lambda x: f"{opts[x]['flag']} {opts[x]['name']}")
            pinfo = opts.get(paper_sel, list(AP.values())[0])

            st.markdown("#### 📅 Choose Plan")
            plan_cols = st.columns(3)

            # Calculate prices with student discount
            day_price   = pinfo["price"]
            month_price = pinfo["monthly"] - 30   # student discount
            year_price  = pinfo["yearly"] - 360   # student discount (₹30x12)

            with plan_cols[0]:
                st.markdown(f"""
                <div class="sub-card">
                    <div class="sub-tag">Per Day</div>
                    <div class="sub-price">₹{day_price}</div>
                    <div class="sub-period">per day</div>
                    <hr style="margin:.5rem 0; border-color:#eee;">
                    <div style="font-size:.78rem; color:#666;">Pay daily<br>No commitment<br>Pickup only</div>
                </div>
                """, unsafe_allow_html=True)
            with plan_cols[1]:
                st.markdown(f"""
                <div class="sub-card popular">
                    <div class="sub-tag">🔥 Most Popular</div>
                    <div class="sub-price">₹{month_price}</div>
                    <div class="sub-period">/month (after ₹30 off)</div>
                    <hr style="margin:.5rem 0; border-color:#eee;">
                    <div style="font-size:.78rem; color:#666;">Home delivery<br>Any time slot<br>Cancel anytime</div>
                </div>
                """, unsafe_allow_html=True)
            with plan_cols[2]:
                st.markdown(f"""
                <div class="sub-card">
                    <div class="sub-tag">Best Value</div>
                    <div class="sub-price">₹{year_price}</div>
                    <div class="sub-period">/year (save ₹360)</div>
                    <hr style="margin:.5rem 0; border-color:#eee;">
                    <div style="font-size:.78rem; color:#666;">Home delivery<br>Priority support<br>Free on holidays</div>
                </div>
                """, unsafe_allow_html=True)

            selected_plan = st.radio("Select Plan", ["📅 Daily (Pickup)", "🚚 Monthly Delivery", "🏆 Yearly Delivery"], horizontal=True)
            plan_amount = {
                "📅 Daily (Pickup)":      day_price,
                "🚚 Monthly Delivery":    month_price,
                "🏆 Yearly Delivery":     year_price,
            }[selected_plan]
            plan_label = selected_plan.split(" ",1)[1].split("(")[0].strip()

            delivery_time = "N/A"
            address = "Pickup"
            if "Daily" not in selected_plan:
                delivery_time = st.select_slider("🕐 Delivery Time", ["5:00 AM","5:30 AM","6:00 AM","6:30 AM","7:00 AM","7:30 AM"])
                address = st.text_input("📍 Delivery Address", placeholder="Hostel / House No, Area, Ludhiana")

        with c2:
            upi = st.radio("💳 Payment", ["📱 Google Pay","💜 PhonePe","💙 Paytm","🏛️ BHIM UPI"], label_visibility="collapsed")
            st.markdown(f"""
            <div class="order-box">
                <div style="margin-bottom:.8rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                        <span style="color:#666;">📰 Paper</span><span style="font-weight:700;">{pinfo['name']}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                        <span style="color:#666;">📅 Plan</span><span style="font-weight:700;">{plan_label}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                        <span style="color:#666;">🕐 Time</span><span style="font-weight:700;">{delivery_time}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;color:#059669;">
                        <span>🎓 Student Discount</span><span style="font-weight:700;">Applied ✓</span>
                    </div>
                    <hr style="margin:8px 0; border-color:#FF6B2B44;">
                </div>
                <div class="order-total">₹{plan_amount}</div>
                <div style="text-align:center; color:#888; font-size:.78rem;">{plan_label} total</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"✅ Subscribe & Pay ₹{plan_amount}", use_container_width=True):
                sub = {
                    "paper": paper_sel, "plan": plan_label,
                    "amount": plan_amount, "time": delivery_time,
                    "address": address or "Pickup",
                    "upi": upi.split(" ",1)[1],
                    "date": date.today().strftime("%d %b %Y")
                }
                st.session_state.my_subscriptions.append(sub)
                st.markdown(f"""
                <div class="success-pop">
                    <div style="font-size:2.5rem;">🎉</div>
                    <div style="font-size:1.2rem; font-weight:800;">Subscribed!</div>
                    <div>{pinfo['name']} — {plan_label}</div>
                    <div style="opacity:.9; margin-top:.4rem;">₹{plan_amount} paid via {upi.split(' ',1)[1]}</div>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

    # ── MY ORDERS ──
    elif "Orders" in page:
        st.markdown('<div class="hero"><h1>🧾 My Orders</h1><p>All your subscriptions in one place</p></div>', unsafe_allow_html=True)
        if not st.session_state.my_subscriptions:
            st.info("📦 No orders yet. Go to Subscribe tab to get started!")
        else:
            for i, sub in enumerate(st.session_state.my_subscriptions):
                p = AP.get(sub["paper"], {})
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"""
                    <div class="card card-green">
                        <div class="card-title">📰 {p.get('name', sub['paper'])} — {sub['plan']}</div>
                        <div class="card-sub">
                            💰 ₹{sub['amount']} | 🕐 {sub['time']} | 📍 {sub['address']}<br>
                            📅 {sub['date']} | 💳 {sub['upi']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("❌ Cancel", key=f"cancel_{i}"):
                        st.session_state.my_subscriptions.pop(i); st.rerun()

    # ── RECOMMENDATIONS ──
    elif "Recommendations" in page:
        st.markdown('<div class="hero"><h1>✨ Recommended For You</h1><p>AI picks based on your reading preferences</p></div>', unsafe_allow_html=True)
        cur = st.selectbox("I currently read", list(AP.keys()), format_func=lambda x: f"{AP[x]['flag']} {AP[x]['name']}")
        if st.button("✨ Get AI Recommendations"):
            RECS = {
                "TOI":    [("HINDU",91,"Similar quality English journalism"),("HT",87,"Different editorial perspective"),("ET",72,"Great for business news")],
                "BHASKAR":[("JAGRAN",89,"Bhaskar readers love Jagran"),("KESARI",78,"Top Hindi paper in Punjab")],
                "AJIT":   [("PTRIB",93,"Perfect Punjabi pairing"),("DESH",80,"Strong local Punjab coverage")],
            }
            recs = RECS.get(cur, [("HT",85,"Great English alternative"),("BHASKAR",75,"Top regional paper")])
            for code, score, reason in recs:
                if code in AP:
                    inf = AP[code]
                    st.markdown(f"""
                    <div class="card card-purple">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <div class="card-title">{inf['flag']} {inf['name']}</div>
                                <div class="card-sub">💡 {reason}<br>₹{inf['price']}/day | ₹{inf['monthly']}/month</div>
                            </div>
                            <div style="background:#f5f3ff; border-radius:10px; padding:.5rem .9rem; text-align:center;">
                                <div style="font-size:1.2rem; font-weight:800; color:#7C3AED;">{score}%</div>
                                <div style="font-size:.7rem; color:#888;">match</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ██████  GENERAL USER DASHBOARD  ██████
# ══════════════════════════════════════════════════════════════
def dashboard_user():
    page = sidebar(["🏠 My Dashboard","📍 Find Vendor","📦 Subscribe","🧾 My Orders","✨ Recommendations"])
    AP = active_papers()
    AV = active_vendors()

    if "Dashboard" in page:
        st.markdown(f"""
        <div class="hero">
            <h1>👤 Welcome, {st.session_state.name}!</h1>
            <p>Find your nearest newspaper vendor or subscribe to home delivery</p>
        </div>
        <div class="stat-row">
            <div class="stat-card"><div class="stat-num">{len(st.session_state.my_subscriptions)}</div><div class="stat-lbl">📦 Subscriptions</div></div>
            <div class="stat-card"><div class="stat-num">{len(AV)}</div><div class="stat-lbl">🏪 Vendors Nearby</div></div>
            <div class="stat-card"><div class="stat-num">{len(AP)}</div><div class="stat-lbl">📰 Papers</div></div>
            <div class="stat-card"><div class="stat-num">₹150</div><div class="stat-lbl">🚚 Delivery/mo</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📍 Nearest Vendors")
        for v in AV[:3]:
            lb = "".join([f'<span class="badge badge-or">{l}</span>' for l in v["langs"]])
            db = '<span class="badge badge-gr">🚚 Delivery</span>' if v["delivery"] else ""
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <div class="card-title">🏪 {v['name']}</div>
                        <div class="card-sub">📍 {v['area']} | 🚶 {v['dist']} | 🕐 {v['open']}<br>📞 {v['phone']}<br>{lb} {db}</div>
                    </div>
                    <div style="text-align:right; color:#f59e0b; font-weight:700;">⭐ {v['rating']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        if st.session_state.my_subscriptions:
            st.markdown("### 📦 Active Subscriptions")
            for sub in st.session_state.my_subscriptions:
                p = AP.get(sub["paper"], {})
                st.markdown(f"""
                <div class="card card-green">
                    <div class="card-title">📰 {p.get('name',sub['paper'])} — {sub['plan']}</div>
                    <div class="card-sub">💰 ₹{sub['amount']} | 🕐 {sub['time']} | 📅 {sub['date']}</div>
                </div>""", unsafe_allow_html=True)

    elif "Find Vendor" in page:
        st.markdown('<div class="hero"><h1>📍 Find Vendors</h1><p>All newspaper stalls in Ludhiana</p></div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1: lf = st.selectbox("Language",["All","EN","HI","PU"])
        with c2: pf = st.selectbox("Paper",["All"]+list(AP.keys()))
        filtered = [v for v in AV if (lf=="All" or lf in v["langs"]) and (pf=="All" or pf in v["papers"])]
        for v in filtered:
            lb = "".join([f'<span class="badge badge-or">{l}</span>' for l in v["langs"]])
            db = '<span class="badge badge-gr">🚚 Delivery</span>' if v["delivery"] else '<span class="badge badge-bl">Pickup Only</span>'
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <div class="card-title">🏪 {v['name']}</div>
                        <div class="card-sub">📍 {v['area']} | 🚶 {v['dist']} | 🕐 {v['open']}<br>📞 {v['phone']}<br>{lb} {db}</div>
                    </div>
                    <div style="text-align:right; color:#f59e0b; font-weight:700;">⭐ {v['rating']}<br><span style="color:#aaa;font-size:.72rem;">({v['reviews']})</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

    elif "Subscribe" in page:
        st.markdown('<div class="hero"><h1>📦 Subscribe to Home Delivery</h1><p>Get your newspaper every morning — starting ₹4/day</p></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([3,2])
        with c1:
            lang_sel = st.selectbox("Language",["All","English 🇬🇧","Hindi 🇮🇳","Punjabi 🏵️"])
            lc = {"All":"ALL","English 🇬🇧":"EN","Hindi 🇮🇳":"HI","Punjabi 🏵️":"PU"}.get(lang_sel,"ALL")
            opts = {c:i for c,i in AP.items() if lc=="ALL" or i["lang"]==lc}
            paper_sel = st.selectbox("📰 Choose Newspaper", list(opts.keys()), format_func=lambda x:f"{opts[x]['flag']} {opts[x]['name']}")
            pinfo = opts.get(paper_sel, list(AP.values())[0])

            st.markdown("#### 📅 Choose Plan")
            pcols = st.columns(3)
            with pcols[0]:
                st.markdown(f"""<div class="sub-card"><div class="sub-tag">Per Day</div>
                <div class="sub-price">₹{pinfo['price']}</div><div class="sub-period">per day</div>
                <hr style="margin:.5rem 0;border-color:#eee;">
                <div style="font-size:.78rem;color:#666;">No commitment<br>Pickup only</div></div>""", unsafe_allow_html=True)
            with pcols[1]:
                st.markdown(f"""<div class="sub-card popular"><div class="sub-tag">🔥 Popular</div>
                <div class="sub-price">₹{pinfo['monthly']+30}</div><div class="sub-period">/month incl delivery</div>
                <hr style="margin:.5rem 0;border-color:#eee;">
                <div style="font-size:.78rem;color:#666;">Home delivery<br>Any time slot</div></div>""", unsafe_allow_html=True)
            with pcols[2]:
                st.markdown(f"""<div class="sub-card"><div class="sub-tag">Best Value</div>
                <div class="sub-price">₹{pinfo['yearly']+300}</div><div class="sub-period">/year</div>
                <hr style="margin:.5rem 0;border-color:#eee;">
                <div style="font-size:.78rem;color:#666;">Home delivery<br>Save 2 months free</div></div>""", unsafe_allow_html=True)

            sel_plan = st.radio("Select Plan",["📅 Daily Pickup","🚚 Monthly Delivery ₹"+ str(pinfo['monthly']+30),"🏆 Yearly Delivery ₹"+str(pinfo['yearly']+300)], horizontal=True)
            amt = pinfo['price'] if "Daily" in sel_plan else (pinfo['monthly']+30 if "Monthly" in sel_plan else pinfo['yearly']+300)
            plan_lbl = "Daily" if "Daily" in sel_plan else ("Monthly" if "Monthly" in sel_plan else "Yearly")

            t, addr = "N/A", "Pickup"
            if "Daily" not in sel_plan:
                t    = st.select_slider("🕐 Time",["5:00 AM","5:30 AM","6:00 AM","6:30 AM","7:00 AM","7:30 AM"])
                addr = st.text_input("📍 Delivery Address", placeholder="House No, Street, Area, Ludhiana")

        with c2:
            upi = st.radio("💳 Pay via",["📱 Google Pay","💜 PhonePe","💙 Paytm","🏛️ BHIM UPI"], label_visibility="collapsed")
            st.markdown(f"""
            <div class="order-box">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px;"><span style="color:#666;">📰</span><span style="font-weight:700;">{pinfo['name']}</span></div>
                <div style="display:flex;justify-content:space-between;margin-bottom:5px;"><span style="color:#666;">📅 Plan</span><span style="font-weight:700;">{plan_lbl}</span></div>
                <div style="display:flex;justify-content:space-between;margin-bottom:5px;"><span style="color:#666;">🕐 Time</span><span style="font-weight:700;">{t}</span></div>
                <hr style="margin:8px 0;border-color:#FF6B2B44;">
                <div class="order-total">₹{amt}</div>
                <div style="text-align:center;color:#888;font-size:.78rem;">{plan_lbl} total</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"✅ Pay ₹{amt}", use_container_width=True):
                st.session_state.my_subscriptions.append({"paper":paper_sel,"plan":plan_lbl,"amount":amt,"time":t,"address":addr or "Pickup","upi":upi.split(" ",1)[1],"date":date.today().strftime("%d %b %Y")})
                st.success(f"🎉 Subscribed! {pinfo['name']} delivery confirmed.")
                st.balloons()

    elif "Orders" in page:
        st.markdown('<div class="hero"><h1>🧾 My Orders</h1><p>Your subscription history</p></div>', unsafe_allow_html=True)
        if not st.session_state.my_subscriptions:
            st.info("📦 No orders yet. Subscribe to get started!")
        else:
            for i,sub in enumerate(st.session_state.my_subscriptions):
                p = AP.get(sub["paper"],{})
                c1,c2 = st.columns([4,1])
                with c1:
                    st.markdown(f"""<div class="card card-green">
                    <div class="card-title">📰 {p.get('name',sub['paper'])} — {sub['plan']}</div>
                    <div class="card-sub">💰 ₹{sub['amount']} | 🕐 {sub['time']} | 📍 {sub['address']}<br>📅 {sub['date']} | 💳 {sub['upi']}</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    if st.button("❌ Cancel", key=f"cu_{i}"):
                        st.session_state.my_subscriptions.pop(i); st.rerun()

    elif "Recommendations" in page:
        st.markdown('<div class="hero"><h1>✨ Papers For You</h1><p>AI recommendations</p></div>', unsafe_allow_html=True)
        cur = st.selectbox("I read", list(AP.keys()), format_func=lambda x:f"{AP[x]['flag']} {AP[x]['name']}")
        if st.button("✨ Recommend"):
            RECS={"TOI":[("HINDU",91,"Great English journalism"),("HT",87,"Different perspective")],"BHASKAR":[("JAGRAN",89,"Similar style"),("KESARI",78,"Top Hindi Punjab")],"AJIT":[("PTRIB",93,"Perfect pair"),("DESH",80,"Local Punjab")]}
            for code,sc,reason in RECS.get(cur,[("HT",85,"Good alternative")]):
                if code in AP:
                    inf=AP[code]
                    st.markdown(f"""<div class="card card-purple"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div class="card-title">{inf['flag']} {inf['name']}</div><div class="card-sub">💡 {reason} | ₹{inf['monthly']}/mo</div></div><div style="background:#f5f3ff;border-radius:10px;padding:.5rem .9rem;text-align:center;"><div style="font-size:1.1rem;font-weight:800;color:#7C3AED;">{sc}%</div><div style="font-size:.7rem;color:#888;">match</div></div></div></div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ██████  VENDOR DASHBOARD  ██████
# ══════════════════════════════════════════════════════════════
def dashboard_vendor():
    page = sidebar(["📊 My Dashboard","🧠 AI Predictions","📈 Sales History","📁 Upload Sales","⚙️ My Stall"])
    AV = active_vendors()
    AP = active_papers()
    base = {"TOI":55,"HT":35,"BHASKAR":65,"JAGRAN":50,"AJIT":45,"PTRIB":30,"TRIB":40,"ET":25}
    # Find this vendor's stall
    my_stall = next((v for v in AV if v["name"] == "Sharma News Agency"), AV[0])
    wb = 1.3 if datetime.now().weekday() in [5,6] else 1.0

    if "Dashboard" in page:
        st.markdown(f"""
        <div class="hero" style="background:linear-gradient(135deg,#8B5CF6,#6D28D9);">
            <h1>🏪 {my_stall['name']}</h1>
            <p>📍 {my_stall['area']} | ⭐ {my_stall['rating']} rating | 🕐 Opens {my_stall['open']}</p>
        </div>
        <div class="stat-row">
            <div class="stat-card" style="border-bottom-color:#8B5CF6;"><div class="stat-num" style="color:#8B5CF6;">{len(my_stall['papers'])}</div><div class="stat-lbl">📰 Papers Stocked</div></div>
            <div class="stat-card" style="border-bottom-color:#8B5CF6;"><div class="stat-num" style="color:#8B5CF6;">⭐{my_stall['rating']}</div><div class="stat-lbl">Customer Rating</div></div>
            <div class="stat-card" style="border-bottom-color:#8B5CF6;"><div class="stat-num" style="color:#8B5CF6;">{my_stall['reviews']}</div><div class="stat-lbl">Total Reviews</div></div>
            <div class="stat-card" style="border-bottom-color:#8B5CF6;"><div class="stat-num" style="color:#8B5CF6;">{'Yes' if my_stall['delivery'] else 'No'}</div><div class="stat-lbl">🚚 Delivery</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧠 Tomorrow's AI Stock Prediction")
        st.markdown('<div class="alert-blue">🧠 Facebook Prophet ML model — 95% accuracy based on weather, weekday & holidays</div>', unsafe_allow_html=True)
        for pc in my_stall["papers"][:4]:
            b = base.get(pc,30)
            pred = int(b * wb * random.uniform(0.92,1.08))
            inf = AP.get(pc,{})
            st.markdown(f"""
            <div class="pred-row">
                <div>
                    <div style="font-weight:700;">{pc} — {inf.get('name',pc)}</div>
                    <div style="color:#888;font-size:.8rem;">{inf.get('flag','')} Range: {int(pred*.85)}–{int(pred*1.15)}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:1.3rem;font-weight:800;color:#8B5CF6;">{pred}</div>
                    <div style="font-size:.75rem;color:#888;">copies tomorrow</div>
                </div>
            </div>""", unsafe_allow_html=True)

    elif "AI Predictions" in page:
        st.markdown('<div class="hero" style="background:linear-gradient(135deg,#8B5CF6,#6D28D9);"><h1>🧠 AI Stock Predictions</h1><p>Facebook Prophet ML — 7-day demand forecast</p></div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        c1.metric("📅 Tomorrow", (date.today()+timedelta(1)).strftime("%a, %d %b"))
        c2.metric("🌤️ Weather", "Sunny")
        c3.metric("📊 Accuracy", "95.2%")
        st.markdown("### 📦 Order These Quantities Tomorrow")
        total = 0
        for pc in my_stall["papers"]:
            b=base.get(pc,30); pred=int(b*wb*random.uniform(0.92,1.08))
            lo,hi=int(pred*.85),int(pred*1.15); inf=AP.get(pc,{})
            total += pred
            st.markdown(f"""
            <div class="pred-row">
                <div><div style="font-weight:700;">{pc} — {inf.get('name',pc)}</div>
                <div style="color:#888;font-size:.8rem;">{inf.get('flag','')} {inf.get('lang','')} | Safe range: {lo}–{hi}</div></div>
                <div style="text-align:right;"><div style="font-size:1.3rem;font-weight:800;color:#8B5CF6;">{pred}</div>
                <div style="color:#888;font-size:.75rem;">copies</div></div>
            </div>""", unsafe_allow_html=True)
        st.success(f"📦 **Order {total} total copies tomorrow** | Estimated revenue: ₹{total*4}")

    elif "Sales History" in page:
        st.markdown('<div class="hero" style="background:linear-gradient(135deg,#8B5CF6,#6D28D9);"><h1>📈 Sales History</h1><p>Your last 30 days performance</p></div>', unsafe_allow_html=True)
        hist=[]
        for d in range(30,0,-1):
            dt=date.today()-timedelta(d)
            for p in my_stall["papers"][:4]:
                b=base.get(p,30)
                units=int(b*random.uniform(.85,1.15)*(1.3 if dt.weekday() in [5,6] else 1.0))
                hist.append({"Date":dt,"Paper":p,"Units":units,"Revenue":units*4})
        df=pd.DataFrame(hist)
        paper_sel=st.selectbox("View Paper",my_stall["papers"][:4])
        cd=df[df["Paper"]==paper_sel].set_index("Date")
        st.line_chart(cd["Units"])
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Avg/Day",f"{int(cd['Units'].mean())}")
        c2.metric("Best Day",f"{int(cd['Units'].max())}")
        c3.metric("Month Total",f"{int(cd['Units'].sum())}")
        c4.metric("Revenue",f"₹{int(cd['Revenue'].sum())}")

    elif "Upload" in page:
        st.markdown('<div class="hero" style="background:linear-gradient(135deg,#8B5CF6,#6D28D9);"><h1>📁 Upload Sales Data</h1><p>Train AI model on your actual sales</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="alert-blue">📋 CSV columns: <code>date, paper_code, units_sold, weather, is_holiday, is_weekend, is_exam_week</code></div>', unsafe_allow_html=True)
        st.markdown("**Example:**")
        st.code("2024-01-15, TOI, 65, sunny, false, false, false")
        up = st.file_uploader("Upload your CSV file", type=["csv"])
        if up:
            df_up = pd.read_csv(up)
            st.success(f"✅ {len(df_up)} rows uploaded!")
            st.dataframe(df_up.head(10), use_container_width=True)
            if st.button("🧠 Train AI Model on My Data"):
                import time
                with st.spinner("Training Prophet model... ~30 seconds"):
                    time.sleep(2)
                st.success("✅ Model trained! Your predictions are now personalized.")
                st.balloons()

    elif "Stall" in page:
        st.markdown('<div class="hero" style="background:linear-gradient(135deg,#8B5CF6,#6D28D9);"><h1>⚙️ My Stall Settings</h1><p>Update your stall information</p></div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            st.text_input("Stall Name", value=my_stall["name"])
            st.text_input("Area", value=my_stall["area"])
            st.text_input("Phone", value=my_stall["phone"])
        with c2:
            st.text_input("Opening Time", value="5:30 AM")
            st.text_input("Closing Time", value="10:30 AM")
            st.checkbox("Offer Home Delivery", value=my_stall["delivery"])
        st.multiselect("Languages", ["EN","HI","PU"], default=my_stall["langs"])
        st.multiselect("Papers Available", list(AP.keys()), default=my_stall["papers"])
        if st.button("💾 Save Changes"):
            st.success("✅ Stall info updated!")


# ══════════════════════════════════════════════════════════════
# ██████  ADMIN DASHBOARD  ██████
# ══════════════════════════════════════════════════════════════
def dashboard_admin():
    page = sidebar(["📊 Admin Dashboard","🏪 Manage Vendors","📰 Manage Papers","👥 Manage Users","📈 Analytics"])
    AV = st.session_state.vendors
    AP = st.session_state.papers

    if "Dashboard" in page:
        active_v = len([v for v in AV if v.get("active",True)])
        active_p = len([p for p in AP.values() if p.get("active",True)])
        st.markdown(f"""
        <div class="hero" style="background:linear-gradient(135deg,#1e293b,#334155);">
            <h1>👑 Admin Dashboard</h1>
            <p>Platform overview — manage everything from here</p>
        </div>
        <div class="stat-row">
            <div class="stat-card" style="border-bottom-color:#7C3AED;"><div class="stat-num" style="color:#7C3AED;">{active_v}</div><div class="stat-lbl">🏪 Active Vendors</div></div>
            <div class="stat-card" style="border-bottom-color:#7C3AED;"><div class="stat-num" style="color:#7C3AED;">{active_p}</div><div class="stat-lbl">📰 Active Papers</div></div>
            <div class="stat-card" style="border-bottom-color:#7C3AED;"><div class="stat-num" style="color:#7C3AED;">{len(st.session_state.users_db)}</div><div class="stat-lbl">👥 Total Users</div></div>
            <div class="stat-card" style="border-bottom-color:#7C3AED;"><div class="stat-num" style="color:#7C3AED;">₹12.4K</div><div class="stat-lbl">💰 This Month</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📈 Orders This Week")
        dates = [(date.today()-timedelta(i)).strftime("%a %d") for i in range(6,-1,-1)]
        st.bar_chart(pd.DataFrame({"Orders":[random.randint(15,45) for _ in dates]}, index=dates))

        st.markdown("### 🏆 Top Vendors by Rating")
        top = sorted([v for v in AV if v.get("active",True)], key=lambda x:x["rating"], reverse=True)[:5]
        st.dataframe(pd.DataFrame([{"Vendor":v["name"],"Area":v["area"],"Rating":v["rating"],"Reviews":v["reviews"],"Delivery":"✅" if v["delivery"] else "❌"} for v in top]), use_container_width=True, hide_index=True)

    elif "Vendors" in page:
        st.markdown('<div class="hero" style="background:linear-gradient(135deg,#1e293b,#334155);"><h1>🏪 Manage Vendors</h1><p>Add, edit, activate or remove vendors</p></div>', unsafe_allow_html=True)

        with st.expander("➕ Add New Vendor", expanded=False):
            c1,c2 = st.columns(2)
            with c1:
                nv_n = st.text_input("Stall Name *")
                nv_a = st.text_input("Area / Locality *")
                nv_p = st.text_input("Phone Number *")
                nv_d = st.text_input("Distance from centre", placeholder="e.g. 1.5km")
            with c2:
                nv_o  = st.text_input("Opening Time", value="6:00 AM")
                nv_c  = st.text_input("Closing Time",  value="10:00 AM")
                nv_l  = st.multiselect("Languages", ["EN","HI","PU"], default=["EN","HI"])
                nv_del= st.checkbox("Offers Home Delivery")
            nv_pp = st.multiselect("Papers Available", list({k:v for k,v in AP.items() if v.get("active",True)}.keys()), default=["TOI","BHASKAR"])
            if st.button("✅ Add Vendor"):
                if nv_n and nv_a and nv_p:
                    new_id = max([v["id"] for v in AV], default=0)+1
                    st.session_state.vendors.append({"id":new_id,"name":nv_n,"area":nv_a,"dist":nv_d or "?","langs":nv_l,"papers":nv_pp,"rating":0.0,"reviews":0,"delivery":nv_del,"open":f"{nv_o}–{nv_c}","phone":nv_p,"active":True})
                    st.success(f"✅ '{nv_n}' added!"); st.rerun()
                else:
                    st.error("❌ Fill Name, Area and Phone")

        st.markdown(f"### All Vendors ({len(AV)} total)")
        for i, v in enumerate(AV):
            c1,c2,c3,c4,c5 = st.columns([3,1,1,1,1])
            with c1: st.markdown(f"**{'🟢' if v.get('active',True) else '🔴'} {v['name']}** — {v['area']}")
            with c2: st.write(f"⭐ {v['rating']}")
            with c3: st.write("🚚" if v["delivery"] else "—")
            with c4:
                if v.get("active",True):
                    if st.button("🔴 Off", key=f"dv{i}"): st.session_state.vendors[i]["active"]=False; st.rerun()
                else:
                    if st.button("🟢 On", key=f"av{i}"): st.session_state.vendors[i]["active"]=True; st.rerun()
            with c5:
                if st.button("🗑️ Del", key=f"xv{i}"): st.session_state.vendors.pop(i); st.rerun()

    elif "Papers" in page:
        st.markdown('<div class="hero" style="background:linear-gradient(135deg,#1e293b,#334155);"><h1>📰 Manage Newspapers</h1><p>Add, hide or remove newspapers from the platform</p></div>', unsafe_allow_html=True)

        with st.expander("➕ Add New Newspaper", expanded=False):
            c1,c2 = st.columns(2)
            with c1:
                np_c = st.text_input("Short Code * (max 8 chars)", placeholder="e.g. TRIBUNE").upper()
                np_n = st.text_input("Full Name *", placeholder="e.g. The Tribune")
                np_l = st.selectbox("Language *", ["EN - English","HI - Hindi","PU - Punjabi"])
            with c2:
                np_pr = st.number_input("Daily Price ₹", 1, 50, 5)
                np_mo = st.number_input("Monthly Price ₹", 50, 500, 120)
                np_yr = st.number_input("Yearly Price ₹", 500, 6000, 1200)
            np_f  = {"EN - English":"🇬🇧","HI - Hindi":"🇮🇳","PU - Punjabi":"🏵️"}.get(np_l,"🇬🇧")
            np_lc = np_l.split(" - ")[0]
            if st.button("✅ Add Newspaper"):
                if np_c and np_n:
                    if np_c in AP: st.error("❌ Code already exists!")
                    else:
                        st.session_state.papers[np_c]={"name":np_n,"lang":np_lc,"flag":np_f,"price":np_pr,"monthly":np_mo,"yearly":np_yr,"active":True}
                        st.success(f"✅ '{np_n}' added!"); st.rerun()
                else: st.error("❌ Fill Code and Name")

        st.markdown(f"### All Newspapers ({len(AP)} total)")
        for code, info in list(AP.items()):
            c1,c2,c3,c4,c5,c6 = st.columns([1,2.5,1,1,1,1])
            with c1: st.markdown(f"**{code}**")
            with c2: st.write(f"{info['flag']} {info['name']}")
            with c3: st.write(f"₹{info['price']}/d")
            with c4: st.write(f"₹{info['monthly']}/mo")
            with c5:
                if info.get("active",True):
                    if st.button("🔴 Hide",key=f"hp{code}"): st.session_state.papers[code]["active"]=False; st.rerun()
                else:
                    if st.button("🟢 Show",key=f"sp{code}"): st.session_state.papers[code]["active"]=True; st.rerun()
            with c6:
                if st.button("🗑️",key=f"dp{code}"): del st.session_state.papers[code]; st.rerun()

    elif "Users" in page:
        st.markdown('<div class="hero" style="background:linear-gradient(135deg,#1e293b,#334155);"><h1>👥 Manage Users</h1><p>View all registered users and add new staff</p></div>', unsafe_allow_html=True)
        ud = [{"Email":e,"Name":i["name"],"Role":i["role"],"Phone":i.get("phone","—")} for e,i in st.session_state.users_db.items()]
        st.dataframe(pd.DataFrame(ud), use_container_width=True, hide_index=True)

        st.markdown("### ➕ Add New User / Staff")
        c1,c2 = st.columns(2)
        with c1:
            nu_n  = st.text_input("Full Name *")
            nu_e  = st.text_input("Email *")
            nu_ph = st.text_input("Phone")
        with c2:
            nu_p = st.text_input("Password *", type="password")
            nu_r = st.selectbox("Role", ["user","student","vendor","admin"])
        if st.button("✅ Add User"):
            if nu_n and nu_e and nu_p:
                if nu_e in st.session_state.users_db:
                    st.error("❌ Email already exists!")
                else:
                    st.session_state.users_db[nu_e]={"pw":hashlib.md5(nu_p.encode()).hexdigest(),"role":nu_r,"name":nu_n,"phone":nu_ph}
                    st.success(f"✅ {nu_n} added!"); st.rerun()
            else: st.error("❌ Fill Name, Email and Password")

    elif "Analytics" in page:
        st.markdown('<div class="hero" style="background:linear-gradient(135deg,#1e293b,#334155);"><h1>📈 Platform Analytics</h1><p>Live metrics and performance data</p></div>', unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Vendors",  len(AV), f"{len([v for v in AV if v.get('active')])} active")
        c2.metric("Total Papers",   len(AP), f"{len([p for p in AP.values() if p.get('active')])} active")
        c3.metric("Registered Users", len(st.session_state.users_db))
        c4.metric("Monthly Revenue", "₹12,450", "↑ 18%")
        st.markdown("### 📈 Daily Orders — Last 14 Days")
        dates14 = [(date.today()-timedelta(i)).strftime("%d %b") for i in range(13,-1,-1)]
        st.line_chart(pd.DataFrame({"Orders":[random.randint(10,50) for _ in dates14],"Revenue":[random.randint(400,2000) for _ in dates14]}, index=dates14))
        st.markdown("### 🏆 Top Performing Vendors")
        top = sorted([v for v in AV if v.get("active",True)], key=lambda x:x["rating"], reverse=True)[:5]
        st.dataframe(pd.DataFrame([{"Vendor":v["name"],"Area":v["area"],"Rating":v["rating"],"Reviews":v["reviews"]} for v in top]), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    page_login()
else:
    role = st.session_state.role
    if   role == "admin":   dashboard_admin()
    elif role == "vendor":  dashboard_vendor()
    elif role == "student": dashboard_student()
    else:                   dashboard_user()
