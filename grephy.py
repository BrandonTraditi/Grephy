import argparse
from auto import post_NFA, NFA_DFA, learn_alphabet,reg_post, get_DFA

def main():
    args = parseArgument()
    alphabet = learn_alphabet(args.input_file)
    regpost = reg_post(args.RegEx, alphabet)
    nfa = post_NFA(regpost)
    dfa = NFA_DFA(nfa, alphabet)
    compute_DFA(dfa, args.input_file)



def parseArgument():
    parser = argparse.ArgumentParser(description='Grep')
    parser.add_argument("-n",help="File to output a NFA")
    parser.add_argument("-d", help="File to output a DFA")
    parser.add_argument('RegEx', metavar='REGEX-PATTERN', type=str,help="Regular expression to search input file")
    parser.add_argument('input_file', metavar='INPUT-FILE',help="RegEx test file")
    argument = parser.parseArgument()
    return argument

if __name__ == "__main__":
    main()
