# Sampler

import py0d as zd

def Sampler_func (s):
    return f'FINI: {s}'

def Sampler_handler (eh, msg):
    if msg.port == "":
        eh.instance_data += msg.datum.srepr ()
        zd.send (eh, "req", zd.new_datum_bang (), msg)
    elif msg.port == "req":
        zd.send (eh, "req", zd.new_datum_bang (), msg)
    elif msg.port == "eof":
        returned_string = zd.new_datum_string (Sampler_func (eh.instance_data))
        zd.send (eh, "", returned_string, msg)
        zd.send (eh, "eof", zd.new_datum_bang (), msg)
    else:
        raise Exception (f'*** internal error, unknown message on port "{msg.port}"')

def Sampler (reg, owner, name, template_data):
    name_with_id = zd.gensym ("Sampler")
    return zd.make_leaf (name_with_id, owner, "", Sampler_handler)
