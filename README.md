# Welcome to Reality Check

This repository contains the codebase for our Hack Sprint project. Our web application provides businesses with a powerful tool to visualize and analyze their data through a user-friendly dashboard.

# Project Overview

The Reality Check Dashboard is designed to help businesses unlock the full potential of their data. With our platform, users can easily visualize representations of their data, including charts, graphs, and tables, allowing for better decision-making and strategic planning. This service is perfect for any business looking to gain a deeper understanding of their operations and enhance their performance through data-driven insights.  It is also a demo of how companies can have website applications deployed that are dynamic with real-time data, all without any added expense of any outside database services to pay for.  Granted, with only one week to work on this, our main objective was to open people's vision of what is possible.

We used a variety of datasources including realtime API's with daily data refreshes from the Tulsa Fire Department showing types of incidents and locations in the last 24 hours.  In addition, the Tulsa Fire department sent us a year's worth of data to use for data analysis.  In addition, though sales data is hard to get access to, we found for educational purposes a legacy database as an API in xml format (https://services.odata.org/V3/northwind/Northwind.svc/).  XML is extensively used for financial data, particularly in scenarios where data interchange among different systems is required. It allows for a structured representation of data and is used in financial reporting, configurations, and messaging systems like those in banking for transactions.

Our intention was to simply show what can be done with the technologies we implemented that show a savings to any company .  The technologies implemented here include:  Flask for web app deployment; Dash for creating dashboards; Python programming for creating DataFrames used in reading, parsing, merging and manipulating and aggregating of data to then create graphs and dashboards that allow for better understanding of one's data.  A lot of experience was gained in data manipulation and some basic but powerful bar, line, time-series and geo-location graphs were done.  

Some issues we encountered include:  (1) For the sales database, since no longitude and latitude data was included in the XML dataset, we used plotly geopy.geocoders API that gave us these lat lon coordinates.  Since excessive use of this API would start to incur a cost, hence it made sense in the code to subsequently hardcode geo-coordinates for each city and have them easily accessible without having to look them up each time.  (2)  We used a couple of different ways to create dashboards to demo what is possible to do.  One way was to make use HTML cards to build a dashboard and this was demoed with the json data provided by the Fire department.  The second way was to create a dashboard using dash programming, which also effectively allows you to create containers and specify however many columns per row.  This way also effectively separated the data processing from the rendering for easy maintenance and optimization.  (3) the question arose, how to render the dashboards since these are not simple webpages but each dashboard is an application unto itself that is maintained in realtime.  The solution came by deploying the applications with different routes (i.e., /app1, /app2) so that to the user experience at the click of a button they are sent to a dashboard just as if they were simply going to another webpage.  (4) The process of choosing which technologies to use and which ones to discard due to its time investment was most of work we did the first couple of day.  Some technologies we considered yet discarded due to time limitations included Fireside Service to store and retrieve data as well as fun things to add to any web application such as QR codes and ML chatbots, all of which are highly valued in the marketplace of today. 

# Instructions

## Step 1

**Clone reality-check repository into terminal with this link**
[Github link](https://github.com/abrielleperry/reality-check.git)

     ($) git clone https://[PAT]@github.com/abrielleperry/reality-check.git

## Step 2

Go into the fire-dashboard folder

    cd web/fire-dashboard

## Step 3

In your terminal, run:

    ($) python3 fire_app.py

## Step 4

Open a second terminal and go back into the **web** folder

    ($) cd ..
    ($) pwd
    /root/reality-check/web

## Step 5

Open file **index.html** with Live Server
\*Live Server shortcut is **CMD+L+O\***

Alternatively, if you prefer running from the commandline: 
from the web folder run:  python -m http.server 8000

## Step 6

In order to launch dashboards from a flask application with routes to localhost:5000/app1 and /app2 and for them to be accessible from buttons on our main index page.

please run from the web folder:  python3 ./flaskapp.py

## Step 7

Explore our webpage and try our **LIVE DEMO'S** in **Services** to see **dashboard data and analysis**.



## Authors

- Allyson Ugarte allyson.ugarte@atlasschool.com
- Abrielle Perry abrielle.perry@atlasschool.com
