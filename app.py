import streamlit as st 
import datetime
import requests

'''
# Taxi Fare Prediction

This front queries a [taxi fare model API]
(https://predict-taxifare-iwuisdewea-ez.a.run.app/predict_fare)'''

key = '2012-10-06 12:10:20.0000001'
pickup_date = st.date_input('pickup date', value=datetime.datetime.today())
pickup_time = st.time_input('pickup time', value=datetime.datetime.now())
pickup_datetime = f'{pickup_date} {pickup_time}UTC'
pickup_longitude = st.number_input('pickup longitude', value=40.7614327)
pickup_latitude = st.number_input('pickup latitude', value=-73.9798156)
dropoff_longitude = st.number_input('dropoff longitude', value=40.6413111)
dropoff_latitude = st.number_input('dropoff latitude', value=-73.7803331)
passenger_count = st.number_input('passenger_count', min_value=1, max_value=8, step=1, value=1)

url = "https://predict-taxifare-iwuisdewea-ez.a.run.app/predict_fare"

params = dict(
    key=key,
    pickup_datetime=pickup_datetime,
    pickup_longitude=pickup_longitude,
    pickup_latitude=pickup_latitude,
    dropoff_longitude=dropoff_longitude,
    dropoff_latitude=dropoff_latitude,
    passenger_count=passenger_count
)

response = requests.get(url, params=params)

prediction = response.json()
pred = prediction['prediction']
pred