import numpy as np
from revelare.cryptography import crypt_byte, str_to_ndarray
from revelare.gui.main import AppWindow, show_open_file_dialog, show_save_file_dialog


class CryptoAppState:
    text_bytes: np.ndarray = None
    result_bytes: np.ndarray = None


def connect_cryptography(window: AppWindow, state: CryptoAppState):
    window.rc4KeyLineEdit.textChanged.connect(lambda: __crypto_refresh(window, state))
    window.MessageField.textChanged.connect(lambda: __crypto_refresh(window, state))
    window.messageLoadBtn.clicked.connect(lambda: __load_file(window, state))
    window.resultSaveBtn.clicked.connect(lambda: __save_file(window, state))


# ----- STATE UPDATE FUNCTIONS ----- #


def __crypto_refresh(window: AppWindow, state: CryptoAppState):
    # Update state
    state.text_bytes = str_to_ndarray(window.MessageField.toPlainText())

    # Encrypt/Decrypt
    result = crypt_byte(state.text_bytes, str_to_ndarray(window.rc4KeyLineEdit.text()))

    # Update permutation table
    for i in range(256):
        window.permutationLineEdit[i].setText(str(result["perm"][i]))
        window.permutationLineEdit[i].setStyleSheet("border: 1px solid black")
    window.permutationLineEdit[result["keystream_obj"]["latest-i"]].setStyleSheet(
        "border: 3px solid green;"
    )
    window.permutationLineEdit[result["keystream_obj"]["latest-j"]].setStyleSheet(
        "border: 3px solid blue;"
    )
    window.permutationLineEdit[result["keystream_obj"]["latest-t"]].setStyleSheet(
        "border: 3px solid red;"
    )
    perm_i = window.permutationLineEdit[result["keystream_obj"]["latest-i"]].text()
    perm_j = window.permutationLineEdit[result["keystream_obj"]["latest-j"]].text()
    perm_t = window.permutationLineEdit[result["keystream_obj"]["latest-t"]].text()
    window.explanationLabel.setText(
        '<html><head/><body><p align="center">'
        "<span style=\" color:'green';\">i = "
        + str(result["keystream_obj"]["latest-i"])
        + "</span>"
        "<span> dan </span>"
        "<span style=\" color:'blue';\">j = "
        + str(result["keystream_obj"]["latest-j"])
        + "</span>"
        "<span> menyebabkan </span>"
        "<span style=\" color:'red';\">t = perm[i] + perm[j] = "
        + perm_i
        + " + "
        + perm_j
        + " = "
        + str(result["keystream_obj"]["latest-t"])
        + "</span>"
        "<span> sehingga menghasilkan karakter keystream perm[t] = chr("
        + perm_t
        + ") = "
        + chr(int(perm_t))
        + "</span>"
        "</p></body></html>"
    )

    # Update keystream and result
    window.KeystreamField.setText(result["keystream"])
    window.ResultField.setText(result["result"])

    # Update state
    state.result_bytes = result["result_byte"]


def __load_file(window: AppWindow, state: CryptoAppState):
    filename = show_open_file_dialog()
    if len(filename) == 0:
        return
    if window.textRadioBtn.isChecked():
        with open(filename, "r", encoding="utf-8", errors="replace") as file:
            isi = file.read()
            # print(isi)
            window.MessageField.setText(isi)
            file.close()
    else:
        with open(filename, "rb") as file:
            isi = file.read()
            window.MessageField.setText("".join(map(chr, isi)))
            file.close()


def __save_file(window: AppWindow, state: CryptoAppState):
    filename = show_save_file_dialog()
    if len(filename) == 0:
        return
    if window.textRadioBtn.isChecked():
        with open(filename, "w", encoding="utf-8", errors="replace") as file:
            file.write(window.ResultField.toPlainText())
            file.close()
    else:
        with open(filename, "wb") as file:
            file.write(state.result_bytes)
            file.close()
