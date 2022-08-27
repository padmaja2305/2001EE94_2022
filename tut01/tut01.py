def factorial(x):
    n=1
    for i in range (2,x+1):
        n=n*i
    print (n)

x=int(input("Enter the number whose factorial is to be found"))
factorial(x)
