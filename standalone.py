import sys

from PyQt5.QtCore import (
    QSize,
    Qt,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from src.dxf2plasmac.dxf_to_plasmac_gui import dxfGui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('dxf2QtPlasmaC')
        self.resize(1000, 650)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.dxf_gui = dxfGui('metric', '#004080')
        self.layout.addWidget(self.dxf_gui)
        self.dxf_gui.D2P.lead_type = 'arc'
        self.dxf_gui.D2P.lead_length = 3.0
        self.dxf_gui.D2P.last_cut = (0.0, 0.0)
        self.dxf_gui.D2P.flattening_distance = 0.025
        self.dxf_gui.D2P.gap_tolerance = 0.001
        self.dxf_gui.D2P.lead_angle = 45
        self.dxf_gui.D2P.precision = 2
        self.dxf_gui.D2P.small_hole = 32
        self.dxf_gui.shape_color = Qt.darkYellow#'#808080'#Qt.black
        self.dxf_gui.rapid_color = Qt.gray
        self.dxf_gui.leadin_color = Qt.cyan
        self.dxf_gui.cut_color_external = Qt.red
        self.dxf_gui.cut_color_internal = Qt.green
        self.dxf_gui.invalid_color  = Qt.magenta
        self.dxf_gui.cross_marker_color = Qt.red
        self.dxf_gui.load_material_file('test/test_material.cfg')
        self.dxf_gui.sidebar_container.setFixedWidth(190)
        self.dxf_gui.menu_width = 160

# example ***********************************
#  add a tool button to the toolbar
#  click the button to hide dxf2plasmac
#  click the empty window to restore dxf2plasmac
#
        icon = self.style().standardIcon(QStyle.SP_DialogCancelButton)
        b = QToolButton()
        # b.setText('B')
        b.setFixedSize(32, 32)
        b.setIcon(icon)
        b.setIconSize(QSize(28, 28))
        b.clicked.connect(self.example)
        # self.dxf_gui.toolbar.insertWidget(10, b)
        # self.dxf_gui.toolbar.insertSpacing(11, 24)
        self.dxf_gui.toolbar.addStretch()
        self.dxf_gui.toolbar.addWidget(b)

    def example(self):
#         self.dxf_gui.hide()
        self.quit()
#
#     @override
#     def mousePressEvent(self, a0):
#         self.dxf_gui.show()
#         super().mousePressEvent(a0)
#*****************************************************************************

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
