from PyQt5.QtCore import QMetaObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QMainWindow,
    QPushButton,
    QSpacerItem,
    QTabWidget,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
)


class AppWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.resize(800, 600)

        font = QFont()
        font.setFamily("Segoe UI")
        self.setFont(font)

        self.init_ui()

    def init_ui(self):
        # ==== INIT ====
        self.mainWidget = QTabWidget(self)
        self.tab1 = QWidget()
        self.mainWidget.addTab(self.tab1, "RC4 Encryption")
        self.tab2 = QWidget()
        self.mainWidget.addTab(self.tab2, "Stefanosaurus")

        # ==== RC4 TAB ====

        # ==== Stego TAB ====
        self.horizontalLayout = QHBoxLayout(self.tab2)

        # -- Left Column --
        self.coverLayoutWidget = QWidget(self.mainWidget)
        self.coverObjLayout = QVBoxLayout(self.coverLayoutWidget)
        self.coverObjLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.addWidget(self.coverLayoutWidget)

        # Column Title
        self.coverLayoutTitle = QLabel(self.coverLayoutWidget)
        self.coverLayoutTitle.setText(
            '<html><head/><body><p align="center">'
            '<span style=" font-size:12pt; font-weight:600;">Cover Object & Embedded Message</span>'
            "</p></body></html>"
        )
        self.coverObjLayout.addWidget(self.coverLayoutTitle)

        # Object Frame
        self.coverObjectFrame = QFrame(self.coverLayoutWidget)
        self.coverObjectFrame.setFrameShape(QFrame.StyledPanel)
        self.coverObjectFrame.setFrameShadow(QFrame.Plain)
        self.coverObjectFrame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.coverObjLayout.addWidget(self.coverObjectFrame)

        # Form
        self.coverFormWidget = QWidget(self.coverLayoutWidget)
        self.coverFormLayout = QFormLayout(self.coverFormWidget)
        self.coverFormLayout.setContentsMargins(0, 0, 0, 0)
        self.coverObjLayout.addWidget(self.coverFormWidget)

        # Load File Input
        self.coverObjInputLabel = QPushButton("Load File", self.coverFormWidget)
        self.coverObjInputField = QLabel("No file inserted", self.coverFormWidget)
        self.coverObjInputField.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.coverObjInputField.setWordWrap(True)
        self.coverFormLayout.setWidget(0, QFormLayout.LabelRole, self.coverObjInputLabel)
        self.coverFormLayout.setWidget(0, QFormLayout.FieldRole, self.coverObjInputField)

        # Save File Button
        self.coverObjSaveBtn = QPushButton("Save File", self.coverFormWidget)
        self.coverFormLayout.setWidget(1, QFormLayout.LabelRole, self.coverObjSaveBtn)

        self.tempSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.coverObjLayout.addItem(self.tempSpacer)

        # -- Middle Column --
        self.settingWidget = QWidget(self.mainWidget)
        self.settingWidget.setMaximumWidth(100)
        self.settingLayout = QVBoxLayout(self.settingWidget)
        self.settingLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.addWidget(self.settingWidget)

        self.tempSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.settingLayout.addItem(self.tempSpacer)

        # Embed Button
        self.embedBtn = QPushButton("--Embed->", self.settingWidget)
        self.settingLayout.addWidget(self.embedBtn)

        # Extract Button
        self.extractBtn = QPushButton("<-Extract--", self.settingWidget)
        self.settingLayout.addWidget(self.extractBtn)

        # Enkripsi / not
        self.stegoEncryptField = QCheckBox("Encrypt", self.settingWidget)
        self.settingLayout.addWidget(self.stegoEncryptField)

        # Sequential / Random
        self.embedModeLabel = QLabel("Mode", self.settingWidget)
        self.settingLayout.addWidget(self.embedModeLabel)
        self.embedModeField = QComboBox(self.settingWidget)
        self.embedModeField.addItem("Sequential")
        self.embedModeField.addItem("Dispersed")
        self.settingLayout.addWidget(self.embedModeField)

        self.tempSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.settingLayout.addItem(self.tempSpacer)

        # -- Right Column --
        self.stegoLayoutWidget = QWidget(self.mainWidget)
        self.stegoObjLayout = QVBoxLayout(self.stegoLayoutWidget)
        self.stegoObjLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.addWidget(self.stegoLayoutWidget)

        # Column Title
        self.stegoLayoutTitle = QLabel(self.stegoLayoutWidget)
        self.stegoLayoutTitle.setText(
            '<html><head/><body><p align="center">'
            '<span style=" font-size:12pt; font-weight:600;">Cover Object & Embedded Message</span>'
            "</p></body></html>"
        )
        self.stegoObjLayout.addWidget(self.stegoLayoutTitle)

        # Object Frame
        self.stegoObjectFrame = QFrame(self.stegoLayoutWidget)
        self.stegoObjectFrame.setFrameShape(QFrame.StyledPanel)
        self.stegoObjectFrame.setFrameShadow(QFrame.Plain)
        self.stegoObjectFrame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.stegoObjLayout.addWidget(self.stegoObjectFrame)

        # Form
        self.stegoFormWidget = QWidget(self.stegoLayoutWidget)
        self.stegoFormLayout = QFormLayout(self.stegoFormWidget)
        self.stegoFormLayout.setContentsMargins(0, 0, 0, 0)
        self.stegoObjLayout.addWidget(self.stegoFormWidget)

        # Load File Input
        self.stegoObjInputLabel = QPushButton("Load File", self.stegoFormWidget)
        self.stegoObjInputField = QLabel("No file inserted", self.stegoFormWidget)
        self.stegoObjInputField.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.stegoObjInputField.setWordWrap(True)
        self.stegoFormLayout.setWidget(0, QFormLayout.LabelRole, self.stegoObjInputLabel)
        self.stegoFormLayout.setWidget(0, QFormLayout.FieldRole, self.stegoObjInputField)

        # Save File Button
        self.stegoObjSaveBtn = QPushButton("Save File", self.stegoFormWidget)
        self.stegoFormLayout.setWidget(1, QFormLayout.LabelRole, self.stegoObjSaveBtn)

        self.tempSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.stegoObjLayout.addItem(self.tempSpacer)

        self.setCentralWidget(self.mainWidget)

        QMetaObject.connectSlotsByName(self)


def window():
    import sys

    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()
