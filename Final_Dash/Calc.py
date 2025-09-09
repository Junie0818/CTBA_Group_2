import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error
import plotly.express as px
import matplotlib.pyplot as plt
# df_temp = pd.read_csv("data/US_States_Median_Housing.csv")




df = pd.read_csv("data/US_Median_Housing_Prices.csv", header=0, index_col=0)
df = df.astype(float)
df.index = pd.to_datetime(df.index)




df_diff = df.diff().diff().dropna()



# # Arima(0, d, q)
model = ARIMA(df['California'], order=(1, 1, 2))
model_fit = model.fit()
# print(model_fit.summary())


##Forecast sample
forecast = model_fit.forecast(steps=60)


plt.figure(figsize=(10,5))
plt.plot(df.index, df['California'], label='Actual')
plt.plot(pd.date_range(df.index[-1] + pd.offsets.MonthBegin(1), periods=60, freq='M'), 
         forecast, label='Forecast', linestyle='--')
plt.title("California Housing Prices Forecast")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()