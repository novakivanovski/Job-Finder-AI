from UI import UI
from multiprocessing import freeze_support
import logging

if __name__ == '__main__':
    freeze_support()
    logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)
    g = UI()


