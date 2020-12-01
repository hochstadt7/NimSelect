import struct


def choice_validity(heap_dict, heap_choice, num_choice):
    if heap_dict[heap_choice] < num_choice:
        return "ILLEGAL"
    elif heap_dict[heap_choice] >= num_choice:
        heap_dict[heap_choice] -= num_choice
        return "LEGAL"


def heap_sum(heap_dict):
    sum = 0
    for heap in heap_dict:
        sum += heap_dict[heap]
    return sum


def data_to_send(message_type, heap_dict):
    return struct.pack("i i i i", message_type, heap_dict['A'], heap_dict['B'], heap_dict['C'])


def bring_heap_letter(heap_num):
    if heap_num == 0:
        return 'A'
    elif heap_num == 1:
        return "B"
    elif heap_num == 2:
        return "C"
    else:
        return "E"


def reset_heap(heap, a, b, c):
    heap["A"] = a
    heap["B"] = b
    heap["C"] = c

    return heap


