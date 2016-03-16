# Package: kuwtg.utils
import logging
import os

from kuwtg.config.configuration import Configuration


def _break_lines(item, max_length):
    if len(item) < max_length:
        return [item]
    else:
        head, tail = item[:max_length], item[max_length:]
        rightmost_space_index = head.rfind(' ')
        if rightmost_space_index == -1 or rightmost_space_index > max_length:
            whole_line = head
        else:
            whole_line = head[:rightmost_space_index]
            tail = head[rightmost_space_index:] + tail
        return [whole_line.strip()] + break_lines(tail.strip(), max_length)


def break_lines(item, max_length):
    return [line for line in _break_lines(item, max_length) if len(line) > 0]


def render_lines(lines):
    line_break = '\r\n' if lines.find('\r\n') >= 0 else '\n'
    return ' '.join([line
                     for line in lines.split(line_break)
                     if len(line) > 0])


def get_logger(module_name):
    configuration = Configuration()
    log_file = configuration.log_file
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s <%(module)s>: %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
