import logging
from colorlog import ColoredFormatter
from IPython import get_ipython

formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
logger = logging.getLogger("Proyecto Final")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def is_notbook():
    """
    CHequea si el entorno es un Jupyter Notebook.
    Returns:
        bool: True si el entorno es un Jupyter Notebook, False en caso contrario.
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":  # Jupyter Notebook
            return True
        else:
            return False
    except (NameError, ImportError):
        return False


if is_notbook():
    logger.setLevel(logging.WARNING)
