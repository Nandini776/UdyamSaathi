import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor

def predict_future_sales(df,forecast_days=7):
    if df.empty:
        return None, {}

    sales_df = df[df['type']=='Income'].copy()
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    daily_sales= sales_df.groupby('date').agg({'amount':'sum'}).reset_index()

    if(len(daily_sales) < 30):
        return None, {}

    daily_sales['day_of_week'] = daily_sales['date'].dt.dayofweek
    daily_sales['day_of_month'] = daily_sales['date'].dt.day
    daily_sales['lag_1'] = daily_sales['amount'].shift(1)  
    daily_sales['lag_7'] = daily_sales['amount'].shift(7)

    train_data = daily_sales.dropna().copy()

    X = train_data[['day_of_week', 'day_of_month', 'lag_1', 'lag_7']]
    y = train_data['amount']

    model =RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    future_predictions = []
    max_date = daily_sales['date'].max()
    recent_amounts = list(daily_sales['amount'].tail(7).values)

    for i in range(1, forecast_days + 1):
        next_date = max_date + timedelta(days=i)
        dow = next_date.dayofweek
        dom = next_date.day
        
        lag_1 = recent_amounts[-1]
        lag_7 = recent_amounts[-7] if len(recent_amounts) >= 7 else recent_amounts[0]

        features = pd.DataFrame([[dow, dom, lag_1, lag_7]], 
                                columns=['day_of_week', 'day_of_month', 'lag_1', 'lag_7'])
        
        pred = model.predict(features)[0]
        pred = max(50.0, round(float(pred), 2))
        
        future_predictions.append({
            'Date': next_date.strftime('%Y-%m-%d'),
            'Predicted_Sales': pred
        })
        recent_amounts.append(pred)

    forecast_df = pd.DataFrame(future_predictions)

    total_predicted = forecast_df['Predicted_Sales'].sum()
    avg_daily = forecast_df['Predicted_Sales'].mean()

    insights = {
        "avg_daily": round(avg_daily, 2),
        "total_revenue": round(total_predicted, 2),
        "stock_budget": round(total_predicted * 0.60, 2)
    }

    return forecast_df, insights

def get_top_items(df):
    sales_df = df[df['type'] == 'Income']
    if sales_df.empty:
        return []
    top_items = sales_df.groupby('item')['amount'].sum().sort_values(ascending=False).head(3)
    return top_items.index.tolist()