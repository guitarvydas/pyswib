# Sampler

import py0d as zd

# Sampler

def Sampler (vm):
    vm.execute ([
        vm.push_new_string,
        vm.enter, "Sampler",
          vm.call, Stuff_swib,
          vm.append_returned_string,
        vm.exit, "Sampler",
        vm.return_string_pop
        ])

def Stuff (vm):
    vm.execute ([
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
            
def Hello(vm):
    vm.execute ([
        vm.push_new_string,
        vm.enter, "Hello", 
          vm.expect_and_append, "Hello World",
        vm.exit, "Hello",
        vm.return_string_pop
        ])


def Sampler_handler (eh, msg):
    if msg.port == "":
        vm = eh.instance_data
        vm.resume (msg.datum.srepr ())
    elif msg.port == "req":
        # begin parsing when downstream asks for a string
        vm = eh.instance_data
        vm.resume (None)
    elif msg.port == "eof":
        zd.send (eh, "eof", zd.new_datum_bang (), msg)
    else:
        raise Exception (f'*** internal error, unknown message on port "{msg.port}"')
    
def Sampler (reg, owner, name, template_data):
    name_with_id = zd.gensym ("Sampler")
    vm = SwibVM ([vm_call, Sampler_swib])
    return zd.make_leaf (name_with_id, owner, vm, Sampler_handler)
