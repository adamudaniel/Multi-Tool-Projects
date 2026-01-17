# Historical weather data application
Author: Adamu Daniel Teriv
General overview

This is a weather data application built in Python, designed to interact with a SQLite database. This applications queries and processes data stored in a localsqlite3 database called 'CIS4044-N-SDI-OPENMETEO-PARTIAL.db' and either prints it to the console or outputs as visualisation. This application utilises the sqlite3, Matplotlib and requests libraries. 

System Components

There are three python scripts and their uses are as follows:

Phase 1: Data Queries

    Geography Retrieval: Selects and displays all records from the countries and cities tables.

    Temperature Analysis: Calculates average annual temperatures for specific cities.

    Precipitation Analysis: Calculates 7-day average precipitation and total annual precipitation grouped by country.

    City Comparisons: Ranks cities by their average mean temperature within a specified date range.

Phase 2: Visualizations

    Generates high-quality plots with formatted axes, legends, and titles.

    Supports saving plots directly to the local file system as image files.

    Handles missing data by defaulting null precipitation values to 0.0 to ensure chart continuity.
Chart Descriptions and Functionality

    1. 7-Day Precipitation Bar Chart

        Function: plot_7day_precipitation(connection, city_id, start_date)

        Description: Generates a bar chart showing the daily precipitation (in mm) for a single city over a one-week window.

    Inputs:

        city_id: The unique identifier for the city in the database.

        start_date: The beginning date of the 7-day period (format: 'YYYY-MM-DD').

        Key Features: Automatically handles missing data by defaulting null values to 0.0.

    2. Period Precipitation for Multiple Cities

        Function: plot_period_precipitation_for_cities(connection, city_ids, date_from, date_to)

        Description: A comparative bar chart showing the total accumulated precipitation for a specified list of cities during a custom date range.

    Inputs:

        city_ids: A list of city identifiers.

        date_from / date_to: The custom range for data aggregation.

        Key Features: Sorts cities by the highest total precipitation for easier comparison.

    3. Yearly Precipitation by Country

        Function: plot_avg_yearly_precip_by_country(connection, year)

        Description: Displays a bar chart showing the total annual precipitation for every country recorded in the database for a given year.

    Inputs:

        year: The specific calendar year (e.g., 2022).

        Key Features: Aggregates data across all cities within each country to provide a national-level overview.

    4. Grouped Temperature and Precipitation Statistics

        Function: plot_grouped_min_max_mean(connection, entity_ids, date_from, date_to, by='city')

        Description: A complex grouped bar chart that clusters four metrics: Minimum Temperature, Maximum Temperature, Mean Temperature, and Total Precipitation.

    Inputs:

        entity_ids: List of IDs for cities or countries.

        by: A toggle to group data by either 'city' or 'country'.

        Key Features: Provides a side-by-side comparison of disparate metrics to identify correlations between temperature extremes and rainfall.

    5. Daily Min/Max Temperature Multi-Line Chart

        Function: plot_daily_min_max_for_month(connection, city_id, year, month)

        Description: A time-series multi-line plot showing the daily fluctuations of min and max temperatures for a city over a specific month.

    Inputs:

        year / month: The specific time frame to analyze.

        Key Features: Uses markers (o) on each line to clearly denote daily readings and includes a legend for clarity.

    6. Average Temperature vs. Average Precipitation Scatter Plot

        Function: plot_scatter_avg_temp_vs_avg_precip(connection, level='city', date_from=None, date_to=None)

        Description: A scatter plot designed to visualize the relationship (correlation) between average heat and average rainfall.

    Inputs:

        level: Can be set to 'city', 'country', or 'all'.

        Key Features: At the city and country levels, individual points are labeled with their names to help identify outliers (e.g., high-temperature/low-precipitation cities).


Phase 3: Data Acquisition & Storage

    API Integration: Uses the requests library to fetch data from the Open-Meteo archive endpoint.

    Database Management: Automatically creates the daily_weather_entries table if it does not exist, including columns for min_temp, max_temp, mean_temp, and precipitation.

    Chunked Fetching: Implements a chunking mechanism to fetch large date ranges in smaller segments (default 31 days) to respect API stability and avoid timeouts.

    Command Line Interface: Supports adding new cities and fetching weather data via CLI arguments.

Setup and Usage
Prerequisites

    Python 3.x

    SQLite3

    matplotlib library

    requests library

Execution

    Initialize Database: Ensure the SQLite database file path is correctly set in the scripts.

    Run Analytics: Execute phase_1.py for text-based reports.

    Generate Charts: Execute phase_2.py to view or save visualizations.

    Fetch Data: Use phase_3.py to populate the database with API data:
    Bash    
        python phase_3.py --cities 1,2 --start-date 2022-01-01 --end-date 2022-12-31

Note: Ensure the path of the DB is in the root folder (as specified in the scripts)