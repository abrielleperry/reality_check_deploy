import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle

data = pd.read_csv('../data/fire-datetime.csv')
data['datetime'] = pd.to_datetime(
    data['datetime'],
    format='%Y-%m-%d %I:%M:%S %p',
    errors='coerce')

imputer = SimpleImputer(strategy='most_frequent')
data[['incident', 'action_taken']] = imputer.fit_transform(
    data[['incident', 'action_taken']])

encoder_incident = OneHotEncoder(sparse_output=False)
encoder_action_taken = OneHotEncoder(sparse_output=False)
incident_encoded = encoder_incident.fit_transform(data[['incident']])
action_taken_encoded = encoder_action_taken.fit_transform(
    data[['action_taken']])
incident_encoded_df = pd.DataFrame(
    incident_encoded,
    columns=encoder_incident.get_feature_names_out(
        ['incident']))
action_taken_encoded_df = pd.DataFrame(
    action_taken_encoded,
    columns=encoder_action_taken.get_feature_names_out(
        ['action_taken']))

data_encoded = pd.concat(
    [data, incident_encoded_df, action_taken_encoded_df], axis=1)
data_encoded['date'] = data_encoded['datetime'].dt.date
features = data_encoded.drop(['datetime',
                              'incident_num',
                              'address',
                              'incident',
                              'action_taken',
                              'property',
                              'location_name'],
                             axis=1)

daily_features = features.groupby('date').mean()
daily_incidents = data_encoded.groupby('date').size()
X_train, X_test, y_train, y_test = train_test_split(
    daily_features, daily_incidents, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"The RMSE of the model is: {rmse}")

with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(list(daily_features.columns), f)
