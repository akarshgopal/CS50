import cs50

print("How much change is owed?: \n" , end = "")
change = cs50.get_float()*100%100
count = 0
count = count + change//25
change = change%25
count = count+ change//10
change = change%10
count = count+ change//5
change = change%5
count = count+ change//1
print(int(count))
