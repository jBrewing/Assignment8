#
# Assignment 7 - Using Python to Access Hydrologic Data From Web Services
#
# Made by: Joseph Brewer
# For: CEE 6110 Hydroinformatics - Horsburgh
#
# Description:  This script will explore the data available from the
# USGS Unit Values WaterOneFlow web service,
# retrieve a time series of 15-minute discharge values,
# calculate daily summarized data, and then visualize outputs.

#Pseudocode

# 1. import libraries
import datetime
from suds.client import Client
from pandas import Series
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 2. connect to website
# Get time 'now' to bring data to present
now = datetime.datetime.now()
now1 = now.strftime("%Y-%m-%d %H:%M:%S")

# Create the inputs needed for the web service call
wsdlURL = 'http://hydroportal.cuahsi.org/nwisuv/cuahsi_1_1.asmx?WSDL'
siteCode = 'NWISUV:09315000'
variableCode = 'NWISUV:00060'
beginDate = '2018-08-01'
endDate = now1

# Create a new object named "NWIS" for calling the web service methods
NWIS = Client(wsdlURL).service

# Call the GetValuesObject method to return datavalues
response = NWIS.GetValuesObject(siteCode, variableCode, beginDate, endDate)

# Get the site's name from the response
siteName = response.timeSeries[0].sourceInfo.siteName

# 3. Load called objects into pandas series
# Create some blank lists in which to put the values and their dates
a = []  # The values
b = []  # The dates

# Get the values and their dates from the web service response
values = response.timeSeries[0].values[0].value

# Loop through the values and load into the blank lists using append
for v in values:
    a.append(float(v.value))
    b.append(v._dateTime)

# Create a Pandas Series object from the lists
# Set the index of the Series object to the dates
ts = Series(a, index=b)

# 4. Resample data on daily interval with mean/min/max functions
# create hourly max, min, and avg series.
hourlyTotDisAvg = ts.resample(rule='1D', base=0).mean()
hourlyTotDisMax = ts.resample(rule='1D', base=0).max()
hourlyTotDisMin = ts.resample(rule='1D', base=0).min()


#  5. Plot stuff
# Use MatPlotLib to create a plot of the time series
# Create a plot of the streamflow statistics
# ------------------------------------------
# Create a figure object and add a subplot
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(1, 1, 1)  # arguments for add_subplot - add_subplot(nrows, ncols, plot_number)

# Call the plot() methods on the series object to plot the data
ts.plot(color='grey', linestyle='solid', label='15-minute streamflow values', alpha=0.5, linewidth=0.5)
hourlyTotDisAvg.plot(color='green', linestyle='solid', label='Daily avg flows',
                     marker = 'o', ms=2, linewidth =0.75)
hourlyTotDisMax.plot(color='red', linestyle='solid', label='Daily max flows',
                     marker = 'o', ms=2, linewidth =0.75)
hourlyTotDisMin.plot(color='blue', linestyle='solid', label='Daily min flows',
                     marker = 'o', ms=2, linewidth =0.75)
# Set some properties of the subplot to make it look nice
ax.set_ylabel('Discharge, cubic feet per second')
ax.set_xlabel('Date')
ax.grid(True)
ax.set_title('Daily Max, Min, & Avg Flows for: ' + siteName + ', ' + siteCode)
ax.set_xlim(beginDate, endDate) #set limits with date variables
# Add a legend with some customizations
legend = ax.legend(loc='upper left', shadow=True)
fig.autofmt_xdate()  # use auto-formatter to enable accurate date representation with mouse
ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))  # set ticks interval for every 15 days.

# Create a frame around the legend.
frame = legend.get_frame()
frame.set_facecolor('0.95')

# Set the font size in the legend
for label in legend.get_texts():
    label.set_fontsize('large')

for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width

plt.show()

print('Done!')
