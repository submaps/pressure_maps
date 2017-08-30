import pandas as pd
from geopy.distance import vincenty
from scipy import ndimage

from plot_artist import plot_xyz, basemap_plot_xyz
import numpy as np


def get_nearest_ij(name, plat, plon, lats, lons):
    ijd_list = []
    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            d = vincenty((lat, lon), (plat, plon)).km
            ijd_list.append([i, j, d])
            if d < 0.5 and z[i, j] == 0:
                print(name, plat, plon, d)
                return i, j
    i, j, d = min(ijd_list, key=lambda x: x[2])
    return i, j

if __name__ == '__main__':
    ifile = r'fromIsoline_boreholes.csv'
    df = pd.read_csv(ifile, sep='\t')
    lons_init = df['Y'].values
    lats_init = df['X'].values
    names = df['Номер'].values
    p_init = df['Забой'].values
    min_lon, max_lon = lons_init.min(), lons_init.max()
    min_lat, max_lat = lats_init.min(), lats_init.max()

    max_lon += 0.025
    max_lat += 0.025

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
    # z = np.full(x.shape, p_init.mean())
    print(x.shape, y.shape, z.shape)

    for name, plat, plon, p in zip(names, lats_init, lons_init, p_init):
        try:
            i, j = get_nearest_ij(name, plat, plon, lats, lons)
            z[i, j] = int(p)
            print('-'*10, p)
        except TypeError as te:
            print('@@@@@@@@', name, plat, plon)

    # z = ndimage.gaussian_filter(z, sigma=0.1)
    plot_points = [lats_init, lons_init, names]
    plot_xyz(x, y, z, xnew, ynew, plot_points, rect)
