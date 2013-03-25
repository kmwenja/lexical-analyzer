# lexical analyzer

# version: 2.0
# author: Kennedy Mwenja, <mwenja07@gmail.com>
# author: Mwathi Wakaba, <mwathy11@gmail.com>

import sys

import source_compartment
import delimiter_compartment
import token_compartment


class LexicalAnalyzer(object):
    '''the lexical analyzer proper'''
    
    def __init__(self, source_code, lookup_table):
        '''initialize the analyzer with its components'''
        
        # initialize the source compartment with the source code
        self._source_compartment = source_compartment.SourceCompartment(source_code)
        
        # initialize the delimiter compartment with the source compartment
        self._delimiter_compartment = delimiter_compartment.DelimiterCompartment(self._source_compartment)
        
        # initialize the token compartment with the delimiter and the lookup table
        self._token_compartment = token_compartment.TokenCompartment(self._delimiter_compartment, lookup_table)
    
    def next_token(self):
        '''return the next token gotten from the token compartment'''
        return self._token_compartment.nextToken()

def get_lookup_table(filename, elements=2, add_space=True):
    '''retrieve the lookup table from a file
    
    the lookup file should have the regex, token type 
    '''
    lookup_table = []
    
    f = open(filename)
    for i in f:
        splits = i.split(" ", elements) # elements must be separated by a space
        
        splits[-1] = splits[-1][:-1] # remove the new line from the last element
        
        token = tuple(splits)
        lookup_table.append(token)
    
    if add_space:
        lookup_table.insert(0, (r" ", "spaceTok"))
    
    return lookup_table

def main():
    if len(sys.argv) < 3:
        print 'Usage: python lexical_analyzer.py source_code_file lookup_file'
        return
    
    source_code_file = sys.argv[1]
    lookup_file = sys.argv[2]
    try:
        # get the source code
        f = open(source_code_file)
        source_code = f.read()
        f.close()
        
        # get the lookup table
        lookup_table = get_lookup_table(lookup_file, elements=3)
        
        # initialize the analyzer
        la = LexicalAnalyzer(source_code, lookup_table)
        
        # iterate through the tokens
        next_token = la.next_token()
        while next_token[0]:
            print repr(next_token)            
            next_token = la.next_token()
        
        print "Done"

    except Exception, e:
        print repr(e)

if __name__ == "__main__":
    main()
