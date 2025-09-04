# Team 2: Rachel Cole, Cade Haskins, Joshua Vasquez, Violet Zhao
# To run this code, make sure to have yfinance and matplotlib installed in your Python environment.



# Story：As an aggregation of the top 500 companies, the S&P 500 is a good representation of the how the stock market is doing. By comparing the clsoing value of NVIDIA (NVDA) to the closing value of S&P 500, we can not only visualize how well NVIDIA is doing relative to the market, but we can also get a better picture of how well NVIDIA is doing as a leading AI enterprise.
# The red dashed line serves as a benchmark for NVIDIA's average performance relative to the S&P 500 over the two years. When below the line, that means it is performing worse on average, and above the line means it is performing better than average. As can be seen in the graph, NVIDIA has been continuing to perform better than average for almost an entire year, showcasing how strong its growth has been.

# Data Choices: We used yfinance to pull Nvidia stock (representing a leading AI company) and compare it to the S&P 500 stock (the market benchmark). They were our two tickeres.
# We chose monthly closing stock prices over the course of two years. This was chosen as our team beleived closing stock represnted the value of NVIDIA relative to the S&P 500 in the best way. We chose over the occurance of two years to give a long enough time scale, and we chose monthly to make the data more easily readable in graphical form.
# So readers can clearly see whether NVIDIA’s market value has remained above the market average over time.

# Takeaway：The black line represents the monthly trend of NVIDIA’s closing market value relative to the S&P 500, and the continued increase showcases how NVIDIA is continuing to grow relative to the average of the other S&P 500 companies. 
# Not only is it continuing to grow, but the amount with which it has grown, with it almost tripling in its ratio to the S&P 500 showcases its rapid and continuing potential for growth.



#AI Assitance: Used ChatGPT to help with labeling x-axis dates in Month Year format.

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
NVDA_copy.iloc[:, 0] = (NVDA_copy.iloc[:, 0] / SP_data.iloc[:, 0] * 100).astype(float)



# --- Plotting ---
plt.figure(figsize=(8, 4))
plt.plot(NVDA_data.index, NVDA_copy["Close"], label="NVDA", color="black")
# plt.plot(TSLA.index, TSLA["Close"], label="TSLA", color="blue")
# plt.plot(AMZN.index, AMZN["Close"], label="AMZN", color="orange")
plt.axhline(y=avg_ratio, color='red', linestyle='--', label='Benchmark (Avg Ratio)')


# # --- Aesthetic + label changes ---
plt.title("NVIDIA Monthly Close Trading Value Relative to S&P 500")
plt.xlabel("Date (Monthly Intervals)")
plt.ylabel("Relative Trade Value (%)")

plt.legend(frameon=False, loc="upper left")
plt.grid(True, linestyle=':', linewidth=0.7, alpha=0.7)
plt.tight_layout()
plt.figtext(0.01, 0.01, "Source: Yahoo Finance | 2-year monthly data",
            ha="left", fontsize=9, style="italic", color="gray")

# Edit x-axis to show Month Year format
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b %Y"))
plt.xticks(NVDA_copy.index, rotation=45, ha='right')

#Make a png of the plt
plt.savefig("NVIDIA.png")
plt.show()
