import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_field(x, y, z, lons, lats, names, lons_labels, lats_labels):
    plt.figure()
    pc = plt.pcolor(x, y, z)
    # pc = plt.pcolor(x, y, z, cmap='RdYlBu')
    c = plt.contour(x, y, z, 15, linewidths=0.75, colors='black')
    plt.clabel(c, inline=1, fontsize=7, fmt='%.1f')
    plt.colorbar(pc)
    plt.scatter(lons, lats, marker='^', color='red', zorder=100)

    for lat, lon, name in zip(lats, lons, names):
        plt.annotate(name, (lon, lat))

    n = 7
    m = 5

    y_ticks = np.linspace(y.min(), y.max(), n)
    x_ticks = np.linspace(x.min(), x.max(), m)

    y_ticks_labels = np.round(np.linspace(lats_labels.min(), lats_labels.max(), n), 3)
    x_ticks_labels = np.round(np.linspace(lons_labels.min(), lons_labels.max(), m), 3)

    plt.yticks(y_ticks, y_ticks_labels)
    plt.xticks(x_ticks, x_ticks_labels)

    plt.title("Initial field")
    # plt.savefig('img_plot_field00.png')
    plt.show()


if __name__ == '__main__':
    field_file = r'fromIsoline_field.csv'
    df_field = pd.read_csv(field_file, sep=';')
    x = df_field['Y']
    y = df_field['X']
    z = df_field['Z']

    bore_file = r'fromIsoline_boreholes.csv'
    df_bore = pd.read_csv(bore_file, sep='\t')
    lons_init = df_bore['X'].values
    lats_init = df_bore['Y'].values
    names = df_bore['Номер'].values

    # xnew = np.linspace(x.min(), x.max(), 441)
    # ynew = np.linspace(y.min(), y.max(), 437)

    xnew, ynew = sorted(set(y.values)), sorted(set(x.values))

    xnew, ynew = np.meshgrid(xnew, ynew)
    znew = np.reshape(z, (-1, len(ynew))).T

    xh = xnew.max() - xnew.min()
    yh = ynew.max() - ynew.min()

    lonh = lons_init.max() - lons_init.min()
    lath = lats_init.max() - lats_init.min()

    lons = (lons_init - lons_init.min()) / lonh * (xnew.max()-xnew.min()) + xnew.min()
    lats = (lats_init - lats_init.min()) / lath * (ynew.max()-ynew.min()) + ynew.min()
    plot_field(xnew, ynew, znew, lons, lats, names, lons_init, lats_init)
