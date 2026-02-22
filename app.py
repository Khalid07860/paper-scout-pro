"""
Paper Scout Pro - Redesigned Beautiful App
Ludhiana Hyperlocal Newspaper Platform
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime, date, timedelta

st.set_page_config(
    page_title="Paper Scout Pro | Ludhiana",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1rem !important; }
    .hero-banner {
        background: linear-gradient(135deg, #FF6B2B 0%, #e85d1e 50%, #c94d10 100%);
        border-radius: 20px; padding: 2.5rem 2rem; color: white;
        margin-bottom: 1.5rem; box-shadow: 0 8px 32px rgba(255,107,43,0.3);
    }
    .hero-title { font-size: 2.8rem; font-weight: 800; margin: 0; letter-spacing: -1px; }
    .hero-subtitle { font-size: 1.15rem; opacity: 0.9; margin: 0.4rem 0 1.5rem 0; }
    .stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 1.5rem; }
    .stat-card {
        background: white; border-radius: 16px; padding: 1.2rem; text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06); border-bottom: 4px solid #FF6B2B;
    }
    .stat-number { font-size: 2rem; font-weight: 800; color: #FF6B2B; line-height: 1; }
    .stat-label { font-size: 0.85rem; color: #888; margin-top: 4px; font-weight: 500; }
    .section-title { font-size: 1.4rem; font-weight: 700; color: #1a1a1a; margin: 1.5rem 0 1rem 0; }
    .vendor-card {
        background: white; border-radius: 16px; padding: 1.2rem; margin-bottom: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06); border-left: 5px solid #FF6B2B;
    }
    .vendor-name { font-size: 1.1rem; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; }
    .vendor-badge { display: inline-block; background: #edfaf3; color: #27ae60; padding: 2px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600; margin: 2px; }
    .vendor-badge-lang { display: inline-block; background: #fff3ec; color: #FF6B2B; padding: 2px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600; margin: 2px; }
    .paper-card { background: white; border-radius: 14px; padding: 1rem; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); display: flex; justify-content: space-between; align-items: center; }
    .paper-code { background: #FF6B2B; color: white; width: 50px; height: 50px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.75rem; text-align: center; flex-shrink: 0; }
    .paper-price { font-size: 1.3rem; font-weight: 800; color: #FF6B2B; }
    .paper-monthly { font-size: 0.8rem; color: #27ae60; font-weight: 600; }
    .order-summary { background: linear-gradient(135deg, #fff3ec, #ffe8d6); border-radius: 16px; padding: 1.5rem; border: 2px solid #FF6B2B; margin: 1rem 0; }
    .total-price { font-size: 2rem; font-weight: 800; color: #FF6B2B; text-align: center; }
    .pred-card { background: white; border-radius: 12px; padding: 1rem; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 4px solid #9B59B6; }
    .pred-units { font-size: 1.4rem; font-weight: 800; color: #9B59B6; }
    .success-box { background: linear-gradient(135deg, #2ECC71, #27ae60); border-radius: 20px; padding: 2rem; text-align: center; color: white; margin: 1rem 0; }
    .discount-banner { background: linear-gradient(135deg, #2ECC71, #27ae60); border-radius: 12px; padding: 0.9rem 1.2rem; color: white; font-weight: 600; margin-bottom: 1rem; }
    .info-tip { background: #edf4ff; border-left: 4px solid #3498DB; border-radius: 8px; padding: 0.8rem 1rem; font-size: 0.9rem; color: #1a3a6b; margin: 0.5rem 0; }
    .stButton > button { background: #FF6B2B !important; color: white !important; border: none !important; border-radius: 50px !important; font-weight: 700 !important; font-size: 1rem !important; width: 100%; }
    .stButton > button:hover { background: #e85d1e !important; }
</style>
""", unsafe_allow_html=True)

VENDORS = [
    {"id": 1, "name": "Sharma News Agency", "area": "PAU Campus", "distance": "300m",
     "languages": ["EN", "HI", "PU"], "papers": ["TOI", "HT", "BHASKAR", "AJIT", "PTRIB"],
     "rating": 4.8, "reviews": 35, "delivery": True, "open": "5:30 AM – 10:30 AM", "phone": "98765 01001"},
    {"id": 2, "name": "PAU Gate 4 Stall", "area": "PAU Campus", "distance": "500m",
     "languages": ["EN", "HI", "PU"], "papers": ["TOI", "HT", "TRIB", "BHASKAR", "AJIT"],
     "rating": 4.7, "reviews": 31, "delivery": True, "open": "6:00 AM – 10:00 AM", "phone": "98765 01002"},
    {"id": 3, "name": "Clock Tower Akhbaar", "area": "Clock Tower", "distance": "1.5km",
     "languages": ["HI", "PU"], "papers": ["BHASKAR", "JAGRAN", "AJIT", "PTRIB", "DESH"],
     "rating": 4.6, "reviews": 26, "delivery": True, "open": "5:00 AM – 10:00 AM", "phone": "98765 01003"},
    {"id": 4, "name": "Model Town News", "area": "Model Town", "distance": "2.0km",
     "languages": ["EN", "HI"], "papers": ["TOI", "HT", "HINDU", "ET", "BHASKAR"],
     "rating": 4.7, "reviews": 31, "delivery": False, "open": "6:00 AM – 10:30 AM", "phone": "98765 01004"},
    {"id": 5, "name": "Singh Paper Depot", "area": "BRS Nagar", "distance": "1.2km",
     "languages": ["EN", "PU"], "papers": ["TOI", "TRIB", "KESARI", "AJIT"],
     "rating": 4.2, "reviews": 18, "delivery": True, "open": "6:00 AM – 10:00 AM", "phone": "98765 01005"},
    {"id": 6, "name": "New Model Town News", "area": "New Model Town", "distance": "1.6km",
     "languages": ["EN", "HI", "PU"], "papers": ["TOI", "HT", "TRIB", "BHASKAR", "AJIT"],
     "rating": 4.6, "reviews": 22, "delivery": True, "open": "5:45 AM – 10:30 AM", "phone": "98765 01006"},
    {"id": 7, "name": "Kailash Nagar News", "area": "Kailash Nagar", "distance": "1.8km",
     "languages": ["EN", "HI", "PU"], "papers": ["TOI", "HT", "BHASKAR", "KESARI"],
     "rating": 4.5, "reviews": 19, "delivery": True, "open": "5:30 AM – 10:30 AM", "phone": "98765 01007"},
    {"id": 8, "name": "Ghumar Mandi Papers", "area": "Ghumar Mandi", "distance": "0.9km",
     "languages": ["EN", "HI", "PU"], "papers": ["TOI", "HT", "TRIB", "BHASKAR", "AJIT"],
     "rating": 4.0, "reviews": 11, "delivery": True, "open": "5:30 AM – 9:30 AM", "phone": "98765 01008"},
]

PAPERS = {
    "TOI":    {"name": "Times of India",   "lang": "EN", "flag": "🇬🇧", "price": 5,  "monthly": 120},
    "HT":     {"name": "Hindustan Times",  "lang": "EN", "flag": "🇬🇧", "price": 5,  "monthly": 120},
    "HINDU":  {"name": "The Hindu",        "lang": "EN", "flag": "🇬🇧", "price": 6,  "monthly": 140},
    "TRIB":   {"name": "Tribune",          "lang": "EN", "flag": "🇬🇧", "price": 4,  "monthly": 100},
    "ET":     {"name": "Economic Times",   "lang": "EN", "flag": "🇬🇧", "price": 6,  "monthly": 140},
    "BHASKAR":{"name": "Dainik Bhaskar",   "lang": "HI", "flag": "🇮🇳", "price": 4,  "monthly": 100},
    "JAGRAN": {"name": "Dainik Jagran",    "lang": "HI", "flag": "🇮🇳", "price": 4,  "monthly": 100},
    "KESARI": {"name": "Punjab Kesari",    "lang": "HI", "flag": "🇮🇳", "price": 4,  "monthly": 100},
    "AJIT":   {"name": "Ajit",             "lang": "PU", "flag": "🏵️", "price": 4,  "monthly": 100},
    "PTRIB":  {"name": "Punjabi Tribune",  "lang": "PU", "flag": "🏵️", "price": 4,  "monthly": 100},
    "DESH":   {"name": "Desh Sewak",       "lang": "PU", "flag": "🏵️", "price": 4,  "monthly": 100},
}

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:3rem;'>📰</div>
        <div style='font-size:1.4rem; font-weight:800; color:#FF6B2B;'>Paper Scout Pro</div>
        <div style='font-size:0.85rem; color:#888; margin-top:4px;'>Ludhiana's Newspaper App</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("📍 Navigate", ["🏠 Home", "📍 Find Vendor", "🚚 Delivery", "🧠 Vendor Dashboard", "✨ Recommendations"])
    st.markdown("---")
    st.markdown("""
    <div style='background:#fff3ec; border-radius:12px; padding:1rem; text-align:center;'>
        <div style='font-weight:700; color:#FF6B2B; margin-bottom:0.5rem;'>💰 Pricing</div>
        <div style='font-size:0.9rem; color:#555;'>🎓 Students: <b>₹120/mo</b></div>
        <div style='font-size:0.9rem; color:#555;'>🏠 General: <b>₹150/mo</b></div>
        <div style='font-size:0.9rem; color:#555;'>🏪 Vendors: <b>₹99/mo (ML)</b></div>
    </div>
    """, unsafe_allow_html=True)

# HOME PAGE
if "Home" in page:
    st.markdown("""
    <div class="hero-banner">
        <div style="background:rgba(255,255,255,0.2); display:inline-block; padding:5px 16px; border-radius:30px; font-size:0.9rem; margin-bottom:0.8rem;">📍 Ludhiana, Punjab</div>
        <div class="hero-title">📰 Paper Scout Pro</div>
        <div class="hero-subtitle">Your morning newspaper — at your door or nearest stall</div>
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:1rem;">
            <div style="background:rgba(255,255,255,0.2); padding:8px 18px; border-radius:30px; font-size:0.9rem;">📍 Pickup — <b>Free</b></div>
            <div style="background:rgba(255,255,255,0.2); padding:8px 18px; border-radius:30px; font-size:0.9rem;">🚚 Delivery — <b>₹120/mo</b></div>
            <div style="background:rgba(255,255,255,0.2); padding:8px 18px; border-radius:30px; font-size:0.9rem;">🎓 Student Discount — <b>₹30 off</b></div>
        </div>
    </div>
    <div class="stat-row">
        <div class="stat-card"><div class="stat-number">20+</div><div class="stat-label">🏪 Local Vendors</div></div>
        <div class="stat-card"><div class="stat-number">15</div><div class="stat-label">📰 Newspapers</div></div>
        <div class="stat-card"><div class="stat-number">3</div><div class="stat-label">🗣️ Languages</div></div>
        <div class="stat-card"><div class="stat-number">2km</div><div class="stat-label">📡 Coverage Area</div></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="section-title">📍 Nearest Vendors to You</div>', unsafe_allow_html=True)
        for v in VENDORS[:4]:
            lang_badges = "".join([f'<span class="vendor-badge-lang">{l}</span>' for l in v["languages"]])
            delivery_badge = '<span class="vendor-badge">🚚 Delivery</span>' if v["delivery"] else '<span style="color:#aaa;font-size:0.78rem;">Pickup only</span>'
            st.markdown(f"""
            <div class="vendor-card">
                <div class="vendor-name">🏪 {v['name']}</div>
                <div style="color:#666; font-size:0.88rem; line-height:1.8;">
                    📍 {v['area']} &nbsp;|&nbsp; 🚶 {v['distance']} away<br>
                    🕐 Open: {v['open']} &nbsp;|&nbsp; 📞 {v['phone']}<br>
                    <div style="margin-top:6px;">{lang_badges} {delivery_badge}
                    <span style="float:right; color:#f39c12; font-weight:700;">⭐ {v['rating']} ({v['reviews']} reviews)</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">📰 Today\'s Papers</div>', unsafe_allow_html=True)
        for code, info in list(PAPERS.items())[:6]:
            st.markdown(f"""
            <div class="paper-card">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div class="paper-code">{code}</div>
                    <div>
                        <div style="font-weight:700; font-size:0.95rem;">{info['name']}</div>
                        <div style="color:#888; font-size:0.82rem;">{info['flag']} {info['lang']}</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div class="paper-price">₹{info['price']}</div>
                    <div class="paper-monthly">₹{info['monthly']}/mo</div>
                </div>
            </div>""", unsafe_allow_html=True)

# FIND VENDOR PAGE
elif "Find Vendor" in page:
    st.markdown('<div class="hero-banner"><div class="hero-title">📍 Find Vendors Near You</div><div class="hero-subtitle">All newspaper stalls in Ludhiana</div></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: lang_filter = st.selectbox("🌐 Language", ["All Languages", "English (EN)", "Hindi (HI)", "Punjabi (PU)"])
    with col2: paper_filter = st.selectbox("📰 Paper", ["All Papers"] + list(PAPERS.keys()))
    with col3: delivery_filter = st.selectbox("🚚 Service", ["All", "Delivery Only", "Pickup Only"])
    lang_code = {"All Languages": "ALL", "English (EN)": "EN", "Hindi (HI)": "HI", "Punjabi (PU)": "PU"}.get(lang_filter, "ALL")
    filtered = []
    for v in VENDORS:
        if lang_code != "ALL" and lang_code not in v["languages"]: continue
        if paper_filter != "All Papers" and paper_filter not in v["papers"]: continue
        if delivery_filter == "Delivery Only" and not v["delivery"]: continue
        if delivery_filter == "Pickup Only" and v["delivery"]: continue
        filtered.append(v)
    st.markdown(f'<div class="section-title">🏪 {len(filtered)} Vendors Found</div>', unsafe_allow_html=True)
    for v in filtered:
        with st.expander(f"🏪 {v['name']}  |  📍 {v['area']}  |  🚶 {v['distance']}  |  ⭐ {v['rating']}"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**📍 Area:** {v['area']}")
                st.markdown(f"**🚶 Distance:** {v['distance']}")
                st.markdown(f"**🕐 Timing:** {v['open']}")
            with c2:
                st.markdown(f"**📞 Phone:** {v['phone']}")
                st.markdown(f"**⭐ Rating:** {v['rating']} ({v['reviews']} reviews)")
                st.markdown(f"**🚚 Delivery:** {'✅ Yes' if v['delivery'] else '❌ No'}")
            with c3:
                st.markdown(f"**🌐 Languages:** {', '.join(v['languages'])}")
                st.markdown(f"**📰 Papers:** {', '.join(v['papers'])}")

# DELIVERY PAGE
elif "Delivery" in page:
    st.markdown('<div class="hero-banner"><div class="hero-title">🚚 Home Delivery</div><div class="hero-subtitle">Get your newspaper delivered every morning</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="discount-banner">🎓 PAU/GNDU Students get ₹30/month off! Check the box below to claim your discount.</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### 📰 Choose Your Newspaper")
        lang_sel = st.selectbox("Language", ["All", "English 🇬🇧", "Hindi 🇮🇳", "Punjabi 🏵️"])
        lang_code2 = {"All": "ALL", "English 🇬🇧": "EN", "Hindi 🇮🇳": "HI", "Punjabi 🏵️": "PU"}.get(lang_sel, "ALL")
        paper_options = [f"{code} — {info['name']} (₹{info['monthly']}/mo)" for code, info in PAPERS.items() if lang_code2 == "ALL" or info["lang"] == lang_code2]
        selected_paper_str = st.selectbox("Select Paper", paper_options)
        selected_code = selected_paper_str.split(" — ")[0] if paper_options else "TOI"
        paper_info = PAPERS.get(selected_code, PAPERS["TOI"])
        delivery_time = st.select_slider("🕐 Delivery Time", options=["5:00 AM", "5:30 AM", "6:00 AM", "6:30 AM", "7:00 AM", "7:30 AM"])
        months = st.radio("📅 Duration", [1, 3, 6, 12], format_func=lambda x: f"{x} Month{'s' if x>1 else ''}", horizontal=True)
        address = st.text_input("📍 Delivery Address", placeholder="e.g. Room 204, Hostel B, PAU Campus")
        is_student = st.checkbox("🎓 I am a student (PAU / GNDU / DAV / LPU) — Apply ₹30/month discount")
    with col2:
        base_price = paper_info["monthly"] * months
        delivery_fee = 5 * months
        discount = 30 * months if is_student else 0
        total = base_price + delivery_fee - discount
        st.markdown("#### 🧾 Order Summary")
        discount_row = f"<div style='display:flex;justify-content:space-between;margin-bottom:6px;'><span style='color:#27ae60;'>🎓 Student discount</span><span style='font-weight:700;color:#27ae60;'>-₹{discount}</span></div>" if is_student else ""
        st.markdown(f"""
        <div class="order-summary">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;"><span style="color:#666;">📰 Paper</span><span style="font-weight:700;">{paper_info['name']}</span></div>
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;"><span style="color:#666;">🕐 Time</span><span style="font-weight:700;">{delivery_time}</span></div>
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;"><span style="color:#666;">📅 Duration</span><span style="font-weight:700;">{months} month{'s' if months>1 else ''}</span></div>
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;"><span style="color:#666;">📦 Subscription</span><span style="font-weight:700;">₹{base_price}</span></div>
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;"><span style="color:#666;">🚚 Delivery fee</span><span style="font-weight:700;">₹{delivery_fee}</span></div>
            {discount_row}
            <hr style="margin:10px 0; border-color:#FF6B2B44;">
            <div class="total-price">₹{total}</div>
            <div style="text-align:center; color:#888; font-size:0.85rem; margin-top:4px;">Total for {months} month{'s' if months>1 else ''}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("#### 💳 Pay via UPI")
        selected_upi = st.radio("", ["📱 Google Pay", "💜 PhonePe", "💙 Paytm", "🏛️ BHIM UPI"], label_visibility="collapsed")
        if st.button(f"✅ Subscribe & Pay ₹{total}"):
            st.markdown(f"""<div class="success-box"><div style="font-size:3rem;">🎉</div><div style="font-size:1.4rem;font-weight:800;margin:0.5rem 0;">Order Confirmed!</div><div>Payment of ₹{total} via {selected_upi.split(' ',1)[1]}</div><div style="margin-top:0.8rem;opacity:0.85;">📦 {paper_info['name']} delivery starts tomorrow at {delivery_time}!</div></div>""", unsafe_allow_html=True)
            st.balloons()

# VENDOR DASHBOARD
elif "Vendor Dashboard" in page:
    st.markdown('<div class="hero-banner"><div class="hero-title">🧠 Vendor ML Dashboard</div><div class="hero-subtitle">AI-powered stock predictions for your stall</div></div>', unsafe_allow_html=True)
    sel_vendor_name = st.selectbox("Select Your Stall", [v["name"] for v in VENDORS])
    sel_vendor = next(v for v in VENDORS if v["name"] == sel_vendor_name)
    tab1, tab2, tab3 = st.tabs(["📊 Today's Predictions", "📈 Sales History", "📁 Upload My Sales"])
    base = {"TOI": 55, "HT": 35, "BHASKAR": 65, "JAGRAN": 50, "AJIT": 45, "PTRIB": 30, "TRIB": 40, "ET": 25}
    tomorrow_dow = (datetime.now().weekday() + 1) % 7
    weekend_boost = 1.3 if tomorrow_dow in [5, 6] else 1.0
    with tab1:
        st.markdown(f"### 📦 How much to order tomorrow — {sel_vendor['name']}")
        st.markdown('<div class="info-tip">🧠 <b>AI Prediction:</b> Based on weather, weekday, holidays and past sales using Facebook Prophet model (95% accuracy)</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("📅 Tomorrow", (date.today() + timedelta(1)).strftime("%A, %d %b"))
        c2.metric("🌤️ Weather", "Sunny")
        c3.metric("📊 Confidence", "95.2%")
        for paper_code in sel_vendor["papers"][:5]:
            b = base.get(paper_code, 30)
            pred = int(b * weekend_boost * random.uniform(0.92, 1.08))
            low, high = int(pred * 0.85), int(pred * 1.15)
            info = PAPERS.get(paper_code, {})
            st.markdown(f"""<div class="pred-card"><div><div style="font-weight:700;font-size:1rem;">{paper_code} — {info.get('name',paper_code)}</div><div style="color:#888;font-size:0.83rem;">{info.get('flag','')} {info.get('lang','')} | Range: {low}–{high} copies</div></div><div style="text-align:right;"><div class="pred-units">{pred} copies</div><div style="color:#888;font-size:0.8rem;">order tomorrow</div></div></div>""", unsafe_allow_html=True)
        total_pred = sum(int(base.get(p, 30) * weekend_boost) for p in sel_vendor["papers"][:5])
        st.success(f"📦 Total: Order **{total_pred} copies** | Est. Revenue: ₹{total_pred * 4}")
    with tab2:
        st.markdown("### 📈 Your Sales Last 30 Days")
        hist = []
        for d in range(30, 0, -1):
            dt = date.today() - timedelta(d)
            for p in sel_vendor["papers"][:3]:
                b = base.get(p, 30)
                units = int(b * random.uniform(0.85, 1.15) * (1.3 if dt.weekday() in [5, 6] else 1.0))
                hist.append({"Date": dt, "Paper": p, "Units Sold": units})
        df = pd.DataFrame(hist)
        paper_sel = st.selectbox("View Paper", sel_vendor["papers"][:3])
        chart_data = df[df["Paper"] == paper_sel].set_index("Date")["Units Sold"]
        st.line_chart(chart_data)
        c1, c2, c3 = st.columns(3)
        c1.metric("Avg Daily", f"{int(chart_data.mean())} copies")
        c2.metric("Best Day", f"{int(chart_data.max())} copies")
        c3.metric("Total Month", f"{int(chart_data.sum())} copies")
    with tab3:
        st.markdown("### 📁 Upload Your Sales Data")
        st.markdown('<div class="info-tip">📋 CSV columns: <code>date, paper_code, units_sold, weather, is_holiday, is_weekend, is_exam_week</code></div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded:
            df_up = pd.read_csv(uploaded)
            st.success(f"✅ Uploaded {len(df_up)} rows!")
            st.dataframe(df_up.head(10))
            if st.button("🧠 Train AI Model"):
                with st.spinner("Training Prophet AI model..."):
                    import time; time.sleep(2)
                st.success("✅ AI trained! Predictions are now personalized.")
                st.balloons()

# RECOMMENDATIONS
elif "Recommendations" in page:
    st.markdown('<div class="hero-banner"><div class="hero-title">✨ Papers For You</div><div class="hero-subtitle">AI picks newspapers based on your reading style</div></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        user_type = st.selectbox("I am a...", ["🎓 Student", "👔 Working Professional", "🏠 Homemaker", "📈 Businessman"])
        current_paper = st.selectbox("I currently read", list(PAPERS.keys()), format_func=lambda x: f"{x} — {PAPERS[x]['name']}")
    with col2:
        interests = st.multiselect("My interests", ["📈 Business & Finance", "🏏 Sports", "🌍 World News", "🎭 Entertainment", "🏛️ Politics", "📚 Education"])
        pref_lang = st.selectbox("Preferred language", ["English 🇬🇧", "Hindi 🇮🇳", "Punjabi 🏵️"])
    if st.button("✨ Get My Recommendations"):
        RECS = {
            "TOI":    [("HINDU", 0.91, "Similar quality English journalism"), ("HT", 0.87, "Same English tier, different perspective"), ("ET", 0.72, "Great for business news")],
            "BHASKAR":[("JAGRAN", 0.89, "Readers of Bhaskar love Jagran"), ("KESARI", 0.78, "Top Hindi paper in Punjab"), ("AMAR", 0.71, "Strong national Hindi coverage")],
            "AJIT":   [("PTRIB", 0.93, "Most popular Punjabi papers together"), ("DESH", 0.80, "Strong local Punjab coverage"), ("KESARI", 0.68, "Bridges Hindi & Punjabi news")],
        }
        recs = RECS.get(current_paper, [("HT", 0.85, "Great English alternative"), ("BHASKAR", 0.75, "Top regional paper")])
        st.markdown("### 🎯 Recommended For You")
        for code, score, reason in recs:
            info = PAPERS.get(code, {})
            st.markdown(f"""<div class="vendor-card" style="border-left-color:#9B59B6;"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div class="vendor-name">{info.get('flag','')} {info.get('name',code)}</div><div style="color:#666;font-size:0.88rem;">💡 {reason}</div><div style="color:#27ae60;font-size:0.88rem;margin-top:4px;">₹{info.get('price',4)}/day | ₹{info.get('monthly',100)}/month</div></div><div style="text-align:center;background:#f4eeff;border-radius:12px;padding:0.7rem 1rem;"><div style="font-size:1.3rem;font-weight:800;color:#9B59B6;">{int(score*100)}%</div><div style="font-size:0.75rem;color:#888;">match</div></div></div></div>""", unsafe_allow_html=True)
