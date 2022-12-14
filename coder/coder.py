import zlib

symbol_db = {}

class Symbol:
    def __init__(self):
        self.name = ""
        self.probability = 0.0
        self.arr = [0] * 20
        self.code = ""

    def __str__(self):
        return self.name
class Node:
    def __init__(self):
        self.symbol = Symbol()
        self.top = 0

def shannon(num: int, num_of_symbols: int, list_of_nodes: list[Node]):
    pack1 = 0
    pack2 = 0
    if (num + 1) == num_of_symbols or num == num_of_symbols or num > num_of_symbols:
        if num == num_of_symbols or num > num_of_symbols:
            return
        list_of_nodes[num_of_symbols].top += 1
        list_of_nodes[num_of_symbols].symbol.arr[list_of_nodes[num_of_symbols].top] = 0
        list_of_nodes[num].top += 1
        list_of_nodes[num].symbol.arr[list_of_nodes[num].top] = 1
        return
    else:
        for i in range(num, num_of_symbols):
            pack1 = pack1 + list_of_nodes[i].symbol.probability
        pack2 = pack2 + list_of_nodes[num_of_symbols].symbol.probability
        diff1 = pack1 - pack2
        if diff1 < 0:
            diff1 = diff1 * -1
        j = 2
        k = 0
        while j != num_of_symbols - num + 1:
            k = num_of_symbols - j
            pack1 = pack2 = 0
            for i in range(num, k + 1):
                pack1 = pack1 + list_of_nodes[i].symbol.probability
            for i in range(num_of_symbols, k, -1):
                pack2 = pack2 + list_of_nodes[i].symbol.probability
            diff2 = pack1 - pack2
            if diff2 < 0:
                diff2 = diff2 * -1
            if diff2 >= diff1:
                break
            diff1 = diff2
            j += 1
        else:
            k += 1
        for i in range(num, k + 1):
            list_of_nodes[i].top += 1
            list_of_nodes[i].symbol.arr[list_of_nodes[i].top] = 1

        for i in range(k + 1, num_of_symbols + 1):
            list_of_nodes[i].top += 1
            list_of_nodes[i].symbol.arr[list_of_nodes[i].top] = 0

        # Invoke shannon function
        shannon(num, k, list_of_nodes)
        shannon(k + 1, num_of_symbols, list_of_nodes)


def sortByProbability(num_of_symbols: int, list_of_nodes: list[Node]) -> None:
    temp = Node()
    for j in range(1, num_of_symbols):
        for i in range(num_of_symbols - 1):
            if list_of_nodes[i].symbol.probability > list_of_nodes[i + 1].symbol.probability:
                temp.probability = list_of_nodes[i].symbol.probability
                temp.symbol.name = list_of_nodes[i].symbol.name

                list_of_nodes[i].symbol.probability = list_of_nodes[i + 1].symbol.probability
                list_of_nodes[i].symbol.name = list_of_nodes[i + 1].symbol.name

                list_of_nodes[i + 1].symbol.probability = temp.probability
                list_of_nodes[i + 1].symbol.name = temp.symbol.name


def display(number_of_symbols: int, nodes_list: list[Node]) -> None:
    print("\n\n\n\tSymbol\tProbability\tCode", end='')
    for i in range(number_of_symbols - 1, -1, -1):
        print("\n\t", nodes_list[i].symbol, "\t\t", nodes_list[i].symbol.probability, "\t", end='')
        for j in range(nodes_list[i].top + 1):
            symbol_db[nodes_list[i].symbol.name] = nodes_list[i].symbol
            nodes_list[i].symbol.code += str(nodes_list[i].symbol.arr[j])
            print(nodes_list[i].symbol.arr[j], end='')
    print("\n")

def main():
    total = 0
    with open("input.txt", "r") as f:
        symbols, symb_probabilities = f.readlines()
        symbols = symbols.split()
        symb_probabilities = symb_probabilities.split()
    num_of_symbols = len(symbols)
    nodes = [Node() for _ in range(num_of_symbols)]
    for i in range(num_of_symbols):
        nodes[i].symbol.name += symbols[i]

    for i in range(num_of_symbols):
        nodes[i].symbol.probability = float(symb_probabilities[i])
        total = total + nodes[i].symbol.probability

        if total > 1:
            print("Invalid. Enter new values")
            exit()

    sortByProbability(num_of_symbols, nodes)

    for i in range(num_of_symbols):
        nodes[i].top = -1

    shannon(0, num_of_symbols - 1, nodes)

    display(num_of_symbols, nodes)
    to_encode = input()
    result = ""
    for symb in to_encode:
        result += symbol_db[symb].code
    with open("result.txt", "wb") as f:
        f.write(zlib.compress(result.encode("utf-8")))


if __name__ == '__main__':
    main()
