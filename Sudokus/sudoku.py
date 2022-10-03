import numpy as np

sudoku = np.array([[0,1,0,5,2,0,4,3,0],
                   [0,0,8,0,0,6,0,0,0],
                   [5,0,3,7,9,0,2,0,0],
                   [0,2,7,0,0,9,0,0,5],
                   [0,3,6,2,4,0,0,0,7],
                   [9,0,4,0,7,3,0,6,0],
                   [0,7,0,0,8,0,0,1,0],
                   [0,0,0,9,6,0,7,0,4],
                   [0,0,0,3,0,0,6,0,0]])


def validate(ycor, xcor, number):
    global sudoku
    #check column
    for i in range(0,9):
        if sudoku[ycor][i] == number:
            return False
    #check row
    for i in range(0,9):
        if sudoku[i][xcor] == number:
            return False
    #check subcell
    x_regions = (xcor//3)*3
    y_regions = (ycor//3)*3
    for i in range(0,3):
        for j in range(0,3):
            if sudoku[y_regions+i][x_regions+j] == number:
                return False
    return True

def solve():
    global sudoku
    for ycor in range(9):
        for xcor in range(9):
            if sudoku[ycor][xcor] == 0:
                for number in range(1,10):
                    if validate(ycor,xcor,number):
                        sudoku[ycor][xcor] = number
                        solve()
                        sudoku[ycor][xcor] = 0
                return
    print(sudoku)

solve()







        



