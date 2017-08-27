import numpy as np
from mpl_toolkits.basemap import Basemap
from scipy import interpolate
import matplotlib.pyplot as plt


def plot_xyz(x, y, z, xnew, ynew, plot_points):
    plt.figure()
    plt.pcolor(x, y, z)
    plt.pcolormesh(x, y, z)
    plt.contour(x, y, z)
    plt.colorbar()

    if plot_points:
        plt.scatter(plot_points[0], plot_points[1], marker='^', color='red')
        for name, lat, lon in zip(*plot_points):
            plt.annotate(name, (lon, lat))
        # plt.scatter(x, y, marker='^', color='blue')

    plt.title("Initial field")
    plt.savefig('img_00.png')
    # plt.show()

    tck = interpolate.bisplrep(x, y, z, s=0)
    znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

    # znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)
    # tck = interpolate.bisplrep(x, y, z, kx=5, ky=2)
    # znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)
    # znew = interpolate.PPoly.from_spline(xnew[:, 0], ynew[0, :], tck)

    plt.figure()
    plt.pcolormesh(xnew, ynew, znew)
    contour = plt.contour(xnew, ynew, znew, 10, colors='black', linewidths=0.75)
    plt.clabel(contour, inline=1, fontsize=10, fmt='%.1f')
    # xx, yy = np.meshgrid(x, y)
    # contour = m.contour(xx, yy, p, 30, colors='black', linewidths=0.2)
    # plt.clabel(contour, inline=1, fontsize=10, fmt='%.1f')
    plt.colorbar()
    if plot_points:
        plt.scatter(plot_points[0], plot_points[1], marker='^', color='red')
        for name, lat, lon in zip(*plot_points):
            plt.annotate(name, (lon, lat))
    # plt.scatter(x, y, marker='^', color='blue')
    plt.title("Result field")
    plt.savefig('img_01.png')
    # plt.show()


def basemap_plot_xyz(x, y, z):
    max_lat, max_lon, min_lat, min_lon = x.max(), y.max(), x.min(), y.min()
    m = Basemap(projection='cyl', llcrnrlat=min_lat, llcrnrlon=min_lon, urcrnrlat=max_lat, urcrnrlon=max_lon)
    m.pcolor(x, y, z)
    m.pcolormesh(x, y, z)
    m.contour(x, y, z)
    m.colorbar()
    plt.title("Initial field")
    plt.show()

    m = Basemap(projection='cyl', llcrnrlat=min_lat, llcrnrlon=min_lon, urcrnrlat=max_lat, urcrnrlon=max_lon)
    # xnew, ynew = np.mgrid[-1:1:70j, -1:1:70j]
    xnew, ynew = np.meshgrid(x, y)
    tck = interpolate.bisplrep(x, y, z, s=0)
    znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)
    m.pcolormesh(xnew, ynew, znew)
    contour = m.contour(xnew, ynew, znew, colors='black', linewidths=0.75)
    plt.clabel(contour, inline=1, fontsize=10, fmt='%.1f')
    # xx, yy = np.meshgrid(x, y)
    # contour = m.contour(xx, yy, p, 30, colors='black', linewidths=0.2)
    # plt.clabel(contour, inline=1, fontsize=10, fmt='%.1f')
    m.colorbar()
    plt.title("Result field")
    plt.show()


if __name__ == '__main__':
    # lons = np.arange(60, 70, 0.1)
    # lats = np.arange(50, 60, 0.5)
    # lons = np.arange(0, 90, 1)
    # lats = np.arange(30, 50, 0.5)

    # x, y = np.meshgrid(lons, lats)
    # z = (x + y) * np.exp(-6.0 * (x * x + y * y))

    startlon, endlon = 60, 70
    startlat, endlat = 50, 60

    lons = np.arange(startlon, endlon, 0.5)
    lats = np.arange(startlat, endlat, 0.5)

    newlons = np.arange(startlon, endlon, 0.25)
    newlats = np.arange(startlat, endlat, 0.25)

    # x, y = np.mgrid[-1:1:20j, -1:1:10j]
    # x, y = np.mgrid[startlon:1:endlon]
    # xnew, ynew = np.mgrid[-1:1:70j, -1:1:70j]

    # x, y = np.meshgrid(lons, lats)
    # xnew, ynew = np.meshgrid(newlons, newlats)

    # x, y = np.mgrid[-1:1:20j, -1:1:10j]
    # xnew, ynew = np.mgrid[-1:1:70j, -1:1:70j]

    # x, y = np.mgrid[0:len(lons):0.1, 0:len(lats):0.2]
    # xnew, ynew = np.mgrid[0:len(newlons):0.5, 0:len(newlats):0.2]

    x, y = np.mgrid[startlat:endlon:0.5, startlon:endlon:0.5]
    xnew, ynew = np.mgrid[startlat:endlat:0.1, startlon:endlon:0.1]

    print(x.shape)
    print(xnew.shape)
    z = np.zeros(x.shape)

    z[z.shape[0] // 2, z.shape[1] // 2] = 89
    z[z.shape[0] // 2 - 1, 6] = 100
    z[z.shape[0] // 2 - 1, 7] = 80
    z[z.shape[0] // 2 + 1, 5] = 100
    z[z.shape[0] // 2 + 1, 6] = 100
    z[z.shape[0] // 2 - 1, 5] = 10
    z[-1, -1] = -30
    plot_points = []
    plot_xyz(x, y, z, xnew, ynew, plot_points)

    # basemap_plot_xyz(x, y, z)
