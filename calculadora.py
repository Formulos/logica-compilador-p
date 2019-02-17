import operator
print("palavra: ")
world = str(input())


def separacao(world):
    conta = []
    numero = ""
    print(world)
    for i in world:
        if i == "+" or i == "-":
            conta.append(int(numero))
            conta.append(i)
            numero = ""
        elif i != "":
            numero += i

    if numero != "":
        conta.append(int(numero))

    return conta

conta = separacao(world)
resp = conta[0]
for i in range(len(conta)):
    if conta[i] == "+":
        resp += conta[i+1]
    if conta[i] == "-":
        resp -= conta[i+1]
print("resposta:", resp)
