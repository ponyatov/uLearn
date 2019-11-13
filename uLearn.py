
HOST = '127.0.0.1'
PORT = 18888

########################################################################

import os,sys

################################################### extended frame model

class Frame:

    def __init__(self,V):
            # type/class tag /required for lexer using PLY library/
            self.type = self.__class__.__name__.lower()
            # scalar value: symbol name, string, number
            self.val  = V
            # slots = attributes = vocabulary
            self.slot = {}
            # AST nested = universal ordered container = stack
            self.nest = []

    ## dump
    
    # print/str conversion
    def __repr__(self):
        return self.dump()
    
    # full tree dump
    def dump(self,depth=0,prefix=''):
        # subtree header
        tree = self._pad(depth) + self.head(prefix)
        # infty recursion block
        if not depth: Frame._dump = []
        if self in Frame._dump: return tree + ' _/'
        else: Frame._dump.append(self)
        # slot{}s
        for i in self.slot:
            tree += self.slot[i].dump(depth+1,'%s = '%i)
        # nest[]ed
        idx = 0
        for j in self.nest:
            tree += j.dump(depth+1,'%i: '%idx) ; idx +=1
        # resulting subtree
        return tree
    
    # short <T:V> header-only dump
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix,self.type,self._val(),id(self))
    # tree dump padding
    def _pad(self,depth):
        return '\n' + '\t' * depth
    # .val in dump must be overridable for strings, numbers,..
    def _val(self):
        return '%s' % self.val

    ## operators

    # ` A[key] get ` frame by slot name
    def __getitem__(self,key):
        return self.slot[key]
    
    # ` A[key] = B ` set/create slot with name and frame
    def __setitem__(self,key,that):
        if isinstance(that,Frame): self.slot[key] = that
        elif isinstance(that,str): self.slot[key] = String(that)
        elif isinstance(that,int): self.slot[key] = Integer(that)
        else: raise TypeError([type(that),that])
        return self
    
    # ` A << B ` set slot with A[B.val] = B
    def __lshift__(self,that):
        if isinstance(that,Frame): self[that.val] = that
        else: raise TypeError([type(that),that])
        return self
    
    # ` A // B ` push to nest[]ed
    def __floordiv__(self,that):
        if isinstance(that,Frame): self.nest.append(that)
        elif isinstance(that,str): self.nest.append(String(that))
        elif isinstance(that,int): self.nest.append(Integer(that))
        else: raise TypeError([type(that),that])
        return self

    # ` A + B ` add
    def __add__(self,that):
        if isinstance(that,str): return String(self.val + that)
        else: raise TypeError([type(that),that])
        return self

## Primitives

class Primitive(Frame): pass

class Symbol(Primitive): pass

class String(Primitive):
    def _val(self,maxlen=55):
        s = ''
        l = 0
        for c in self.val:
            if l < maxlen:
                l += 1
                if   c == '\n': s += r'\n'
                elif c == '\t': s += r'\t'
                else:           s += c
        return s

class Number(Primitive): pass
class Integer(Number): pass

## EDS: Executable Data Structure

class Active(Frame): pass            

################################################# global virtual machine

class VM(Active): pass

vm = VM('metaL') ; vm['vm'] = vm

######################################################## metaprogramming

class Meta(Frame): pass
class Module(Meta): pass

vm['MODULE'] = Module(os.path.split(sys.argv[0])[-1][:-3])
vm['TITLE'] = 'microlearning service platform'

##################################################################### IO

class IO(Frame): pass
class Dir(IO): pass
class File(IO): pass

################################################################ network

class Net(IO): pass
class IP(Net): pass
class Port(Net): pass
class Web(Net): pass

######################################################## initialization

vm['ini'] = File(vm['MODULE'].val + '.ini')

if __name__ == '__main__':
    with open(vm['ini'].val) as F:
        vm // F.read()
    
#################################################################### web

vm['HOST'] = IP(HOST)
vm['PORT'] = Port(PORT)

import flask

web = flask.Flask(vm['MODULE'].val) ; vm['web'] = Web(web)

web.secret_key = os.urandom(64)

@web.route('/')
def index(): return flask.render_template('index.html',vm=vm)

@web.route('/<path>.css')
def css(path): return flask.render_template(path+'.css',mimetype='text/css',vm=vm)

@web.route('/<path>.png')
def png(path): return web.send_static_file(path+'.png')

web.run(host=HOST,port=PORT,debug=True,extra_files=[vm['ini'].val])
