"""
Given two series of keystrokes, determine if they result in the same output.
The character "<" represents a backspace.

Example 1:
keys1 = "asd" => "asd"
keys2 = "asdd" => "asdd"
false

Example 2:
keys1 = "asd" => "asd"
keys2 = "asx<d" => "asd"
true
"""

def compare_keys(keys1, keys2):
    
    def next_char(keys, index):
        """ Determines the index of the next char to process in keys. Returns -1 if nothing left to process. """
        backspaces = 0

        while index >= 0:
            if keys[index] == "<":
                backspaces += 1
            else:
                if backspaces == 0:
                    return index
                backspaces -= 1
            index -= 1

        return -1

    #initialize index 1 and 2 to the first valid index (if it exists)
    index1 = next_char(keys1, len(keys1) - 1)
    index2 = next_char(keys2, len(keys2) - 1)

    while index1 >= 0 and index2 >= 0:
        if keys1[index1] != keys2[index2]:
            return False
        index1 = next_char(keys1, index1 - 1)
        index2 = next_char(keys2, index2 - 1)

    return index1 == index2


