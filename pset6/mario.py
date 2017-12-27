import cs50

print("Height: ")
height = cs50.get_int()
i=j=0
if height>0:
    for i in range(height):
        print(" "*(height-i-1),end="")
        print("#"*(i+1),end="")
        print("  ",end="")
        print("#"*(i+1))

