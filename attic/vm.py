
#####


class InCharacter:
    def __init__ (self, c='', position=0):
        self.c = c
        self.position = position

class Breadcrumb:
    def __init__ (self, name, depth, pos):
        self.name = name
        self.depth = depth
        self.position = pos
        
class CharacterStream:
    # we put input characters in a cache 
    # when pattern matching is successful, we grab (accept) the string in the cache and reset the cache
    # when pattern matching is unsuccessful, we simply rewind the stream to the front and try again
    
    def __init__ (self, instream):
        self.position = 0
        self.instream = instream
        self.clear ()

    def getc (self):
        # ensure that the next character is in the cache
        # if the cache is not empty and the index is in bounds, then the character is already in place
        # else, get a character from instream and append it to the cache
        # for convenience EOF is a character and is defined above
        if len (self.cache) == 0:
            c = self.instream.read (1)
            if 1 > len (c):
                c = self.endchar ()
            self.position += 1
            self.cache = [InCharacter (c=c, position=self.position)]
            self.cache_index = 0
        elif len (self.cache) == (self.cache_index + 1):
            c = self.instream.read (1)
            if 1 > len (c):
                c = self.endchar ()
            self.position += 1
            self.cache.append (InCharacter (c=c, position=self.position))
            self.cache_index += 1
        elif self.cache [self.cache_index] != self.endchar ():
            self.cache_index += 1
        else:
            pass

    def rewind (self):
        self.cache_index = 0

    def clear (self):
        self.cache = []
        self.cache_index = None
        self.getc ()

    def accept (self):
        r = self.cache_toString ()
        self.clear ()
        return r

    def current_char (self):
        return self.cache [self.cache_index].c

    def current_input_position (self):
        return self.position

    def cache_toString (self):
        s = ""
        for in_c in self.cache:
            s = s + in_c.c
        return s

    def endchar (self):
        return chr (0)

class VM:
    # A receptor VM parses the input stream of characters and keeps track of how it got there and what it is working on.
    # A receptor uses rules that can call other rules (so, we need to use stacks, to keep everything separated).
    # Each rule begins a fresh string and builds it up.
    # When a rule finishes, it pops its own string off of the string stack and puts it onto the return stack - the caller
    #  deals with the returned string (typically by adding it to its own string). The caller must delete the returned value
    #  from the return stack. Note that the caller can further parse the returned string, if it so wishes.

    def __init__ (self, instream, eh):
        self.instream = CharacterStream (instream)
        self.script = []
        self.IP = -1
        self.string_stack = []
        self.return_stack = []
        self.call_stack = []
        self.cycle_stack = []
        self.breadcrumb_stack = []
        self.breadcrumb_wip_stack = []
        self.breadcrumb_wip_depth = 0
        self.eh = eh

        self.op_push_new_string = 0
        self.op_enter = 1
        self.op_exit = 2
        self.op_call = 3
        self.op_append_returned_string = 3
        self.op_return_string_pop = 4
        self.op_begin_cycle = 5
        self.op_end_cycle = 6
        self.op_mark = 7
        self.op_peek_string = 8
        self.op_peek_eof = 9
        self.op_expect_and_append = 10
        self.op_break = 11
        self.op_continue = 12

    def execute (self, script):
        self.IP = len (self.script)
        self.script.push (script)
        self.stepper ()

    def stepper (self):
        op = self.script [self.IP]
        # each op must bump self.IP appropriately...
        if op == self.op_push_new_string:
            self.push_new_string ()
            self.IP += 1
        elif op == self.op_enter:
            self.IP += 1
            s = self.script [self.IP]
            self.IP += 1
            self.enter (s)
        elif op == self.op_exit:
            self.IP += 1
            s = self.script [self.IP]
            self.IP += 1
            self.exit (s)
        elif op == self.op_call:
            self.IP += 1
            func = self.script [self.IP]
            self.IP += 1
            self.callstack.push (self.IP)
            func (self)
        elif op == self.op_append_returned_string:
            self.IP += 1
            self.append_returned_string ()
        elif op == self.op_return_string_pop:
            self.IP += 1
            self.return_string_pop ()
        elif op == self.op_begin_cycle:
            self.IP += 1
            self.cycle_stack.push (self.IP)
        elif op == self.op_end_cycle:
            self.IP += 1
            self.cycle_stack.pop ()
        elif op == self.op_mark:
            self.IP += 1
            # noop            
        elif op == self.op_break:
            self.IP += 1
            # GOTO instruction after cycle_end 
            self.goto_forward (self.cycle_end)
        elif op == self.op_continue:
            self.IP += 1
            # GOTO instruction after cycle_begin 
            self.goto_backward (self.cycle_begin)
        elif op == self.op_peek_string:
            self.IP += 1
            s = self.script [self.IP]
            self.IP += 1
            if self.peek (s):
                pass
            else:
                self.goto_next_choice ()
        elif op == self.op_peek_eof:
            self.IP += 1
            if self.at_eof (s):
                pass
            else:
                self.goto_next_choice ()
        elif op == self.op_expect_and_append:
            self.IP += 1
            s = self.script [self.IP]
            self.IP += 1
            self.expect_and_append (s)
        else:
            raise Exception (f'VM illegal op "{op}"')


    def goto_next_choice (self):
        while True:
            op = self.script [self.IP]
            if op == self.vm_cycle_end:
                break
            elif op == self.vm_mark:
                self.IP += 1
                break
            else:
                self.IP += 1
                
    def goto_forward (self, op):
        while not (op == self.script [self.IP]):
            self.IP += 1
        self.IP += 1

    def goto_backward (self, op):
        while not (op == self.script [self.IP]):
            self.IP -= 1
        self.IP += 1

    def push_new_string (self):
        self.string_stack.append ("")
        
    def return_string_pop (self):
            r = self.string_stack.pop ()
            self.return_stack.append (r)

    def return_ignore_pop (self):
            r = self.string_stack.pop ()
            self.return_stack.append ("")

    def enter (self, name):
        self.breadcrumb_wip_depth += 1
        b = Breadcrumb (name, self.breadcrumb_wip_depth, self.instream.current_input_position ())
        self.breadcrumb_wip_stack.append (b)
        
    def exit (self, name):
        b = self.breadcrumb_wip_stack.pop ()
        self.breadcrumb_stack.append (b)
        self.breadcrumb_wip_depth -= 1

    def trace (self, s):
        print (f'\x1B[102m{self.breadcrumb_wip_stack [-1].name} depth={self.breadcrumb_wip_stack [-1].depth} pos={self.breadcrumb_wip_stack [-1].position} c="{self.instream.current_char ()}" {s}\x1B[0m')

    def call (self, f):
        f (self) # for future consideration ...

    def peek (self, s):
        if self.peek_recursively (s):
            self.instream.rewind ()
            return True
        else:
            self.instream.rewind ()
            return False

    def at_eof (self):
        return self.instream.endchar () == self.instream.current_char ()

    ### helpers
    
    # def peek_recursively (self, s):
    #     if 0 == len (s):
    #         if self.at_eof ():
    #             return True
    #         else:
    #             return False
    #     elif s [0] == self.instream.current_char ():
    #         if 1 == len (s):
    #             return True
    #         else:
    #             self.instream.getc ()
    #             return self.peek_recursively (s [1:])
    #     else:
    #         return False
    def peek_recursively (self, s_parameter):
        self.eh.temp_stack.push (s_parameter)
        # anti-recursion - recursion simply saves state on the callstack, let's save state, too, but, in an explicit stack instead of the callstack
        while True:
            s = self.eh.temp_stack.pop ()
            if 0 == len (s):
                if self.at_eof ():
                    return True
                else:
                    return False
            elif s [0] == self.instream.current_char ():
                if 1 == len (s):
                    return True
                else:
                    self.eh.temp_stack.push (s [1:]) # CDR(s)
                    r = self.instream.getc ()
                    if r == self.instream._blocked:
                        ???
                    else:
                        pass
                    # continue looping, as if this is a recursive call
            else:
                return False

# ??? what's used and what's dead ??
    
#     def append (self, s):
#         self.string_stack [-1] = self.string_stack [-1] + s
        
#     def accept_and_append (self):
#         s = self.instream.accept ()
#         self.append (s)

#     def endchar (self):
#         return self.instream.endchar ()


#     def append_returned_string (self):
#         s = self.return_stack.pop ()
#         self.append (s)

#     def expect_and_append (self, s):
#         if self.peek (s):
#             self.accept_and_append ()
#         else:
#             self.error (s)

#     def maybe_append (self, s):
#         if self.peek (s):
#             self.accept_and_append ()
#             return True
#         else:
#             return False

#     def pop_return_value (self):
#         r = self.return_stack.pop ()
#         return r

    def error (self, s):
        b = self.breadcrumb_wip_stack [-1]
        c = self.instream.current_char ()
        c = self.make_printable (c)
        s = self.make_printable (s)
        print (f'\x1B[101mReceptor error at input position {self.instream.current_input_position ()} wanted "{s}" got "{c}" (rule {b.name} beginning at {b.position})"\x1B[0m')
        sys.exit (1)

    def make_printable (self, c):
        if c == self.instream.endchar ():
            c = "_end"
        elif c == "\n":
            c = "_newline"
        elif c == "\t":
            c = "_tab"
        elif c == " ":
            c = "_space"
        else:
            pass
        return c
            

