from dataclasses import dataclass
from typing import List, Union, TypeAlias, Optional
from typing import Optional

HTree: TypeAlias = Union[None, 'HuffmanNode']

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
    if a.freq < b.freq: #if the first node's frequency is less than the second node, wil return True
        return True
    elif a.freq == b.freq: #if frequency is equal, will return True if first node's ascii is less than the 2nd node
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

    if comes_before(a, b): #assigns left and right of new node based on smaller frequency
        left = a
        right = b
    else:
        left = b
        right = a

    if a.char_ascii < b.char_ascii: #assigns ascii based on smaller ascii value of the 2 nodes
        ascii = a.char_ascii
    else:
        ascii = b.char_ascii

    freq = a.freq + b.freq #frequency is the sum of the frequency of both nodes

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
                for char in line: #traverses through every character in the file
                    freq_list[ord(char)] += 1 #If ascii value of the character matches the index, increments the value by 1
    except FileNotFoundError: #raises error if file is not found
        raise FileNotFoundError
    return freq_list

def create_huff_tree(char_freq: List) -> Optional[HuffmanNode]:
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""

    if sum(char_freq) == 0: #returns None if there are no characters in the file
        return None
    lst = []

    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            node = HuffmanNode(i, char_freq[i]) #creates a new node based on index (ascii value) and value (frequency)
            lst.append(node)
    lst.sort()

    if len(lst) == 1: #if there is only 1 unique character, returns the node at index 0
        return lst[0]

    else:
        while len(lst) > 1: #while the there is more than one item in the list, pops the first 2 items from list
            a = lst.pop(0)
            b = lst.pop(0)
            lst.append(combine(a, b)) #combines the first 2 nodes using combine method
            lst.sort() #sorts the list
        return lst[0] #returns the combined nodes => one single node

def create_code(node: Optional[HuffmanNode]) -> List:
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the array, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""

    codeLst = [""] * 256
    if node is not None:
        helper(node, "", codeLst)
    return codeLst


def helper(node: Optional[HuffmanNode], code: str, codeLst: List) -> None:
    if node.left is None and node.right is None: #if the node is a leaf node, attaches a code based on its position in the tree
        codeLst[node.char_ascii] = code
    else:
        helper(node.left, code + "0", codeLst) #attaches 0 if moving left on tree
        helper(node.right, code + "1", codeLst) #attaches 1 if moving right on tree


def create_header(freqs: List) -> str:
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list associated with "aaabbbbcc, would return “97 3 98 4 99 2” """

    header = ""
    for i in range(len(freqs)):
        if freqs[i] != 0:
            header = header + str(i) + " " + str(freqs[i]) + " " #creates header with ascii value and frequency

    return header[:-1] #returns header without the last space at the end


def huffman_encode(in_file: str, out_file: str) -> None:
    """Takes input file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""

    try:
        freq = cnt_freq(in_file)
    except FileNotFoundError:
        raise FileNotFoundError #raises error if file is not found
    hTree = create_huff_tree(freq)
    code = create_code(hTree)
    header = create_header(freq)

    if sum(freq) == 0:
        # Handles empty file case
        return

    elif hTree.right is None and hTree.left is None: # Handles single character, by only writing ascii value and frequency
        with open(out_file, "w") as file:
            file.write(str(hTree.char_ascii) + " " + str(hTree.freq))
    else:
        with open(out_file, "w") as file:
            file.write(header) #writes header for first line
            file.write("\n") #new line
            text = ''
            with open(in_file, "r") as infile:
                input_text = infile.read()
                for char in input_text:
                    text += code[ord(char)] #for every character, attaches code based on ascii value of the char stored in code list
                file.write(text)

def parse_header(header_string: str) -> List:
    lst = [0] * 256
    freq = header_string.split()
    for index in range(0, len(freq), 2): #frequency for information stored in the header
        lst[int(freq[index])] = int(freq[index + 1])
    return lst

def huffman_decode(encoded_file, decode_file) -> None:
    try:
        efile = open(encoded_file, "r")
    except:
        raise FileNotFoundError
    first = efile.readline()
    sec = efile.readline()
    freq = parse_header(first)
    tree = create_huff_tree(freq)
    pos = tree
    with open(decode_file, "w") as dfile:
        for num in sec:
            if num == "0": #decoding the file by identifying if the number is 0 or 1
                pos = pos.left
                if pos.left is None and pos.right is None:
                    dfile.write(chr(pos.char_ascii))
                    pos = tree
            elif num == "1":
                pos = pos.right
                if pos.left is None and pos.right is None:
                    dfile.write(chr(pos.char_ascii))
                    pos = tree






