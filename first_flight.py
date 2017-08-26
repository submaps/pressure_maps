import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def rename_ds(ds):
    rename_dict = {
        'MSL': 'PMSL',
        'lat': 'XLAT',
        'lon': 'XLONG'
    }
    return ds.rename(rename_dict)


def plot_basemap(lats, lons, p, rect):
    m = Basemap(projection='cyl', llcrnrlat=30, llcrnrlon=-30, urcrnrlat=77, urcrnrlon=60)
    m.drawcoastlines()
    m.bluemarble(alpha=0.42)
    m.drawparallels(np.array([-90, -45, 0, 45, 90]), labels=[1, 0, 0, 0])
    m.drawmeridians(np.array([0, 90, 180, 270, 360]), labels=[0, 0, 0, 1])
    x, y = m(lons, lats)
    max_lat, max_lon, min_lat, min_lon = rect
    p = p / 100
    m.pcolormesh(x, y, p)
    xx, yy = np.meshgrid(x, y)
    contour = m.contour(xx, yy, p, 30, colors='black', linewidths=0.2)
    plt.clabel(contour, inline=1, fontsize=10, fmt='%.1f')
    m.scatter(min_lon, min_lat, color='red', marker='x')
    m.scatter(max_lon, max_lat, color='red', marker='x')
    plt.show()


if __name__ == '__main__':
    print('polar low creator started')
    ifile = r'./era-2008-01-01.nc'
    print(ifile)
    ds = xr.open_dataset(ifile)

    max_lat = 69.13998289252973
    max_lon = 10.615568076095242
    min_lat = 65.56413400146687
    min_lon = 0.5444319239047584

    rect = max_lat, max_lon, min_lat, min_lon
    ds = rename_ds(ds)

    lats = ds['XLAT'].values
    lons = ds['XLONG'].values
    p = ds['PMSL'][0][:, :].values  # get first timestamp

    print('lat: ', min_lat, max_lat)
    print('XLAT: ', lats.min(), lats.max())
    print('lon: ', min_lon, max_lon)
    print('XLONG: ', lons.min(), lons.max())
    print('min p: ', p.min())

    i = np.argmin(p, axis=0)[0]
    j = np.argmin(p, axis=1)[0]
    ans = np.gradient(p)

    print(p[i, j])
    plot_basemap(lats, lons, p, rect)
