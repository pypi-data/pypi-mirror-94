from easydev.decorators import requires, ifpandas, ifpylab, _require


class A(object):

    def __init__(self):
        pass

    def create(self):
        self.a = 1
        self.b = 1

    @requires("a", "what to do")
    def print_str(self):
        print(self.a)

    @requires(["a",'b'], "what to do")
    def print_list(self):
        print(self.a +self.b)
    
    @_require("a", "what to do")
    def print_list(self):
        print(self.a)


def test():
    a = A()
    try:
        a.print_str()
        assert False
    except:
        assert True
    try:
        a.print_list()
        assert False
    except:
        assert True

    a.create()
    a.print_str()
    a.print_list()


@ifpandas
def test_deco_pandas():
    print(1)


@ifpylab
def test_deco_pylab():
    print(1)
