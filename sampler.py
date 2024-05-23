# Sampler

import py0d as zd

# Sampler

def Sampler_init (vm):
    vm.add_script ("Sampler", [
        vm.push_new_string,
        vm.enter, "Sampler",
          vm.call, Stuff_swib,
          vm.append_returned_string,
          vm.expect_and_append_eof
        vm.exit, "Sampler",
        vm.return_string_pop
        ])

def Stuff_init (vm):
    vm.add_script ("Stuff", [
        vm.push_new_string,
        vm.enter, "Stuff",
          vm.begin_cycle,

            vm.mark,
            vm.peek_string, "Hello World",
              vm.call, Hello,
              vm.append_returned_string
              vm.continue
        
            vm.mark,
            vm.peek_eof,
              vm.break,

          vm.end_cycle,
        vm.exit, "Stuff",
        vm.return_string_pop
        ])

def Hello_init (vm):
    vm.add_script ("Hello", [
        vm.push_new_string,
        vm.enter, "Hello", 
          vm.expect_and_append, "Hello World",
        vm.exit, "Hello",
        vm.return_string_pop
        ])

def begin (vm):
    Sampler_init (vm)
    Stuff_init (vm)
    Hello_init (vm)
    vm.set_IP ("Sampler")
    # don't resume() here, resume() when "" message received (see below)

import vm

class SWIB_State:
    def __init__ (self):
        self.state = "idle"
        self.vm = vm.VM ()
        
def Sampler_handler (eh, msg):
    if eh.instance_data.state == "io_blocked" and  msg.port == "":
        eh.state = "running"
        c = msg.datum.srepr ()
        eh.instance_data.vm.resume (c)
    elif eh.instance_data.state != "io_blocked" and msg.port == "req":
        eh.instance_data.vm.reset ()
        eh.instance_data.state = "io_blocked"
        send (eh, "req", new_datum_bang (), msg)
    elif msg.port == "eof":
        send (eh, "eof" new_datum_bang (), msg)
        if eh.instance_data.state != "io_blocked":
            eh.instance_data.vm.resume (self.endchar ())
    else:
        raise Exception ("unknown message to Sampler in state {eh.instance_data.state} on port '{msg.port}'")

def Sampler (reg, owner, name, template_data):
    name_with_id = gensym ("Echo")
    swibstate = SWIB_State ()
    return make_leaf (name_with_id, owner, swibstate, Sampler_handler)
