from icecream import ic
from revelare.gui.main import AppWindow
from revelare.gui.steganography import StegoAppState, connect_app_to_state
from revelare.utils import load_wav

from PyQt5.QtWidgets import QApplication


class RevelareApplication(AppWindow):
    stego_state = StegoAppState()

    def __init__(self) -> None:
        super().__init__()

        self.connect_buttons()

    def connect_buttons(self):
        connect_app_to_state(self, self.stego_state)


def window():
    import sys

    app = QApplication(sys.argv)
    win = RevelareApplication()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()
