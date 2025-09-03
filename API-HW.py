# Team 2: Rachel Cole, Cade Haskins, Joshua Vasquez, Violet Zhao
# Data Choices: We are using yfinance to pull Nvidia stock(representing a leading AI company) and compare it to the S&P 500 stock ((the market benchmark))
# Story： By comparing NVIDIA (NVDA) with the average closing value of S&P 500 constituents, analyse and visualise the market value of NVIDIA (NVDA) as a leading AI enterprise.
# Takeaway：The black line represents the monthly trend of NVIDIA’s closing market value relative to the S&P 500.The red dashed line serves as a benchmark for comparing whether NVIDIA’s market value has consistently exceeded the overall market average.
# So readers can clearly see whether NVIDIA’s market value has remained above the market average over time.
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# NVDA = yf.Ticker("NVDA")
# SP = yf.Ticker("SPY")
# print(NVDA.history(period="1y"))

NVDA_data = yf.download("NVDA", period="2y", interval="1mo",auto_adjust=True)
SP_data   = yf.download("SPY", period="2y", interval="1mo", auto_adjust=True)

# print(NVDA.info["sharesOutstanding"])
# print(NVDA_data)
# print(SP_data)
NVDA_copy = NVDA_data.copy().astype(float)
avg_NVDA = NVDA_data['Close'].mean(skipna=True)

avg_SP = SP_data["Close"].mean(skipna=True)

avg_ratio = avg_NVDA.iloc[0] / avg_SP.iloc[0] * 100


for i in range(len(NVDA_copy.columns)):
    NVDA_copy.iloc[:, i] = (NVDA_copy.iloc[:, i] / SP_data.iloc[:, i] * 100).astype(float)






# # NVDA_copy.plot(y="Volume", use_index=True)
plt.figure(figsize=(10, 6))
plt.plot(NVDA_data.index, NVDA_copy["Close"], label="NVDA", color="black")
plt.axhline(y=avg_ratio, color='red', linestyle='--', label='Benchmark (Avg Ratio)')


# # --- Aesthetic + label changes ---
plt.title("NVIDIA Monthly Close Trading Value Relative to S&P 500")
plt.xlabel("Date (Monthly Intervals)")
plt.ylabel("Relative Trade Value (%)")

plt.legend(frameon=False, loc="upper left")
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle=':', linewidth=0.7, alpha=0.7)
plt.tight_layout()
plt.figtext(0.01, 0.01, "Source: Yahoo Finance | 2-year monthly data",
            ha="left", fontsize=9, style="italic", color="gray")

plt.show()
