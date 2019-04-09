from PyQt5.QtWidgets import (   QWidget, QPlainTextEdit,
                                QHBoxLayout, QSizePolicy)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ResponseTab(QWidget):
    """
    Tab for response information.
    """
    def __init__(self, parent, database_api, selection_manager):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.selection_manager = selection_manager
        self.database_api = database_api
        self.instrument_id = -1
        self.textBox = QPlainTextEdit()
        self.textBox.setStyleSheet("background: white")
        self.textBox.setReadOnly(True)

        self.response_plotter = ResponsePlotter(self)

        self.updateResponseTab(self.instrument_id)
        self.response_plotter.plot(None)
        self.layout.addWidget(self.textBox)
        self.layout.addWidget(self.response_plotter)

    def updateResponseTab(self, instrument_id):
        """
        Function for updating the ResponseTab
        """
        self.instrument_id = instrument_id
        if (self.instrument_id == -1):
            self.textBox.setPlainText("No instrument chosen!")
        else:
            resp = self.database_api.getResponse(self.instrument_id)
            if resp is None:
                return
            self.textBox.setPlainText(str(resp))
            self.response_plotter.plot(resp)

class ResponsePlotter(FigureCanvas):
    """
    Class for plotting the response with matplotlib
    """
    def __init__(self, parent):
        self.figs, self.axs = plt.subplots(2, 1)
        FigureCanvas.__init__(self, self.figs)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, response):
        """
        Plot the response
        """
        self.axs[0].clear()
        self.axs[1].clear()

        if response is None:
            self.draw()
            return

        if response.response_format == 'paz':
            z = [complex(zero[0], zero[1]) for zero in response.zeros]
            p = [complex(pole[0], pole[1]) for pole in response.poles]

            a_0 = response.scale_factor

            f_bode1 = np.logspace(-3, 2)
            f_bode2 = np.logspace(3, 0)

            s_bode1 = 2 * np.pi * f_bode1 * 1j
            s_bode2 = 2 * np.pi * f_bode2 * 1j

            h_bode1 = a_0 * np.prod([s_bode1 - zi for zi in z], axis = 0) / np.prod([s_bode1 - pi for pi in p], axis=0)
            h_bode2 = a_0 * np.prod([s_bode2 - zi for zi in z], axis = 0) / np.prod([s_bode2 - pi for pi in p], axis=0)

            self.axs[0].loglog(f_bode1,np.abs(h_bode1))
            self.axs[0].set_xlabel('Hz')
            self.axs[0].set_ylabel('Disp [nm/count]')
            self.axs[0].grid(b=True, which='minor', color='r', linestyle='--')

            self.axs[1].semilogx(f_bode2, np.degrees(np.angle(h_bode2)))
            self.axs[1].set_xlabel('Hz')
            self.axs[1].set_ylabel(u'Phase [°]')
            self.axs[1].set_ylim([-180,180])
            self.axs[1].grid(b = True, color = 'r', linestyle = '--')
            self.draw()

        elif response.response_format == 'fap':
            f_bode1 = np.logspace(-3, 2)
            f_bode2 = np.logspace(3, 0)

            disp = []
            phase = []
            freq = []
            for fap in response.fap:
                freq.append(fap[0])
                disp.append(fap[1])
                phase.append(fap[2])

            self.axs[0].loglog(freq, disp)
            self.axs[0].set_xlabel('Hz')
            self.axs[0].set_ylabel('Disp [nm/count]')
            self.axs[0].grid(b=True, which='minor', color='r', linestyle='--')
