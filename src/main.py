import logging
from utils import update_sheets

logging.basicConfig(level=logging.INFO, filename="Automaton_main.log", filemode="w",
                    format="%(asctime)s 0 %(levelname)s - %(message)s")

def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + ' ' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")

if __name__ == "__main__":
    update_sheets.update_items()
    logging.info("Program successfully completed operation")
