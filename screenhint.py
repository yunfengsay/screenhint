from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPixmap, QScreen
from PyQt5.QtCore import Qt, QRect, QPoint

class FloatingScreenshot(QWidget):
    def __init__(self, pixmap):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.label.setPixmap(pixmap)
        self.show()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        self.close()

class ScreenshotTool(QWidget):
    def __init__(self, parent=None):
        super(ScreenshotTool, self).__init__(parent)
        self.start = None
        self.end = None
        self.setWindowOpacity(0.4)
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        self.start = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.hide()
        QApplication.processEvents()
        screenshot = QApplication.primaryScreen().grabWindow(0)
        rect = QRect(self.start, self.end).normalized()
        screenshot = screenshot.copy(rect)
        self.floating = FloatingScreenshot(screenshot)
        self.close()

    def paintEvent(self, event):
        if self.start is not None and self.end is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QColor(255, 255, 255, 0))
            painter.drawRect(self.rect())
            painter.setBrush(QColor(255, 255, 255, 255))
            painter.drawRect(QRect(self.start, self.end))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    screenshot_tool = ScreenshotTool()
    screenshot_tool.showFullScreen()
    sys.exit(app.exec_())
