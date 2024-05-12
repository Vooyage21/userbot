


def _fix_logging(handler):
    handler._builtin_open = open

    def _new_open(self):
        open_func = self._builtin_open
        return open_func(self.baseFilename, self.mode)

    setattr(handler, "_open", _new_open)


def _ask_input():
    # Ask for Input even on Vps and other platforms.
    def new_input(*args, **kwargs):
        raise EOFError("args=" + str(args) + ", kwargs=" + str(kwargs))

    __builtins__["input"] = new_input
