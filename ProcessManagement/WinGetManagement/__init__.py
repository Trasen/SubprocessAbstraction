import asyncio

from ProcessManagement import run_shell_process
from ProcessManagement.ShellProcessExceptions import BaseShellProcessException


class WingetException(BaseShellProcessException):
    def __init__(self, reason:str):
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


async def winget_install(application_name: str, silent_fail_on_soft_errors: bool = False):
    response = await run_shell_process(
        "winget install " + application_name + " --silent --accept-package-agreements --accept-source-agreements --disable-interactivity")

    if not silent_fail_on_soft_errors:

        if response.return_code == NoPackageNameEntered.code:
            raise NoPackageNameEntered()

        if response.return_code == ApplicationAlreadyInstalled.code:
            raise ApplicationAlreadyInstalled(application_name)

    if response.return_code == NoPackagesFound.code:
        raise NoPackagesFound(application_name)

    if response.return_code == MultiplePackagesFound.code:
        multiple_packages = response.decoded_success_output().splitlines()
        raise MultiplePackagesFound(application_name, multiple_packages[5:len(multiple_packages)])

    return response


async def winget_install_silent_fail_on_soft_errors(application_name: str, ):
    return await winget_install(application_name, True)


async def winget_uninstall(application_name: str):
    return await run_shell_process("winget uninstall " + application_name + " --silent --accept-source-agreements")

