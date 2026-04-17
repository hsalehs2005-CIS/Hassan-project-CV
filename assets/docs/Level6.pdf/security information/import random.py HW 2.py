import random

otp= random.randint(0000,9999)
print("OTP is:",otp)
c=0
for i in range (0000,9999):
     c=c+1
     print("Trying:",i)
     if i == otp:
         print("coge found:",i)
         print("Number of Tries",c)
         break