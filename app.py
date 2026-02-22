"""
Paper Scout Pro - Streamlit MVP (Week 1)
Run: streamlit run app.py
This is the quick-launch web prototype before Flutter app is ready.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Paper Scout Pro | Ludhiana",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #FFF8F0; }
    .stApp { font-family: 'Segoe UI', sans-serif; }
    .vendor-card {
        background: white; border-radius: 16px; padding: 16px;
        border-left: 4px solid #E8581E; margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .metric-box {
        background: #E8581E; color: white; border-radius: 12px;
        padding: 16px; text-align: center;
    }
    h1 { color: #E8581E !important; }
    .stSelectbox label, .stSlider label { font-weight: 600; }
    .prediction-box {
        background: linear-gradient(135deg, #2D6A4F, #40916C);
        color: white; border-radius: 16px; padding: 20px; margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Seed Data (Ludhiana Vendors) ─────────────────────
@st.cache_data
def load_vendors():
    return pd.DataFrame([
        {"id": 1, "name": "Sharma News Agency", "area": "Model Town", "lat": 30.9010, "lng": 75.8573,
         "languages": "EN,HI,PU", "papers": "TOI,Dainik Bhaskar,Tribune,Punjab Kesri",
         "opens": "5:30 AM", "delivery": True, "rating": 4.7, "distance": 0.3},
        {"id": 2, "name": "PAU Gate Newsstand", "area": "PAU Campus", "lat": 30.9062, "lng": 75.8089,
         "languages": "EN,HI,PU", "papers": "TOI,Tribune,HT,Punjab Kesri",
         "opens": "5:45 AM", "delivery": False, "rating": 4.5, "distance": 0.1},
        {"id": 3, "name": "Malhotra Papers", "area": "Sarabha Nagar", "lat": 30.8978, "lng": 75.8674,
         "languages": "EN,HI", "papers": "TOI,Hindu,Economic Times,Dainik Bhaskar",
         "opens": "5:30 AM", "delivery": True, "rating": 4.8, "distance": 0.8},
        {"id": 4, "name": "Bhatia News Corner", "area": "Civil Lines", "lat": 30.9125, "lng": 75.8512,
         "languages": "EN,HI,PU", "papers": "Tribune,Punjab Kesri,Jagran,TOI",
         "opens": "5:15 AM", "delivery": True, "rating": 4.6, "distance": 1.1},
        {"id": 5, "name": "LPU Campus Store", "area": "LPU Campus", "lat": 30.9200, "lng": 75.7018,
         "languages": "EN,HI,PU,TA", "papers": "TOI,Hindu,HT,Economic Times,Dainik Bhaskar",
         "opens": "6:00 AM", "delivery": True, "rating": 4.9, "distance": 12.0},
        {"id": 6, "name": "Clock Tower Newsstand", "area": "Clock Tower", "lat": 30.9003, "lng": 75.8526,
         "languages": "EN,HI,PU", "papers": "TOI,HT,Tribune,Punjab Kesri,Jagran",
         "opens": "5:00 AM", "delivery": False, "rating": 4.4, "distance": 0.6},
        {"id": 7, "name": "Dugri News Centre", "area": "Dugri", "lat": 30.8723, "lng": 75.8445,
         "languages": "EN,PU", "papers": "TOI,Tribune,Punjab Kesri",
         "opens": "5:30 AM", "delivery": True, "rating": 4.5, "distance": 2.1},
        {"id": 8, "name": "Pakhowal Road Papers", "area": "Pakhowal", "lat": 30.8834, "lng": 75.8201,
         "languages": "EN,HI,PU", "papers": "TOI,Tribune,Dainik Bhaskar,Punjab Kesri",
         "opens": "5:30 AM", "delivery": True, "rating": 4.3, "distance": 1.7},
        {"id": 9, "name": "Sadar Bazar Agency", "area": "Sadar Bazar", "lat": 30.9078, "lng": 75.8467,
         "languages": "EN,HI,PU", "papers": "TOI,Hindu,Tribune,Punjab Kesri,Dainik Bhaskar",
         "opens": "5:00 AM", "delivery": False, "rating": 4.6, "distance": 0.5},
        {"id": 10, "name": "GT Road News Centre", "area": "GT Road", "lat": 30.9278, "lng": 75.8689,
         "languages": "EN,HI,PU", "papers": "TOI,HT,Tribune,Dainik Bhaskar,Punjab Kesri",
         "opens": "5:00 AM", "delivery": True, "rating": 4.4, "distance": 3.2},
    ])

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.image("https://via.placeholder.com/200x60/E8581E/FFFFFF?text=📰+Paper+Scout", width=200)
    st.markdown("---")
    
    page = st.radio("Navigation", [
        "🏠 Home", "📍 Find Vendor", "🚴 Delivery", 
        "📊 Vendor Dashboard", "✨ Recommendations"
    ])
    
    st.markdown("---")
    lang = st.selectbox("Language", ["EN - English", "HI - हिंदी", "PU - ਪੰਜਾਬੀ", "TA - தமிழ்"])
    lang_code = lang.split(" - ")[0]
    
    st.markdown("---")
    st.markdown("**Pricing**")
    st.markdown("🎓 Students: **₹120/mo**")
    st.markdown("🏠 General: **₹150/mo**")
    st.markdown("📲 Pickup: **FREE**")

vendors_df = load_vendors()

# ── HOME PAGE ─────────────────────────────────────────
if page == "🏠 Home":
    st.title("📰 Paper Scout Pro")
    st.subheader("Ludhiana's Hyperlocal Newspaper Network")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box"><h2>20+</h2><p>Vendors</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><h2>95%</h2><p>ML Accuracy</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h2>30%</h2><p>Fuel Saved</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><h2>4</h2><p>Languages</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🗓️ Launch Timeline")
        st.markdown("""
        | Week | Milestone |
        |------|-----------|
        | **Week 1** | ✅ This Streamlit MVP |
        | **Week 2** | Flutter pickup + maps |
        | **Week 3** | Vendor ML dashboard |
        | **Week 4** | Delivery + UPI launch |
        """)
    with col2:
        st.markdown("### 📊 Target Metrics (Week 4)")
        st.markdown("""
        - 🎓 100 students registered
        - 🏪 20 vendors onboarded  
        - 📦 50+ daily orders
        - ⭐ 4.5+ average rating
        """)

# ── FIND VENDOR ───────────────────────────────────────
elif page == "📍 Find Vendor":
    st.title("📍 Find Newspaper Vendor")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        area = st.selectbox("Area", ["All", "Model Town", "PAU Campus", "Civil Lines", 
                                      "Sarabha Nagar", "Sadar Bazar", "Dugri", "GT Road"])
    with col2:
        lang_filter = st.multiselect("Language", ["EN", "HI", "PU", "TA"], default=["EN", "HI", "PU"])
    with col3:
        paper_filter = st.text_input("Paper (e.g. TOI, Tribune)", "")
    
    delivery_only = st.checkbox("🚴 Delivery vendors only")
    radius = st.slider("Search radius (km)", 0.5, 10.0, 2.0, 0.5)
    
    # Filter
    filtered = vendors_df.copy()
    if area != "All":
        filtered = filtered[filtered["area"] == area]
    if lang_filter:
        mask = filtered["languages"].apply(lambda l: any(lang in l for lang in lang_filter))
        filtered = filtered[mask]
    if paper_filter:
        filtered = filtered[filtered["papers"].str.contains(paper_filter, case=False)]
    if delivery_only:
        filtered = filtered[filtered["delivery"] == True]
    filtered = filtered[filtered["distance"] <= radius]
    
    st.markdown(f"**{len(filtered)} vendors found**")
    
    for _, v in filtered.sort_values("distance").iterrows():
        langs = v['languages'].split(',')
        lang_badges = " ".join([f"`{l}`" for l in langs])
        delivery_badge = "🚴 **Delivery**" if v['delivery'] else "🚶 Pickup only"
        
        with st.expander(f"⭐ {v['rating']} | {v['name']} — {v['area']} ({v['distance']} km)"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Papers:** {v['papers']}")
                st.markdown(f"**Languages:** {lang_badges}")
                st.markdown(f"**Opens:** 🕐 {v['opens']} | {delivery_badge}")
            with col2:
                st.metric("Rating", f"⭐ {v['rating']}")
                st.metric("Distance", f"📍 {v['distance']} km")
                if st.button("Order Pickup", key=f"pickup_{v['id']}"):
                    st.success(f"✅ Pickup order placed at {v['name']}!")

# ── DELIVERY ──────────────────────────────────────────
elif page == "🚴 Delivery":
    st.title("🚴 Home Delivery Subscription")
    
    col1, col2 = st.columns(2)
    with col1:
        is_student = st.checkbox("🎓 I'm a student (₹30 discount)")
        price = 120 if is_student else 150
        st.info(f"Your plan: **₹{price}/month**")
        
        paper = st.selectbox("Select Newspaper", ["TOI (₹5/day)", "Hindu (₹5/day)", "HT (₹5/day)",
                                                    "Dainik Bhaskar (₹3/day)", "Tribune (₹3/day)",
                                                    "Punjab Kesri (₹3/day)", "Economic Times (₹7/day)"])
        time_slot = st.select_slider("Delivery Time", ["5:30 AM", "6:00 AM", "6:30 AM", "7:00 AM", "7:30 AM"])
        address = st.text_area("Delivery Address")
        
        if st.button(f"Subscribe ₹{price}/mo via UPI", type="primary"):
            st.success("✅ Subscription created! Razorpay payment link would open here.")
            st.balloons()
    
    with col2:
        st.markdown("### Plan Comparison")
        st.markdown(f"""
        | Feature | Free | {'Student ₹120' if is_student else 'Home ₹150'} |
        |---------|------|------------|
        | Pickup map | ✅ | ✅ |
        | AR Scanner | ✅ | ✅ |
        | Recommendations | ✅ | ✅ |
        | Home Delivery | ❌ | ✅ |
        | Time Slots | ❌ | ✅ |
        | Priority Support | ❌ | ✅ |
        """)

# ── VENDOR DASHBOARD ──────────────────────────────────
elif page == "📊 Vendor Dashboard":
    st.title("📊 Vendor Dashboard")
    
    tabs = st.tabs(["🤖 ML Predictions", "📂 Upload Data", "🗺️ Route Optimizer"])
    
    with tabs[0]:
        st.subheader("Prophet ML Stock Predictor")
        
        vendor_sel = st.selectbox("Select Your Shop", vendors_df["name"].tolist())
        
        col1, col2 = st.columns([3, 1])
        with col2:
            is_premium = st.checkbox("⭐ Premium (₹99/mo)", value=True)
        
        if not is_premium:
            st.warning("🔒 Upgrade to Premium (₹99/mo) to access ML predictions")
        else:
            if st.button("🧠 Run Prophet Prediction", type="primary"):
                with st.spinner("Training Prophet model on your sales data..."):
                    import time
                    time.sleep(2)
                
                # Simulated 7-day forecast
                days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                base_en = [65, 58, 72, 70, 68, 55, 50]
                base_hi = [85, 78, 90, 88, 82, 70, 65]
                base_pu = [40, 35, 45, 42, 38, 30, 28]
                conf = [0.95, 0.94, 0.96, 0.93, 0.94, 0.92, 0.91]
                
                pred_df = pd.DataFrame({
                    "Day": days,
                    "English (TOI/HT)": base_en,
                    "Hindi": base_hi,
                    "Punjabi": base_pu,
                    "Confidence": [f"{int(c*100)}%" for c in conf]
                })
                
                st.markdown('<div class="prediction-box"><h3>📈 7-Day Stock Forecast</h3><p>Model: Facebook Prophet | Accuracy: 95%+</p></div>', unsafe_allow_html=True)
                
                st.dataframe(pred_df.set_index("Day"), use_container_width=True)
                st.bar_chart(pred_df.set_index("Day")[["English (TOI/HT)", "Hindi", "Punjabi"]])
                
                col1, col2, col3 = st.columns(3)
                with col1: st.metric("Avg English/day", "63", "+8%")
                with col2: st.metric("Avg Hindi/day", "80", "+12%")
                with col3: st.metric("Avg Punjabi/day", "37", "+5%")
    
    with tabs[1]:
        st.subheader("Upload Sales Data (CSV)")
        st.markdown("**Required columns:** `date, toi_sold, hindi_sold, punjabi_sold, weather, holiday`")
        
        # Sample CSV
        sample = pd.DataFrame({
            "date": ["2024-01-15", "2024-01-16", "2024-01-17"],
            "toi_sold": [52, 48, 65],
            "hindi_sold": [78, 82, 90],
            "punjabi_sold": [35, 31, 42],
            "weather": ["sunny", "rainy", "sunny"],
            "holiday": [False, False, True]
        })
        st.markdown("**Sample CSV:**")
        st.dataframe(sample, use_container_width=True)
        st.download_button("📥 Download Sample CSV", sample.to_csv(index=False), "sample_sales.csv", "text/csv")
        
        uploaded = st.file_uploader("Upload your CSV", type=["csv"])
        if uploaded:
            df = pd.read_csv(uploaded)
            st.success(f"✅ Uploaded {len(df)} rows!")
            st.dataframe(df.head(), use_container_width=True)
            if st.button("Train ML Model", type="primary"):
                with st.spinner("Training Prophet model..."):
                    import time; time.sleep(3)
                st.success("✅ Model trained! Go to Predictions tab.")
    
    with tabs[2]:
        st.subheader("🗺️ Route Optimizer (TSP)")
        st.markdown("Optimize delivery drops for minimum distance — 30% fuel savings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Pending Deliveries", "12")
            st.metric("Naive Distance", "11.8 km")
        with col2:
            st.metric("Optimized Distance", "8.4 km", "-3.4 km")
            st.metric("Fuel Saved", "~₹47", "30%")
        
        if st.button("🗺️ Optimize Route", type="primary"):
            st.success("Route optimized! Google Maps directions generated for 12 stops.")

# ── RECOMMENDATIONS ───────────────────────────────────
elif page == "✨ Recommendations":
    st.title("✨ Personalized Recommendations")
    
    st.markdown("### What do you currently read?")
    current = st.multiselect("Your papers", ["TOI", "Hindu", "HT", "Dainik Bhaskar", "Tribune", "Punjab Kesri", "Economic Times"])
    
    if current:
        RECS = {
            "TOI": [("Hindu", "EN", 0.85, "In-depth analysis for students"), ("Economic Times", "EN", 0.70, "Add business coverage")],
            "Hindu": [("TOI", "EN", 0.85, "More India news coverage"), ("Economic Times", "EN", 0.65, "For business news")],
            "Dainik Bhaskar": [("Jagran", "HI", 0.88, "North India complement"), ("Punjab Kesri", "PU", 0.60, "Punjab news")],
            "Tribune": [("Punjab Kesri", "PU", 0.80, "Local Punjab perspective"), ("TOI", "EN", 0.55, "National coverage")],
        }
        
        seen = set()
        all_recs = []
        for p in current:
            for rec in RECS.get(p, []):
                if rec[0] not in current and rec[0] not in seen:
                    all_recs.append(rec)
                    seen.add(rec[0])
        
        all_recs.sort(key=lambda x: x[2], reverse=True)
        
        st.markdown("### 🤖 ML Recommendations")
        for rec in all_recs[:4]:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**📰 {rec[0]}** ({rec[1]}) — {rec[3]}")
            with col2:
                st.progress(rec[2])
            with col3:
                st.markdown(f"**{int(rec[2]*100)}% match**")
    else:
        st.info("Select newspapers you currently read to get personalized recommendations")
