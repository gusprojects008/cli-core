class Operations:
    def __init__(self, context):    
        self.ctx = context
        self.dispatch_table = {"operation_example": lambda args: self.operation_example(args.arg1, args.arg2)}

    def dispatch(self):
        args = self.ctx.config.get("argparse").get("args")
        handler = self.dispatch_table.get(args.command)

        if not handler:
            raise ValueError(f"Unknown command: {args.command}")

        return handler(args)

    def operation_example(self, value1, value2):
        pass
