
def game_seq_progress(message_type, heap_a,heap_b,heap_c):  # Returns True if game continues and False if game is over.
    indicator = True
    if (message_type == 0):  # INITIAL SERVER MESSAGE
        print("Now you are playing against the server!")
        print(f"Heap A: {heap_a}", f"Heap B: {heap_b}", f"Heap C: {heap_c}", sep="\n")
        print("Your turn:")
    elif (message_type == 1):  # LEGAL MOVE
        print("Move accepted")
        print(f"Heap A: {heap_a}", f"Heap B: {heap_b}", f"Heap C: {heap_c}", sep="\n")
        print("Your turn:")
    elif (message_type == 2):  # ILLEGAL MOVE
        print("Illegal move")
        print(f"Heap A: {heap_a}", f"Heap B: {heap_b}", f"Heap C: {heap_c}", sep="\n")
        print("Your turn:")
    elif (message_type == 3):  # WIN
        print("Move accepted")
        print(f"Heap A: {heap_a}", f"Heap B: {heap_b}", f"Heap C: {heap_c}", sep="\n")
        print("You win!")
        indicator = False
    elif (message_type == 4):  # LOSE
        print("Move accepted")
        print(f"Heap A: {heap_a}", f"Heap B: {heap_b}", f"Heap C: {heap_c}", sep="\n")
        print("Server win!")
        indicator = False
    elif (message_type == 5):  # instead of QUIT- illegal and gameover both
        print("Illegal move")
        print("Heap A: 0 Heap B: 0 Heap C: 0")
        print("Server win!") # client can't win in such a case
        indicator = False
    elif (message_type == 6):
        print("You are waiting to play against the server!")
        indicator=True
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