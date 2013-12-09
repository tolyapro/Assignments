import itertools
import sys


def segment_string(input, dict):
    if input in dict:
        return [input]

    length = len(input)
    for i in range(1, length):
        prefix = input[0:i]
        if prefix in dict:
            suffix = input[i:length]
            seg_suffix = segment_string(suffix, dict)
            if seg_suffix:
                return [prefix] + seg_suffix

    return None


def check_bad_input(code_words): # e.g. {01 23 45 012345}
    biggest_word = code_words[0]
    for code in code_words:
        if len(code) > len(biggest_word):
            biggest_word = code

    other_words = [word for word in code_words if word != biggest_word]
    return segment_string(biggest_word, other_words) != None


def find_super_string(begin, end, dict):
    results = []
    if begin + end in dict:
        results.append('')
    for i in range(1,len(dict)):
        for variant in itertools.permutations(dict, i):
            candidate = begin
            for word in variant:
                candidate += word
            candidate += end
            if candidate in dict:
                results.append(variant)
    return results


def path(matrix, next, i, j, infinity):
    if matrix[i][j] == infinity:
        return None

    intermediate = next[i][j]

    if intermediate == -1:
        return [(i,j)]
    else:
        return path(matrix, next, i, intermediate, infinity) + path(matrix, next, intermediate, j, infinity)


def main():
    code_words = []

    with open("input.txt", "r") as input_file:
        code_words = input_file.read().split()

    prefixes = set()
    suffixes = set()


    if check_bad_input(code_words):
        biggest_word = code_words[0]
        for code in code_words:
            if len(code) > len(biggest_word):
                biggest_word = code

        with open('output.txt', 'w') as f:
            f.write(biggest_word)

    else:
        for word in code_words:
            for i in range(1, len(word)):
                prefix = word[0:i]
                if prefix not in code_words and len(prefix) > 0:
                    prefixes.add(prefix)


            for i in range(1, len(word)):
                suffix = word[i:len(word)]
                if suffix not in code_words and len(suffix) > 0:
                    suffixes.add(suffix)

        vertices = prefixes.intersection(suffixes)

        vertices = list(vertices)
        vertices.append('')

        infinity = len(code_words) * max([len(word) for word in code_words]) * max([len(word) for word in code_words]) + 1 

        matrix = [[infinity] * len(vertices) for x in range(len(vertices))] # distance matrix for Floyd algorithm
        codes = [[''] * len(vertices) for x in range(len(vertices))] # matrix containing code words on edges
        next = [[-1] * len(vertices) for x in range(len(vertices))] # matrix for path reconstruction in Floyd algorithm



        for i in range(len(vertices)):
            u = vertices[i]
            for j in range(len(vertices)):
                v = vertices[j]
                if i != j:
                    # checking for edge

                    super_strings = find_super_string(u, v, code_words)

                    if len(super_strings) > 0:
                        possible_variants = []
                        min_len = len(''.join(super_strings[0]))
                        min_ind = 0
                        for string_ind in range(len(super_strings)):
                            super_string = super_strings[string_ind]
                            current_string = ''.join(super_string)
                            if len(current_string) < min_len:
                                min_len = len(current_string)
                                min_ind = string_ind
                            possible_variants.append(current_string)

                        best_variant = possible_variants[min_ind]
                        matrix[i][j] = len(u) + len(best_variant)
                        codes[i][j] = best_variant



        #Floyd algorithm

        V = len(vertices)
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    if matrix[i][k] + matrix[k][j] < matrix[i][j]:
                        matrix[i][j] = matrix[i][k] + matrix[k][j]
                        next[i][j] = k


        min_dist = infinity
        pair = 0


        i = len(vertices)-1 # epsilon vertex

        u = vertices[len(vertices)-1]
        for j in range(len(vertices)):
            v = vertices[j]
            if i != j:
                if matrix[i][j] + matrix[j][i] < min_dist:
                    min_dist = matrix[i][j] + matrix[j][i]
                    pair = (i,j)

        if pair == 0: #no cycle
            with open('output.txt', 'w') as f:
                pass
        else:
            ambiguos_code = ''

            for vert in path(matrix, next, pair[0], pair[1], infinity):
                ambiguos_code += vertices[vert[0]]
                ambiguos_code += codes[vert[0]][vert[1]]

            for vert in path(matrix, next, pair[1], pair[0], infinity):
                ambiguos_code += vertices[vert[0]]
                ambiguos_code += codes[vert[0]][vert[1]]

            with open('output.txt', 'w') as f:
                f.write(ambiguos_code)


if __name__ == '__main__':
    main()