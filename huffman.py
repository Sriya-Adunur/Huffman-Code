from dataclasses import dataclass
from typing import List, Union, TypeAlias, Optional
from typing import Optional

#HTree: TypeAlias = Union[None, 'HuffmanNode']
HTree: TypeAlias = Optional['HuffmanNode']

@dataclass
class HuffmanNode:
    char_ascii: int         # stored as an integer - the ASCII character code value
    freq: int               # the frequency associated with the node
    left: HTree = None      # Huffman tree (node) to the left
    right: HTree = None     # Huffman tree (node) to the right


    def __lt__(self, other: 'HuffmanNode') -> bool:
        return comes_before(self, other)


def comes_before(a: HuffmanNode, b: HuffmanNode) -> bool:
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq < b.freq:
        return True
    elif a.freq == b.freq:
        if a.char_ascii < b. char_ascii:
            return True
        else:
            return False
    else:
        return False

def combine(a: HuffmanNode, b: HuffmanNode) -> HuffmanNode:
    """Creates a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lower of the a and b char ASCII values"""

    if comes_before(a, b):
        left = a
        right = b
    else:
        left = b
        right = a

    if a.char_ascii < b.char_ascii:
        ascii = a.char_ascii
    else:
        ascii = b.char_ascii

    freq = a.freq + b.freq

    node = HuffmanNode(ascii, freq, left, right)
    return node

def cnt_freq(filename: str) -> List:
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""

    freq_list = [0] * 256
    try:
        with open(filename, "r") as file:
            for line in file:
                for char in line:
                    freq_list[ord(char)] += 1
    except FileNotFoundError:
        raise FileNotFoundError
    return freq_list

def create_huff_tree(char_freq: List) -> Optional[HuffmanNode]:
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""

    if sum(char_freq) == 0:
        return None
    lst = []

    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            node = HuffmanNode(i, char_freq[i])
            lst.append(node)
    lst.sort()

    if len(lst) == 1:
        return lst[0]

    else:
        while len(lst) > 1:
            a = lst.pop(0)
            b = lst.pop(0)
            lst.append(combine(a, b))
            lst.sort()
        return lst[0]

def create_code(node: Optional[HuffmanNode]) -> List:
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the array, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""

    codeLst = [""] * 256
    if node is not None:
        helper(node, "", codeLst)
    return codeLst


def helper(node: Optional[HuffmanNode], code: str, codeLst: List) -> None:
    if node.left is None and node.right is None:
        codeLst[node.char_ascii] = code
    else:
        helper(node.left, code + "0", codeLst)
        helper(node.right, code + "1", codeLst)


def create_header(freqs: List) -> str:
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """

    header = ""
    for i in range(len(freqs)):
        if freqs[i] != 0:
            header = header + str(i) + " " + str(freqs[i]) + " "

    return header[:-1]


def huffman_encode(in_file: str, out_file: str) -> None:
    """Takes input file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""

    try:
        freq = cnt_freq(in_file)
    except FileNotFoundError:
        raise FileNotFoundError
    hTree = create_huff_tree(freq)
    code = create_code(hTree)
    header = create_header(freq)

    if sum(freq) == 0:
        # Handle empty file case
        return

    elif hTree.right is None and hTree.left is None:
        with open(out_file, "w") as file:
            file.write(str(hTree.char_ascii) + " " + str(hTree.freq))
    else:
        with open(out_file, "w") as file:
            file.write(header)
            file.write("\n")
            text = ''
            with open(in_file, "r") as infile:
                input_text = infile.read()
                for char in input_text:
                    text += code[ord(char)]
                file.write(text)