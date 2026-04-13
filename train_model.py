import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

# 1. تحميل البيانات
df = pd.read_csv('Walmart_Sales.csv')
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# 2. هندسة الميزات (Feature Engineering)
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Week'] = df['Date'].dt.isocalendar().week.astype(int)

# 3. اختيار الميزات والهدف
# سنستخدم المتغيرات التي لها تأثير على المبيعات
features = ['Store', 'Holiday_Flag', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Year', 'Month', 'Week']
X = df[features]
y = df['Weekly_Sales']

# 4. تقسيم البيانات (تدريب واختبار)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. تدريب النموذج (Random Forest)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. التقييم
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"--- تقييم النموذج ---")
print(f"Mean Absolute Error (MAE): {mae:,.2f}")
print(f"R2 Score (Accuracy): {r2:.4f}")

# 7. أهمية الميزات (Feature Importance)
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=False)
print("\n--- أهمية الميزات في التنبؤ ---")
print(feature_importance_df)

# 8. حفظ النموذج



import joblib

# حفظ الموديل بضغط عالي (Level 3 كافي جداً)
joblib.dump(model, 'walmart_model1.pkl', compress=3)

import os
size = os.path.getsize('walmart_model1.pkl') / (1024 * 1024)
print(f"حجم الموديل الجديد: {size:.2f} MB")