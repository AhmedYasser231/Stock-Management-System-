import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
# 1. تحميل البيانات
print("--- جاري تحميل البيانات... ---")
df = pd.read_csv('Walmart_Sales.csv')
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# 2. هندسة الميزات (Feature Engineering) - ضروري لتوافق الموديل مع الواجهة
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Week'] = df['Date'].dt.isocalendar().week.astype(int)

# 3. اختيار الميزات والهدف (يجب أن تتطابق مع مدخلات الواجهة)
features = ['Store', 'Holiday_Flag', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Year', 'Month', 'Week']
X = df[features]
y = df['Weekly_Sales']

# 4. تقسيم البيانات
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. تدريب النموذج
print("--- جاري تدريب النموذج (قد يستغرق لحظات)... ---")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. التقييم
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"دقة النموذج (R2 Score): {r2:.4f}")

# 7. حفظ النموذج النهائي
# حفظ الموديل مضغوط في نفس المسار
joblib.dump(model, 'walmart_model.pkl', compress=3)

print("\n✅ تم حفظ النموذج بنجاح في walmart_model.pkl")
print("الآن يمكنك تشغيل واجهة streamlit (app_beautiful.py) وستعمل صفحة التنبؤ بدون أخطاء.")
