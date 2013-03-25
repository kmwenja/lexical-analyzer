# source compartment

class SourceCompartment(object):
    '''compartment responsible for pre-processing the source code
    and giving other compartments single characters from the source code'''
    
    def __init__(self, data):
        self._data = data
        self._current_index = 0
        self._len = len(data)
        self._definitions = {}
        self._in_directive = False
    
    def current_char(self):
        return self._data[self._current_index]
    
    def increment(self):
        self._current_index = self._current_index + 1
    
    def is_end(self):
        return self._current_index == self._len
    
    def nextCh(self):
        '''preprocesses compiler directives and returns a character 
        from the preprocessed source code'''
        
        # check if we've reached the end
        if self.is_end():
            # return an empty string
            return ''
        
        # get a character from the source code
        curr_char = self.current_char()
        
        # move the cursor to the next character
        self.increment();
        
        # check if the character is the beginning of a directive
        if curr_char == '#' and not self._in_directive:
            self._in_directive = True
            
            # find out what directive it is
            directive = ''
            
            next_char = self.nextCh()
            while(next_char != ' '):
                if next_char == '':
                    raise Exception("Reached end of file without completing operation at %s" % directive)
                
                directive = directive + next_char
                next_char = self.nextCh()
            
            # if the directive is define
            if directive == 'define':
                # get definition name
                definition = ''
                
                next_char = self.nextCh()
                while(next_char != ' '):
                    if next_char == '':
                        raise Exception("Reached end of file without completing operation at %s" % definition)
                    definition = definition + next_char
                    next_char = self.nextCh()
                
                # get definition body
                body = ''
                
                next_char = self.nextCh()
                while(next_char != '#'):
                    if next_char == '':
                        raise Exception("Reached end of file without completing operation at %s" % body)
                    body = body + next_char
                    next_char = self.nextCh()
                
                # get closing to confirm directive
                closing = ''
                
                next_char = self.nextCh()
                while(next_char != ' '):
                    if next_char == '':
                        raise Exception("Reached end of file without completing operation at %s" % closing)
                    if next_char == '\n':
                        break
                    closing = closing + next_char
                    next_char = self.nextCh()
                
                if closing != 'enddef':
                    raise Exception("Illegal define: %s" % definition)
                    
                self._definitions[definition] = body
                
                self._in_directive = False
                
                return self.nextCh()
                    
            elif directive == 'include':
                # get file
                filename = ''
                
                next_char = self.nextCh()
                while(next_char != ' '):
                    if next_char == '':
                        raise Exception("Reached end of file without completing operation at %s" % filename)
                    if next_char == '\n':
                        break
                    filename = filename + next_char
                    next_char = self.nextCh()
                
                # check if filename conforms to rules
                if filename[0] != '<' or filename[-1] != '>':
                    raise Exception("Illegal include: %s" % filename)
                
                # open the included file
                f = open(filename[1:-1])
                new_data = f.read()
                f.close()
                
                # add the file's source code to data stream at the cursor
                self._data= self._data[:self._current_index] + new_data + self._data[self._current_index:]
                self._len = self._len + len(new_data)
                
                # finish directive processing
                self._in_directive = False
                                
                return self.nextCh()
            
            elif directive in self._definitions:
                # get the definition body
                body = self._definitions[directive]
                
                # add the body to the data stream at the cursor
                self._data= self._data[:self._current_index] + body + self._data[self._current_index:]
                self._len = self._len + len(body)
                
                # finish directive processing
                self._in_directive = False
                
                return self.nextCh()
                
            else:
                # there is no such directive
                raise Exception("Illegal directive: %s" % directive)
                
        
        return curr_char

