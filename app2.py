import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import joblib
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="Smart Stock Management System", layout="wide")

# الحصول على المسار الحالي للمجلد لضمان الوصول للملفات على السيرفر
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. تحميل النموذج والبيانات
@st.cache_resource
def load_model():
    # دمج المسار الحالي مع اسم الموديل لضمان عدم حدوث FileNotFoundError
    model_path = os.path.join(BASE_DIR, 'walmart_model1.pkl')
    return joblib.load(model_path)

@st.cache_data
def load_data():
    # دمج المسار الحالي مع اسم ملف البيانات
    data_path = os.path.join(BASE_DIR, 'Walmart_Sales.csv')
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    return df

# تنفيذ التحميل
try:
    model = load_model()
    df = load_data()
except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الملفات: {e}")
    st.stop()

# 3. واجهة المستخدم (Sidebar)
st.sidebar.title("إعدادات النظام 🛠️")
menu = st.sidebar.selectbox("اختر الصفحة:", ["لوحة التحكم العامة", "التنبؤ بالمبيعات المستقبلية"])

# --- الصفحة الأولى: لوحة التحكم العامة ---
if menu == "لوحة التحكم العامة":
    st.title("📊 لوحة تحكم إدارة المخازن الذكية (Walmart)")
    
    # عرض إحصائيات سريعة
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي المبيعات", f"${df['Weekly_Sales'].sum():,.0f}")
    col2.metric("متوسط المبيعات الأسبوعية", f"${df['Weekly_Sales'].mean():,.0f}")
    col3.metric("عدد المتاجر", df['Store'].nunique())

    # رسم بياني لاتجاه المبيعات
    st.subheader("📈 اتجاه المبيعات مع الوقت")
    sales_trend = df.groupby('Date')['Weekly_Sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=sales_trend, x='Date', y='Weekly_Sales', ax=ax)
    st.pyplot(fig)

    # تأثير العطلات
    st.subheader("🏖️ تأثير العطلات على المبيعات")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x='Holiday_Flag', y='Weekly_Sales', ax=ax2)
    ax2.set_xticklabels(['أسبوع عادي', 'أسبوع عطلة'])
    st.pyplot(fig2)

# --- الصفحة الثانية: التنبؤ بالمبيعات المستقبلية ---
elif menu == "التنبؤ بالمبيعات المستقبلية":
    st.title("🔮 التنبؤ الذكي بالمبيعات والمخزون")
    st.write("أدخل البيانات التالية للحصول على المبيعات المتوقعة:")

    col1, col2 = st.columns(2)
    
    with col1:
        store = st.number_input("رقم المتجر (Store)", min_value=1, max_value=45, value=1)
        date = st.date_input("تاريخ الأسبوع المستقبلي", datetime.now())
        holiday = st.selectbox("هل يوجد عطلة في هذا الأسبوع؟", [0, 1], format_func=lambda x: "نعم" if x == 1 else "لا")

    with col2:
        temp = st.slider("درجة الحرارة المتوقعة (F)", min_value=0, max_value=110, value=60)
        fuel = st.slider("سعر الوقود المتوقع", min_value=2.0, max_value=5.0, value=3.5)
        cpi = st.number_input("مؤشر أسعار المستهلك (CPI)", value=211.0)
        unemp = st.number_input("معدل البطالة المتوقع (%)", value=8.0)

    # معالجة التاريخ للمدخلات
    year = date.year
    month = date.month
    week = date.isocalendar()[1]

    # زر التنبؤ
    if st.button("احسب المبيعات المتوقعة 🚀"):
        # إنشاء DataFrame بنفس أسماء الأعمدة التي تدرب عليها الموديل
        input_data = pd.DataFrame([[store, holiday, temp, fuel, cpi, unemp, year, month, week]], 
                                 columns=['Store', 'Holiday_Flag', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Year', 'Month', 'Week'])
        
        prediction = model.predict(input_data)[0]
        
        st.success(f"المبيعات المتوقعة لهذا الأسبوع هي: **${prediction:,.2f}**")
        
        # تنبيه ذكي للمخزون
        if prediction > df['Weekly_Sales'].mean() * 1.5:
            st.warning("⚠️ تنبيه: مبيعات عالية جداً متوقعة! يرجى التأكد من توفر مخزون كافٍ.")
        else:
            st.info("ℹ️ حالة المخزون الحالية كافية لتغطية الطلب المتوقع.")