import math
def cube(a,b,c):
    print("Kvadratnoe uravnenie: " + str(a) + "x^2 + " + str(b) + "x + " + str(c) + " = 0")
    d = b**2 - 4*a*c
    print("Diskriminant = ",d)

    if d > 0:
        x1 = ((-b - math.sqrt(d)))/2*a
        x2 = ((-b + math.sqrt(d)))/2*a
        print("Korni: ", x1, " and ", x2)
    elif d < 0:
        print("Korney net.")
    else:
        print(int(-b/2*a))
    print()

cube(4,9,2)
cube(1,2,1)
cube(1,2,3)

