# Team 2: Rachel Cole, Cade Haskins, Joshua Vasquez, Violet Zhao
# We are using yfinance to pull Nvidia stock and compare it to the S&P 500 stock 
#We used a period of 2 years to examine stocks from both Nvidia and S&P 500
# We want to compare both stock sets and view Nvidia stocks reletaive to S&P
# We are using the mean stocks for each month in the sampling period, originally we used everyday, but it gave a messy and overloaded graph 
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

NVDA = yf.Ticker("NVDA")
# print(NVDA.history(period="1y"))

NVDA_data = yf.download("NVDA", period="2y", interval="1mo",auto_adjust=True)
SP_data   = yf.download("^GSPC", period="2y", interval="1mo", auto_adjust=True)

NVDA_copy = NVDA_data.copy().astype(float)
# NVDA_copy.index = NVDA_copy.index.strftime("%B %d, %Y")
avg_NVDA = NVDA_copy['Volume'].mean(skipna=True)
avg_SP = SP_data["Volume"].mean(skipna=True)

print(avg_NVDA)
avg_ratio = avg_NVDA / avg_SP * 100

for i in range(len(NVDA_copy.columns)):
    NVDA_copy.iloc[:, i] = (NVDA_copy.iloc[:, i] / SP_data.iloc[:, i] * 100).astype(float)



# recent_data.to_csv("NVDA.csv", index=False)
# print(recent_data)
# print(NVDA_data)
# print(SP_data)
# print(NVDA_copy.head())
print(avg_ratio)

# print(NVDA_copy.index)
# NVDA_copy.plot(y="Volume", use_index=True)
# plt.figure(figsize=(10, 6))
# plt.plot(NVDA_data.index, NVDA_copy["Volume"], label="NVDA", color="green")
# plt.axhline(y=avg_ratio, color='red', linestyle='--', label='Benchmark (Avg Ratio=100%)')
# # plt.plot(SP_data.index, SP_data["Volume"], label="S&P 500", color="blue")

# plt.title("Stock Volume of NVDIA relative to S&P 500")
# plt.xlabel("Date")
# plt.ylabel("Stock Volume")
# plt.legend()
# plt.xticks(rotation=45, ha='right')
# plt.show()
