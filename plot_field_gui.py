#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np
import matplotlib

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QSizePolicy,
        QMenu, QDesktopWidget, QAction, qApp)
from PyQt5.QtGui import QIcon

matplotlib.use('QT5Agg')


class ApplicationWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Plotting fields')

        statusbar = self.statusBar()
        statusbar.showMessage('Ready')
        self.init_menu()

        plot = PlotCanvas()
        self.setCentralWidget(plot)

        self.center()

    def init_menu(self):
        exitAction = QAction(QIcon(''), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)

        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        file_menu.addAction(exitAction)

    def center(self, width=640, height=480):
        self.resize(width, height)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class PlotCanvas(Canvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        Canvas.__init__(self, fig)
        self.setParent(parent)

        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)
        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)

        df_field = pd.read_csv('fromIsoline_field.csv', sep=';')
        x = df_field['Y']
        y = df_field['X']
        z = df_field['Z']

        df_bore = pd.read_csv('fromIsoline_boreholes.csv', sep='\t')
        lons_init = df_bore['X'].values
        lats_init = df_bore['Y'].values
        names = df_bore['Номер'].values

        xnew, ynew = sorted(set(y.values)), sorted(set(x.values))
        xnew, ynew = np.meshgrid(xnew, ynew)
        znew = np.reshape(z, (-1, len(ynew))).T

        xh = xnew.max() - xnew.min()
        yh = ynew.max() - ynew.min()

        lonh = lons_init.max() - lons_init.min()
        lath = lats_init.max() - lats_init.min()

        lons = (lons_init - lons_init.min()) / lonh * xh + xnew.min()
        lats = (lats_init - lats_init.min()) / lath * yh + ynew.min()

        pc = ax.pcolor(xnew, ynew, znew)
        c = ax.contour(xnew, ynew, znew, 15, linewidths=0.75, colors='black')

        ax.clabel(c, inline=1, fontsize=7, fmt='%.1f')
        self.figure.colorbar(pc)
        ax.scatter(lons, lats, marker='^', color='red', zorder=100)

        for lat, lon, name in zip(lats, lons, names):
            ax.annotate(name, (lon, lat))

        n = 7
        m = 5
        yticks = np.linspace(ynew.min(), ynew.max(), n)
        xticks = np.linspace(xnew.min(), xnew.max(), m)

        yticklabels = np.round( np.linspace(lats_init.min(), lats_init.max(), n), 2)
        xticklabels = np.round( np.linspace(lons_init.min(), lons_init.max(), m), 2)

        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ApplicationWindow()
    ex.show()
    sys.exit(app.exec_())
