import unittest
from huffman import *

class TestList(unittest.TestCase):
    def test_cnt_freq(self) -> None:
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)

    def test_combine(self) -> None:
        a = HuffmanNode(65, 1)
        b = HuffmanNode(66, 2)
        c = combine(a, b)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii,65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:   # pragma: no cover
            self.fail()
        c = combine(b, a)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii,65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:   # pragma: no cover
            self.fail()

    def test_create_huff_tree(self) -> None:
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        if hufftree is not None:
            self.assertEqual(hufftree.freq, 32)
            self.assertEqual(hufftree.char_ascii, 97)
            left = hufftree.left
            right = hufftree.right
            if (left is not None) and (right is not None):
                self.assertEqual(left.freq, 16)
                self.assertEqual(left.char_ascii, 97)
                self.assertEqual(right.freq, 16)
                self.assertEqual(right.char_ascii, 100)
            else: # pragma: no cover
                self.fail()
        else: # pragma: no cover
            self.fail()

    def test_create_header(self) -> None:
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

    def test_create_code(self) -> None:
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_01_textfile(self) -> None:
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("file1_out.txt", "file1_soln.txt"))

    def tests_textfile(self) -> None:
        huffman_encode("declaration.txt", "declarationout.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("declaration_soln.txt", "declarationout.txt"))

    def tests2_textfile(self) -> None:
        huffman_encode("file2.txt", "file2out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("file2_soln.txt", "file2out.txt"))

    def tests3_textfile(self) -> None:
        huffman_encode("file5.txt", "file5out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("file5_soln.txt", "file5out.txt"))

    def test_error2_textfile(self) -> None:
        with self.assertRaises(FileNotFoundError):  # uses context manager for checking exception
            cnt_freq("file3.txt")
        with self.assertRaises(FileNotFoundError):  # uses context manager for checking exception
            huffman_encode("file3.txt", "file3_out")
        lst = [0] * 256
        self.assertEqual(create_huff_tree(lst), None)
        lst = [4] + [0] * 255
        self.assertEqual(create_huff_tree(lst), HuffmanNode(0, 4))
        huffman_encode("file4.txt", "file4compare.txt")
        self.assertTrue(compare_files("file4.txt", "file4compare.txt"))

    def test_parse_header(self) -> None:
      header = "97 2 98 4 99 8 100 16 102 2"
      freqlist = parse_header(header)
      anslist = [0]*256
      anslist[97:104] = [2, 4, 8, 16, 0, 2, 0]
      self.assertListEqual(freqlist[97:104], anslist[97:104])

    def test_parse_header2(self) -> None:
       header = "65 3 66 1 67 5 68 2"
       freqlist = parse_header(header)
       anslist = [0] * 256
       anslist[65:69] = [3, 1, 5, 2]
       self.assertListEqual(freqlist[65:69], anslist[65:69])

    def test_decode_01(self) -> None:
      huffman_decode("file1_soln.txt", "file1_decode.txt")
      # detect errors by comparing your encoded file with a *known* solution file
      self.assertTrue(compare_files("file1.txt", "file1_decode.txt"))

    def test_decode_02(self) -> None:
      huffman_decode("declaration_soln.txt", "declaration_decode.txt")
      # detect errors by comparing your encoded file with a *known* solution file
      self.assertTrue(compare_files("declaration.txt", "declaration_decode.txt"))

    def test_error3_textfile(self) -> None:
       with self.assertRaises(FileNotFoundError):  # uses context manager for checking exception
           huffman_decode("file7_soln.txt", "file1_decode.txt")

def compare_files(file1: str, file2: str) -> bool: # pragma: no cover
        match = True
        done = False
        with open(file1, "r") as f1:
            with open(file2, "r") as f2:
                while not done:
                    line1 = f1.readline().strip()
                    line2 = f2.readline().strip()
                    if line1 == '' and line2 == '':
                        done = True
                    if line1 != line2:
                        done = True
                        match = False
        return match


if __name__ == '__main__':
    unittest.main()
