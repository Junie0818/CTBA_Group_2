import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

NVDA = yf.Ticker("NVDA")
# print(NVDA.history(period="1y"))

NVDA_data = yf.download("NVDA", period="2y", auto_adjust=True)
SP_data   = yf.download("^GSPC", period="2y", auto_adjust=True)

NVDA_copy = NVDA_data.copy().astype(float)
# NVDA_copy.index = NVDA_copy.index.strftime("%B %d, %Y")

for i in range(len(NVDA_copy.columns)):
    NVDA_copy.iloc[:, i] = (NVDA_copy.iloc[:, i] / SP_data.iloc[:, i] * 100).astype(float)
  

# recent_data.to_csv("NVDA.csv", index=False)
# print(recent_data)
# print(NVDA_data)
# print(SP_data)
print(NVDA_copy.head())

# print(NVDA_copy.index)
# NVDA_copy.plot(y="Volume", use_index=True)
# plt.show()