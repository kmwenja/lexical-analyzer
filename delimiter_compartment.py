# delimiter compartment

class DelimiterCompartment(object):
    _src_compartment = None
    _temp = None
    
    def __init__(self, src_compt):
        self._src_compartment = src_compt
        self._temp = ''
   
    def nextChar(self):
        if len(self._temp)>0:
            temp = self._temp
            self._temp = ''
            return temp
        
        return self._src_compartment.nextCh()
    
    def is_skippable(self, char):
        if char == ' ':
            return True
        
        if char == '\n':
            return True
        
        if char == '\t':
            return True
        
        return False
    
    def skipBlank(self):
        curr_char = self.nextChar()
        
        # check for comments
        
        # check if current character is a /
        if curr_char == '/':
            # check if the next character is * or /
            next_char = self.nextChar()
            
            if next_char == '*':
                # comment mode
                # skip content till end
                curr_char = self.nextChar()
                wait_for_slash = False
                while(True):
                    if curr_char == '':
                        break
                    
                    if curr_char == '/' and wait_for_slash:
                        break
                    
                    if wait_for_slash and curr_char != '/':
                        wait_for_slash = False
                    
                    if curr_char == '*' and not wait_for_slash:
                        wait_for_slash = True
                    
                    curr_char = self.nextChar()
                
                return self.skipBlank()
            
            elif next_char == '/':
                # comment mode
                # skip content till end
                curr_char = self.nextChar()
                while(True):
                    if curr_char == '':
                        break
                    
                    if curr_char == '\n':
                        break
                    
                    curr_char = self.nextChar()
                
                return self.skipBlank()
            
            else:
                # save the next char for later
                self._temp = next_char
                
                # just return the /
                return curr_char
        
        # check for blanks, newlines, tabs
        # skip newlines, blanks, tabs
        if(self.is_skippable(curr_char)):
            return ' '
        
        return curr_char

