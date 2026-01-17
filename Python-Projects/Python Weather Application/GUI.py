import sqlite3
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import phase_3
import phase_2
import phase_1

DB_DEFAULT = 'CIS4044-N-SDI-OPENMETEO-PARTIAL.db'

def get_cities(db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            rows = phase_1.select_all_cities(conn)
            if not rows:
                return []
            return [(row['id'], row['name']) for row in rows]
    except Exception:
        return []


def parse_id_list(s):
    s = s.strip().strip('[]')
    parts = s.replace(',', ',').split(',') if s else []
    ids = []
    for p in parts:
        try:
            ids.append(int(p))
        except ValueError:
            continue
    return ids

class WeatherGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Daniel's Weather Data Application")
        self.geometry('720x380')

        # The DB path
        tk.Label(self, text='DB Path:').grid(row=0, column=0, sticky='w', padx=6, pady=6)
        self.db_var = tk.StringVar(value=DB_DEFAULT)
        tk.Entry(self, textvariable=self.db_var, width=80).grid(row=0, column=1, columnspan=3, padx=6, pady=6)

        # Cities dropdown
        tk.Label(self, text='City:').grid(row=1, column=0, sticky='w', padx=6)
        self.city_combo = ttk.Combobox(self, values=[], state='readonly')
        self.city_combo.grid(row=1, column=1, sticky='w', padx=6)

        tk.Button(self, text='Refresh Cities', command=self.load_cities).grid(row=1, column=2, padx=6)

        # Dates and timezone
        tk.Label(self, text='Start Date (YYYY-MM-DD):').grid(row=2, column=0, sticky='w', padx=6)
        self.start_var = tk.StringVar()
        tk.Entry(self, textvariable=self.start_var).grid(row=2, column=1, sticky='w', padx=6)

        tk.Label(self, text='End Date (YYYY-MM-DD):').grid(row=2, column=2, sticky='w', padx=6)
        self.end_var = tk.StringVar()
        tk.Entry(self, textvariable=self.end_var).grid(row=2, column=3, sticky='w', padx=6)

        tk.Label(self, text='Timezone:').grid(row=3, column=0, sticky='w', padx=6, pady=6)
        self.tz_var = tk.StringVar(value='Europe/London')
        tk.Entry(self, textvariable=self.tz_var).grid(row=3, column=1, sticky='w', padx=6)

        # Actions
        tk.Button(self, text='Fetch & Store For City', command=self.on_fetch).grid(row=4, column=0, padx=6, pady=12)
        tk.Button(self, text='Plot 7-day Precip', command=self.on_plot_7day).grid(row=4, column=1, padx=6)
        tk.Button(self, text='Plot Period Precip (IDs)', command=self.on_plot_period).grid(row=4, column=2, padx=6)

        tk.Label(self, text='City IDs for period (e.g. 1,2):').grid(row=5, column=0, sticky='w', padx=6)
        self.ids_var = tk.StringVar()
        tk.Entry(self, textvariable=self.ids_var).grid(row=5, column=1, sticky='w', padx=6)

        # Status bar
        self.status = tk.StringVar(value='Ready')
        tk.Label(self, textvariable=self.status, anchor='w').grid(row=6, column=0, columnspan=4, sticky='we', padx=6, pady=8)

        self.load_cities()

    def load_cities(self):
        db = self.db_var.get()
        cities = get_cities(db)
        display = [f"{c[0]}: {c[1]}" for c in cities]
        self.city_map = {f"{c[0]}: {c[1]}": c[0] for c in cities}
        self.city_combo['values'] = display
        if display:
            self.city_combo.current(0)
        self.status.set(f'Loaded {len(display)} cities')

    def on_fetch(self):
        sel = self.city_combo.get()
        if not sel:
            messagebox.showwarning('No city', 'Please select a city')
            return
        city_id = self.city_map.get(sel)
        start = self.start_var.get()
        end = self.end_var.get()
        tz = self.tz_var.get()
        if not start or not end or not tz:
            messagebox.showwarning('Missing fields', 'Please provide start date, end date and timezone')
            return

        def worker():
            self.status.set('Fetching...')
            try:
                with sqlite3.connect(self.db_var.get()) as conn:
                    # lookup latlong for the selected city id
                    cur = conn.cursor()
                    cur.execute('SELECT latlong FROM cities WHERE id = ?', (city_id,))
                    row = cur.fetchone()
                    if not row:
                        raise RuntimeError(f'City id {city_id} not found in DB')
                    latlong = row[0]
                    lat_str, lon_str = latlong.split(',')
                    lat = float(lat_str.strip())
                    lon = float(lon_str.strip())

                    data = phase_3.fetch_archive_daily(lat, lon, start, end, timezone=tz)
                    if not data:
                        raise RuntimeError('No data returned from Open-Meteo')
                    inserted = phase_3.insert_daily_entries(conn, city_id, data)

                self.status.set(f'Fetch complete: inserted {inserted} rows')
                messagebox.showinfo('Fetch complete', f'Inserted {inserted} rows')
            except Exception as e:
                self.status.set('Fetch failed')
                messagebox.showerror('Error', str(e))

        threading.Thread(target=worker, daemon=True).start()

    def on_plot_7day(self):
        sel = self.city_combo.get()
        if not sel:
            messagebox.showwarning('No city', 'Please select a city')
            return
        city_id = self.city_map.get(sel)
        start = self.start_var.get()
        if not start:
            messagebox.showwarning('Missing start date', 'Please provide a start date')
            return
        try:
            with sqlite3.connect(self.db_var.get()) as conn:
                phase_2.plot_7day_precipitation(conn, city_id, start)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def on_plot_period(self):
        ids = parse_id_list(self.ids_var.get())
        if not ids:
            messagebox.showwarning('No IDs', 'Please enter one or more city IDs (e.g. 1,2)')
            return
        start = self.start_var.get()
        end = self.end_var.get()
        if not start or not end:
            messagebox.showwarning('Missing dates', 'Please provide start and end dates')
            return
        try:
            with sqlite3.connect(self.db_var.get()) as conn:
                phase_2.plot_period_precipitation_for_cities(conn, ids, start, end)
        except Exception as e:
            messagebox.showerror('Error', str(e))


if __name__ == '__main__':
    app = WeatherGUI()
    app.mainloop()