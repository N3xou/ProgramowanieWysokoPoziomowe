# Zadanie 1
a,b,c,d = 2,5,5.0,4.2
print('a=',a,'b=',b,'c=',c,'d=',d)
print('a + b:',a + b,'\na + c:', a + c,'\na + d:', a + d)
print('a * b:',a * b,'\na * c:', a * c,'\na * d:', a * d)

# inty zmieniaja sie na floaty

# Zadanie 2
s = 'pies'
t = 'kot'
print (s + t, t + s + t, 2 * s)

# Zadanie 3
i=input('Podaj i')
j=input('Podaj j')
print(i,j)
print(type(i))
print(i+j)
print(type(i+j))

# wartosci traktowane sa jako string nawet przy wpisaniu numerycznych

# Zadanie 4
i=int(input('Podaj i'))
j=int(input('Podaj j'))
print(i,j)
print(type(i))
print(i+j)
print(type(i+j))

# mozemy wprowadzic tylko int, inaczej jest blad. inty dodaja sie normalnie(jak liczby)

# Zadanie 5

a,b = 2,3
print(a%b)
b = 4
print(a%b)
b = 10
print(a%b)
a,b = 5,3
print(a%b)
a = 6
print(a%b)
# % jest reszta z dzielenia

# Zadanie 6
a,b,c = int(input('a: ')), int(input('b: ')), int(input('c: '))
for l in [a,b,c]:
    if l > 10:
        print(l)

# Zadanie 7

a = int(input('a: '))
if a % 2 == 0:
    print('Parzysta')
else:
    print('Nieparzysta')

# Zadanie 8
#rok = 5
rok  = int(input('Rok: '))

if rok % 400 == 0:
    print('Przestepny')
elif rok % 100 == 0:
    print('Nie Przestepny')
elif rok % 4 == 0:
    print('Przestepny')
else:
    print('Nie Przestepny')

# Zadanie 9

#f = 93.7415
f = float(input('f: '))
print(int(f))
print(round(f%1,1))

# Zadanie 10

#f,g = 2.314,65.45
f = float(input('f: '))
g = float(input('g: '))
print(round(int(f) + g%1, 4))
print(round(int(g) + f%1, 4))

# Zadanie 11
#a,b = 3,2
a = float(input('a: '))
b = float(input('b: '))
if a**b == b**a:
    print('Oba potęgowania są równe: ', a**b)
elif a**b > b**a:
    print(f"{a} do potęgi {b} = {a ** b}, większe od {b} do potęgi {a} = {b ** a}")

else:
    print(f"{b} do potęgi {a} = {b ** a}, większe od {a} do potęgi {b} = {a ** b}")

# Zadanie 12
print('a = pierw 2\nb = pierw 3 stopnia z 3\nc = pierw 5 stopnia z 5')
a,b,c = 2**(1/2),3**(1/3), 5**(1/5)
if a > b and a > c:
    print(f'Największa to a: {a}')
elif b > a and b > c:
    print(f'Największa to b: {b}')
else:
    print(f'Największa to c: {c}')
if a < b and a < c:
    print(f'Najmniejsza to a: {a}')
elif b < a and b < c:
    print(f'Najmniejsza to b: {b}')
else:
    print(f'Najmniejsza to c: {c}')