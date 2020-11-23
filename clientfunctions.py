
def game_seq_progress(message_type, heap_A):  # Returns True if game continues and False if game is over.
    indicator = True
    if (message_type == 0):  # INITIAL SERVER MESSAGE
        print("Now you are playing against the server!")
    elif (message_type == 1):  # LEGAL MOVE
        print("Move accepted")
    elif (message_type == 2):  # ILLEGAL MOVE
        print("Illegal move")
    elif (message_type == 3):  # WIN
        print("You win!")
        indicator = False
    elif (message_type == 4):  # LOSE
        print("Server win!")
        indicator = False
    elif (message_type == 5):  # instead of QUIT- illegal and gameover both
        print("Illegal move")
        print(f"Heap A: 0", f"Heap_B: 0", f"Heap C: 0", sep="\n")
        if (heap_A == 0): # we will set heap_A to 0 iff client wins, otherwise to 1
            print("You win!")
        else:
            print("Server win!")
        indicator = False
    return indicator


def is_valid_input(input_string):
    input_segments = input_string.split()
    if (len(input_segments) != 2):
        return False
    else:
        heap_letter, num = input_segments
        if heap_letter not in ['A', 'B', 'C']:
            return False
        try:
            if float(num) < 0 or int(float(num)) != float(num):
                return False
        except ValueError:
            return False
        return True


def pick_heap_num(heap_letter):
    if heap_letter == "A":
        return 0
    elif heap_letter == "B":
        return 1
    elif heap_letter == "C":
        return 2
    else:
        return 3