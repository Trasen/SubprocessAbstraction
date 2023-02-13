from ProcessManagement import run_shell_process, ShellProcessCommand
from ProcessManagement.WinGetManagement.WinGetExceptions import MultiplePackagesFound, NoPackagesFound, NoPackageNameEntered, \
    ApplicationAlreadyInstalled
from ProcessManagement.WinGetManagement.WinGetExceptions import MultiplePackagesFound, NoPackagesFound, \
    NoPackageNameEntered, ApplicationAlreadyInstalled


async def winget_install(application_name: str, silent_fail_on_soft_errors: bool = False):
    command = ShellProcessCommand(application="winget", command="install", args=[application_name], trailing_flags=[
        "--silent",
        "--accept-package-agreements",
        "--accept-source-agreements",
        "--disable-interactivity"]
                                  )

    response = await run_shell_process(command, True)

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
    command = ShellProcessCommand(application="winget", command="uninstall", args=[application_name], trailing_flags=[
        "--silent",
        "--accept-source-agreements"]
                                  )

    return await run_shell_process(command)
