# bonus- best strategy for server

def compute_nim_sum(heaps,num_heaps):
    nim_sum=0
    for index in range(num_heaps):
        nim_sum^=heaps[index]

def compute_win_heap(heaps,num_heaps,nim_sum):
    for index in range(num_heaps):
        if heaps[index]^nim_sum<heaps[index]:
            return index
        return -1

def comp_move(heaps,num_heaps):

    nim_sum=compute_nim_sum(heaps,num_heaps)
    if nim_sum:
        win_heap=compute_win_heap(heaps,num_heaps,nim_sum)
        remove=heaps[win_heap]-heaps[win_heap]^nim_sum
        heaps[win_heap]-=remove
    else:
        for index in range(num_heaps):
            if heaps[index]>0:
                heaps[index]-=1
                break