from revelare.utils import load_img, load_wav, write_img, write_wav
from revelare.steganography import extract_message, inject_message, is_valid
import numpy as np
from revelare.gui.main import AppWindow, show_error_box, show_open_file_dialog, show_save_file_dialog

IMAGE_FILE_TYPE = 0
AUDIO_FILE_TYPE = 1


class StegoAppState:
    cover_obj_filename: str
    stego_obj_filename: str
    embed_msg_filename: str
    cover_obj_data: np.ndarray
    stego_obj_data: np.ndarray
    embed_msg_data: np.ndarray
    working_file_type: int = -1

    audio_sample_rate: int


def connect_app_to_state(window: AppWindow, state: StegoAppState):
    window.coverObjInputLabel.clicked.connect(lambda: __load_cover_obj(window, state))
    window.embeddedMsgLabel.clicked.connect(lambda: __load_embed_msg(window, state))
    window.embedBtn.clicked.connect(lambda: __run_embed(window, state))
    window.extractBtn.clicked.connect(lambda: __run_extract(window, state))
    window.stegoObjInputLabel.clicked.connect(lambda: __load_stego_obj(window, state))
    window.stegoObjSaveBtn.clicked.connect(lambda: __save_stego_obj(window, state))


# ----- STATE UPDATE FUNCTIONS ----- #


def __load_cover_obj(window: AppWindow, state: StegoAppState):
    filename = show_open_file_dialog("Image Files (*.png *.bmp);;Audio Files (*.wav)")
    filetype = __check_file_type(filename)

    if filetype == IMAGE_FILE_TYPE:
        state.cover_obj_data = load_img(filename)
        state.working_file_type = IMAGE_FILE_TYPE
    elif filetype == AUDIO_FILE_TYPE:
        state.audio_sample_rate, state.cover_obj_data = load_wav(filename)
        state.working_file_type = AUDIO_FILE_TYPE
    else:
        return

    state.cover_obj_filename = filename
    window.coverObjInputField.setText(filename)

    state.stego_obj_filename = None
    window.stegoObjInputField.setText("No file inserted")
    state.stego_obj_data = None


def __load_embed_msg(window: AppWindow, state: StegoAppState):
    filename = show_open_file_dialog("All Files (*)")
    if len(filename) == 0:
        return

    try:
        f = open(filename, "rb")
    except Exception:
        show_error_box("Cannot read file")

    with f:
        state.embed_msg_data = np.array(list(f.read())).view(np.uint8)

    print(state.embed_msg_data)
    print(state.embed_msg_data.view(np.uint))

    state.embed_msg_filename = filename
    window.embeddedMsgField.setText(filename)

    state.stego_obj_filename = None
    window.stegoObjInputField.setText("No file inserted")
    state.stego_obj_data = None


def __load_stego_obj(window: AppWindow, state: StegoAppState):
    filename = show_open_file_dialog("Image Files (*.png *.bmp);;Audio Files (*.wav)")
    filetype = __check_file_type(filename)

    if filetype == IMAGE_FILE_TYPE:
        state.stego_obj_data = load_img(filename)
        state.working_file_type = IMAGE_FILE_TYPE
    elif filetype == AUDIO_FILE_TYPE:
        state.audio_sample_rate, state.stego_obj_data = load_wav(filename)
        state.working_file_type = AUDIO_FILE_TYPE
    else:
        return

    state.stego_obj_filename = filename
    window.stegoObjInputField.setText(filename)


def __save_stego_obj(window: AppWindow, state: StegoAppState):
    if state.stego_obj_data is None:
        show_error_box("Cannot save file", "No data to write")
        return
    if state.working_file_type == 0:
        filename = show_save_file_dialog("Portable Network Graphics (*.png);;Bitmap File (*.bmp)")
        if len(filename) == 0:
            return
        write_img(state.stego_obj_data, filename)
    elif state.working_file_type == 1:
        filename = show_save_file_dialog("WAV File (*.wav)")
        if len(filename) == 0:
            return
        write_wav(state.stego_obj_data, state.audio_sample_rate, filename)

    state.stego_obj_filename = filename
    window.stegoObjInputField.setText(filename)


def __run_embed(window: AppWindow, state: StegoAppState):
    message = state.embed_msg_data
    data = state.cover_obj_data
    seed = window.get_seed()
    random = window.get_embed_mode() == 1

    if data is None:
        show_error_box("Execution Failure", "No cover object to embed to")
        return

    if not is_valid(data):
        show_error_box("Execution Failure", "Cover object invalid")
        return

    state.stego_obj_data = inject_message(data, message, random=random, seed=seed)


def __run_extract(window: AppWindow, state: StegoAppState):
    data = state.stego_obj_data

    if data is None:
        show_error_box("Execution Failure", "No stego object to extract from")
        return

    print(extract_message(data))
    print(extract_message(data).view(np.uint))

    filename = show_save_file_dialog("All Files (*)")
    if len(filename) == 0:
        return

    try:
        f = open(filename, "wb")
    except Exception:
        show_error_box("Cannot read file")

    with f:
        f.write(bytes(extract_message(data).view(np.uint).tolist()))


# ----- UTILS ----- #


def __check_file_type(filename: str):
    if filename.endswith(".png"):
        return IMAGE_FILE_TYPE
    elif filename.endswith(".bmp"):
        return IMAGE_FILE_TYPE
    elif filename.endswith(".wav"):
        return AUDIO_FILE_TYPE
    else:
        if len(filename) != 0:
            show_error_box("Cannot read file", "This file has an unrecognize file type")
