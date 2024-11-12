import heapq
import json
from collections import Counter, namedtuple
import base64


class Leaf(namedtuple('Leaf', 'char')):

    def walk(self, code: dict[str, str], acc: str) -> None:
        code[self.char] = acc or "0"


class Node(namedtuple('Node', ["left", "right"])):

    def walk(self, code: dict[str, str], acc: str) -> None:
        """
        :param code:
        :param acc: префикс кода, который мы накопили, спускаясь от корня до данного узла или листа
        """
        self.left.walk(code, acc + "0")
        self.right.walk(code, acc + "1")


class Tree:
    def __init__(self, dictionary_with_freq: dict[str, float]) -> None:
        self.dictionary_with_freq = dictionary_with_freq

    # noinspection PyMethodMayBeStatic
    def build(self) -> dict[str, str]:
        """
        Построение дерева Хаффмана, чтобы в дальнейшем закодировать слово
        """
        queue_with_priority = []
        code = {}

        for char, freq in self.dictionary_with_freq.items():
            queue_with_priority.append((freq, len(queue_with_priority), Leaf(char)))

        heapq.heapify(queue_with_priority)

        count = 0
        while len(queue_with_priority) > 1:
            minimal_frequency, _, left = heapq.heappop(queue_with_priority)
            _, pre_minimal_freq, right = heapq.heappop(queue_with_priority)
            heapq.heappush(queue_with_priority, (minimal_frequency + pre_minimal_freq, count, Node(left, right)))
            count += 1

        if queue_with_priority:
            [(_freq, _count, root)] = queue_with_priority
            root.walk(code, "")

        return code


class Huffman:
    def __init__(self, tree: Tree) -> None:
        self.tree = tree.build()

    def encode(self, string: str) -> str:
        return "".join(self.tree[char] for char in string)

    def decode(self, encoded_string: str) -> str:
        """
        Метод для декодирования последовательности символов.
        :param encoded_string: Закодированное слово, которое нужно вернуть в исходное.
        :param code: Таблица символов соответствия (дерево - Хаффмана), где каждому символу вы назначили код
        """
        reverse_code = {v: k for k, v in self.tree.items()}
        decoded_string = ""
        temp = ""

        for bit in encoded_string:
            temp += bit
            if temp in reverse_code:
                decoded_string += reverse_code[temp]
                temp = ""

        return decoded_string


def main() -> None:
    choices = {"1": encode, "2": decode}
    file_path = input("Введите путь до файла ")
    choices[input("Введите что хотите сделать (1) - закодировать, (2) - декодировать")](file_path)


def encode(file_path: str) -> None:
    with open(file_path, mode="rb") as f:
        word = base64.b64encode(f.read()).decode('utf-8')

    map_with_freq: dict[str, float] = {char: count / len(word) for char, count in Counter(word).items()}
    tree = Tree(map_with_freq)
    print(tree.build())
    coder = Huffman(tree)
    encoded = coder.encode(word)

    with open("./encoded_files/encoded.txt", mode="w") as f:
        json.dump([encoded, map_with_freq], f)


def decode(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as text_file:
        word = text_file.read()

    data, map_with_freq = json.loads(word)
    tree = Tree(map_with_freq)
    print(tree.build())
    coder = Huffman(tree)
    decoded = coder.decode(data)

    with open("output_image.png", mode="wb") as f:
        f.write(base64.b64decode(decoded))


if __name__ == "__main__":
    main()
