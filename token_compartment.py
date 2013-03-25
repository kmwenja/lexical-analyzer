# token compartment

import re

class TokenCompartment(object):
    _matchers = None
    _delimiter_compartment = None
    _buffer = None
    _space_token_type = None
    _ignore_space = None
    
    def __init__(self, delimiter_compartment, lookup_table = [], space_token_type="spaceTok", ignore_space=True):
        self._delimiter_compartment = delimiter_compartment
        self._buffer = ''
        self._matchers = []
        self._space_token_type = space_token_type
        self._ignore_space = ignore_space
        
        # initialize the matchers
        for val in lookup_table:
            regex = val[0]
            obj = re.compile(r'^'+regex+r'$') # get exact matches
            self._matchers.append((obj,val[1]))
    
    def nextChar(self):
        return self._delimiter_compartment.skipBlank()
    
    def match_return(self, prev_matcher, prev_match_pos):
        # build the lexeme
        match = (self._matchers[prev_matcher][1], self._buffer[:prev_match_pos])
        
        # reset the buffer
        self._buffer = self._buffer[prev_match_pos:]
        
        # check if match is space token
        if match[0] == self._space_token_type:
            # check if we're supposed to ignore spaces
            if self._ignore_space:
                # return the next token
                return self.nextToken()
        
        # return the lexeme
        return match
    
    def nextToken(self):
        prev_matcher = None
        prev_match_pos = None
        prev_match = None
        
        while True:
            for index in xrange(0,len(self._matchers)):
                # match regex to current buffer
                key = self._matchers[index][0]
                res = key.match(self._buffer)
                
                if res:
                    # we have a match
                    prev_matcher = index
                    prev_match_pos = len(self._buffer)
                    prev_match = res
                    break
            
            # if there was no match
            if not res:
                # check if we had a previous match
                if prev_match:
                    # return the match
                    return self.match_return(prev_matcher, prev_match_pos)
                
            # add the next character to the buffer
            curr_char = self.nextChar()
            
            # if we've reached the end
            if curr_char == '':
                if prev_match:
                    # return the match
                    return self.match_return(prev_matcher, prev_match_pos)
                else:
                    if len(self._buffer)> 0:
                        raise Exception("Error processing: %s" % self._buffer)
                    
                    return (None, None)
            
            self._buffer = self._buffer + curr_char

