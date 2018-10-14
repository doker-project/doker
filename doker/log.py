# -*- coding: utf-8 -*-

import logging

logging.basicConfig(format='[%(levelname)s] %(message)s')
log = logging.getLogger('doker')
log.setLevel(logging.INFO)

def critical(msg, *args, **kwargs):
    return log.critical(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    return log.error(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    return log.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    return log.warning(msg, *args, **kwargs)