# Sampler

def Sampler_swib (_r):
    _r.push_new_string ()
    _r.begin_breadcrumb ("Sampler")
    _r.call (Stuff_swib)
    _r.append_returned_string ()
    _r.end_breadcrumb ("Sampler")
    return _r.return_string_pop ()

def Stuff_matcher (_r):
    _r.push_new_string ()
    _r.begin_breadcrumb ("Stuff")
    while True:
        if False:
            pass
        elif _r.peek ("Hello World"):
            _r.call (Hello_swib)
            _r.append_returned_string ()
            pass
        elif _r.eof ():
            break
            pass
        elif True:
            _r.accept_and_append ()
            pass
    _r.end_breadcrumb ("Stuff")
    return _r.return_string_pop ()
            
def Hello_swib (_r):
    _r.push_new_string ()
    _r.begin_breadcrumb ("Hello")
    _r.need_and_append ("Hello World")
    _r.end_breadcrumb ("Hello")
    return _r.return_string_pop ()


def Sampler_handler (eh, msg):
    
    _r.call (Sampler_swib)
    return _r.return_string_pop ()
    

import receptor
import sys
import py0d as zd
class Place_Holder:
    def __init__ (self):
        self.name = "place-holder-name"
_r = receptor.Receptor (sys.stdin, zd.make_leaf (zd.gensym ("swib"), Place_Holder (), None, "place-holder handler"))
Sampler (_r)
s = _r.pop_return_value ()
return s
