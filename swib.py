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
        
        
