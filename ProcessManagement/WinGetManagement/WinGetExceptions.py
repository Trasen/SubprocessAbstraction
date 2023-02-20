from ProcessManagement import ShellProcessCommand, ProcessResponse
from ProcessManagement.ShellProcessExceptions import BaseShellProcessException


class WingetException(BaseShellProcessException):
    def __init__(self, reason: str, command: ShellProcessCommand, response: ProcessResponse):
        super(WingetException, self).__init__(reason, command, response)


class WingetSoftException(WingetException):
    def __init__(self, reason: str, command: ShellProcessCommand, response: ProcessResponse):
        super(WingetSoftException, self).__init__(reason, command, response)


class WingetHardException(WingetException):
    def __init__(self, reason: str, command: ShellProcessCommand, response: ProcessResponse):
        super(WingetHardException, self).__init__(reason, command, response)


class MultiplePackagesFound(WingetHardException):
    code = 2316632086


    def __init__(self, command: ShellProcessCommand, response: ProcessResponse):
        decoded_response = response.decoded_success_output()
        multiple_packages = decoded_response.splitlines()
        data = multiple_packages[5:len(multiple_packages)]

        super(MultiplePackagesFound, self).__init__("Multiple packages found for: " + "".join(command.args)
                                                    + ",  data: " + "".join(data))
        self.package_name = "".join(command.args)
        self.available_packages = data


class NoPackagesFound(WingetHardException):
    code = 2316632084

    def __init__(self, command: ShellProcessCommand, response: ProcessResponse):
        package_name = "".join(command.args)
        super(NoPackagesFound, self).__init__("No package found matching input criteria: " + package_name, command, response)
        self.package_name: str = package_name


class NoPackageNameEntered(WingetSoftException):
    code = 2316632066

    def __init__(self, command: ShellProcessCommand, response: ProcessResponse):
        super(NoPackageNameEntered, self).__init__("You have to enter a package name, empty package name will not work", command, response)


class ApplicationAlreadyInstalled(WingetSoftException):
    code = 2316632107

    def __init__(self, command: ShellProcessCommand, response: ProcessResponse):
        super(ApplicationAlreadyInstalled, self).__init__("Application " + "".join(command.args) + " is already installed", command, response)


def get_all_hard_exceptions() -> [int, WingetHardException]:
    errors: [int, BaseException] = {}

    for cls in WingetHardException.__subclasses__():
        errors.__setitem__(cls.code, cls)

    return errors


def get_all_soft_exceptions() -> [int, WingetSoftException]:
    errors: [int, BaseException] = {}

    for cls in WingetSoftException.__subclasses__():
        errors.__setitem__(cls.code, cls)

    return errors
