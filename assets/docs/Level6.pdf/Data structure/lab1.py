#quastion 4-----------------------
from array import array
arr = array('i', [1, 3, 5, 7, 9])
print("Original array:", arr)
print("Length in bytes of one array item:", arr.itemsize)


#quastion 2------------------------

from array import array

arr = array('i', [1, 3, 5, 7, 9])
print("number array:", arr)

arr.append(11)
print("New array:", arr)

#quastion 6------------------------

from array import array
arr = array('i', [1, 3, 5, 3, 7, 9, 3])
print("Original array:", arr)
count = arr.count(3)
print("Number of occurrences of the number 3 in the said array:", count)

#quastion 3------------------------

from array import array
arr = array('i', [1, 3, 5, 3, 7, 1, 9, 3])
print("Original array:", arr)

arr.reverse()
print("Reverse the order of the items:")
print(arr)

#quastion 5------------------------

from array import array

arr = array('i', [1, 3, 5, 7, 9])
info = arr.buffer_info()
print("Memory address and length:", info)
print("Size in bytes:", info[1] * arr.itemsize)
