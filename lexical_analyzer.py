# lexical analyzer

# version: 2.0
# author: Kennedy Mwenja, <mwenja07@gmail.com>
# author: Mwathi Wakaba, <mwathy11@gmail.com>
# author: James Macharia, <cjmasha@gmail.com>
# author: Brian Busolo, <brianbusolo@gmail.com>

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

def delimit_into_tuple_list(filename, elements=None):
    tuple_list = []
    
    f = open(filename)
    
    for i in f:
        # elements must be separated by a space
        splits = i.split(" ", elements) if elements else i.split(" ")
        
        # remove the new line from the last element
        splits[-1] = splits[-1][:-1] 
        
        tuple_element = tuple(splits)
        tuple_list.append(tuple_element)
        
    return tuple_list

def get_lookup_table(filename, elements=2, add_space=True):
    '''retrieve the lookup table from a file
    
    the lookup file should have the regex, token type 
    '''
    lookup_table = delimit_into_tuple_list(filename, elements)
    
    if add_space:
        lookup_table.insert(0, (r" ", "spaceTok"))
    
    return lookup_table

def get_reference_table(filename, elements=2):
    '''retrieve the reference codes from a file
    
    the reference file should have the token type and its code
    '''
    
    reference_list = delimit_into_tuple_list(filename, elements)
    reference_table = {}
    
    for i in reference_list:
        reference_table[i[0]] = i[1]
    
    return reference_table

def main():
    # check if the filenames were provided in the terminal
    if len(sys.argv) < 4:
        print 'Usage: python lexical_analyzer.py source_code_file lookup_file reference_file'
        return
    
    # get the filenames from the terminal
    source_code_file = sys.argv[1]
    lookup_file = sys.argv[2]
    reference_file = sys.argv[3]
    
    try:
        # get the source code
        f = open(source_code_file)
        source_code = f.read()
        f.close()
        
        # get the lookup table
        lookup_table = get_lookup_table(lookup_file)
        
        # get the reference table
        reference_table = get_reference_table(reference_file)
        
        symbol_table = {}
        
        DEFAULT_START = 8000
        
        counter = DEFAULT_START
        
        # initialize the analyzer
        la = LexicalAnalyzer(source_code, lookup_table)
        
        # iterate through the tokens/lexemes
        next_token = la.next_token()
        while next_token:
            token_type = next_token[0]
            value = next_token[1]
            
            if value not in symbol_table:
                code = reference_table[token_type]
            
                # cater for codes for tokens whose codes that change ie identifier tokens
                if code == '*':
                    code = counter
                    counter = counter + 1
                
                symbol_table[value] = { "type": token_type, "code": code }
            else:
                code = symbol_table[value]["code"]
            
            print "Token Type:",token_type,"Code:",code,"Value:",value    
            next_token = la.next_token()
        
        print "Done"

    except Exception, e:
        print repr(e)

if __name__ == "__main__":
    main()
