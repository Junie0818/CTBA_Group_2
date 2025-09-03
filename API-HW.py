# Team 2: Rachel Cole, Cade Haskins, Joshua Vasquez, Violet Zhao
# Data Choices: We are using yfinance to pull Nvidia stock(representing a leading AI company)) and compare it to the S&P 500 stock ((the market benchmark))
# Story： By comparing NVIDIA (NVDA) with the average trading volume liquidity of S&P 500 constituents, analyse and visualise the market activity of NVIDIA (NVDA) as a leading AI enterprise.
# Takeaway：The green line represents the monthly trend of NVIDIA’s trading volume relative to the S&P 500.The red dashed lineserves as a benchmark for comparing whether NVIDIA’s market activity has consistently exceeded the overall market average.
# So readers can clearly see whether NVIDIA’s liquidity has remained above the market average over time.
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
print(avg_NVDA)
avg_SP = SP_data["Volume"].mean(skipna=True)
print(avg_SP)
print()
# print(avg_NVDA)
avg_ratio = avg_NVDA[0] / avg_SP[0] * 100
print(avg_ratio)

for i in range(len(NVDA_copy.columns)):
    NVDA_copy.iloc[:, i] = (NVDA_copy.iloc[:, i] / SP_data.iloc[:, i] * 100).astype(float)



# recent_data.to_csv("NVDA.csv", index=False)
# print(recent_data)
# print(NVDA_data)
# print(SP_data)
# print(NVDA_copy.head())
# print(avg_ratio)


# NVDA_copy.plot(y="Volume", use_index=True)
plt.figure(figsize=(10, 6))
plt.plot(NVDA_data.index, NVDA_copy["Volume"], label="NVDA", color="green")
plt.axhline(y=avg_ratio, color='red', linestyle='--', label='Benchmark (Avg Ratio)')


# --- Aesthetic + label changes ---
plt.title("NVIDIA Monthly Trading Volume Relative to S&P 500")
plt.xlabel("Date (Monthly Intervals)")
plt.ylabel("Relative Trading Volume (%)")

plt.legend(frameon=False, loc="upper left")
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle=':', linewidth=0.7, alpha=0.7)
plt.tight_layout()
plt.figtext(0.01, 0.01, "Source: Yahoo Finance | 2-year monthly data",
            ha="left", fontsize=9, style="italic", color="gray")

plt.show()
