# Package: kuwtg.utils
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
        return [whole_line] + break_lines(tail, max_length)


def break_lines(item, max_length):
    return [line.strip() for line in _break_lines(item, max_length)]
