class ExpressionEngine:

    @staticmethod
    def evaluate(variable, value):
        expression = variable.expression
        if not expression:
            return value
        x = value
        return eval(
            expression,
            {
                "__builtins__": {},
            },
            {
                "x": x,
            },
        )