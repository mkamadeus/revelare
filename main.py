from revelare.utils import load_wav
from icecream import ic

b = load_wav("./mocks/wav/lounge.wav")
ic(b[1].mean())
