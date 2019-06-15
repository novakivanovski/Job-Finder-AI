from Storage.config import logging_config
from UI.CLI import CLI


if __name__ == '__main__':
    logging_config.setup_logger('run.log')
    interface = CLI()




