def add_num(num1,num2):
    return num1 + num2

def sub_num(num1,num2):
    return num1-num2

def mul_num(num1,num2):
    return num1 * num2

def div_num(num1,num2):
    quotient = int(num1/num2)
    remainder = num1 % num2
    print("Quotient:{x} \nRemainder:{y}".format(x=quotient,y=remainder))
    return (quotient,remainder)
