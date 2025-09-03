# Team 2: Rachel Cole, Cade Haskins, Joshua Vasquez, Violet Zhao
<<<<<<< HEAD
# Data Choices: We used yfinance to pull Nvidia stock(representing a leading AI company)) and compare it to the S&P 500 stock ((the market benchmark))
# We chose monthly closing stock prices over the course of two years. This was chosen as our team beleived closing stock represnted the value of NVIDIA relative to the S&P 500 in the best way. We chose over the ocurse of two years to give a long enough time scale, and we chose monthly to make the data more easily readable in graphical form.
# Story：As an aggregation of the top 500 companies, the S&P 500 is a good representation of the how the stock market is doing. By comparing the clsoing value of NVIDIA (NVDA) to the closing value of S&P 500, we can not only visualize how well NVIDIA is doing relative to the market, but we can also get a better picture of how well NVIDIA is doing as a leading AI enterprise.
# Takeaway：The green line represents the monthly trend of NVIDIA’s closing market value relative to the S&P 500, and it showcases both how big NVIDIA is (being greater than 10% after a certain point), as well as how NVIDIA is seeing rapid growth. The red dashed line serves as a benchmark for NVIDIA's average performance relative to the S&P 500. When below the line, that means it is performing worse on average, and above the line means it is performing better than average.
=======
# Data Choices: We are using yfinance to pull Nvidia stock(representing a leading AI company) and compare it to the S&P 500 stock ((the market benchmark))
# Story： By comparing NVIDIA (NVDA) with the average closing value of S&P 500 constituents, analyse and visualise the market value of NVIDIA (NVDA) as a leading AI enterprise.
# Takeaway：The black line represents the monthly trend of NVIDIA’s closing market value relative to the S&P 500.The red dashed line serves as a benchmark for comparing whether NVIDIA’s market value has consistently exceeded the overall market average.
>>>>>>> cae292815e226a98da995b44d800e7c5584e2298
# So readers can clearly see whether NVIDIA’s market value has remained above the market average over time.


import yfinance as yf
import matplotlib.pyplot as plt


#Download stock data for NVIDIA and S&P 500 
NVDA_data = yf.download("NVDA", period="2y", interval="1mo",auto_adjust=True)
SP_data   = yf.download("SPY", period="2y", interval="1mo", auto_adjust=True)


NVDA_copy = NVDA_data.copy().astype(float)

#Find the average closing price for both stocks and calculate the ratio. 
avg_NVDA = NVDA_data['Close'].mean(skipna=True)
avg_SP = SP_data["Close"].mean(skipna=True)
#Use the ratio as a benchmark to compare how well NVIDIA is doing relative to the S&P 500 than normal
avg_ratio = avg_NVDA.iloc[0] / avg_SP.iloc[0] * 100

# Calculate NVDA's monthly closing price as a percentage of SPY's monthly closing price
for i in range(len(NVDA_copy.columns)):
    NVDA_copy.iloc[:, i] = (NVDA_copy.iloc[:, i] / SP_data.iloc[:, i] * 100).astype(float)






# --- Plotting ---
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
