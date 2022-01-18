from collections import Counter, namedtuple
import heapq


class Node(namedtuple("Node", ["left", "right"])):
    def walk(self, code, acc):
        self.left.walk(code, acc + "0")
        self.right.walk(code, acc + "1")


class Leaf(namedtuple("Leaf", ["char"])):
    def walk(self, code, acc):
        code[self.char] = acc or "0"

# -----Coding
def huffman_encode(s):
    h = []
    for ch, freq in Counter(s).items():
        h.append((freq, len(h), Leaf(ch)))

    heapq.heapify(h)

    count = len(h)
    while len(h) > 1:
        freq1, _count1, left = heapq.heappop(h)
        freq2, _count2, right = heapq.heappop(h)
        heapq.heappush(h, (freq1 + freq2, count, Node(left, right)))
        count += 1

    code = {}
    if h:
        [(_freq, count, root)] = h
        root.walk(code, "")
    return code

# -----Decoding
def huffman_decode(encoded, code):
    pointer = 0
    encoded_str = ""
    while pointer < len(encoded):
        for ch in code.keys():
            if encoded.startswith(code[ch], pointer):
                encoded_str += ch
                pointer += len(code[ch])
    return encoded_str

# -----Main function
def main():
    s = "files/start.txt"
    m = "files/encode.txt"
    f = "files/decode.txt"

    s = open(s).read()
    m = open(m, "w")
    f = open(f, "w")

    code = huffman_encode(s)
    encoded = "".join(code[ch] for ch in s)
    decode = huffman_decode(encoded, code)

    m.write("{} {}".format(len(code), len(encoded)))
    for ch in sorted(code):
        m.write("{}: {}\n".format(ch, code[ch]))
    m.write(encoded)
    f.write(decode)

    m.close()
    f.close()


if __name__ == "__main__":
    main()
