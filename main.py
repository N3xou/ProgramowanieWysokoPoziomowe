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
#i=input('Podaj i')
#j=input('Podaj j')
#print(i,j)
#print(type(i))
#print(i+j)
#print(type(i+j))

# wartosci traktowane sa jako string nawet przy wpisaniu numerycznych

# Zadanie 4
#i=int(input('Podaj i'))
#j=int(input('Podaj j'))
#print(i,j)
#print(type(i))
#print(i+j)
#print(type(i+j))

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
#a,b,c = int(input('a: ')), int(input('b: ')), int(input('c: '))
g  = [a,b,c]
for l in g:
    if l > 10:
        print(l)

# Zadanie 7

#a = int(input('a: '))
if a % 2 == 0:
    print('Parzysta')
else:
    print('Nieparzysta')

# Zadanie 8

rok  = int(input('Rok: '))

if rok % 400 == 0:
    print('Przestepny')
elif rok % 100 == 0:
    print('Nie Przestepny')
elif rok % 4 == 0:
    print('Przestepny')
else:
    print('Nie Przestepny')