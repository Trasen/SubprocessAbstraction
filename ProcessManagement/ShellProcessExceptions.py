from ProcessManagement import ProcessResponse, ShellProcessCommand


class BaseShellProcessException(BaseException):
    def __init__(self, reason: str, command: ShellProcessCommand, response: ProcessResponse):
        super(BaseShellProcessException, self).__init__(reason)
        self.command = command
        self.response = response


class EmptyCommand(BaseShellProcessException):
    def __init__(self, command: ShellProcessCommand, response: ProcessResponse):
        super(EmptyCommand, self).__init__("Empty command is not allowed - please enter a non empty command", command, response)


class NonRecognizableCommand(BaseShellProcessException):
    def __init__(self, command: ShellProcessCommand, response: ProcessResponse):
        super(NonRecognizableCommand, self).__init__("'" + command.combine() + "' is not recognized as an internal "
                                                                                "or external"
                                                                      "command, operable program or batch file",
                                                     command,
                                                     response)
