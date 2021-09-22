from revelare.utils import load_bmp
from revelare.steganography import extract_message, inject_message
from icecream import ic

b = load_bmp("./mocks/bmp/snail.bmp")
img = inject_message(b, "asdas", random=True)
msg = extract_message(img)
ic(msg)
# write_bmp(img, "lol.bmp")
