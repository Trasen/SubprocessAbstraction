from ProcessManagement.ShellProcessExceptions import BaseShellProcessException


class WingetException(BaseShellProcessException):
    def __init__(self, reason: str):
        super(WingetException, self).__init__(reason)


class WingetSoftError(WingetException):
    def __init__(self, reason: str):
        super(WingetSoftError, self).__init__(reason)


class WingetHardError(WingetException):
    def __init__(self, reason: str):
        super(WingetHardError, self).__init__(reason)


class MultiplePackagesFound(WingetHardError):
    code = 2316632086

    def __init__(self, package_name: str, data: [str]):
        super(MultiplePackagesFound, self).__init__("Multiple packages found for: " + package_name
                                                    + ",  data: " + "".join(data))
        self.package_name = package_name
        self.available_packages = data


class NoPackagesFound(WingetHardError):
    code = 2316632084

    def __init__(self, package_name: str):
        super(NoPackagesFound, self).__init__("No package found matching input criteria: " + package_name)
        self.package_name: str = package_name


class NoPackageNameEntered(WingetSoftError):
    code = 2316632066

    def __init__(self):
        super(NoPackageNameEntered, self).__init__("You have to enter a package name, empty package name will not work")


class ApplicationAlreadyInstalled(WingetSoftError):
    code = 2316632107

    def __init__(self, application_name: str):
        super(ApplicationAlreadyInstalled, self).__init__("Application " + application_name + " is already installed")
