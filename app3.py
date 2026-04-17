import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="Smart Inventory AI & Automation", layout="wide", page_icon="🤖")

# تحسين المظهر باستخدام CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. دوال النظام الأساسية ---
@st.cache_resource
def load_model():
    try:
        with open('walmart_model1.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return None

@st.cache_data
def load_data():
    df = pd.read_csv('Walmart_Sales.csv')
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    return df

# دالة الأتمتة: حساب الكمية الاقتصادية للطلب (EOQ Automation)
def calculate_eoq(annual_demand):
    # معادلة EOQ = sqrt((2 * Demand * Ordering Cost) / Holding Cost)
    S = 100  # تكلفة إعداد الطلب (Fixed Cost)
    H = 5    # تكلفة تخزين القطعة (Holding Cost)
    eoq = np.sqrt((2 * annual_demand * S) / H)
    return int(eoq)

# دالة الأتمتة: محاكاة إرسال إيميل طلب توريد
def trigger_automated_order(product, qty):
    with st.spinner(f'🤖 النظام يقوم بإرسال طلب توريد تلقائي لمنتج {product}...'):
        time.sleep(2) # محاكاة وقت الإرسال
        st.toast(f"✅ تم إرسال طلب لـ {qty} وحدة إلى المورد بنجاح!", icon='📧')
        return True

# --- 3. تهيئة البيانات والنظام ---
model = load_model()
df = load_data()

if 'inventory_db' not in st.session_state:
    st.session_state.inventory_db = pd.DataFrame({
        'المنتج': ['الإلكترونيات', 'الأدوات المنزلية', 'الملابس', 'المواد الغذائية', 'الألعاب'],
        'الكمية الحالية': [120, 500, 250, 900, 40],
        'حد إعادة الطلب': [50, 150, 100, 300, 50],
        'التصنيف (ABC)': ['A', 'B', 'B', 'A', 'C'],
        'سعر الوحدة': [500, 100, 50, 20, 30]
    })

# --- 4. القائمة الجانبية (Navigation) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/8644/8644443.png", width=100 )
st.sidebar.title("Smart Stock AI v2.0")
st.sidebar.markdown("---")
page = st.sidebar.radio("القائمة الرئيسية:", ["🏠 لوحة التحكم", "📦 المستودع الذكي", "🔮 التنبؤ والأتمتة"])

# --- الصفحة الأولى: لوحة التحكم ---
if page == "🏠 لوحة التحكم":
    st.title("📊 مركز تحليل البيانات والأداء")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("إجمالي المبيعات", f"${df['Weekly_Sales'].sum():,.0f}")
    with col2: st.metric("متوسط الطلب الأسبوعي", f"${df['Weekly_Sales'].mean():,.0f}")
    with col3: st.metric("قيمة المخزون الحالي", f"${(st.session_state.inventory_db['الكمية الحالية'] * st.session_state.inventory_db['سعر الوحدة']).sum():,.0f}")
    
    low_stock_count = len(st.session_state.inventory_db[st.session_state.inventory_db['الكمية الحالية'] <= st.session_state.inventory_db['حد إعادة الطلب']])
    with col4: st.metric("تنبيهات النقص الآلية", low_stock_count, delta_color="inverse")

    st.markdown("---")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📈 تحليل الاتجاه الزمني (Time Series)")
        fig, ax = plt.subplots(figsize=(10, 4))
        df.groupby('Date')['Weekly_Sales'].sum().plot(ax=ax, color='#007bff', linewidth=2)
        plt.grid(True, alpha=0.3)
        st.pyplot(fig)
    with c2:
        st.subheader("🎯 تصنيف المخزون الذكي")
        fig2, ax2 = plt.subplots()
        st.session_state.inventory_db['التصنيف (ABC)'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2, colors=['#ff9999','#66b3ff','#99ff99'])
        st.pyplot(fig2)

# --- الصفحة الثانية: المستودع الذكي ---
elif page == "📦 المستودع الذكي":
    st.title("📦 نظام إدارة المستودع التفاعلي")
    st.write("يمكنك تعديل الكميات يدوياً أو ترك النظام يقوم بالتحديث التلقائي.")
    
    edited_df = st.data_editor(st.session_state.inventory_db, use_container_width=True, num_rows="dynamic")
    if st.button("حفظ التحديثات يدوياً 💾"):
        st.session_state.inventory_db = edited_df
        st.success("تم تحديث قاعدة بيانات المخزن.")

    st.markdown("---")
    st.subheader("🔍 الرقابة الآلية على المخزون")
    critical_items = st.session_state.inventory_db[st.session_state.inventory_db['الكمية الحالية'] <= st.session_state.inventory_db['حد إعادة الطلب']]
    
    if not critical_items.empty:
        st.error(f"🚨 اكتشف النظام نقصاً في {len(critical_items)} منتجات!")
        for index, row in critical_items.iterrows():
            col_a, col_b = st.columns([3, 1])
            col_a.warning(f"المنتج: {row['المنتج']} | الكمية الحالية: {row['الكمية الحالية']} (أقل من الحد المسموح: {row['حد إعادة الطلب']})")
            if col_b.button(f"طلب توريد لـ {row['المنتج']}", key=row['المنتج']):
                trigger_automated_order(row['المنتج'], calculate_eoq(1000))
    else:
        st.success("✅ حالة المخزون ممتازة، لا توجد طلبات توريد مطلوبة حالياً.")

# --- الصفحة الثالثة: التنبؤ والأتمتة ---
elif page == "🔮 التنبؤ والأتمتة":
    st.title("🔮 محرك التنبؤ والأتمتة (AI Engine)")
    st.markdown("يربط هذا القسم خوارزمية **Random Forest** بنظام اتخاذ القرار التلقائي.")

    with st.expander("🛠️ إعدادات محاكي السوق (Market Simulator)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            store_id = st.selectbox("اختر المتجر", range(1, 46))
            target_date = st.date_input("تاريخ التنبؤ", datetime.now())
        with c2:
            holiday = st.radio("هل يوجد عطلة؟", [0, 1], format_func=lambda x: "نعم" if x==1 else "لا", horizontal=True)
            temp = st.slider("درجة الحرارة (F)", 0, 110, 65)
        with c3:
            fuel = st.number_input("سعر الوقود", 2.0, 5.0, 3.5)
            unemp = st.number_input("معدل البطالة (%)", 0.0, 15.0, 7.5)
            cpi = st.number_input("مؤشر الأسعار (CPI)", 120.0, 230.0, 215.0)

    if st.button("تشغيل محرك التنبؤ والأتمتة ⚡"):
        # تجهيز البيانات للنموذج
        input_data = pd.DataFrame([[store_id, holiday, temp, fuel, cpi, unemp, target_date.year, target_date.month, target_date.isocalendar()[1]]],
                                 columns=['Store', 'Holiday_Flag', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Year', 'Month', 'Week'])
        
        if model:
            pred_sales = model.predict(input_data)[0]
            st.markdown("---")
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.subheader("📈 نتيجة التنبؤ (AI Output)")
                st.metric("المبيعات المتوقعة", f"${pred_sales:,.2f}")
                st.info(f"بناءً على النمط التاريخي، يتوقع النظام طلباً {'مرتفعاً' if pred_sales > df['Weekly_Sales'].mean() else 'عادياً'}.")

            with res_col2:
                st.subheader("🤖 قرار الأتمتة (Automated Action)")
                # تحويل الدولار لقطع (افتراضياً سعر القطعة 50$)
                expected_units = int(pred_sales / 50)
                current_stock = st.session_state.inventory_db['الكمية الحالية'].sum()
                
                st.write(f"القطع المتوقع بيعها: **{expected_units}** قطعة")
                st.write(f"المخزون الإجمالي المتوفر: **{current_stock}** قطعة")

                if expected_units > current_stock:
                    deficit = expected_units - current_stock
                    st.error(f"🚨 عجز متوقع قدره {deficit} قطعة!")
                    
                    # حساب الكمية المثالية للطلب آلياً
                    optimal_qty = calculate_eoq(expected_units * 52) # سنوياً
                    st.write(f"💡 **القرار الآلي:** تم حساب كمية الطلب المثالية (EOQ): **{optimal_qty}** وحدة.")
                    
                    if st.button("تنفيذ طلب التوريد التلقائي الآن 🚀"):
                        trigger_automated_order("مخزون عام", optimal_qty)
                else:
                    st.success("✅ المخزون كافٍ لتغطية الطلب المتوقع. لا حاجة لطلب توريد.")
        else:
            st.error("خطأ: ملف النموذج `walmart_model.pkl` غير موجود!")

