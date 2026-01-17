# Author: Daniel Teriv Adamu
# Student ID: F5101328

import sqlite3
import matplotlib.pyplot as plt

def get_7day_precipitation(connection, city_id, start_date):
    
    query = '''
        SELECT date, precipitation
        FROM daily_weather_entries
        WHERE city_id = ? AND date >= ? AND date < date(?, '+7 days')
        ORDER BY date
    '''
    try:
        cursor = connection.cursor()
        rows = cursor.execute(query, (city_id, start_date, start_date)).fetchall()
        return [(r[0], r[1] if r[1] is not None else 0.0) for r in rows]
    except sqlite3.OperationalError as ex:
        print("SQL error in get_7day_precipitation:", ex)
        return []


def plot_7day_precipitation(connection, city_id, start_date):
    data = get_7day_precipitation(connection, city_id, start_date)
    if not data:
        print("No precipitation data to plot.")
        return

    dates = [d for d, _ in data]
    precs = [p for _, p in data]

    plt.figure(figsize=(8,4))
    plt.bar(dates, precs)
    plt.title(f"7-day Precipitation for City {city_id} starting {start_date}")
    plt.xlabel('Date')
    plt.ylabel('Precipitation (mm)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_period_precipitation_for_cities(connection, city_ids, date_from, date_to):
    
    placeholders = ','.join('?' for _ in city_ids)
    query = f'''
        SELECT ci.id, ci.name, SUM(d.precipitation) as total_precip
        FROM daily_weather_entries d
        JOIN cities ci ON d.city_id = ci.id
        WHERE d.date >= ? AND d.date <= ? AND ci.id IN ({placeholders})
        GROUP BY ci.id, ci.name
        ORDER BY total_precip DESC
    '''
    params = [date_from, date_to] + city_ids
    try:
        cursor = connection.cursor()
        rows = cursor.execute(query, params).fetchall()
    except sqlite3.OperationalError as ex:
        print("SQL error in plot_period_precipitation_for_cities:", ex)
        return

    if not rows:
        print("No data returned for the requested cities/period.")
        return

    names = [r[1] for r in rows]
    totals = [r[2] if r[2] is not None else 0.0 for r in rows]

    plt.figure(figsize=(8,4))
    plt.bar(names, totals)
    plt.title(f"Total precipitation {date_from} to {date_to}")
    plt.xlabel('City')
    plt.ylabel('Total Precipitation (mm)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_avg_yearly_precip_by_country(connection, year):
    """Bar chart that shows average precipitation by country for the given year"""
    start = f"{year}-01-01"
    end = f"{year+1}-01-01"
    query = '''
        SELECT co.id, co.name, AVG(d.precipitation) as avg_precip
        FROM daily_weather_entries d
        JOIN cities ci ON d.city_id = ci.id
        JOIN countries co ON ci.country_id = co.id
        WHERE d.date >= ? AND d.date < ?
        GROUP BY co.id, co.name
        ORDER BY avg_precip DESC
    '''
    try:
        cursor = connection.cursor()
        rows = cursor.execute(query, (start, end)).fetchall()
    except sqlite3.OperationalError as ex:
        print("SQL error in plot_avg_yearly_precip_by_country:", ex)
        return

    if not rows:
        print("No precipitation data for the requested year.")
        return

    names = [r[1] for r in rows]
    totals = [r[2] if r[2] is not None else 0.0 for r in rows]

    plt.figure(figsize=(10,5))
    plt.bar(names, totals)
    plt.title(f"Average precipitation by country in {year}")
    plt.xlabel('Country')
    plt.ylabel('Average Precipitation (mm)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_grouped_min_max_mean(connection, entity_ids, date_from, date_to, by='city'):
    """Grouped bar chart displaying min/max/mean temperature and precipitation values for selected cities or countries."""
    if by not in ('city', 'country'):
        raise ValueError("by must be 'city' or 'country'")

    try:
        if by == 'city':
            placeholders = ','.join('?' for _ in entity_ids)
            query = f'''
                SELECT ci.id, ci.name,
                       MIN(d.min_temp) as min_temp,
                       MAX(d.max_temp) as max_temp,
                       AVG(d.mean_temp) as mean_temp,
                       SUM(d.precipitation) as total_precip
                FROM daily_weather_entries d
                JOIN cities ci ON d.city_id = ci.id
                WHERE d.date >= ? AND d.date <= ? AND ci.id IN ({placeholders})
                GROUP BY ci.id, ci.name
            '''
            params = [date_from, date_to] + entity_ids
        else:
            placeholders = ','.join('?' for _ in entity_ids)
            query = f'''
                SELECT co.id, co.name,
                       MIN(d.min_temp) as min_temp,
                       MAX(d.max_temp) as max_temp,
                       AVG(d.mean_temp) as mean_temp,
                       SUM(d.precipitation) as total_precip
                FROM daily_weather_entries d
                JOIN cities ci ON d.city_id = ci.id
                JOIN countries co ON ci.country_id = co.id
                WHERE d.date >= ? AND d.date <= ? AND co.id IN ({placeholders})
                GROUP BY co.id, co.name
            '''
            params = [date_from, date_to] + entity_ids

        cursor = connection.cursor()
        rows = cursor.execute(query, params).fetchall()
    except sqlite3.OperationalError as ex:
        print("SQL error in plot_grouped_min_max_mean:", ex)
        return

    if not rows:
        print("No data returned for grouped plot.")
        return

    labels = [r[1] for r in rows]
    mins = [r[2] if r[2] is not None else 0.0 for r in rows]
    maxs = [r[3] if r[3] is not None else 0.0 for r in rows]
    means = [r[4] if r[4] is not None else 0.0 for r in rows]
    precs = [r[5] if r[5] is not None else 0.0 for r in rows]

    x = list(range(len(labels)))
    width = 0.2

    pos_min = [xi - 1.5 * width for xi in x]
    pos_max = [xi - 0.5 * width for xi in x]
    pos_mean = [xi + 0.5 * width for xi in x]
    pos_prec = [xi + 1.5 * width for xi in x]

    plt.figure(figsize=(10,5))
    plt.bar(pos_min, mins, width, label='Min Temp (°C)')
    plt.bar(pos_max, maxs, width, label='Max Temp (°C)')
    plt.bar(pos_mean, means, width, label='Mean Temp (°C)')
    plt.bar(pos_prec, precs, width, label='Total Precip (mm)')

    plt.xticks(x, labels, rotation=45)
    plt.ylabel('Value')
    plt.title('Grouped min/max/mean temps and precipitation')
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_daily_min_max_for_month(connection, city_id, year, month):
    """multi-line chart showing daily min and max temperature for a given month for a specific city"""
    ym = f"{year:04d}-{month:02d}"
    query = '''
        SELECT date, min_temp, max_temp
        FROM daily_weather_entries
        WHERE city_id = ? AND strftime('%Y-%m', date) = ?
        ORDER BY date
    '''
    try:
        cursor = connection.cursor()
        rows = cursor.execute(query, (city_id, ym)).fetchall()
    except sqlite3.OperationalError as ex:
        print("SQL error in plot_daily_min_max_for_month:", ex)
        return

    if not rows:
        print("No daily temp data for that month/city.")
        return

    dates = [r[0] for r in rows]
    mins = [r[1] if r[1] is not None else 0.0 for r in rows]
    maxs = [r[2] if r[2] is not None else 0.0 for r in rows]

    plt.figure(figsize=(10,5))
    plt.plot(dates, mins, marker='o', label='Min Temp')
    plt.plot(dates, maxs, marker='o', label='Max Temp')
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Daily Min/Max Temperatures for City {city_id} - {ym}')
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_scatter_avg_temp_vs_avg_precip(connection, level='city', date_from=None, date_to=None):
    """Scatter plot of average temperature vs average precipitation.

    level: 'city', 'country', or 'all'
    date_from/date_to optional date range; if omitted, uses all data.
    """
    try:
        cursor = connection.cursor()
        if level == 'city':
            query = '''
                SELECT ci.name, AVG(d.mean_temp) as avg_temp, AVG(d.precipitation) as avg_precip
                FROM daily_weather_entries d
                JOIN cities ci ON d.city_id = ci.id

            '''
            where = ''
            params = []
            if date_from and date_to:
                where = 'WHERE d.date >= ? AND d.date <= ?'
                params = [date_from, date_to]
            query = query + where + ' GROUP BY ci.id, ci.name'
            rows = cursor.execute(query, params).fetchall()
            labels = [r[0] for r in rows]
            temps = [r[1] if r[1] is not None else 0.0 for r in rows]
            precs = [r[2] if r[2] is not None else 0.0 for r in rows]

            plt.figure(figsize=(8,6))
            plt.scatter(temps, precs)
            for i, lab in enumerate(labels):
                plt.annotate(lab, (temps[i], precs[i]))
            plt.xlabel('Average Temperature (°C)')
            plt.ylabel('Average Precipitation (mm)')
            plt.title('Avg Temp vs Avg Precipitation (by city)')
        elif level == 'country':
            query = '''
                SELECT co.name, AVG(d.mean_temp) as avg_temp, AVG(d.precipitation) as avg_precip
                FROM daily_weather_entries d
                JOIN cities ci ON d.city_id = ci.id
                JOIN countries co ON ci.country_id = co.id
            '''
            where = ''
            params = []
            if date_from and date_to:
                where = 'WHERE d.date >= ? AND d.date <= ?'
                params = [date_from, date_to]
            query = query + where + ' GROUP BY co.id, co.name'
            rows = cursor.execute(query, params).fetchall()
            labels = [r[0] for r in rows]
            temps = [r[1] if r[1] is not None else 0.0 for r in rows]
            precs = [r[2] if r[2] is not None else 0.0 for r in rows]

            plt.figure(figsize=(8,6))
            plt.scatter(temps, precs)
            for i, lab in enumerate(labels):
                plt.annotate(lab, (temps[i], precs[i]))
            plt.xlabel('Average Temperature (°C)')
            plt.ylabel('Average Precipitation (mm)')
            plt.title('Avg Temp vs Avg Precipitation (by country)')
        else:  # 'all'
            query = 'SELECT AVG(mean_temp), AVG(precipitation) FROM daily_weather_entries'
            rows = cursor.execute(query).fetchone()
            if not rows:
                print('No data')
                return
            temps = [rows[0]]
            precs = [rows[1]]
            plt.figure(figsize=(6,6))
            plt.scatter(temps, precs)
            plt.xlabel('Average Temperature (°C)')
            plt.ylabel('Average Precipitation (mm)')
            plt.title('Global Avg Temp vs Avg Precipitation')

        plt.tight_layout()
        plt.show()
    except sqlite3.OperationalError as ex:
        print('SQL error in plot_scatter_avg_temp_vs_avg_precip:', ex)


if __name__ == '__main__':
    with sqlite3.connect('CIS4044-N-SDI-OPENMETEO-PARTIAL.db') as conn:

        print(".............PLOT 7-DAY PRECIPITATION FOR A CITY..............")
        City_id = int(input("Enter city ID (e.g., 1): "))
        Start_date = input("Enter start date (YYYY-MM-DD) e.g '2022-01-01': ")
        plot_7day_precipitation(conn, City_id, Start_date)

        print(".............PRECIPITATION FOR TWO CITIES BETWEEN TWO DATES..............")
        City_ids = input("Enter comma-and-space separated city IDs e.g., '[1, 2]': ")
        Date_from = input("Enter start date (YYYY-MM-DD) e.g '2022-01-01': ")
        Date_to = input("Enter end date (YYYY-MM-DD): ")
        plot_period_precipitation_for_cities(conn, City_ids, Date_from, Date_to)

        print(".............AVERAGE YEARLY PRECIPITATION BY COUNTRY..............")
        Year = int(input("Enter year for average yearly precipitation by country (e.g., 2022): "))
        plot_avg_yearly_precip_by_country(conn, Year)

        print(".............GROUPED MIN/MAX/MEAN TEMP AND RAINFALL OF TWO CITIES..............")
        ID = input("Enter comma separated city IDs e.g., '[1,2]': ")
        Start = input("Enter start date (YYYY-MM-DD): ")
        End = input("Enter end date (YYYY-MM-DD): ")
        BY = input("Group by 'city' or 'country'?: ")
        plot_grouped_min_max_mean(conn, ID, Start, End, by=BY)

        print(".............DAILY MIN/MAX TEMPERATURE FOR A CITY IN A MONTH..............")
        city_no = int(input("Enter city ID (e.g., 1): "))
        year = int(input("Enter year (e.g., 2022): "))
        month = int(input("Enter month (1-12): "))
        plot_daily_min_max_for_month(conn, city_no, year, month)

        print(".............SCATTER PLOT OF AVG TEMP VS AVG PRECIPITATION..............")
        level = input("Enter level ('city', 'country', or 'all'): ")
        date_from = input("Enter start date (YYYY-MM-DD) or leave blank for all data: ")
        date_to = input("Enter end date (YYYY-MM-DD) or leave blank for all data: ")
        plot_scatter_avg_temp_vs_avg_precip(conn, level, date_from, date_to)
