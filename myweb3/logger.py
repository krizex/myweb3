import logging


def set_root_logger(level=logging.INFO):
    logging.addLevelName(logging.WARNING, 'WARN')
    root = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s.%(msecs)03d-%(name)s-%(levelname)s: %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root.setLevel(level)
    root.addHandler(handler)
