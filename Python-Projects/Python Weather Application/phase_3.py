# Author: Daniel Teriv Adamu
# Student ID: F5101328

import requests
import sqlite3

DB_NAME = "CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
TIMEZONE = "Europe/London"

def ensure_daily_table(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS daily_weather_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            city_id INTEGER NOT NULL,
            min_temp REAL,
            max_temp REAL,
            mean_temp REAL,
            precipitation REAL
        )
    ''')
    conn.commit()


def fetch_archive_daily(lat, lon, start_date, end_date, timezone=TIMEZONE):
    params = {
        'latitude': lat,
        'longitude': lon,
        'start_date': start_date,
        'end_date': end_date,
        'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
        'temperature_unit': 'celsius',
        'precipitation_unit': 'mm',
        'timezone': timezone
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print('Request error:', e)
        return None


def insert_daily_entries(conn: sqlite3.Connection, city_id: int, daily_json: dict):
    if not daily_json or 'daily' not in daily_json:
        return 0
    daily = daily_json['daily']
    times = daily.get('time', [])
    tmax = daily.get('temperature_2m_max', [])
    tmin = daily.get('temperature_2m_min', [])
    precip = daily.get('precipitation_sum', [])

    rows = []
    for i, d in enumerate(times):
        mx = tmax[i] if i < len(tmax) else None
        mn = tmin[i] if i < len(tmin) else None
        pr = precip[i] if i < len(precip) else None
        mean = None
        if mx is not None and mn is not None:
            mean = (mx + mn) / 2.0
        rows.append((d, city_id, mn, mx, mean, pr))

    cur = conn.cursor()
    cur.executemany('''
        INSERT INTO daily_weather_entries (date, city_id, min_temp, max_temp, mean_temp, precipitation)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', rows)
    conn.commit()
    return cur.rowcount


def load_cities_from_db(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT id, name, latlong FROM cities")
    return cur.fetchall()


def main():
    print('This script will fetch daily archive data from Open-Meteo and store into your local DB.')
    db = DB_NAME
    start_date = input('Enter start date (YYYY-MM-DD): ').strip()
    end_date = input('Enter end date (YYYY-MM-DD): ').strip()
    if not start_date or not end_date:
        print('Start and end dates are required. Exiting.')
        return

    try:
        with sqlite3.connect(db) as conn:
            ensure_daily_table(conn)
            cities = load_cities_from_db(conn)
            if not cities:
                print('No cities found in the local `cities` table. Populate cities first.')
                return
            total = 0
            for cid, name, latlong in cities:
                try:
                    lat_str, lon_str = latlong.split(',')
                    lat = float(lat_str.strip())
                    lon = float(lon_str.strip())
                except Exception:
                    print(f'Skipping city {name} (id={cid}) due to invalid latlong: {latlong}')
                    continue

                print(f'Fetching {name} ({lat},{lon}) from {start_date} to {end_date}...')
                data = fetch_archive_daily(lat, lon, start_date, end_date, timezone=TIMEZONE)
                if data:
                    inserted = insert_daily_entries(conn, cid, data)
                    print(f'Inserted {inserted} rows for city {name} (id={cid})')
                    total += inserted
                else:
                    print(f'No data for city {name} (id={cid})')

            print(f'Completed. Total rows inserted: {total}')
    except Exception as e:
        print('Error:', e)


if __name__ == '__main__':
    main()