#!/usr/bin/ppython

def rplaca(e, v):
    '''Replace specified value of environment??'''
    return None

class Cons(object):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        return '({} . {})'.format(self.car, self.cdr)

# instructions
#
# they take few args; secd machine and others...
OPCODE = {
    'ld': lambda m, n: ([e.n] + m.s, m.e, m.c[1:], m.d),
    'ldc': lambda m, v: ([v] + m.s, m.e, m.c[1:], m.d),
    'ldf': None,
    'ap': None,
    'rtn': None,
    'dum': None,
    'rap': None,
    'sel': lambda m, ct, cf: (m.s[1:], m.e, m.c[0] if m.s[0] else m.c[1], [m.c[2:]] + m.d),
    'join': lambda m: (m.s, m.e, m.d[0], m.d[1:]),
    'car': lambda m: ([m.s[0].cdr] + m.s[1:], m.e, m.c[1:], m.d),
    'cdr': lambda m: ([m.s[0].cdr] + m.s[1:], m.e, m.c[1:], m.d),
    'atom': lambda m: ([type(m.s[0]) is Cons] + m.s[1:], m.e, m.c[1:], m.d),
    'cons': lambda m: ([Cons(m.s[0], m.s[1])] + m.s[2:], m.e, m.c[1:], m.d),
    'eq': lambda m: ([(m.s[0] == m.s[1])] + m.s[2:], m.e, m.c[1:], m.d),
    'add': lambda m: ([(m.s[0] + m.s[1])] + m.s[2:], m.e, m.c[1:], m.d),
    'sub': lambda m: ([(m.s[0] - m.s[1])] + m.s[2:], m.e, m.c[1:], m.d),
    'mul': lambda m: ([(m.s[0] * m.s[1])] + m.s[2:], m.e, m.c[1:], m.d),
    'div': lambda m: ([(m.s[0] / m.s[1])] + m.s[2:], m.e, m.c[1:], m.d),
    'rem': lambda m: ([(m.s[0] % m.s[1])] + m.s[2:], m.e, m.c[1:], m.d),
    'leq': lambda m: ([(m.s[0] <= m.s[1])] + m.s[2:], m.e, m.c[1:], m.d),
    'stop': lambda m: m._stop() or (m.s, m.e, m.c, m.d),
}


class Machine(object):
    '''SECD machine: state and runner'''

    def __init__(self):
        self.s = []
        self.e = []
        self.c = []
        self.d = None

        self._stop_ = False
        self._debug_ = False

    def __getattr__(self, name):
        if name == 'st':
            return (self.s, self.e, self.c, self.d)
        else:
            return self.__getattribute__(name)

    def __repr__(self):
        return '''machine:
  s = {}
  e = {}
  c = {}
  d = {}
'''.format(*self.st)

    def _stop(self):
        self._stop_ = True

    def step(self):
        op = self.c[0]

        if self._debug_ is True:
            print(self)
            print('  OP: {}'.format(op))

        s, e, c, d = OPCODE[op[0]](self, *op[1:])
        self.s = s
        self.e = e
        self.c = c
        self.d = d

    def run(self):
        while not self._stop_:
            if len(self.c) == 0:
                print('Machine stopped by empty code.')
                print(self)
                return

            self.step()

        print('Machine stopped.')
        print(self)



if __name__ == '__main__':
    code = [['ldc', 42], ['ldc', 1], ['cons'], ['car'], ['stop']]
    m = Machine()
    m.c = code
    m._debug_ = True

    m.run()
