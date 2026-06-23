#if Elif 
Hungry = True
if Hungry == True:
    print ("feed the dog")
    

else:
    print ("dont feed the dog")

# For  loop
mylist = [1,2,3,4,5]
for num in mylist:
    if num % 2 == 0:
        print (str(num) + " is even")
    else:
        print (str(num) + " is odd")

# Tuple unpacking
my_list =[(1,2),(3,4),(5,6),(7,8)]


for a, b in my_list:
    print("First element:", a)
    print("Second element:", b)


my_dict = {"name": "Alice", "age": 30, "city": "New York"}
for key,value in my_dict.items():
    print(value)
    print(key)

for vlaue in my_dict.values():
    print(value)

# While loop
X =0
while X < 5:
    print (f'\nvalue of X is {X}')
    X += 1

Y = 0
while Y < 5:
    if Y == 2:
        break
    print (f'\nvalue of Y is {Y}')
    Y += 1

# Continue statement
my_list = [1, 2, 3, 4, 5]
for num in my_list:
    if num == 3:
        continue
    print(f'Value of my list is {num}')

#break statement
my_list = [1, 2, 3, 4, 5]
for num in my_list:
    if num == 3:
        break
    print(f'Value of my list before break is {num}')

#enumerate function
my_list = ['a', 'b', 'c', 'd']
for index, value in enumerate(my_list):
    print(f'Index: {index}, Value: {value}')
    print('\n') 

#zip function
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
list3 = [10, 20, 30]
for item in zip(list1, list2, list3):
    print(f'Item: {item}')  

#in operator
my_list = [1, 2, 3, 4, 5]
if 3 in my_list:
    print("3 is in the list")
else:
    print("3 is not in the list")

#min and max function
my_list = [1, 2, 3, 4, 5]
min_value = min(my_list)
max_value = max(my_list)
print(f'Minimum value: {min_value}')
print(f'Maximum value: {max_value}')    

#random function  
from random import randint
random_number = randint(1, 100)

#input function
# user_input = input("Please enter your name: ")
# print(f'Hello, {user_input}!')  

# user_age = input("Please enter a Age: ")
# print(f'Your age is {user_age}!')    

#list comprehension
my_list = [x for x in 'word']
print(my_list)  

# list compression with for loop
my_list = []
my_string = "Hello World"
for char in my_string:
    my_list.append(char)
print(my_list)  

#list comprehension with condition
my_list = [x for x in range (1,10) if x % 2 == 0]
print(my_list)
