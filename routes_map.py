import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from datetime import datetime
import sys


def read_data():
    return pd.read_csv('data/routes.csv', delimiter=','), pd.read_csv('data/airports.csv', delimiter=',')


def draw_map(source_long, source_lat, airports_long, airports_lat, airports_color='b', routes_color='b'):
    date = datetime.utcnow()
    m = Basemap(projection='robin', lon_0=0, lat_0=0)
    m.drawcountries()
    m.drawcoastlines(linewidth=0.5)
    m.drawmapboundary(fill_color=(233 / 255, 246 / 255, 255 / 255, 1))
    m.fillcontinents(color=(197 / 255, 229 / 255, 255 / 255, 1), lake_color=(233 / 255, 246 / 255, 255 / 255, 1))
    m.nightshade(date)

    x, y = m(airports_long, airports_lat)
    m.plot(x, y, airports_color + 'o', markersize=2)

    for dest_long, dest_lat in zip(airports_long, airports_lat):
        m.drawgreatcircle(source_long, source_lat, dest_long, dest_lat, linewidth=0.4, color=routes_color, alpha=0.8)

    source_long, source_lat = m(source_long, source_lat)
    m.plot(source_long, source_lat, marker='D', color='r', markersize=2)

    plt.show()


def main():
    source_airport = sys.argv[1].upper()

    routes_data, airports_data = read_data()

    source_dest_airports = routes_data[
        (routes_data['source_airport'] == source_airport) & (routes_data['destination_airport_id'] != '\\N')][
        'destination_airport_id'].to_numpy(float)

    source_lat = airports_data[airports_data['3_code'] == source_airport].iloc[0, 6]
    source_long = airports_data[airports_data['3_code'] == source_airport].iloc[0, 7]

    airports_long = [airports_data[airports_data['id'] == dest]['long'].to_numpy(dtype=float)[0]
                     for dest in source_dest_airports if len(airports_data[airports_data['id'] == dest]) == 1]

    airports_lat = [airports_data[airports_data['id'] == dest]['lat'].to_numpy(dtype=float)[0]
                    for dest in source_dest_airports if len(airports_data[airports_data['id'] == dest]) == 1]

    draw_map(source_long, source_lat, airports_long, airports_lat)


if __name__ == '__main__':
    main()
