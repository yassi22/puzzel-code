#output 16 =data
#output 20 = latch
#output 21 = clock
#output 5 = data2

import RPi.GPIO as GPIO
import time
import numpy as np
import sys
import copy


def create_from_any_list_with_strings_np_array(list_with_string):
    innit_array = np.zeros((8, 8), dtype=int)

    # Define the shape
    shape = list_with_string

    # Convert the string representation to a NumPy array
    shaped_array = np.array([[int(char) for char in row] for row in shape])

    # Place the heart shape in the center of the 8x8 array
    row_start = (innit_array.shape[0] - shaped_array.shape[0]) // 2
    col_start = (innit_array.shape[1] - shaped_array.shape[1]) // 2

    innit_array[row_start:row_start + shaped_array.shape[0],
    col_start:col_start + shaped_array.shape[1]] = shaped_array

    return shaped_array




#define shift register update function
def cleanup():
    update_board(inverted_array_input_1, inverted_array_input_2, dataPIN, dataPIN2, clockPIN, latchPIN, 0.001)

def cords_converter(array):
    list_with_positive_columns = []

    for row in array:
        list_cords = []
        index = 1

        for number in row:
            if number == 1:
                list_cords.append("C" + str(index))
            index += 1

        list_with_positive_columns.append(list_cords)

    return list_with_positive_columns

def input_loader(list_with_positive_columns):

    for x,row in enumerate(list_with_positive_columns):
        result_list = copy.deepcopy(list_of_inputs_inv)
        for column in row:
            a,b = column_dict[column]
            result_list[a][b] = 0

        x += 1
        c,d = row_dict["R" + str(x)]
        result_list[c][d] = 1
        update_board(result_list[0], result_list[1], dataPIN, dataPIN2, clockPIN,latchPIN,0.000001)
    return result_list



def update_board(input1, input2 ,data, data2, clock, latch, delay): #put latch down to start data sending GPIO.output(data,0)
    GPIO.output(latch, 0)
    time.sleep(delay)

    #load data in reverse order
    for i in range(7,-1,-1):
        GPIO.output(clock, 0)
        time.sleep(delay)
        GPIO.output(data, int(input1[i]))
        GPIO.output(data2, int(input2[i]))
        time.sleep(delay)
        GPIO.output(clock, 1)
        time.sleep(delay)

        # put latch up to store data on register
    GPIO.output(clock, 0)
    time.sleep(delay)
    GPIO.output(latch, 1)
    time.sleep(delay)
    GPIO.output(latch, 0)   
    time.sleep(delay)

   
column_dict = {"C1": (0, 7),
               "C2": (0, 6),
               "C3": (0, 2),
               "C4": (1, 2),
               "C5": (0, 1),
               "C6": (1, 5),
               "C7": (1, 4),
               "C8": (0, 5)}
row_dict = {"R1": (1, 3),
            "R2": (1, 6),
            "R3": (1, 1),
            "R4": (1, 7),
            "R5": (0, 3),
            "R6": (1, 0),
            "R7": (0, 4),
            "R8": (0, 0)}
# original array is when everything is on
original_array_input_1 = np.array([1,0,0,1,1,0,0,0])
original_array_input_2 = np.array([1,1,0,1,0,0,1,1])
# Invert the array
inverted_array_input_1 = original_array_input_1 ^ 1
inverted_array_input_2 = original_array_input_2 ^ 1
list_of_inputs_inv = [inverted_array_input_1, inverted_array_input_2]
# define PINs according to cabling
dataPIN = 6
latchPIN = 13
clockPIN = 19
dataPIN2 = 16
# set pins to putput
GPIO.setmode(GPIO.BCM)
GPIO.setup((dataPIN, dataPIN2, latchPIN, clockPIN), GPIO.OUT)

# het toevoegen van weerstand voor de knoppen
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)     


#variabelen voor de knoppen.
INPIN1 = 17 
INPIN2 = 27
INPIN3 = 22 
INPIN4 = 24


# het checken of een knop ingedrukt is.
GPIO.add_event_detect(INPIN1, GPIO.FALLING, callback=lambda _:  callback(INPIN1), bouncetime=400)
GPIO.add_event_detect(INPIN2, GPIO.FALLING, callback=lambda  _: callback(INPIN2), bouncetime=400) 
GPIO.add_event_detect(INPIN3, GPIO.FALLING, callback=lambda  _: callback(INPIN3), bouncetime=400)
GPIO.add_event_detect(INPIN4, GPIO.FALLING, callback=lambda  _: callback(INPIN4), bouncetime=400)



all_on_shape_string_list = [
    "11111111",
    "11111111",
    "11111111",
    "11111111",
    "11111111",
    "11111111",
    "11111111",
    "11111111"
] 


pattern_numbers = [
[
    "01111110",
    "10000001",
    "00000001",
    "00000110",
    "00011000",
    "00100000",
    "01000000",
    "11111111",
], 
[
    "00000100",
    "00001100",
    "00010100",
    "00100100",
    "01000100",
    "11111111",
    "00000100",
    "00000100",
], 
[
    "00111100",
    "01000010",
    "10000001",
    "10000000",
    "10111100",
    "11000010",
    "10000010",
    "01111100",
], 
[ 
    "00111100",
    "01000010",
    "10000001",
    "10000001",
    "01111110",
    "10000001",
    "10000001",
    "01111110",
]

] 




pattern_dolhof_2 = [
    "11111111",
    "12000001",
    "10111101",
    "10000101",
    "00110000",
    "10101101",
    "10000003",
    "11111111",
]  

 
pattern_dolhof_3 = [
    "11111111",
    "12001000",
    "10110101",
    "10100001",
    "10101101",
    "10101101",
    "00000103",
    "11111111",
] 


pattern_dolhof_4 = [
    "11111111",
    "12001000",
    "10110101",
    "10100001",
    "10101101",
    "10101101",
    "00000103",
    "11111111",
]


# patroon wat gebruikt om de doolhof te laten zien.
pattern_dolhof = [
    "11111111",
    "12000001",
    "10111011",
    "10100011",
    "10101111",
    "10100011",
    "10001003",
    "11111111",
]

pattern_dolhof_1 = [
    "11111111",
    "12000001",
    "10111011",
    "10100011",
    "10101111",
    "10100011",
    "10001003",
    "11111111",
]
print(pattern_dolhof)


# de player omzetten zodat de player op het 8*8 led matrix verschijnt.
def find_2_change_to_1(list_with_strings):
    return [line.replace("2", "1") for line in list_with_strings]

def find_end_change_3_to_0(list_with_strings): 
    return [line.replace("3", "0") for line in list_with_strings]

#de dolhof aanpassen dat de player telkens geupdate word doormiddel van de movments.
def setup_code(dolhof):
    pattern_dolhof_ivan_code  = copy.deepcopy(dolhof)
    pattern_end_dolhof_code = find_end_change_3_to_0(pattern_dolhof_ivan_code) 
    pattern_dolhof_ivan_code_final = find_2_change_to_1(pattern_end_dolhof_code) 
    return pattern_dolhof_ivan_code_final


#player position start
start_row = 1
start_col = 1
pattern_dolhof[start_row] = pattern_dolhof[start_row][:start_col] + '2' + pattern_dolhof[start_row][start_col + 1:] 


#endpoint in dolhof
 
end_row = 6
end_col = 7
pattern_dolhof[end_row] = pattern_dolhof[end_row][:end_col] + '3' +pattern_dolhof[end_row][end_col + 1:]



#print het patteroon uit van het dolhof op het scherm ps(dit kan later uit).
def print_pattern():
    for row in pattern_dolhof:
        pass

# vind de player van het spel.
def find_cursor_position():
    for i, row in enumerate(pattern_dolhof):
        if '2' in row:
            print(i,row.index('2'))
            return i, row.index('2')

# find de end point op de dolhof
def find_end_position(): 
    global pattern_dolhof 
    for i, row in enumerate(pattern_dolhof): 
        if '3' in row:  
            print(i,row.index('3'))
            return i, row.index('3') 
        
END_POSITION_X, END_POSITION_Y = find_end_position()
level = 0


level1_reset = copy.deepcopy(pattern_dolhof_1)
level2_reset = copy.deepcopy(pattern_dolhof_2)
level3_reset = copy.deepcopy(pattern_dolhof_3)
level4_reset = copy.deepcopy(pattern_dolhof_4)



def check_if_won(x,y):
    global END_POSITION_X
    global END_POSITION_Y
    global pattern_dolhof_1
    global pattern_dolhof_2
    global pattern_dolhof_3
    global pattern_dolhof_4 
    global level1_reset 
    global level2_reset 
    global level3_reset
    global level4_reset

    if (x == END_POSITION_X) and (y == END_POSITION_Y):
        global pattern_dolhof 
        global level
        if level == 0:
            pattern_dolhof  = pattern_dolhof_2 
            level += 1 
        elif level == 1:
            pattern_dolhof = pattern_dolhof_3
            level += 1
        elif level == 2: 
            pattern_dolhof = pattern_dolhof_4 
            level +=1
        elif level == 3: 
            print("won")
            for number in pattern_numbers:
                time.sleep(1)
                print(number)
                pattern_dolhof = number

            time.sleep(3)
            level = 0
            pattern_dolhof_1 = copy.deepcopy(level1_reset)
            pattern_dolhof_2 = copy.deepcopy(level2_reset)
            pattern_dolhof_3 = copy.deepcopy(level3_reset)
            pattern_dolhof_4 = copy.deepcopy(level4_reset)
            pattern_dolhof = pattern_dolhof_1
            


 
        print(pattern_dolhof)
        END_POSITION_X, END_POSITION_Y = find_end_position()




# het bewegen van de player 
def move_cursor(direction):
    current_row, current_col = find_cursor_position()
    end_row, end_col = END_POSITION_X, END_POSITION_Y

    print("\n")
    print(f"direction is:{direction}") 

    if direction == 17 :
        next_postion_x = current_row - 1
        next_postion_y = current_col

        check_if_won(next_postion_x,next_postion_y)

    elif direction == 22:
        next_postion_x = current_row + 1
        next_postion_y = current_col

        check_if_won(next_postion_x, next_postion_y)

    elif direction == 27:
        next_postion_x = current_row 
        next_postion_y = current_col - 1

        check_if_won(next_postion_x, next_postion_y)


    elif direction == 24:
        next_postion_x = current_row 
        next_postion_y = current_col + 1

        check_if_won(next_postion_x, next_postion_y)





    #up
    if (direction == 17) and (current_row > 0) and (pattern_dolhof[current_row - 1][current_col] == '0'):
        #check here if you won
     

        pattern_dolhof[current_row] = pattern_dolhof[current_row][:current_col] + '0' + pattern_dolhof[current_row][current_col + 1:]
        pattern_dolhof[current_row - 1] = pattern_dolhof[current_row - 1][:current_col] + '2' + pattern_dolhof[current_row - 1][current_col + 1:]

    #down
    elif direction == 22 and current_row < len(pattern_dolhof) - 1 and pattern_dolhof[current_row + 1][current_col] == '0':

       


        pattern_dolhof[current_row] = pattern_dolhof[current_row][:current_col] + '0' + pattern_dolhof[current_row][current_col + 1:]
        pattern_dolhof[current_row + 1] = pattern_dolhof[current_row + 1][:current_col] + '2' + pattern_dolhof[current_row + 1][current_col + 1:]
    #left
    elif direction == 27 and current_col > 0 and pattern_dolhof[current_row][current_col - 1] == '0':

        

        pattern_dolhof[current_row] = pattern_dolhof[current_row][:current_col - 1] + '2' + pattern_dolhof[current_row][current_col:]
        pattern_dolhof[current_row] = pattern_dolhof[current_row][:current_col] + '0' + pattern_dolhof[current_row][current_col + 1:]
    #right
    elif direction == 24 and current_col < len(pattern_dolhof[current_row]) - 1 and pattern_dolhof[current_row][current_col + 1] == '0':

        
        pattern_dolhof[current_row] = pattern_dolhof[current_row][:current_col] + pattern_dolhof[current_row][current_col + 1] + '2' + pattern_dolhof[current_row][current_col + 2:] 

       


    if current_col == end_col and current_row == end_row: 
        print("YOU WON")
    else: 
        print("Keep Playing....") 

    global final_dolhof
    final_dolhof = setup_code(pattern_dolhof)
    for line in pattern_dolhof:
        print(line)

#het uitlezen welke input ingedrukt is.
def callback(INPUT):  
    move_cursor(INPUT)
    print(INPUT)

def patroon():
    final_list = []
    # init
    base_list = "0" * 8
    init_list = [base_list for _ in range(8)]  # creates a list of 8 identical strings, each '00000000'

    for i in range(8):  # for each row
        for x in range(8):  # for each column
            # modify the specified row by changing one '0' to '1' at position x
            modified_row = init_list[i][:x] + "1" + init_list[i][x+1:]
            # replace the row in init_list with modified_row
            modified_init_list = init_list[:i] + [modified_row] + init_list[i+1:]
            # add the modified list to final_list
            final_list.append(modified_init_list)

    return final_list



try:
    
    #for pattern in pattern_numbers:  
    while True:
        final_dolhof = setup_code(pattern_dolhof)
        frame = create_from_any_list_with_strings_np_array(final_dolhof) 
        input_loader(cords_converter(frame)) 

except KeyboardInterrupt:
    GPIO.cleanup()

# PINs final cleaning
GPIO.cleanup()