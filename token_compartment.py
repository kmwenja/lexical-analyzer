# token compartment

import re

class TokenCompartment(object):
    '''the compartment that builds the tokens'''
    
    def __init__(self, delimiter_compartment, lookup_table = [], 
        space_token_type="spaceTok", ignore_space=True):
        '''initialize the token compartment with the delimiter compartment, the lookup table
        and some other compartment specific options'''
        
        self._delimiter_compartment = delimiter_compartment
        
        # an empty string that will hold the current fragment of 
        # the source code that is being processed into a token
        self._buffer = ''
        
        # an array of regex matchers that will be used to determine a token
        self._matchers = []
        
        # string that describes the space token type ie spaceTok
        self._space_token_type = space_token_type
        
        # boolean value that will check if we are not to tokenize spaces
        self._ignore_space = ignore_space
        
        # initialize the matchers
        for val in lookup_table:
            # get the regex for the token
            regex = val[0]
            
            # initialize a matcher for that regex
            obj = re.compile(r'^'+regex+r'$') # get exact matches
            
            # add the matcher to our list of matchers
            self._matchers.append((obj,val[1])) # add the token type for reference
    
    def nextChar(self):
        '''helper to return the next character 
        from the delimiter compartment'''
        
        return self._delimiter_compartment.skipBlank()
    
    def match_return(self, prev_matcher, prev_match_pos):
        '''helper to create the return object (lexeme) for tokens 
        ie (token_type, token_value)'''
        
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
        '''tokenize characters from the delimiter compartment into lexemes'''
        
        prev_matcher = None
        prev_match_pos = None
        prev_match = None
        
        # implement longest match rule
        while True:
            # keep building a string of characters until you reach 
            # the longest match
            
            # loop through the matchers
            for index in xrange(0,len(self._matchers)):
                # get the current matcher
                key = self._matchers[index][0]
                
                # match regex to current buffer
                res = key.match(self._buffer)
                
                # check if we have a match
                if res:
                    # save the matcher that made the match
                    prev_matcher = index
                    
                    # save the position (so far) of the buffer that has the match
                    prev_match_pos = len(self._buffer)
                    
                    # the match object itself (which contains the string that matched etc)
                    prev_match = res
                    
                    # exit the for loop because we dont need to find another match
                    break
            
            # if there was no match at the end of the for loop
            if not res:
                # check if we had a previous match
                if prev_match:
                    # return the match (it's token type and actual value)
                    return self.match_return(prev_matcher, prev_match_pos)
                
            # get the next character
            curr_char = self.nextChar()
            
            # check if we've reached the end of the source code
            if curr_char == '':
                # check if we had a previous match
                if prev_match:
                    # return the match
                    return self.match_return(prev_matcher, prev_match_pos)
                else:
                    # check if we've finished with all the source code
                    if len(self._buffer)> 0:
                        # if we still have some source code left then something went wrong
                        raise Exception("Error processing: %s" % self._buffer)
                    # return a blank token to mark the end
                    return None
            
            # add the next character to the buffer
            self._buffer = self._buffer + curr_char

