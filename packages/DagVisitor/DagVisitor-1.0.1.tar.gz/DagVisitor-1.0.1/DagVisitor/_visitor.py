class Visited(object):

    #Defaults to the class name
    def kind(self) -> str:
        return [type(self).__name__]

    def children(self):
        raise NotImplemented()

class Dag:
    def __init__(self, parents):
        self._parents = parents

    def parents(self):
        return self._parents

    @property
    def num_parents(self):
        return len(self._parents)

class VisitorMeta(type):
    def __new__(self,name,bases,dct):
        if bases and "visit" in dct:
            raise SyntaxError("Cannot override visit")
        return type.__new__(self,name,bases,dct)

class Visitor(metaclass=VisitorMeta):
    def __init__(self, dag):
        self._dag_cache = set()
        for output in dag.parents():
            self.visit(output)

    def visit(self, data_obj):
        if data_obj in self._dag_cache:
            return
        visited = False
        for kind_str in data_obj.kind():
            visit_name = f"visit_{kind_str}"
            if hasattr(self,visit_name):
                getattr(self,visit_name)(data_obj)
                visited = True
                break
        if not visited:
            self.generic_visit(data_obj)
        self._dag_cache.add(data_obj)

    def generic_visit(self, data_obj):
        #Do nothing for current node
        for child in data_obj.children():
            self.visit(child)

def tuplify(f):
    def decorator(*args,**kwargs):
        out = f(*args,**kwargs)
        return (out,)
    return decorator

def gen_multi_output_visited(custom_isinstance):
    class Node(Visited):
        def __init__(self, Ts, *children):
            if isinstance(Ts, tuple):
                for T in Ts:
                    assert custom_isinstance(T)
            else:
                assert custom_isinstance(Ts)
                Ts = (Ts,)
            _children = []
            for child in children:
                if not isinstance(child, Child):
                    assert isinstance(child,Node)
                    child = Child(child,0)
                _children.append(child)

            self.Ts = Ts
            self._children = _children

        def children(self):
            yield from (child.node for child in self._children)

        def inputs(self):
            return self._children

        @property
        def num_outputs(self):
            return len(self.Ts)

        #Can only be used on single output types
        @property
        def T(self):
            assert self.num_outputs == 1
            return self.Ts[0]

        def __getitem__(self, key : int):
            assert isinstance(key,int)
            assert key < self.num_outputs
            assert key >= 0
            return Child(self,key)

    class Child:
        def __init__(self,node : Node, idx : int):
            self.node = node
            self.idx = idx
            assert node.num_outputs > idx

        @property
        def T(self):
            return self.node.Ts[self.idx]

    class Input(Node):
        def __init__(self, T):
            assert custom_isinstance(T)
            super().__init__(T)

        def set_value(self,*args,**kwargs):
            raise NotImplementedError()

    #This represents a DAG
    class Expr(Dag):
        def __init__(self, outputs, inputs):
            self.inputs = inputs
            _outputs = []
            for output in outputs:
                if not isinstance(output, Child):
                    assert isinstance(output,Node)
                    output = Child(output,0)
                _outputs.append(output)
            for output in _outputs:
                assert isinstance(output,Child)

            for node in inputs:
                assert isinstance(node, Input)
            super().__init__(_outputs)

        def parents(self):
            yield from (parent.node for parent in Dag.parents(self))

        def outputs(self):
            return self._parents

        @property
        def num_outputs(self):
            return self.num_parents

        @property
        def num_inputs(self):
            return len(self.inputs)

        def __call__(self,*inputs):
            for si,ci in zip(self.inputs,inputs):
                si.set_value(ci)
            outs = tuple(output.node()[output.idx] for output in self.outputs())
            if self.num_outputs == 1:
                return outs[0]
            return outs

    return Node, Child, Input, Expr

