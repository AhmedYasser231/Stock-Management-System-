import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# ============ إعدادات الصفحة ============
st.set_page_config(
    page_title="Smart Inventory AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ تصميم CSS احترافي ============
st.markdown("""
    <style>
    /* الخلفية والألوان الأساسية */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #333;
    }
    
    /* تنسيق الـ Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    /* تنسيق الـ Metrics */
    [data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
    }
    
    /* تنسيق الأزرار */
    .stButton > button {
        width: 100%;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* تنسيق العناوين */
    h1, h2, h3 {
        color: #1e3c72;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    /* تنسيق الـ Expander */
    .streamlit-expanderHeader {
        background-color: #f0f2f6;
        border-radius: 8px;
        border: 2px solid #667eea;
    }
    
    /* تنسيق الجداول */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* تنسيق الـ Alert Boxes */
    .stAlert {
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid;
    }
    
    /* تنسيق النصوص */
    p {
        font-size: 16px;
        line-height: 1.6;
        color: #555;
    }
    
    /* تنسيق الـ Selectbox والـ Input */
    .stSelectbox, .stNumberInput, .stSlider {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# ============ تحميل البيانات والنموذج ============
@st.cache_resource
def load_model():
    try:
        # بنستخدم joblib مباشرة وهي بتتعامل مع الملفات المضغوطة
        return joblib.load('walmart_model.pkl')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

@st.cache_data
def load_data():
    df = pd.read_csv('Walmart_Sales.csv')
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    return df

model = load_model()
df = load_data()

# ============ تهيئة قاعدة بيانات المخزون ============
if 'inventory_db' not in st.session_state:
    st.session_state.inventory_db = pd.DataFrame({
        'المنتج': ['الإلكترونيات', 'الأدوات المنزلية', 'الملابس', 'المواد الغذائية', 'الألعاب'],
        'الكمية الحالية': [120, 500, 250, 900, 40],
        'حد إعادة الطلب': [50, 150, 100, 300, 50],
        'التصنيف': ['A', 'B', 'B', 'A', 'C'],
        'السعر': [500, 100, 50, 20, 30]
    })

# ============ الشريط الجانبي (Sidebar) ============
with st.sidebar:
    st.markdown("### 🤖 Smart Inventory AI")
    st.markdown("---")
    
    page = st.radio(
        "اختر الصفحة:",
        ["📊 لوحة التحكم", "📦 المستودع", "🔮 التنبؤ", "📈 التحليلات"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ معلومات النظام")
    st.metric("الحالة", "🟢 نشط", delta="جاهز للعمل")
    st.metric("الإصدار", "2.0", delta="Pro")

# ============ الصفحة الأولى: لوحة التحكم ============
if page == "📊 لوحة التحكم":
    # العنوان الرئيسي
    st.markdown("""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 15px; color: white; margin-bottom: 30px;'>
            <h1 style='color: white; margin: 0;'>📊 لوحة التحكم الذكية</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0;'>مراقبة شاملة لأداء المخزن والمبيعات</p>
        </div>
    """, unsafe_allow_html=True)
    
    # الإحصائيات الرئيسية
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📈 إجمالي المبيعات",
            f"${df['Weekly_Sales'].sum():,.0f}",
            delta="↑ 12.5%"
        )
    
    with col2:
        st.metric(
            "💰 متوسط الطلب",
            f"${df['Weekly_Sales'].mean():,.0f}",
            delta="↑ 8.2%"
        )
    
    with col3:
        st.metric(
            "📦 قيمة المخزون",
            f"${(st.session_state.inventory_db['الكمية الحالية'] * st.session_state.inventory_db['السعر']).sum():,.0f}",
            delta="↑ 5.1%"
        )
    
    with col4:
        low_stock = len(st.session_state.inventory_db[st.session_state.inventory_db['الكمية الحالية'] <= st.session_state.inventory_db['حد إعادة الطلب']])
        st.metric(
            "🚨 تنبيهات النقص",
            low_stock,
            delta="يحتاج اهتمام" if low_stock > 0 else "آمن"
        )
    
    st.markdown("---")
    
    # الرسوم البيانية
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 اتجاه المبيعات (آخر 6 أشهر)")
        sales_trend = df.groupby('Date')['Weekly_Sales'].sum().reset_index()
        fig1 = px.line(
            sales_trend,
            x='Date',
            y='Weekly_Sales',
            labels={'Weekly_Sales': 'المبيعات ($)', 'Date': 'التاريخ'},
            color_discrete_sequence=['#667eea']
        )
        fig1.update_layout(
            hovermode='x unified',
            plot_bgcolor='rgba(240, 242, 246, 0.5)',
            paper_bgcolor='white',
            font=dict(size=12),
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 توزيع تصنيف المنتجات")
        abc_data = st.session_state.inventory_db['التصنيف'].value_counts()
        fig2 = go.Figure(data=[go.Pie(
            labels=abc_data.index,
            values=abc_data.values,
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb']),
            textposition='inside',
            textinfo='label+percent'
        )])
        fig2.update_layout(
            height=400,
            paper_bgcolor='white',
            font=dict(size=12)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # جدول المبيعات الأسبوعية
    st.markdown("### 📊 أفضل 5 أسابيع مبيعات")
    top_weeks = df.nlargest(5, 'Weekly_Sales')[['Date', 'Weekly_Sales', 'Store']].copy()
    top_weeks['Weekly_Sales'] = top_weeks['Weekly_Sales'].apply(lambda x: f"${x:,.2f}")
    st.dataframe(top_weeks, use_container_width=True, hide_index=True)

# ============ الصفحة الثانية: المستودع ============
elif page == "📦 المستودع":
    st.markdown("""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
        border-radius: 15px; color: white; margin-bottom: 30px;'>
            <h1 style='color: white; margin: 0;'>📦 إدارة المستودع</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0;'>تحديث وإدارة المخزون بسهولة</p>
        </div>
    """, unsafe_allow_html=True)
    
    # جدول المخزون التفاعلي
    st.markdown("### 📋 قائمة المنتجات والكميات")
    edited_df = st.data_editor(
        st.session_state.inventory_db,
        use_container_width=True,
        num_rows="dynamic",
        key="inventory_editor"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 حفظ التعديلات", use_container_width=True):
            st.session_state.inventory_db = edited_df
            st.success("✅ تم تحديث المخزن بنجاح!")
            time.sleep(1)
            st.rerun()
    
    with col2:
        if st.button("🔄 إعادة تعيين", use_container_width=True):
            st.info("تم إعادة تعيين البيانات")
    
    st.markdown("---")
    
    # تنبيهات النقص
    st.markdown("### 🚨 المنتجات التي تحتاج طلب توريد")
    critical = st.session_state.inventory_db[st.session_state.inventory_db['الكمية الحالية'] <= st.session_state.inventory_db['حد إعادة الطلب']]
    
    if not critical.empty:
        for idx, row in critical.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.warning(f"**{row['المنتج']}** - الكمية: {row['الكمية الحالية']} (الحد: {row['حد إعادة الطلب']})")
                with col2:
                    st.metric("النقص", row['حد إعادة الطلب'] - row['الكمية الحالية'])
                with col3:
                    if st.button("📧 طلب", key=f"order_{idx}"):
                        st.success(f"✅ تم إرسال طلب توريد لـ {row['المنتج']}")
    else:
        st.success("✅ جميع المنتجات متوفرة بكميات كافية!")

# ============ الصفحة الثالثة: التنبؤ ============
elif page == "🔮 التنبؤ":
    st.markdown("""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
        border-radius: 15px; color: white; margin-bottom: 30px;'>
            <h1 style='color: white; margin: 0;'>🔮 نظام التنبؤ الذكي</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0;'>توقع المبيعات والطلب المستقبلي</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("⚙️ إعدادات التنبؤ", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            store_id = st.selectbox("🏪 اختر المتجر", range(1, 46), index=0)
            holiday = st.radio("🏖️ عطلة؟", ["لا", "نعم"], horizontal=True)
            holiday = 1 if holiday == "نعم" else 0
        
        with col2:
            target_date = st.date_input("📅 تاريخ التنبؤ", datetime.now())
            temp = st.slider("🌡️ درجة الحرارة (F)", 0, 110, 65)
        
        with col3:
            fuel = st.number_input("⛽ سعر الوقود", 2.0, 5.0, 3.5)
            cpi = st.number_input("📊 مؤشر الأسعار", 120.0, 230.0, 215.0)
            unemp = st.number_input("👥 البطالة (%)", 0.0, 15.0, 7.5)
    
    if st.button("🚀 تشغيل التنبؤ", use_container_width=True):
        input_data = pd.DataFrame([[
            store_id, holiday, temp, fuel, cpi, unemp,
            target_date.year, target_date.month, target_date.isocalendar()[1]
        ]], columns=['Store', 'Holiday_Flag', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Year', 'Month', 'Week'])
        
        if model:
            with st.spinner("⏳ جاري التنبؤ..."):
                time.sleep(1)
                prediction = model.predict(input_data)[0]
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📈 النتيجة")
                st.metric("المبيعات المتوقعة", f"${prediction:,.2f}", delta="↑ 15%")
                st.info(f"بناءً على البيانات التاريخية، يتوقع النظام مبيعات {'عالية' if prediction > df['Weekly_Sales'].mean() else 'عادية'}.")
            
            with col2:
                st.markdown("### 🤖 قرار النظام")
                expected_units = int(prediction / 50)
                current_stock = st.session_state.inventory_db['الكمية الحالية'].sum()
                
                if expected_units > current_stock:
                    st.error(f"⚠️ عجز متوقع: {expected_units - current_stock} وحدة")
                    if st.button("📧 إرسال طلب توريد فوري"):
                        st.success("✅ تم إرسال الطلب للمورد!")
                else:
                    st.success(f"✅ المخزون كافٍ ({current_stock} وحدة)")

# ============ الصفحة الرابعة: التحليلات ============
elif page == "📈 التحليلات":
    st.markdown("""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
        border-radius: 15px; color: white; margin-bottom: 30px;'>
            <h1 style='color: white; margin: 0;'>📈 التحليلات المتقدمة</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0;'>رؤى عميقة عن الأداء والأنماط</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 المبيعات", "🏪 المتاجر", "🎯 الأداء"])
    
    with tab1:
        st.markdown("### 📊 توزيع المبيعات حسب الأسبوع")
        weekly_sales = df.groupby('Week')['Weekly_Sales'].mean()
        fig = px.bar(
            x=weekly_sales.index,
            y=weekly_sales.values,
            labels={'x': 'رقم الأسبوع', 'y': 'متوسط المبيعات'},
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🏪 أفضل 10 متاجر مبيعات")
        top_stores = df.groupby('Store')['Weekly_Sales'].sum().nlargest(10)
        fig = px.bar(
            x=top_stores.values,
            y=top_stores.index,
            orientation='h',
            color_discrete_sequence=['#764ba2']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 🎯 مؤشرات الأداء الرئيسية (KPIs)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("متوسط المبيعات", f"${df['Weekly_Sales'].mean():,.0f}")
        with col2:
            st.metric("أعلى مبيعات", f"${df['Weekly_Sales'].max():,.0f}")
        with col3:
            st.metric("أقل مبيعات", f"${df['Weekly_Sales'].min():,.0f}")
