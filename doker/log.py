# -*- coding: utf-8 -*-

import logging

logging.basicConfig(format='[%(levelname)s] %(message)s')
log = logging.getLogger('doker')
log.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)
log.propagate = False

def critical(msg, *args, **kwargs):
    return log.critical(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    return log.error(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    return log.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    return log.warning(msg, *args, **kwargs)