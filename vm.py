class VM:
    def __init__ (self):
        self.reset ()

    def reset (self):
        self.IP = 0
        self.script = []
        self.on_deck_index = 0
        self.on_deck = []
        self.temp_stack = []
        self.return_stack = []
        self.string_stack = []
        self.call_stack = []
        self.rule_name_stack = []
        self.label_dict = {}

    def resume (self, token):
        self.on_deck_index = len (self.on_deck)
        self.on_deck.push (token)

    def current_token (self):
        return self.on_deck [self.on_deck_index]

    def add_script (self, name, script):
        index = len (self.script)
        if name in self.label_dict:
            raise Exception (f'script label "{name}" already defined')
        self.label_dict [name] = index
        self.script.extend (script)

    def set_IP (self, name):
        if name in self.label_dict:
            self.IP = self.label_dict [name]
        else:
            raise Exception (f'script label "{name}" not found')
        

# We shall deal *only* with characters (Unicode characters). If we want to tokenize the
# input for "efficiency", we can assign one unique Unicode character to each token.
# Note that "efficiency" is usually not an issue for building software targetted at developers - the software
# just needs to run "fast enough" on development machines. If you find yourself wanting to speed this code
# up, you should ask yourself "why?" and "for whom?" first. This code is meant for developers, not end-users.
# If you want to production-engineer this code for end-users, then other, maybe more-important, issues might
# need to be considered first.

class InCharacter:
    def __init__ (self, c='', position=0):
        self.c = c
        self.position = position
        
class CharacterStream:
    # we put input characters into a cache 
    # when pattern matching is successful, we grab (accept) the string in the cache and reset the cache
    # when pattern matching is unsuccessful, we simply rewind the stream to the front and try again
    # When we want to inspect a character, we first check the cache. If the cache contains characters,
    # then there is no need to block waiting for I/O and we can simply forge ahead using characters
    # from the cache

    # creating a CharacterStream always blocks on I/O, waiting for the first character
    # advancing a CharacterStream only sometimes blocks on I/O, if there are no characters in the cache, or
    #  if we've run off the end of the cache
    # "blocking on I/O" means sending a "req" to the upstream reader and waiting until it responds
    #  on the '' port (empty string portname means the port is like stdin)

    def __init__ (self, eh):
        self.position = 0
        self.eh = eh
        return self.clear ()

    def clear (self, eh):
        self.cache = []
        self.cache_index = None
        return self.blocking_getc (eh)

    def blocking_getc (self, eh, msg):
        send (eh, "req", new_datum_bang (), msg):
        return ("io_blocked", None)


    def getc (self, eh, msg):
        if is_cache_empty (self) or (at_end_of_cache (self)):
            send (eh, "req", new_datum_bang (), msg)
            raise 
    
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
