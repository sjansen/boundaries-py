import a
import a.b
from a.b import c as abc


def foo():
    from b import foo

    foo()


class Bar(object):
    import c

    def foo(self):
        self.c.foo()


a.foo()
a.b.foo()
abc.foo()
foo()
Bar().foo()
