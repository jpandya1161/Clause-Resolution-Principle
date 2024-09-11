import re
import sys

def negation(first_literal, second_literal):
    if first_literal == ('~' + second_literal) or second_literal == ('~' + first_literal):
        return True
    else:
        return False

def validation(initial_resolution):
    for r1 in initial_resolution:
        for r2 in initial_resolution:
            if negation(r1, r2):
                return True
    return False

def resolution(first_clause, second_clause, clauses):
    iterative_resolution = first_clause + second_clause
    initial_resolution = None
    hashmap = {}
    for r1 in iterative_resolution:
        if r1 not in hashmap:
            hashmap[r1] = 0

    initial_resolution = list(hashmap.keys())
    ors = list(hashmap.keys())
    for first_literal in first_clause:
        for second_literal in second_clause:
            if negation(first_literal, second_literal):
                initial_resolution.remove(first_literal)
                initial_resolution.remove(second_literal)
                if not initial_resolution:
                    return False
                elif validation(initial_resolution):
                    return True
                else:
                    for cl in clauses:
                        if not difference(initial_resolution, cl):
                            return True
                    return initial_resolution

    if initial_resolution == ors:
        return True

def difference(l1, l2):
    difference_set = set(l1).symmetric_difference(l2)
    return list(difference_set)

def printing(cl, i1, i2):
    for c in cl:
        print()

def main():
    line_number = 1
    clauses = []
    with open(sys.argv[1], errors='ignore') as input_file:
        lines = input_file.readlines()

    for line in lines:
        line = re.sub(r'\n', '', line)
        line = re.sub(r'[ \t]+$', '', line)
        if line:  # Skip empty lines
            clause = line.split(" ")
            clauses.append(clause)

    if not clauses:
        print("No clauses found in the input file.")
        return

    clauses_to_solve = clauses[-1]
    del clauses[-1]

    for clause in clauses:
        print(line_number, ". ", ' '.join(clause), " { }", sep='')
        line_number += 1

    for c in range(len(clauses_to_solve)):
        if '~' in clauses_to_solve[c]:
            clauses_to_solve[c] = re.sub(r'~', '', clauses_to_solve[c])
        else:
            clauses_to_solve[c] = '~' + clauses_to_solve[c]

    for c in clauses_to_solve:
        clauses.append([c])
        print(line_number, ". ", ' '.join([c]), " { }", sep='')
        line_number += 1

    i_clause = 1
    while i_clause < line_number - 1:
        j_clause = 0
        while j_clause < i_clause:
            solution = resolution(clauses[i_clause], clauses[j_clause], clauses)
            if solution is False:
                print(line_number, ". ","Contradiction", ' {', i_clause + 1, ", ", j_clause + 1, '}', sep='')
                line_number += 1
                print("Valid")
                sys.exit(0)
            elif solution is True:
                j_clause += 1
                continue
            else:
                print(line_number, ". ",' '.join(solution), ' {', i_clause + 1, ", ", j_clause + 1, '}', sep='')
                line_number += 1
                clauses.append(solution)
            j_clause += 1
        i_clause += 1
    print('Not Valid')

if __name__ == "__main__":
    main()
