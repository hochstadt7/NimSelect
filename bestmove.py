#!/usr/bin/env python3

# bonus- best strategy for server
arr=["A","B","C"]

def compute_nim_sum(heaps):
    nim_sum=0
    for index in arr:
        nim_sum=nim_sum^heaps[index]
    return nim_sum

def compute_win_heap(heaps,nim_sum):
    for index in arr:
        if (heaps[index]^nim_sum)<heaps[index]:
            return index
    return "D"

def comp_move(heaps):

    nim_sum=compute_nim_sum(heaps)
    if nim_sum!=0:
        win_heap=compute_win_heap(heaps,nim_sum)
        remove=(heaps[win_heap]-(heaps[win_heap]^nim_sum))
        heaps[win_heap]-=remove
    else:
        for index in arr:
            if heaps[index]>0:
                heaps[index]-=1
                break