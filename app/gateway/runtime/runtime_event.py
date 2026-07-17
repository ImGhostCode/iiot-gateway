class RuntimeEvent:

    def __init__(
        self,
        variable,
        old,
        new,

    ):
        self.variable = variable
        self.old = old
        self.new = new