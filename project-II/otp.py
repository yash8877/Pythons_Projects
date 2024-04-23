import random
import pywhatkit

num = int(input("Enter the your phone number- "))
otp = random.randrange(100000, 1000000)
print(otp)
pywhatkit.sendwhatmsg(num,otp,22,52)

