
tuple1 = (1, 2, 3, 4, 5)
dict1 = {"name": "Ashish", "age": 30, "city": "New York"}
print ("Tuple: " + str(tuple1))
print ("Dictionary: " + str(dict1))
print ("1 + 1 = " + str(1 + 1))
my_dog = 2
print ("My dog has " + str(type(my_dog)) + " legs.")
my_dog =["sammy", "labrador"] 
print ("My dog's name is " + my_dog[0] + " and he is a " + my_dog[1] + ".")
type(my_dog)
print ("The type of my_dog is " + str(type(my_dog)))
mystring = "Hello, World!"
print(str(mystring[-1]))
mystring = "abcdefghijk"
print (str(mystring[2:]))
print (str(mystring[0:3]))
name = 'Pam'
last_letters = name[1:]
print ('P' + last_letters)
X = 'Hello World'
X= X.upper()
print (X)
print(X.split('O'))
# String Formatting
print('The {q} {b}{f}'.format(f='fox', b='brown', q='quick'))

# f-string
f='fox'
b='red'
q='quick'
print (f'The {q} {b} {f}')

#list 
my_list = ['one', 'two', 'three','four']
another_list = ['five', 'six', 'seven']
my_list = my_list + another_list
print (my_list)  
my_list.append('eight')
print (my_list)
my_list[0]= 'ONE in ALL CAPS'
print (my_list)
my_list.pop(0)
print (my_list)
num_list = [8,4,9,3,2]
my_list = ['k', 'e', 'x', 'b', 'c']
num_list.sort()
Sorted_num_list = num_list
print (Sorted_num_list)
my_list.sort()
print (my_list)
my_list.reverse()
print (my_list)
my_list.remove('k')
print (my_list)
my_list.insert(1,'k')
print (my_list)
# disctionary
my_dict = {'apple': '$2.10', 'orange': '$3.00', 'banana': '$1.50'}
print ("Price of apple is: " + my_dict['apple'])
print ("Price of orange is: " + my_dict['orange'])
print ("Price of banana is: " + my_dict['banana'])
dic_list = {'key1': [1, 2, 3], 'key2': ['a', 'b', 'need to capitalize this']}
mylist = dic_list['key2'][2].upper()
print (mylist)