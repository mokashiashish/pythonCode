def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def multiply_numbers(a, b):
    return a * b

def divide_numbers(a, b):
    if b != 0:
        return a / b
    else:
        return "Division by zero error"
    
    

print(f'Addition: {add_numbers(5, 3)}')
print(f'Subtraction: {subtract_numbers(5, 3)}')
print(f'Multiplication: {multiply_numbers(5, 3)}')
print(f'Division: {divide_numbers(5, 4)}')  


# even check
def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False
    
print(f'Is 4 even? {is_even(4)}')

# check even list
def even_odd_list(num_list):
    even_odd_numbers = []
    
    for num in num_list:
        if num % 2 == 0:
            even_odd_numbers.append((num, "even"))
        else:
            even_odd_numbers.append((num, "odd"))

    return even_odd_numbers


my_list = [1, 2, 3, 4, 5, 6]
print(f'Numbers in the list: {even_odd_list(my_list)}')

# tuple unpacking
work_hours =[( 'Billy', 38), ('Geroge', 42), ('Pan', 40), ('Geeti', 45)]
def employee_check(work_hours):
    max_hours = 0
    employee_of_month = ''

    for employee, hours in work_hours:
        if hours > max_hours:
            max_hours = hours
            employee_of_month = employee
        else:
            pass

    return (employee_of_month, max_hours)

print(f'Employee of the month: {employee_check(work_hours)}')

# game 

from random import shuffle
 #shuffle function  
def shuffle_list(mylist):
    shuffle(mylist)
    return mylist 

# player guess
def player_guess(mylist):
    guess =  ''
    while guess not in ['0', '1', '2']:
        guess = input("Pick a number: 0, 1 or 2: ")
    return int(guess)

# check guess
def check_guess(mylist, guess):
    if mylist[guess] == 'O':
        print("Correct guess!")
        print(mylist)
    else:
        print("Wrong guess! The correct answer was: ")
        print(mylist)   

#Script
# mylist = [' ', 'O', ' ']
# mixedup_list = shuffle_list(mylist)
# guess = player_guess(mixedup_list)
# check_guess(mixedup_list, guess)

#Map function- call a function for each item in a list and return a new list with the results
def square(num):
    return num * num 

map_list = [1, 2, 3, 4, 5]
squared_list = list(map(square, map_list))
print(f'Squared list: {squared_list}')

