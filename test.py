d = {1: "a", "1":"b", True: "c"} # équivalent à {1: "a", "1": "b", 1: "c"}
# print(d[1], d["1"], d[True]) # parce que 1 et True sont pareils, donc ça écrase la valeur "a" de 1, i.e le dictionnaire réel est {True: "c", "1":"b"} ou encore {1: "c", "1": "b"}


# t = (1,2,3,)
# print(t)

# x=[]
# def append_to(y):
#     x.append(y)
#     return x
    
# print(append_to(1))
# print(append_to(2))

# print(3 * "ab") # donne "ababab"

x = [1, 2, 3]
y = x
z = y
z = z.append(4)
print(x)

def gen():
    yield from range(3)
    yield 3
    
g = gen()

# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g)) au lieu de faire ça, on pourrait faire list(g) et ça exécute le next, jusqu'à finir l'itérateur, au cas où il y a 1000 dans le range()

print("hello".split("e"))

print(all([True, True, False]))

dict =  {
    "name": "Moufid",
    "country":"Portugal",
    "language":"portoghese"
}

# if dict["name"] != None:
#     print("hello")

# if dict.has_key("name"):
#     print("hello")
    
try: 
    print( 1 / 0)
except ZeroDivisionError:
    print("A")
except Exception :
    print("B")
else:
    print("C")
finally: 
    print("D")
    
# try:
#     raise ValueError("Oops")
# except ValueError:
#     print("Error handled")
    
    
    
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c = counter()
print(c(), c())