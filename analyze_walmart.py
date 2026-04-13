import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# إعداد الخطوط لدعم اللغة العربية في الرسومات إذا لزم الأمر (اختياري)
# plt.rcParams['font.family'] = 'DejaVu Sans' 

# 1. تحميل البيانات
df = pd.read_csv('Walmart_Sales.csv')

# 2. فحص أولي للبيانات
print("--- نظرة عامة على البيانات ---")
print(df.head())
print("\n--- معلومات الأعمدة والقيم المفقودة ---")
print(df.info())
print("\n--- الإحصاءات الوصفية ---")
print(df.describe())

# 3. معالجة التواريخ
# تحويل عمود التاريخ إلى datetime (نلاحظ التنسيق في الصورة يوم/شهر/سنة)
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# استخراج ميزات زمنية إضافية
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Week'] = df['Date'].dt.isocalendar().week

# 4. تحليل المبيعات مع الوقت (Time Series)
plt.figure(figsize=(15, 6))
df_monthly = df.groupby('Date')['Weekly_Sales'].sum().reset_index()
sns.lineplot(data=df_monthly, x='Date', y='Weekly_Sales')
plt.title('Total Weekly Sales Over Time (Walmart)')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.grid(True)
plt.savefig('C:\Users\user\Stock Managment System.png')
plt.close()

# 5. تأثير العطلات (Holiday Impact)
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='Holiday_Flag', y='Weekly_Sales')
plt.title('Impact of Holidays on Sales')
plt.xticks([0, 1], ['Normal Week', 'Holiday Week'])
plt.savefig('C:\Users\user\Stock Managment System.png')
plt.close()

# 6. تحليل الارتباط (Correlation Analysis)
plt.figure(figsize=(10, 8))
corr = df[['Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Holiday_Flag']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.savefig('C:\Users\user\Stock Managment System.png')
plt.close()

print("\n--- تم حفظ الرسومات البيانية في المسار الحالي ---")
