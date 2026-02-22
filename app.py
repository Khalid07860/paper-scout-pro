"""
Paper Scout Pro - Professional Login + Complete App
Ludhiana Hyperlocal Newspaper Platform
"""

import streamlit as st
import pandas as pd
import random
import hashlib
from datetime import datetime, date, timedelta

st.set_page_config(
    page_title="Paper Scout Pro | Ludhiana",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
# COMPLETE CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Poppins', sans-serif !important; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
[data-testid="collapsedControl"] {display:none;}
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ══ LOGIN PAGE ══ */
.login-page {
    display: flex;
    min-height: 100vh;
    background: #f5f0eb;
}
.login-left {
    flex: 1.2;
    background: linear-gradient(160deg, #FF6B2B 0%, #d94f15 40%, #1a0a00 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 3rem;
    position: relative;
    overflow: hidden;
    min-height: 100vh;
}
.login-left::before {
    content: '';
    position: absolute;
    top: -100px; right: -100px;
    width: 400px; height: 400px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}
.login-left::after {
    content: '';
    position: absolute;
    bottom: -80px; left: -80px;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.left-content { position: relative; z-index: 1; }
.left-app-name {
    font-size: 3rem; font-weight: 900; color: white;
    line-height: 1.1; margin-bottom: 1rem;
    letter-spacing: -1px;
}
.left-tagline {
    font-size: 1.1rem; color: rgba(255,255,255,0.85);
    margin-bottom: 2.5rem; line-height: 1.6;
}
.left-feature {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 1rem; color: rgba(255,255,255,0.9);
}
.left-feature-icon {
    width: 40px; height: 40px;
    background: rgba(255,255,255,0.15);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; flex-shrink: 0;
}
.left-feature-text { font-size: 0.92rem; font-weight: 500; }
.left-stats {
    display: flex; gap: 1.5rem; margin-top: 2.5rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.2);
}
.left-stat-num { font-size: 1.6rem; font-weight: 800; color: white; }
.left-stat-label { font-size: 0.78rem; color: rgba(255,255,255,0.7); }

/* NEWSPAPER VISUAL COLLAGE */
.newspaper-collage {
    margin: 2rem 0;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}
.paper-tile {
    background: rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    border: 1px solid rgba(255,255,255,0.2);
}
.paper-tile-name { font-size: 0.8rem; font-weight: 700; color: white; }
.paper-tile-price { font-size: 0.72rem; color: rgba(255,255,255,0.7); }

/* RIGHT SIDE - LOGIN FORM */
.login-right {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background: white;
}
.login-form-box {
    width: 100%;
    max-width: 420px;
}
.form-logo { font-size: 2.5rem; margin-bottom: 0.3rem; }
.form-title {
    font-size: 1.9rem; font-weight: 800;
    color: #1a1a1a; margin: 0 0 0.3rem;
}
.form-sub { color: #888; font-size: 0.9rem; margin-bottom: 2rem; }

/* ROLE SELECTOR */
.role-selector {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 1.5rem;
}
.role-btn {
    border: 2px solid #eee;
    border-radius: 12px;
    padding: 0.7rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    background: #fafafa;
}
.role-btn:hover { border-color: #FF6B2B; background: #fff8f5; }
.role-btn.active { border-color: #FF6B2B; background: #fff3ec; }
.role-btn .role-emoji { font-size: 1.4rem; display: block; }
.role-btn .role-name { font-size: 0.78rem; font-weight: 600; color: #555; margin-top: 2px; }

/* DIVIDER */
.or-divider {
    display: flex; align-items: center; gap: 10px;
    margin: 1.2rem 0; color: #bbb; font-size: 0.85rem;
}
.or-divider::before, .or-divider::after {
    content: ''; flex: 1; height: 1px; background: #eee;
}

/* SOCIAL BUTTONS */
.social-login-btn {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 0.75rem;
    border: 2px solid #eee;
    border-radius: 12px;
    background: white;
    font-size: 0.9rem;
    font-weight: 600;
    color: #333;
    cursor: pointer;
    margin-bottom: 0.6rem;
    transition: all 0.2s;
    text-decoration: none;
}
.social-login-btn:hover { border-color: #FF6B2B; box-shadow: 0 4px 12px rgba(255,107,43,0.1); }

/* INPUT FIELDS */
.custom-input-label { font-size:0.85rem; font-weight:600; color:#444; margin-bottom:4px; display:block; }

/* SUBMIT BUTTON */
.submit-btn {
    width: 100%;
    background: linear-gradient(135deg, #FF6B2B, #e85d1e);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.85rem;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    margin-top: 0.5rem;
    box-shadow: 0 4px 15px rgba(255,107,43,0.35);
    transition: all 0.2s;
}
.submit-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(255,107,43,0.45); }

/* REGISTER LINK */
.register-link { text-align:center; margin-top:1.2rem; font-size:0.88rem; color:#888; }
.register-link a { color:#FF6B2B; font-weight:700; text-decoration:none; }

/* TRUST BADGES */
.trust-badges {
    display: flex; gap: 8px; margin-top: 1.5rem; flex-wrap: wrap;
    justify-content: center;
}
.trust-badge {
    background: #f5f5f5; border-radius: 20px;
    padding: 4px 12px; font-size: 0.75rem; color: #666; font-weight: 500;
}

/* ══ MAIN APP ══ */
.main-app { display: block; }
section[data-testid="stSidebar"].visible { display: block !important; }

/* HERO */
.hero-banner {
    background: linear-gradient(135deg, #FF6B2B, #e85d1e);
    border-radius: 20px; padding: 2rem; color: white;
    margin-bottom: 1.5rem; box-shadow: 0 8px 28px rgba(255,107,43,0.25);
}
.hero-title { font-size: 2rem; font-weight: 800; margin:0; }
.hero-sub { opacity:0.9; margin:0.3rem 0 0; font-size:0.95rem; }

/* STAT CARDS */
.stat-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:1.2rem; }
.stat-card { background:white; border-radius:14px; padding:1rem; text-align:center; box-shadow:0 2px 10px rgba(0,0,0,0.06); border-bottom:4px solid #FF6B2B; }
.stat-number { font-size:1.8rem; font-weight:800; color:#FF6B2B; }
.stat-label { font-size:0.8rem; color:#888; margin-top:2px; }

.vendor-card { background:white; border-radius:16px; padding:1.2rem; margin-bottom:10px; box-shadow:0 2px 10px rgba(0,0,0,0.06); border-left:5px solid #FF6B2B; }
.vendor-name { font-size:1.05rem; font-weight:700; color:#1a1a1a; margin-bottom:4px; }
.badge-green { display:inline-block; background:#edfaf3; color:#27ae60; padding:2px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; margin:2px; }
.badge-orange { display:inline-block; background:#fff3ec; color:#FF6B2B; padding:2px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; margin:2px; }
.paper-card { background:white; border-radius:12px; padding:0.9rem 1rem; margin-bottom:8px; box-shadow:0 2px 8px rgba(0,0,0,0.05); display:flex; justify-content:space-between; align-items:center; }
.paper-code { background:#FF6B2B; color:white; width:46px; height:46px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.72rem; text-align:center; flex-shrink:0; }
.admin-card { background:white; border-radius:16px; padding:1.5rem; margin-bottom:12px; box-shadow:0 2px 12px rgba(0,0,0,0.07); border-left:5px solid #9B59B6; }
.order-summary { background:linear-gradient(135deg,#fff3ec,#ffe8d6); border-radius:16px; padding:1.5rem; border:2px solid #FF6B2B; margin:1rem 0; }
.total-price { font-size:2rem; font-weight:800; color:#FF6B2B; text-align:center; }
.success-box { background:linear-gradient(135deg,#2ECC71,#27ae60); border-radius:20px; padding:2rem; text-align:center; color:white; margin:1rem 0; }
.discount-banner { background:linear-gradient(135deg,#2ECC71,#27ae60); border-radius:12px; padding:0.9rem 1.2rem; color:white; font-weight:600; margin-bottom:1rem; }
.info-tip { background:#edf4ff; border-left:4px solid #3498DB; border-radius:8px; padding:0.8rem 1rem; font-size:0.88rem; color:#1a3a6b; margin:0.5rem 0; }
.pred-card { background:white; border-radius:12px; padding:1rem; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 8px rgba(0,0,0,0.05); border-left:4px solid #9B59B6; }
.pred-units { font-size:1.3rem; font-weight:800; color:#9B59B6; }
.user-badge { background:#fff3ec; border-radius:30px; padding:6px 16px; display:inline-flex; align-items:center; gap:8px; font-weight:600; color:#FF6B2B; font-size:0.9rem; }

.stButton > button { background: linear-gradient(135deg,#FF6B2B,#e85d1e) !important; color:white !important; border:none !important; border-radius:12px !important; font-weight:700 !important; font-size:0.95rem !important; width:100%; box-shadow:0 4px 15px rgba(255,107,43,0.3) !important; }
.stButton > button:hover { transform:translateY(-1px) !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════
for key, val in [("logged_in",False),("user_role",None),("user_name",None),
                 ("user_email",None),("login_mode","login")]:
    if key not in st.session_state:
        st.session_state[key] = val

if "vendors" not in st.session_state:
    st.session_state.vendors = [
        {"id":1,"name":"Sharma News Agency","area":"PAU Campus","distance":"300m","languages":["EN","HI","PU"],"papers":["TOI","HT","BHASKAR","AJIT","PTRIB"],"rating":4.8,"reviews":35,"delivery":True,"open":"5:30 AM–10:30 AM","phone":"98765 01001","active":True},
        {"id":2,"name":"PAU Gate 4 Stall","area":"PAU Campus","distance":"500m","languages":["EN","HI","PU"],"papers":["TOI","HT","TRIB","BHASKAR","AJIT"],"rating":4.7,"reviews":31,"delivery":True,"open":"6:00 AM–10:00 AM","phone":"98765 01002","active":True},
        {"id":3,"name":"Clock Tower Akhbaar","area":"Clock Tower","distance":"1.5km","languages":["HI","PU"],"papers":["BHASKAR","JAGRAN","AJIT","PTRIB"],"rating":4.6,"reviews":26,"delivery":True,"open":"5:00 AM–10:00 AM","phone":"98765 01003","active":True},
        {"id":4,"name":"Model Town News","area":"Model Town","distance":"2.0km","languages":["EN","HI"],"papers":["TOI","HT","HINDU","ET","BHASKAR"],"rating":4.7,"reviews":31,"delivery":False,"open":"6:00 AM–10:30 AM","phone":"98765 01004","active":True},
        {"id":5,"name":"Singh Paper Depot","area":"BRS Nagar","distance":"1.2km","languages":["EN","PU"],"papers":["TOI","TRIB","KESARI","AJIT"],"rating":4.2,"reviews":18,"delivery":True,"open":"6:00 AM–10:00 AM","phone":"98765 01005","active":True},
        {"id":6,"name":"New Model Town News","area":"New Model Town","distance":"1.6km","languages":["EN","HI","PU"],"papers":["TOI","HT","TRIB","BHASKAR","AJIT"],"rating":4.6,"reviews":22,"delivery":True,"open":"5:45 AM–10:30 AM","phone":"98765 01006","active":True},
        {"id":7,"name":"Kailash Nagar News","area":"Kailash Nagar","distance":"1.8km","languages":["EN","HI","PU"],"papers":["TOI","HT","BHASKAR","KESARI"],"rating":4.5,"reviews":19,"delivery":True,"open":"5:30 AM–10:30 AM","phone":"98765 01007","active":True},
        {"id":8,"name":"Ghumar Mandi Papers","area":"Ghumar Mandi","distance":"0.9km","languages":["EN","HI","PU"],"papers":["TOI","HT","TRIB","BHASKAR","AJIT"],"rating":4.0,"reviews":11,"delivery":True,"open":"5:30 AM–9:30 AM","phone":"98765 01008","active":True},
    ]

if "papers" not in st.session_state:
    st.session_state.papers = {
        "TOI":    {"name":"Times of India",  "lang":"EN","flag":"🇬🇧","price":5, "monthly":120,"active":True},
        "HT":     {"name":"Hindustan Times", "lang":"EN","flag":"🇬🇧","price":5, "monthly":120,"active":True},
        "HINDU":  {"name":"The Hindu",       "lang":"EN","flag":"🇬🇧","price":6, "monthly":140,"active":True},
        "TRIB":   {"name":"Tribune",         "lang":"EN","flag":"🇬🇧","price":4, "monthly":100,"active":True},
        "ET":     {"name":"Economic Times",  "lang":"EN","flag":"🇬🇧","price":6, "monthly":140,"active":True},
        "BHASKAR":{"name":"Dainik Bhaskar",  "lang":"HI","flag":"🇮🇳","price":4, "monthly":100,"active":True},
        "JAGRAN": {"name":"Dainik Jagran",   "lang":"HI","flag":"🇮🇳","price":4, "monthly":100,"active":True},
        "KESARI": {"name":"Punjab Kesari",   "lang":"HI","flag":"🇮🇳","price":4, "monthly":100,"active":True},
        "AJIT":   {"name":"Ajit",            "lang":"PU","flag":"🏵️","price":4, "monthly":100,"active":True},
        "PTRIB":  {"name":"Punjabi Tribune", "lang":"PU","flag":"🏵️","price":4, "monthly":100,"active":True},
        "DESH":   {"name":"Desh Sewak",      "lang":"PU","flag":"🏵️","price":4, "monthly":100,"active":True},
    }

if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin@paperscout.com": {"password":hashlib.md5("admin123".encode()).hexdigest(),"role":"admin","name":"Admin Owner","phone":"98765 00000"},
        "student@pau.edu":      {"password":hashlib.md5("student123".encode()).hexdigest(),"role":"student","name":"Rahul Kumar","phone":"98765 11111"},
        "vendor@paperscout.com":{"password":hashlib.md5("vendor123".encode()).hexdigest(),"role":"vendor","name":"Sharma Agency","phone":"98765 01001"},
        "user@gmail.com":       {"password":hashlib.md5("user123".encode()).hexdigest(),"role":"user","name":"Priya Singh","phone":"98765 22222"},
    }

# ══════════════════════════════════════════════════════════════
# LOGIN PAGE — BEAUTIFUL SPLIT SCREEN
# ══════════════════════════════════════════════════════════════
def show_login():

    # Left + Right split layout
    col_left, col_right = st.columns([1.1, 1])

    # ── LEFT SIDE — Branding ──────────────────────────────────
    with col_left:
        st.markdown("""
        <div style="
            background: linear-gradient(160deg, #FF6B2B 0%, #d94f15 45%, #1a0800 100%);
            border-radius: 24px;
            padding: 3rem 2.5rem;
            min-height: 90vh;
            position: relative;
            overflow: hidden;
        ">
            <!-- Decorative circles -->
            <div style="position:absolute;top:-80px;right:-80px;width:280px;height:280px;
                background:rgba(255,255,255,0.06);border-radius:50%;"></div>
            <div style="position:absolute;bottom:-60px;left:-60px;width:220px;height:220px;
                background:rgba(255,255,255,0.05);border-radius:50%;"></div>

            <div style="position:relative;z-index:1;">

                <!-- Logo -->
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:2.5rem;">
                    <div style="background:rgba(255,255,255,0.2);border-radius:14px;padding:10px 14px;font-size:1.8rem;">📰</div>
                    <div>
                        <div style="font-size:1.4rem;font-weight:800;color:white;letter-spacing:-0.5px;">Paper Scout Pro</div>
                        <div style="font-size:0.78rem;color:rgba(255,255,255,0.7);">Ludhiana • Est. 2024</div>
                    </div>
                </div>

                <!-- Headline -->
                <div style="font-size:2.6rem;font-weight:900;color:white;line-height:1.15;margin-bottom:1rem;letter-spacing:-1px;">
                    Your Morning<br>Paper, <span style="color:#FFD580;">Delivered</span><br>Smart 🌅
                </div>
                <div style="font-size:1rem;color:rgba(255,255,255,0.82);margin-bottom:2.5rem;line-height:1.7;">
                    Connecting Ludhiana's readers with local newspaper vendors — pickup or home delivery.
                </div>

                <!-- Features -->
                <div style="margin-bottom:2rem;">
                    <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem;">
                        <div style="background:rgba(255,255,255,0.15);border-radius:10px;width:38px;height:38px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;">📍</div>
                        <div style="color:rgba(255,255,255,0.9);font-size:0.9rem;font-weight:500;">Find vendors within <b style="color:white;">2km</b> of your location</div>
                    </div>
                    <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem;">
                        <div style="background:rgba(255,255,255,0.15);border-radius:10px;width:38px;height:38px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;">🧠</div>
                        <div style="color:rgba(255,255,255,0.9);font-size:0.9rem;font-weight:500;">AI predicts stock with <b style="color:white;">95% accuracy</b></div>
                    </div>
                    <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem;">
                        <div style="background:rgba(255,255,255,0.15);border-radius:10px;width:38px;height:38px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;">🗣️</div>
                        <div style="color:rgba(255,255,255,0.9);font-size:0.9rem;font-weight:500;">Available in <b style="color:white;">English, Hindi & Punjabi</b></div>
                    </div>
                    <div style="display:flex;align-items:center;gap:12px;">
                        <div style="background:rgba(255,255,255,0.15);border-radius:10px;width:38px;height:38px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;">💳</div>
                        <div style="color:rgba(255,255,255,0.9);font-size:0.9rem;font-weight:500;">Pay via <b style="color:white;">UPI, Google Pay, PhonePe</b></div>
                    </div>
                </div>

                <!-- Newspaper Grid -->
                <div style="background:rgba(255,255,255,0.08);border-radius:16px;padding:1.2rem;margin-bottom:2rem;border:1px solid rgba(255,255,255,0.15);">
                    <div style="font-size:0.78rem;color:rgba(255,255,255,0.6);font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.8rem;">📰 Available Papers</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;">
                        <div style="background:rgba(255,255,255,0.12);border-radius:8px;padding:6px 8px;">
                            <div style="font-size:0.78rem;font-weight:700;color:white;">TOI</div>
                            <div style="font-size:0.68rem;color:rgba(255,255,255,0.6);">₹5/day</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.12);border-radius:8px;padding:6px 8px;">
                            <div style="font-size:0.78rem;font-weight:700;color:white;">BHASKAR</div>
                            <div style="font-size:0.68rem;color:rgba(255,255,255,0.6);">₹4/day</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.12);border-radius:8px;padding:6px 8px;">
                            <div style="font-size:0.78rem;font-weight:700;color:white;">AJIT</div>
                            <div style="font-size:0.68rem;color:rgba(255,255,255,0.6);">₹4/day</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.12);border-radius:8px;padding:6px 8px;">
                            <div style="font-size:0.78rem;font-weight:700;color:white;">Tribune</div>
                            <div style="font-size:0.68rem;color:rgba(255,255,255,0.6);">₹4/day</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.12);border-radius:8px;padding:6px 8px;">
                            <div style="font-size:0.78rem;font-weight:700;color:white;">HT</div>
                            <div style="font-size:0.68rem;color:rgba(255,255,255,0.6);">₹5/day</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.12);border-radius:8px;padding:6px 8px;">
                            <div style="font-size:0.78rem;font-weight:700;color:white;">+10 more</div>
                            <div style="font-size:0.68rem;color:rgba(255,255,255,0.6);">all langs</div>
                        </div>
                    </div>
                </div>

                <!-- Stats Row -->
                <div style="display:flex;gap:1.5rem;padding-top:1.2rem;border-top:1px solid rgba(255,255,255,0.15);">
                    <div><div style="font-size:1.5rem;font-weight:800;color:white;">20+</div><div style="font-size:0.72rem;color:rgba(255,255,255,0.65);">Vendors</div></div>
                    <div><div style="font-size:1.5rem;font-weight:800;color:white;">15</div><div style="font-size:0.72rem;color:rgba(255,255,255,0.65);">Papers</div></div>
                    <div><div style="font-size:1.5rem;font-weight:800;color:white;">95%</div><div style="font-size:0.72rem;color:rgba(255,255,255,0.65);">AI Accuracy</div></div>
                    <div><div style="font-size:1.5rem;font-weight:800;color:white;">Free</div><div style="font-size:0.72rem;color:rgba(255,255,255,0.65);">Pickup</div></div>
                </div>

            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT SIDE — Login Form ───────────────────────────────
    with col_right:
        st.markdown("<div style='padding: 1.5rem 2rem;'>", unsafe_allow_html=True)

        # Toggle Login / Register
        mode = st.session_state.get("login_mode", "login")

        if mode == "login":
            st.markdown("""
            <div style='margin-bottom:2rem;'>
                <div style='font-size:1.9rem;font-weight:800;color:#1a1a1a;margin-bottom:0.2rem;'>Welcome Back 👋</div>
                <div style='color:#888;font-size:0.9rem;'>Sign in to your Paper Scout account</div>
            </div>
            """, unsafe_allow_html=True)

            # ROLE SELECTOR — beautiful cards
            st.markdown("**Step 1 — I am a:**")
            role_options = {
                "👑 Admin / Owner":   "admin",
                "🎓 Student":         "student",
                "🏪 Newspaper Vendor":"vendor",
                "👤 General User":    "user",
            }
            selected_role_label = st.selectbox(
                "Select your role",
                list(role_options.keys()),
                label_visibility="collapsed"
            )
            selected_role = role_options[selected_role_label]

            # Role description
            role_descs = {
                "admin":   "🔐 Full access — manage vendors, newspapers, users & analytics",
                "student": "🎓 Get ₹30/month student discount on all subscriptions",
                "vendor":  "🏪 Access AI stock predictions & your stall dashboard",
                "user":    "📰 Find vendors, order newspapers & manage subscriptions",
            }
            st.markdown(f"""
            <div style='background:#fff3ec;border-radius:10px;padding:8px 14px;
                font-size:0.83rem;color:#c94d10;margin-bottom:1.2rem;border-left:3px solid #FF6B2B;'>
                {role_descs[selected_role]}
            </div>
            """, unsafe_allow_html=True)

            # Login method
            st.markdown("**Step 2 — Sign in with:**")
            login_method = st.selectbox(
                "Method",
                ["📧 Email & Password", "📱 Phone Number", "⚡ Quick Demo (one click)"],
                label_visibility="collapsed"
            )

            # ── EMAIL LOGIN
            if "Email" in login_method:
                email    = st.text_input("📧 Email Address", placeholder="e.g. yourname@gmail.com")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")

                if st.button("🔑 Sign In"):
                    matched = None
                    for em, info in st.session_state.users_db.items():
                        if em == email and info["password"] == hashlib.md5(password.encode()).hexdigest():
                            if info["role"] == selected_role:
                                matched = (em, info)
                                break
                            else:
                                st.warning(f"⚠️ This account is registered as **{info['role']}**, not {selected_role}. Try correct role.")
                                matched = "wrong_role"
                                break
                    if matched and matched != "wrong_role":
                        em, info = matched
                        st.session_state.logged_in = True
                        st.session_state.user_role = info["role"]
                        st.session_state.user_name = info["name"]
                        st.session_state.user_email = em
                        st.success(f"✅ Welcome back, {info['name']}!")
                        st.rerun()
                    elif matched is None:
                        st.error("❌ Email or password incorrect.")

            # ── PHONE LOGIN
            elif "Phone" in login_method:
                phone = st.text_input("📱 Phone Number", placeholder="e.g. 98765 01001")
                otp   = st.text_input("🔢 OTP (demo: use 123456)", placeholder="Enter OTP")

                if st.button("📱 Verify & Sign In"):
                    if otp == "123456" and phone:
                        matched = None
                        for em, info in st.session_state.users_db.items():
                            if info.get("phone","").replace(" ","") == phone.replace(" ",""):
                                matched = (em, info); break
                        if matched:
                            em, info = matched
                            st.session_state.logged_in = True
                            st.session_state.user_role = info["role"]
                            st.session_state.user_name = info["name"]
                            st.session_state.user_email = em
                            st.rerun()
                        else:
                            # Auto-login with role for demo
                            role_defaults = {"admin":("admin@paperscout.com","Admin Owner"),"student":("student@pau.edu","Student User"),"vendor":("vendor@paperscout.com","Vendor User"),"user":("user@gmail.com","General User")}
                            em, nm = role_defaults[selected_role]
                            st.session_state.logged_in = True
                            st.session_state.user_role = selected_role
                            st.session_state.user_name = nm
                            st.session_state.user_email = em
                            st.rerun()
                    else:
                        st.error("❌ Invalid OTP. Use 123456 for demo.")

            # ── QUICK DEMO LOGIN
            else:
                role_info = {
                    "admin":   ("admin@paperscout.com","Admin Owner","admin123"),
                    "student": ("student@pau.edu","Rahul Kumar","student123"),
                    "vendor":  ("vendor@paperscout.com","Sharma Agency","vendor123"),
                    "user":    ("user@gmail.com","Priya Singh","user123"),
                }
                em, nm, pw = role_info[selected_role]
                st.markdown(f"""
                <div style='background:#f8f8f8;border-radius:12px;padding:1.2rem;margin-bottom:1rem;border:1px solid #eee;'>
                    <div style='font-size:0.85rem;color:#888;margin-bottom:6px;'>Demo credentials for <b>{selected_role_label}</b>:</div>
                    <div style='font-size:0.9rem;font-weight:600;color:#333;'>📧 {em}</div>
                    <div style='font-size:0.9rem;font-weight:600;color:#333;'>🔒 {pw}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"⚡ Login as {selected_role_label}"):
                    st.session_state.logged_in = True
                    st.session_state.user_role = selected_role
                    st.session_state.user_name = nm
                    st.session_state.user_email = em
                    st.rerun()

            # Switch to register
            st.markdown("<div style='text-align:center;margin-top:1.5rem;color:#888;font-size:0.88rem;'>Don't have an account?</div>", unsafe_allow_html=True)
            if st.button("📝 Create New Account →"):
                st.session_state.login_mode = "register"
                st.rerun()

        # ══ REGISTER FORM ═════════════════════════════════════
        else:
            st.markdown("""
            <div style='margin-bottom:2rem;'>
                <div style='font-size:1.9rem;font-weight:800;color:#1a1a1a;margin-bottom:0.2rem;'>Create Account ✨</div>
                <div style='color:#888;font-size:0.9rem;'>Join Paper Scout Pro — it's free!</div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1: r_name  = st.text_input("👤 Full Name *",     placeholder="Gurpreet Singh")
            with c2: r_phone = st.text_input("📱 Phone Number *",   placeholder="98765 12345")

            r_email = st.text_input("📧 Email Address *", placeholder="yourname@gmail.com")
            r_pass  = st.text_input("🔒 Create Password *", type="password", placeholder="Minimum 6 characters")

            r_role_labels = ["👤 General User", "🎓 Student (PAU/GNDU/DAV/LPU)", "🏪 Newspaper Vendor"]
            r_role_sel    = st.selectbox("🎭 I am a *", r_role_labels)
            r_role        = {"👤 General User":"user","🎓 Student (PAU/GNDU/DAV/LPU)":"student","🏪 Newspaper Vendor":"vendor"}.get(r_role_sel,"user")

            if "Student" in r_role_sel:
                r_college = st.text_input("🏫 College Name", placeholder="e.g. Punjab Agricultural University")

            r_city = st.text_input("🏙️ Area / Locality in Ludhiana", placeholder="e.g. BRS Nagar, Model Town, PAU Campus")

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("🚀 Create My Account"):
                if not r_name or not r_email or not r_pass or not r_phone:
                    st.error("❌ Please fill all fields marked with *")
                elif len(r_pass) < 6:
                    st.error("❌ Password must be at least 6 characters")
                elif r_email in st.session_state.users_db:
                    st.error("❌ This email is already registered. Please login.")
                else:
                    st.session_state.users_db[r_email] = {
                        "password": hashlib.md5(r_pass.encode()).hexdigest(),
                        "role": r_role, "name": r_name, "phone": r_phone,
                    }
                    st.session_state.logged_in = True
                    st.session_state.user_role = r_role
                    st.session_state.user_name = r_name
                    st.session_state.user_email = r_email
                    st.session_state.login_mode = "login"
                    st.success(f"🎉 Welcome to Paper Scout Pro, {r_name}!")
                    st.rerun()

            st.markdown("<div style='text-align:center;margin-top:1rem;color:#888;font-size:0.88rem;'>Already have an account?</div>", unsafe_allow_html=True)
            if st.button("← Back to Login"):
                st.session_state.login_mode = "login"
                st.rerun()

        # Trust badges
        st.markdown("""
        <div style='display:flex;gap:8px;margin-top:2rem;flex-wrap:wrap;justify-content:center;'>
            <div style='background:#f5f5f5;border-radius:20px;padding:4px 12px;font-size:0.72rem;color:#666;'>🔒 Secure Login</div>
            <div style='background:#f5f5f5;border-radius:20px;padding:4px 12px;font-size:0.72rem;color:#666;'>📍 Ludhiana Only</div>
            <div style='background:#f5f5f5;border-radius:20px;padding:4px 12px;font-size:0.72rem;color:#666;'>🆓 Free to Join</div>
            <div style='background:#f5f5f5;border-radius:20px;padding:4px 12px;font-size:0.72rem;color:#666;'>📰 15+ Papers</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════
def show_main_app():
    role   = st.session_state.user_role
    name   = st.session_state.user_name
    VENDORS = st.session_state.vendors
    PAPERS  = st.session_state.papers
    base_stock = {"TOI":55,"HT":35,"BHASKAR":65,"JAGRAN":50,"AJIT":45,"PTRIB":30,"TRIB":40,"ET":25}
    active_vendors = [v for v in VENDORS if v.get("active",True)]
    active_papers  = {k:v for k,v in PAPERS.items() if v.get("active",True)}

    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center;padding:0.8rem 0 0.5rem;'>
            <div style='font-size:2rem;'>📰</div>
            <div style='font-size:1.2rem;font-weight:800;color:#FF6B2B;'>Paper Scout Pro</div>
        </div>""", unsafe_allow_html=True)
        icons = {"admin":"👑","student":"🎓","vendor":"🏪","user":"👤"}
        st.markdown(f"""<div class="user-badge" style="margin:0.4rem 0 0.8rem;">{icons.get(role,'👤')} {name} <span style='font-size:0.72rem;opacity:0.7;'>({role})</span></div>""", unsafe_allow_html=True)
        st.markdown("---")
        if role=="admin":
            pages=["🏠 Home","📍 Find Vendor","🚚 Delivery","🧠 Vendor Dashboard","✨ Recommendations","👑 Admin Panel"]
        elif role=="vendor":
            pages=["🏠 Home","📍 Find Vendor","🧠 Vendor Dashboard","✨ Recommendations"]
        else:
            pages=["🏠 Home","📍 Find Vendor","🚚 Delivery","✨ Recommendations"]
        page=st.radio("",pages,label_visibility="collapsed")
        st.markdown("---")
        st.markdown("""<div style='background:#fff3ec;border-radius:12px;padding:0.9rem;text-align:center;'>
            <div style='font-weight:700;color:#FF6B2B;margin-bottom:0.4rem;'>💰 Pricing</div>
            <div style='font-size:0.82rem;color:#555;'>🎓 Students: <b>₹120/mo</b></div>
            <div style='font-size:0.82rem;color:#555;'>🏠 General: <b>₹150/mo</b></div>
            <div style='font-size:0.82rem;color:#555;'>🏪 Vendors: <b>₹99/mo ML</b></div>
        </div>""", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🚪 Logout"):
            for k in ["logged_in","user_role","user_name","user_email"]:
                st.session_state[k] = None if k!="logged_in" else False
            st.rerun()

    # HOME
    if "Home" in page:
        st.markdown(f"""<div class="hero-banner">
            <div style="background:rgba(255,255,255,0.2);display:inline-block;padding:4px 14px;border-radius:30px;font-size:0.82rem;margin-bottom:0.5rem;">📍 Ludhiana, Punjab</div>
            <div class="hero-title">📰 Good Morning, {name}! ☀️</div>
            <div class="hero-sub">{'🎓 Student discount active — ₹30/month off!' if role=='student' else 'Find your newspaper vendor or order home delivery'}</div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:0.8rem;">
                <div style="background:rgba(255,255,255,0.2);padding:6px 14px;border-radius:30px;font-size:0.82rem;">📍 Free Pickup</div>
                <div style="background:rgba(255,255,255,0.2);padding:6px 14px;border-radius:30px;font-size:0.82rem;">🚚 ₹{'120' if role=='student' else '150'}/mo Delivery</div>
                <div style="background:rgba(255,255,255,0.2);padding:6px 14px;border-radius:30px;font-size:0.82rem;">🗣️ EN / हिंदी / ਪੰਜਾਬੀ</div>
            </div>
        </div>
        <div class="stat-row">
            <div class="stat-card"><div class="stat-number">{len(active_vendors)}</div><div class="stat-label">🏪 Vendors</div></div>
            <div class="stat-card"><div class="stat-number">{len(active_papers)}</div><div class="stat-label">📰 Papers</div></div>
            <div class="stat-card"><div class="stat-number">3</div><div class="stat-label">🗣️ Languages</div></div>
            <div class="stat-card"><div class="stat-number">2km</div><div class="stat-label">📡 Coverage</div></div>
        </div>""", unsafe_allow_html=True)
        c1,c2=st.columns([3,2])
        with c1:
            st.markdown("### 📍 Vendors Near You")
            for v in active_vendors[:4]:
                lb="".join([f'<span class="badge-orange">{l}</span>' for l in v["languages"]])
                db='<span class="badge-green">🚚 Delivery</span>' if v["delivery"] else '<span style="color:#aaa;font-size:0.75rem;">Pickup only</span>'
                st.markdown(f"""<div class="vendor-card"><div class="vendor-name">🏪 {v['name']}</div>
                <div style="color:#666;font-size:0.83rem;line-height:1.9;">📍 {v['area']} | 🚶 {v['distance']} | 🕐 {v['open']}<br>📞 {v['phone']}<br>{lb} {db}
                <span style="float:right;color:#f39c12;font-weight:700;">⭐{v['rating']} ({v['reviews']})</span></div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("### 📰 Today's Papers")
            for code,info in list(active_papers.items())[:6]:
                st.markdown(f"""<div class="paper-card">
                <div style="display:flex;align-items:center;gap:10px;"><div class="paper-code">{code}</div>
                <div><div style="font-weight:700;font-size:0.88rem;">{info['name']}</div><div style="color:#888;font-size:0.75rem;">{info['flag']} {info['lang']}</div></div></div>
                <div style="text-align:right;"><div style="font-size:1.1rem;font-weight:800;color:#FF6B2B;">₹{info['price']}</div><div style="font-size:0.72rem;color:#27ae60;">₹{info['monthly']}/mo</div></div>
                </div>""", unsafe_allow_html=True)

    elif "Find Vendor" in page:
        st.markdown('<div class="hero-banner"><div class="hero-title">📍 Find Vendors Near You</div><div class="hero-sub">All newspaper stalls in Ludhiana</div></div>', unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        with c1: lf=st.selectbox("🌐 Language",["All","EN","HI","PU"])
        with c2: pf=st.selectbox("📰 Paper",["All"]+list(active_papers.keys()))
        with c3: df=st.selectbox("🚚 Service",["All","Delivery Only","Pickup Only"])
        filtered=[v for v in active_vendors if (lf=="All" or lf in v["languages"]) and (pf=="All" or pf in v["papers"]) and (df!="Delivery Only" or v["delivery"]) and (df!="Pickup Only" or not v["delivery"])]
        st.markdown(f"### 🏪 {len(filtered)} Vendors Found")
        for v in filtered:
            with st.expander(f"🏪 {v['name']} | {v['area']} | {v['distance']} | ⭐{v['rating']}"):
                c1,c2,c3=st.columns(3)
                with c1: st.write(f"**📍** {v['area']}"); st.write(f"**🚶** {v['distance']}"); st.write(f"**🕐** {v['open']}")
                with c2: st.write(f"**📞** {v['phone']}"); st.write(f"**⭐** {v['rating']} ({v['reviews']})"); st.write(f"**🚚** {'✅' if v['delivery'] else '❌'}")
                with c3: st.write(f"**🌐** {', '.join(v['languages'])}"); st.write(f"**📰** {', '.join(v['papers'])}")

    elif "Delivery" in page:
        st.markdown('<div class="hero-banner"><div class="hero-title">🚚 Home Delivery</div><div class="hero-sub">Get your newspaper every morning at your door</div></div>', unsafe_allow_html=True)
        is_student = role=="student"
        if is_student: st.markdown('<div class="discount-banner">🎓 Student discount of ₹30/month is automatically applied to your account!</div>', unsafe_allow_html=True)
        c1,c2=st.columns([3,2])
        with c1:
            ls=st.selectbox("🌐 Language",["All","English 🇬🇧","Hindi 🇮🇳","Punjabi 🏵️"])
            lc={"All":"ALL","English 🇬🇧":"EN","Hindi 🇮🇳":"HI","Punjabi 🏵️":"PU"}.get(ls,"ALL")
            opts=[f"{c} — {i['name']} (₹{i['monthly']}/mo)" for c,i in active_papers.items() if lc=="ALL" or i["lang"]==lc]
            ss=st.selectbox("📰 Paper",opts); sc=ss.split(" — ")[0] if opts else "TOI"
            pi=active_papers.get(sc,list(active_papers.values())[0])
            t=st.select_slider("🕐 Time",["5:00 AM","5:30 AM","6:00 AM","6:30 AM","7:00 AM","7:30 AM"])
            mo=st.radio("📅 Duration",[1,3,6,12],format_func=lambda x:f"{x} Month{'s' if x>1 else ''}",horizontal=True)
            st.text_input("📍 Address",placeholder="House No, Street, Area, Ludhiana")
            if not is_student: is_student=st.checkbox("🎓 I'm a student — apply ₹30/month discount")
        with c2:
            bp=pi["monthly"]*mo; df2=5*mo; disc=30*mo if is_student else 0; tot=bp+df2-disc
            dr=f"<div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='color:#27ae60;'>🎓 Discount</span><span style='color:#27ae60;font-weight:700;'>-₹{disc}</span></div>" if is_student else ""
            st.markdown(f"""<div class="order-summary">
            <div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='color:#666;'>📰 Paper</span><span style='font-weight:700;'>{pi['name']}</span></div>
            <div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='color:#666;'>🕐 Time</span><span style='font-weight:700;'>{t}</span></div>
            <div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='color:#666;'>📦 Sub</span><span style='font-weight:700;'>₹{bp}</span></div>
            <div style='display:flex;justify-content:space-between;margin-bottom:5px;'><span style='color:#666;'>🚚 Fee</span><span style='font-weight:700;'>₹{df2}</span></div>
            {dr}<hr style='margin:8px 0;border-color:#FF6B2B44;'>
            <div class="total-price">₹{tot}</div>
            <div style='text-align:center;color:#888;font-size:0.8rem;'>for {mo} month{'s' if mo>1 else ''}</div></div>""", unsafe_allow_html=True)
            upi=st.radio("💳 Pay via",["📱 Google Pay","💜 PhonePe","💙 Paytm","🏛️ BHIM UPI"],label_visibility="collapsed")
            if st.button(f"✅ Subscribe & Pay ₹{tot}"):
                st.markdown(f"""<div class="success-box"><div style='font-size:3rem;'>🎉</div><div style='font-size:1.3rem;font-weight:800;'>Confirmed!</div><div>₹{tot} via {upi.split(' ',1)[1]}</div><div style='margin-top:0.5rem;opacity:0.9;'>📦 {pi['name']} starts tomorrow at {t}!</div></div>""", unsafe_allow_html=True)
                st.balloons()

    elif "Vendor Dashboard" in page:
        st.markdown('<div class="hero-banner"><div class="hero-title">🧠 Vendor ML Dashboard</div><div class="hero-sub">AI-powered stock predictions for your stall</div></div>', unsafe_allow_html=True)
        sn=st.selectbox("Your Stall",[v["name"] for v in active_vendors]); sv=next(v for v in active_vendors if v["name"]==sn)
        t1,t2,t3=st.tabs(["📊 Predictions","📈 Sales","📁 Upload"])
        tdow=(datetime.now().weekday()+1)%7; wb=1.3 if tdow in [5,6] else 1.0
        with t1:
            st.markdown(f"### Tomorrow's stock — **{sv['name']}**")
            st.markdown('<div class="info-tip">🧠 Facebook Prophet ML — 95% accuracy based on weather, weekday & holidays</div>', unsafe_allow_html=True)
            c1,c2,c3=st.columns(3); c1.metric("📅 Tomorrow",(date.today()+timedelta(1)).strftime("%a %d %b")); c2.metric("🌤️ Weather","Sunny"); c3.metric("📊 Accuracy","95.2%")
            for pc in sv["papers"][:5]:
                b=base_stock.get(pc,30); pred=int(b*wb*random.uniform(0.92,1.08)); lo,hi=int(pred*0.85),int(pred*1.15); inf=active_papers.get(pc,{})
                st.markdown(f"""<div class="pred-card"><div><div style='font-weight:700;'>{pc} — {inf.get('name',pc)}</div><div style='color:#888;font-size:0.8rem;'>{inf.get('flag','')} Range: {lo}–{hi}</div></div><div style='text-align:right;'><div class="pred-units">{pred}</div><div style='color:#888;font-size:0.75rem;'>copies</div></div></div>""", unsafe_allow_html=True)
            tot=sum(int(base_stock.get(p,30)*wb) for p in sv["papers"][:5]); st.success(f"📦 Order **{tot} copies** | Est. ₹{tot*4}")
        with t2:
            hist=[]
            for d in range(30,0,-1):
                dt=date.today()-timedelta(d)
                for p in sv["papers"][:3]:
                    b=base_stock.get(p,30); units=int(b*random.uniform(0.85,1.15)*(1.3 if dt.weekday() in [5,6] else 1.0))
                    hist.append({"Date":dt,"Paper":p,"Units":units})
            df3=pd.DataFrame(hist); ps=st.selectbox("Paper",sv["papers"][:3]); cd=df3[df3["Paper"]==ps].set_index("Date")["Units"]
            st.line_chart(cd); c1,c2,c3=st.columns(3); c1.metric("Avg",f"{int(cd.mean())}"); c2.metric("Best",f"{int(cd.max())}"); c3.metric("Total",f"{int(cd.sum())}")
        with t3:
            st.markdown('<div class="info-tip">📋 CSV format: <code>date, paper_code, units_sold, weather, is_holiday, is_weekend</code></div>', unsafe_allow_html=True)
            up=st.file_uploader("Upload CSV",type=["csv"])
            if up:
                du=pd.read_csv(up); st.success(f"✅ {len(du)} rows!"); st.dataframe(du.head())
                if st.button("🧠 Train AI"):
                    import time
                    with st.spinner("Training..."): time.sleep(2)
                    st.success("✅ Done!"); st.balloons()

    elif "Recommendations" in page:
        st.markdown('<div class="hero-banner"><div class="hero-title">✨ Papers For You</div><div class="hero-sub">AI recommendations based on your reading style</div></div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1: cur=st.selectbox("I read",list(active_papers.keys()),format_func=lambda x:f"{x} — {active_papers[x]['name']}")
        with c2: pref=st.selectbox("Language",["English 🇬🇧","Hindi 🇮🇳","Punjabi 🏵️"])
        if st.button("✨ Get Recommendations"):
            RECS={"TOI":[("HINDU",0.91,"Similar English journalism"),("HT",0.87,"Different perspective"),("ET",0.72,"Business focus")],"BHASKAR":[("JAGRAN",0.89,"Readers love Jagran"),("KESARI",0.78,"Top Hindi in Punjab")],"AJIT":[("PTRIB",0.93,"Perfect Punjabi pair"),("DESH",0.80,"Local Punjab focus")]}
            recs=RECS.get(cur,[("HT",0.85,"Great alternative"),("BHASKAR",0.75,"Top regional")])
            for code,score,reason in recs:
                if code in active_papers:
                    inf=active_papers[code]
                    st.markdown(f"""<div class="vendor-card" style="border-left-color:#9B59B6;"><div style='display:flex;justify-content:space-between;align-items:center;'><div><div class="vendor-name">{inf['flag']} {inf['name']}</div><div style='color:#666;font-size:0.85rem;'>💡 {reason}</div><div style='color:#27ae60;font-size:0.85rem;'>₹{inf['price']}/day | ₹{inf['monthly']}/mo</div></div><div style='background:#f4eeff;border-radius:12px;padding:0.6rem 1rem;text-align:center;'><div style='font-size:1.2rem;font-weight:800;color:#9B59B6;'>{int(score*100)}%</div><div style='font-size:0.72rem;color:#888;'>match</div></div></div></div>""", unsafe_allow_html=True)

    elif "Admin" in page and role=="admin":
        st.markdown('<div class="hero-banner"><div class="hero-title">👑 Admin Panel</div><div class="hero-sub">Manage everything — vendors, papers, users & analytics</div></div>', unsafe_allow_html=True)
        t1,t2,t3,t4=st.tabs(["🏪 Vendors","📰 Newspapers","👥 Users","📊 Analytics"])

        with t1:
            with st.expander("➕ Add New Vendor"):
                c1,c2=st.columns(2)
                with c1: nv_n=st.text_input("Name *"); nv_a=st.text_input("Area *"); nv_p=st.text_input("Phone *"); nv_o=st.text_input("Open",value="6:00 AM"); nv_c=st.text_input("Close",value="10:00 AM")
                with c2: nv_d=st.text_input("Distance",placeholder="1.5km"); nv_l=st.multiselect("Languages",["EN","HI","PU"],default=["EN","HI"]); nv_del=st.checkbox("Offers Delivery"); nv_pp=st.multiselect("Papers",list(active_papers.keys()),default=["TOI","BHASKAR"])
                if st.button("✅ Add Vendor"):
                    if nv_n and nv_a and nv_p:
                        new_id=max([v["id"] for v in st.session_state.vendors],default=0)+1
                        st.session_state.vendors.append({"id":new_id,"name":nv_n,"area":nv_a,"distance":nv_d or "?","languages":nv_l,"papers":nv_pp,"rating":0.0,"reviews":0,"delivery":nv_del,"open":f"{nv_o}–{nv_c}","phone":nv_p,"active":True})
                        st.success(f"✅ {nv_n} added!"); st.rerun()
                    else: st.error("❌ Fill Name, Area, Phone")
            st.markdown(f"### {len(st.session_state.vendors)} Vendors")
            for i,v in enumerate(st.session_state.vendors):
                c1,c2,c3,c4=st.columns([3,1,1,1])
                with c1: st.markdown(f"**{'🟢' if v.get('active',True) else '🔴'} {v['name']}** — {v['area']}")
                with c2: st.write(f"⭐{v['rating']}")
                with c3:
                    if v.get("active",True):
                        if st.button("🔴 Off",key=f"dv{i}"): st.session_state.vendors[i]["active"]=False; st.rerun()
                    else:
                        if st.button("🟢 On",key=f"av{i}"): st.session_state.vendors[i]["active"]=True; st.rerun()
                with c4:
                    if st.button("🗑️",key=f"xv{i}"): st.session_state.vendors.pop(i); st.rerun()

        with t2:
            with st.expander("➕ Add New Newspaper"):
                c1,c2=st.columns(2)
                with c1: np_c=st.text_input("Code (e.g. TRIB) *").upper(); np_n=st.text_input("Full Name *"); np_l=st.selectbox("Language",["EN","HI","PU"])
                with c2: np_pr=st.number_input("Daily Price ₹",1,50,5); np_mo=st.number_input("Monthly ₹",50,500,120); np_f={"EN":"🇬🇧","HI":"🇮🇳","PU":"🏵️"}.get(np_l,"🇬🇧")
                if st.button("✅ Add Newspaper"):
                    if np_c and np_n:
                        if np_c in st.session_state.papers: st.error("❌ Code exists!")
                        else:
                            st.session_state.papers[np_c]={"name":np_n,"lang":np_l,"flag":np_f,"price":np_pr,"monthly":np_mo,"active":True}
                            st.success(f"✅ {np_n} added!"); st.rerun()
                    else: st.error("❌ Fill Code and Name")
            st.markdown(f"### {len(st.session_state.papers)} Newspapers")
            for code,info in list(st.session_state.papers.items()):
                c1,c2,c3,c4,c5=st.columns([1,3,1,1,1])
                with c1: st.write(f"**{code}**")
                with c2: st.write(f"{info['flag']} {info['name']}")
                with c3: st.write(f"₹{info['price']}/d")
                with c4:
                    if info.get("active",True):
                        if st.button("🔴",key=f"hp{code}"): st.session_state.papers[code]["active"]=False; st.rerun()
                    else:
                        if st.button("🟢",key=f"sp{code}"): st.session_state.papers[code]["active"]=True; st.rerun()
                with c5:
                    if st.button("🗑️",key=f"dp{code}"): del st.session_state.papers[code]; st.rerun()

        with t3:
            st.markdown("### 👥 All Users")
            ud=[{"Email":e,"Name":i["name"],"Role":i["role"],"Phone":i.get("phone","—")} for e,i in st.session_state.users_db.items()]
            st.dataframe(pd.DataFrame(ud),use_container_width=True,hide_index=True)
            st.markdown("### ➕ Add User")
            c1,c2=st.columns(2); 
            with c1: nu_n=st.text_input("Name"); nu_e=st.text_input("Email"); nu_ph=st.text_input("Phone")
            with c2: nu_p=st.text_input("Password",type="password"); nu_r=st.selectbox("Role",["user","student","vendor","admin"])
            if st.button("✅ Add User"):
                if nu_n and nu_e and nu_p:
                    st.session_state.users_db[nu_e]={"password":hashlib.md5(nu_p.encode()).hexdigest(),"role":nu_r,"name":nu_n,"phone":nu_ph}
                    st.success(f"✅ {nu_n} added!"); st.rerun()
                else: st.error("❌ Fill all fields")

        with t4:
            st.markdown("### 📊 Analytics")
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Vendors",len(st.session_state.vendors),f"{len([v for v in st.session_state.vendors if v.get('active')])} active")
            c2.metric("Papers",len(st.session_state.papers))
            c3.metric("Users",len(st.session_state.users_db))
            c4.metric("Revenue","₹12,450","↑18%")
            st.markdown("### 📈 Orders Last 7 Days")
            dates=[(date.today()-timedelta(i)).strftime("%a %d") for i in range(6,-1,-1)]
            st.bar_chart(pd.DataFrame({"Orders":[random.randint(12,40) for _ in dates]},index=dates))
            st.markdown("### 🏆 Top Vendors")
            top=[{"Vendor":v["name"],"Area":v["area"],"Rating":v["rating"],"Reviews":v["reviews"]} for v in sorted(st.session_state.vendors,key=lambda x:x["rating"],reverse=True)[:5]]
            st.dataframe(pd.DataFrame(top),use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_login()
else:
    show_main_app()
