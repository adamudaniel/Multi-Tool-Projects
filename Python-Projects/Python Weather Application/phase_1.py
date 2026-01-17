# Author: Daniel Teriv Adamu
# Student ID: F5101328

import sqlite3


# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.

'''
Satisfactory 50-59
'''
def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        # Define the query
        query = "SELECT * from [countries]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

    except sqlite3.OperationalError as ex:
        print(ex)


def select_all_cities(connection):
    # TODO: Implement this function
    try:
        query = 'select * from cities'
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        results = cursor.execute(query).fetchall()

        for row in results:
            print(f"City Id: {row['id']} -- City Name: {row['name']} -- City Country Id: {row['country_id']} -- City Latitude & Longitude: {row['latlong']}")

        return results
    
    except sqlite3.OperationalError as ex:
        print(ex)
        return None

'''
Good

In additional to successfully completing *all* the "Satisfactory" queries, 
implement the queries that satisfy the each query requirements indicated by the name
of the function and any parameters to achieve a potential mark in the range 60-69.
'''
def average_annual_temperature(connection, city_id, year):
    # Calculate the average annual temperature for a given city and year
    try:
        query = '''
            SELECT AVG(mean_temp) as avg_temp
            FROM daily_weather_entries
            WHERE city_id = ? AND date >= ? AND date < ?
        '''
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        start = f"{year}-01-01" 
        end = f"{year+1}-01-01" #includes a years worth of rain data
        result = cursor.execute(query, (city_id, start, end)).fetchone()
        
        # to check if city id and year exists
        if result and result['avg_temp'] is not None:
            avg_temp = result['avg_temp']
            print(f"Average Annual Temperature for City {city_id} in year {year} is {avg_temp:.2f}°C")
            return avg_temp
        else:
            print(f"No temperature data found for City {city_id} in {year}")
            return None
    except sqlite3.OperationalError as ex:
        print(ex)
        return None

def average_seven_day_precipitation(connection, city_id, start_date):
    # Average 7-day period precipitation
    try:
        query = '''
            SELECT AVG(precipitation) AS avg_precipitation
            FROM daily_weather_entries
            WHERE city_id = ? AND date >= ? AND date < date(?, '+7 days')
        '''
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # using SQLite date() function to add 7 days
        end_row = cursor.execute("SELECT date(?, '+7 days')", (start_date,)).fetchone()
        end = end_row[0] if end_row else None

        result = cursor.execute(query, (city_id, start_date, start_date)).fetchone()

        if result and result['avg_precipitation'] is not None:
            avg_precipitation = result['avg_precipitation']
            if end:
                print(f"The 7 days average precipitation for City {city_id} from {start_date} to {end} is {avg_precipitation:.2f} mm")
            else:
                print(f"The 7 days average precipitation for City {city_id} from {start_date} (7 days) is {avg_precipitation:.2f} mm")
            return avg_precipitation
        else:
            print(f"No precipitation data found")
            return None
    except sqlite3.OperationalError as ex:
        print(ex)
        return None
'''
Very good

In additional to successfully completing *all* the "Satisfactory" and "Good" queries, 
implement the queries that satisfy the each query requirements indicated by the name
of the function and any parameters to achieve a potential mark in the range 70-79.
'''
def average_mean_temp_by_city(connection, date_from, date_to):
    # TODO: Implement this function
    # average of mean temperatures grouped by city
    try:
        query = '''
            SELECT city_id, name, AVG(mean_temp) as avg_mean_temp
            FROM daily_weather_entries d
            JOIN cities c ON d.city_id = c.id
            WHERE d.date >= ? AND d.date <= ?
            GROUP BY c.id, c.name
            ORDER BY avg_mean_temp DESC
        '''
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        results = cursor.execute(query, (date_from, date_to)).fetchall()

        if results:
            for row in results:
                if row['avg_mean_temp'] is not None:
                    print(f"City id:{row['city_id']} -- City name: {row['name']}, mean temperature is {row['avg_mean_temp']:.2f}°C")
                else:
                    print(f"No data")
            return results
        else:
            print(f"No mean temperature data found between {date_from} and {date_to}")
            return None
    except sqlite3.OperationalError as ex:
        print(ex)
        return None

def average_annual_precipitation_by_country(connection, year):
    # finding the total precipitation per country
    try:
        start = f"{year}-01-01"
        end = f"{year+1}-01-01" # includes a years worth of rain data

        query = '''
            SELECT co.id as country_id, co.name as country_name, SUM(d.precipitation) as total_precip
            FROM daily_weather_entries d
            JOIN cities ci ON d.city_id = ci.id
            JOIN countries co ON ci.country_id = co.id
            WHERE d.date >= ? AND d.date < ?
            GROUP BY co.id, co.name
            ORDER BY total_precip DESC
        '''
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        results = cursor.execute(query, (start, end)).fetchall()

        if results:
            for row in results:
                if row['total_precip'] is not None:
                    print(f"Country {row['country_id']} - {row['country_name']}: {row['total_precip']:.2f} mm")
                else:
                    print(f"Country {row['country_id']} - {row['country_name']}: No data")
            return results
        else:
            print(f"No precipitation data found for year {year}")
            return None
    except sqlite3.OperationalError as ex:
        print(ex)
        return None

'''
Excellent'''

if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    with sqlite3.connect('CIS4044-N-SDI-OPENMETEO-PARTIAL.db') as connection:
        print(".................DISPLAY ALL COUNTRIES IN DB?...............................")
        Ans = input("Type 'yes' to continue...:")
        if Ans.lower() != 'yes':
            print("Exiting program.")
            exit()
        else:
            select_all_countries(connection)

        print("......................DISPLAY ALL CITIES IN DB?..........................")
        Ans = input("Type 'yes' to continue...:")
        if Ans.lower() != 'yes':
            print("Exiting program.")
            exit()
        else:
            select_all_cities(connection)

        print(".......................TO GET AVG TEMPERATURE OF A CITY.........................")
        city_id = int(input("Enter city ID (e.g., 1): "))
        year = int(input("Enter year to find temperature(e.g., 2022): "))
        if city_id <= 0:
            print("Invalid city ID. Exiting program.")
            exit()
        else:
            average_annual_temperature(connection, city_id, year)

        print("....................TO GET 7-DAYS AVG PRECIPITATION OF A CITY..........................")
        city_id = int(input("Enter city ID (e.g., 1): "))
        year = input("Enter start date (e.g., '2022-06-01'): ")
        if city_id <= 0:
            print("Invalid city ID. Exiting program.")
            exit()
        else:
            average_seven_day_precipitation(connection, city_id, year)

        print(".............AVG MEAN TEMPERATURE OF ALL CITIES IN DB.....................")
        start_date = input("Enter start date (e.g., '2022-01-01'): ")
        end_date = input("Enter end date (e.g., '2022-12-31'): ")
        if start_date == end_date:
            print("Invalid date input. Exiting program.")
            exit()
        else:
            average_mean_temp_by_city(connection, start_date, end_date)

        print(".............AVG ANNUAL PRECIPITATION OF ALL COUNTRIES IN DB..............")
        year = int(input("Enter year to find precipitation (e.g., 2022): "))
        if year < 0:
            print("Invalid year input. Exiting program.")
            exit()
        else:
            average_annual_precipitation_by_country(connection, year)