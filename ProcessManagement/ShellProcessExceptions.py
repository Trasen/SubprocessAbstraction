from ProcessManagement import ProcessResponse


class BaseShellProcessException(BaseException):
    def __init__(self, reason: str):
        super(ShellProcessException, self).__init__(reason)
        self.return_code: int = 1
        pass


class ShellProcessException(BaseShellProcessException):
    def __init__(self, processResponse: ProcessResponse):
        self.processResponse: ProcessResponse = processResponse


class EmptyCommand(BaseShellProcessException):
    def __init__(self):
        super(EmptyCommand, self).__init__("Empty command is not allowed - please enter a non empty command")


class NonRecognizeableCommand(BaseShellProcessException):
    def __init__(self, command: str):
        super(NonRecognizeableCommand, self).__init__("'" + command + "' is not recognized as an internal or external "
                                                                      "command, operable program or batch file")
