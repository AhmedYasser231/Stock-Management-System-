import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time

# ============ إعدادات الصفحة ============
st.set_page_config(
    page_title="Smart Inventory AI - Ultimate Edition",
    page_icon="📦",
    layout="wide"
)

# ============ بيانات الاتصال ============
SENDER_EMAIL = "alazwakahmed2020@gmail.com"
APP_PASSWORD = "ludb iwfd tuyx jaom"
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1_oEgShll43ztsXSRV44iS7lRuV6a1eQ2On7as0aOU7s/export?format=csv"

# ============ تهيئة سجل الطلبات في الذاكرة ============
if 'order_logs' not in st.session_state:
    st.session_state.order_logs = pd.DataFrame(columns=['التاريخ والوقت', 'المنتج', 'الكمية', 'إيميل المورد', 'الحالة'] )

# ============ تصميم CSS ============
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .stButton>button { background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); color: white; border: none; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# ============ دوال النظام ============
@st.cache_resource
def load_model():
    try:
        # بنستخدم joblib مباشرة وهي بتتعامل مع الملفات المضغوطة
        return joblib.load('walmart_model.pkl')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None
def load_live_data():
    try:
        df = pd.read_csv(GSHEET_URL)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        return df
    except Exception as e:
        st.error(f"خطأ في جلب البيانات من Google Sheets: {e}")
        return None

def send_real_order_email(product, qty, supplier_email):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = supplier_email
    msg['Subject'] = f"🚨 طلب توريد ذكي عاجل: {product}"
    
    body = f"عزيزي المورد،\n\nتم رصد عجز متوقع في منتج: {product}.\nالكمية المطلوبة: {qty} وحدة.\nتاريخ الطلب: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nنظام إدارة المخازن الذكي."
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        # تحديث سجل الطلبات في الذاكرة
        new_log = pd.DataFrame({
            'التاريخ والوقت': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'المنتج': [product],
            'الكمية': [qty],
            'إيميل المورد': [supplier_email],
            'الحالة': ['✅ تم الإرسال']
        })
        st.session_state.order_logs = pd.concat([new_log, st.session_state.order_logs], ignore_index=True)
        return True
    except Exception as e:
        st.error(f"خطأ في إرسال الإيميل: {e}")
        return False

# ============ تحميل البيانات والنموذج ============
model = load_model()
df = load_live_data()

# ============ واجهة المستخدم ============
st.sidebar.title("🚀 Smart Inventory Pro")
page = st.sidebar.radio("القائمة الرئيسية:", ["📊 لوحة التحكم الحية", "🔮 التنبؤ والأتمتة", "📧 سجل الطلبات"])

if df is not None:
    if page == "📊 لوحة التحكم الحية":
        st.title("📊 لوحة التحكم (Live Dashboard)")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("إجمالي المبيعات", f"${df['Weekly_Sales'].sum():,.0f}")
        with col2: st.metric("متوسط المبيعات", f"${df['Weekly_Sales'].mean():,.0f}")
        with col3: st.metric("حالة الربط السحابي", "☁️ متصل")
        
        sales_trend = df.groupby('Date')['Weekly_Sales'].sum().reset_index()
        fig = px.line(sales_trend, x='Date', y='Weekly_Sales', title="اتجاه المبيعات من Google Sheets")
        st.plotly_chart(fig, use_container_width=True)

    elif page == "🔮 التنبؤ والأتمتة":
        st.title("🔮 التنبؤ الذكي والأتمتة")
        col1, col2 = st.columns(2)
        with col1:
            store_id = st.number_input("رقم المتجر", 1, 45, 1)
            target_date = st.date_input("تاريخ التنبؤ", datetime.now())
            holiday = st.selectbox("هل يوجد عطلة؟", [0, 1])
            supplier_email = st.text_input("إيميل المورد:", "alazwakahmed2020@gmail.com")
        with col2:
            temp = st.slider("درجة الحرارة", 0, 110, 65)
            fuel = st.number_input("سعر الوقود", 2.0, 5.0, 3.5)
            cpi = st.number_input("مؤشر الأسعار", 120.0, 230.0, 215.0)
            unemp = st.number_input("البطالة", 0.0, 15.0, 7.5)

        if st.button("🚀 تشغيل التنبؤ والإرسال الآلي"):
            input_data = pd.DataFrame([[store_id, holiday, temp, fuel, cpi, unemp, target_date.year, target_date.month, target_date.isocalendar()[1]]],
                                     columns=['Store', 'Holiday_Flag', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Year', 'Month', 'Week'])
            if model:
                prediction = model.predict(input_data)[0]
                st.write(f"المبيعات المتوقعة: **${prediction:,.2f}**")
                if prediction > df['Weekly_Sales'].mean():
                    st.warning("🚨 عجز متوقع! جاري إرسال طلب توريد...")
                    if send_real_order_email("مخزون عام", 500, supplier_email):
                        st.balloons()
                        st.success("✅ تم الإرسال وتحديث السجل!")
                else:
                    st.info("المخزون كافٍ.")

    elif page == "📧 سجل الطلبات":
        st.title("📧 سجل المراسلات الآلية للموردين")
        st.markdown("يتم تحديث هذا الجدول تلقائياً عند كل عملية إرسال ناجحة.")
        
        if not st.session_state.order_logs.empty:
            st.dataframe(st.session_state.order_logs, use_container_width=True, hide_index=True)
            if st.button("مسح السجل 🗑️"):
                st.session_state.order_logs = pd.DataFrame(columns=['التاريخ والوقت', 'المنتج', 'الكمية', 'إيميل المورد', 'الحالة'])
                st.rerun()
        else:
            st.info("لا توجد طلبات مرسلة حتى الآن. ابدأ باستخدام صفحة التنبؤ لإرسال طلبات توريد.")
