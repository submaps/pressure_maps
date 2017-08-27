import pandas as pd
from geopy.distance import vincenty

from example import plot_xyz, basemap_plot_xyz
from first_flight import plot_basemap
import numpy as np
from scipy import interpolate

# def sub_interpolate(z, x, y):
#     x_ = np.arange(x.min(), x.max(), 0.01)
#     y_ = np.arange(y.min(), y.max(), 0.01)
#     xnew, ynew = np.meshgrid(x_, y_)
#     f = interpolate.interp2d(x, y, z, kind='cubic')
#     return f(x_, y_), x_, y_


if __name__ == '__main__':
    ifile = r'fromIsoline.csv'
    df = pd.read_csv(ifile, sep='\t')
    lons_init = df['X'].values
    lats_init = df['Y'].values
    names = df['Номер'].values
    p_init = df['Забой'].values
    min_lon, max_lon = lons_init.min(), lons_init.max()
    min_lat, max_lat = lats_init.min(), lats_init.max()

    rect = max_lat, max_lon, min_lat, min_lon
    print(min_lon, min_lat)
    print(max_lon, max_lat)
    print(rect)

    step = 0.025
    sstep = step / 2

    lats = np.arange(min_lat, max_lat, step)
    lons = np.arange(min_lon, max_lon, step)

    x, y = np.mgrid[min_lat:max_lat:step, min_lon:max_lon:step]
    xnew, ynew = np.mgrid[min_lat:max_lat:sstep, min_lon:max_lon:sstep]

    z = np.zeros(x.shape)
    print(x.shape, y.shape, z.shape)
    stations_list = []
    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            for name, plat, plon, p in zip(names, lats, lons, p_init):
                d = vincenty((lat, lon), (plat, plon)).km
                print('\t\td=', d)
                try:
                    if d < 0.01 and z[i, j] == 0:
                        # plot_points[name] = (lon, lat)
                        z[i, j] = int(p)
                        stations_list.append(name)

                except:
                    print('@@@@@@@@@@@@@@@@', i, j)

    # plot_points = [lats, lons, names]
    print('missed stations: ', set(stations_list)-set(names))
    plot_points = [lats_init, lons_init, names]
    plot_xyz(x, y, z, xnew, ynew, plot_points)
    # basemap_plot_xyz(x, y, z)
