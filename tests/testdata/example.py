import a
import a.b
from a.b import c as abc

a.foo()
a.b.foo()
abc.foo()


def foo():
    from b import foo

    foo()


foo()


class Bar(object):
    import c

    def foo(self):
        self.c.foo()


Bar().foo()


from d import e

print(type(e))


import d.e

print(type(d.e))
