### Project: CTBA Group 2 Dashboard

##Project Overview
#Problem: With all the news about housing prices being so high, we realized that there was not a place/dashboard where housing information by state could be accessed.
#Not only would this information be useful to have in general for any type of study that may need the data, we also beleived it would be useful for or fellow classmates, 
#a lot of whom do not own their own house and may be curious about housing prices across the U.S.

#Audience: While we believe state level housing data could be useful to most people and homeseekers, we set about this project with the specific audience of students, 
#specifically students like our classmates, or those doing a degree in business. 

#As stated in the problem section, we believe there is a value in having an easily accessible website/dashboard which displays housing data changes over time. In terms of value the value #to our audience, many students will be finding their first homes, and having state level data on housing prices can gives them both the actualy values of the houses by state, but also #shows them the trends of the housing market by state, letting them make better decisions and predictions about what the housing market may look like. To help with this, we included a #housing price to salary ratio, where we took housing prices from 2025 and divided them by the average salary of jobs common for MSBA grads (data analyst, consultant, data scientist). This #way, they may get a better idea of what the actual prices of the houses will be relative to how much money them may be making (by state). Finally, we also included international data on #housing prices, as we figured it would be good to have a frame of reference of how other countries' housing markets are doing.

##How to Run
#The Project was made live on render and can be ran using this link: https://housing-dashboard-group-2.onrender.com
#To run locally, first clone the repository on the local machine
#Make sure to install all dependencies listed in requirements.txt for your local environment
#Afterwards, change directory till you are at Final_Dash
#Assuming you have a python interpreter and are working in an IDE like VS Code, you can then click run on App.py, and the dashboard should run locally.

##	Data sources & data dictionary
#United states housing price dataset was from Zillow.com. The code was data cleaned in google colab before being imported into a csv file. Dataset was then loaded into a dataframe
#International housing price dataset is from BIS Data Portal,The dataset we loaded is international_housing_nominal（CSV）
#Salaries were taken from Zip Recruiter, and the data was cleaned and formatted in google colab
