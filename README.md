# Smart Inventory AI - Stock Management and Sales Forecasting System

## Project Overview

This project presents an intelligent **Stock Management and Sales Forecasting System** designed to optimize inventory levels and automate reordering processes. Built as a Streamlit web application, it leverages machine learning to predict weekly sales and proactively manage stock, sending automated email alerts to suppliers when potential shortages are detected. The system integrates data analysis, model training, and an intuitive user interface to provide a comprehensive solution for inventory optimization.

## Features

-   **Interactive Dashboard**: A live dashboard displaying key sales metrics and trends, fetched from a Google Sheets source.
-   **Sales Forecasting**: Utilizes a pre-trained Machine Learning model (Random Forest Regressor) to predict future weekly sales based on various factors like store ID, holiday flag, temperature, fuel price, CPI, and unemployment.
-   **Automated Reordering**: Automatically triggers email notifications to suppliers when predicted sales indicate a potential stock deficit, ensuring timely replenishment.
-   **Order Log**: Maintains a detailed log of all automated supplier order emails, including product, quantity, supplier email, and status.
-   **Data Analysis**: Includes scripts for Exploratory Data Analysis (EDA) and visualization of historical sales data.
-   **Model Training**: A dedicated script for training and saving the sales forecasting model.

## Project Structure

```
Stock-Management-System-/
├── README.md                   # Project README file
├── Walmart_Sales.csv           # Historical sales data for training and analysis
├── analyze_walmart.py          # Script for Exploratory Data Analysis (EDA) and visualizations
├── last_version_app.py         # Main Streamlit web application
├── requirements.txt            # Python dependencies
├── train_final.py              # Script for training and saving the sales forecasting model
└── walmart_model.pkl           # Pre-trained Machine Learning model (Random Forest Regressor)
```

## Technologies Used

-   **Frontend/Web App**: Streamlit
-   **Backend/Logic**: Python
-   **Data Manipulation**: Pandas, NumPy
-   **Machine Learning**: Scikit-learn (RandomForestRegressor)
-   **Data Visualization**: Plotly Express, Matplotlib, Seaborn
-   **Email Automation**: SMTPLIB
-   **Model Serialization**: Joblib

## Setup and Installation

To set up and run the project locally, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/AhmedYasser231/Stock-Management-System-.git
    cd Stock-Management-System-
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Email (Optional but Recommended for Automation)**:
    -   The `last_version_app.py` uses `alazwakahmed2020@gmail.com` as the sender. If you wish to use your own email for automated orders, you\'ll need to:
        -   Update `SENDER_EMAIL` in `last_version_app.py`.
        -   Generate an App Password for your Gmail account (Google Account -> Security -> App passwords) and update `APP_PASSWORD` in `last_version_app.py`.

5.  **Run the Streamlit application**:
    ```bash
    streamlit run last_version_app.py
    ```

6.  Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

## Usage

-   **Live Dashboard**: View real-time sales data and trends.
-   **Prediction & Automation**: Input parameters like store ID, date, and environmental factors to get sales predictions. If a shortage is predicted, the system can automatically send an order email to the specified supplier.
-   **Order Log**: Monitor the history of all automated order emails sent.

## Training the Model (Optional)

If you wish to retrain the sales forecasting model or use a different dataset:

1.  Ensure `Walmart_Sales.csv` (or your new dataset) is in the project directory.
2.  Run the training script:
    ```bash
    python train_final.py
    ```
    This will generate (or update) `walmart_model.pkl`.

## Exploratory Data Analysis (EDA)

To perform EDA on the `Walmart_Sales.csv` dataset:

1.  Run the analysis script:
    ```bash
    python analyze_walmart.py
    ```
    This will print insights to the console and save various plots (e.g., sales trends, holiday impact, correlation matrix) to your local directory.

## Contributing

Contributions are welcome! Please feel free to fork the repository, create a new branch, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details (if applicable).

## Contact

For any questions or inquiries, please contact [Your Name/Email/GitHub Profile].

---

*This README was generated by Manus AI.*
