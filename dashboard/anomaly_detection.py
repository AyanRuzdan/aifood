import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def detect_anomalies(file_path=None, df=None):
    if df is None:
        if file_path is None:
            raise ValueError("Either file_path or df must be provided")
        df = pd.read_csv(file_path)

    df = df.loc[:, ~df.columns.str.contains('^Unnamed|^$', case=False)]

    df.columns = [col.strip() for col in df.columns]

    for ts_col in ['Timestamp', 'timestamp']:
        if ts_col in df.columns:
            df[ts_col] = pd.to_datetime(df[ts_col])
            df.rename(columns={ts_col: 'Timestamp'}, inplace=True)
            break

    required_columns = ['Temperature (°C)', 'Humidity (%)']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    X = df[['Temperature (°C)', 'Humidity (%)']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(X_scaled)

    df['Anomaly'] = model.predict(X_scaled)
    df['Anomaly'] = df['Anomaly'].map({1: 'Normal', -1: 'Anomaly'})

    return df
