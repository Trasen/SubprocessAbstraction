from ProcessManagement import run_shell_process, ShellProcessCommand, ProcessResponse
from ProcessManagement.WinGetManagement.WinGetExceptions import MultiplePackagesFound, NoPackagesFound, \
    NoPackageNameEntered, \
    ApplicationAlreadyInstalled, hard_exceptions, soft_exceptions
from ProcessManagement.WinGetManagement.WinGetExceptions import MultiplePackagesFound, NoPackagesFound, \
    NoPackageNameEntered, ApplicationAlreadyInstalled


class WingetCommand(ShellProcessCommand):
    def __init__(self, command: str, args:[str], trailing_flags: [str]):
        super(WingetCommand, self).__init__(application="winget", command=command, args=args, trailing_flags=trailing_flags)


async def handle_exception(command: ShellProcessCommand, response: ProcessResponse, silent_fail_on_soft_errors: bool):
    if not silent_fail_on_soft_errors:
        try:
            exception = soft_exceptions[response.return_code]
            raise exception(command, response)
        except KeyError:
            pass

    try:
        exception = hard_exceptions[response.return_code]
        raise exception(command, response)
    except KeyError:
        pass


async def winget(command: ShellProcessCommand, silent_fail_on_soft_errors: bool) -> ProcessResponse:
    response = await run_shell_process(command, True)

    await handle_exception(command, response, silent_fail_on_soft_errors)
    return response


async def winget_install(application_name: str, silent_fail_on_soft_errors: bool = False):
    command = WingetCommand(command="install", args=[application_name], trailing_flags=[
        "--silent",
        "--accept-package-agreements",
        "--accept-source-agreements",
        "--disable-interactivity"]
                                  )
    response = await winget(command, silent_fail_on_soft_errors)

    return response


async def winget_install_silent_fail_on_soft_errors(application_name: str):
    return await winget_install(application_name, True)


async def winget_uninstall(application_name: str):
    command = WingetCommand(command="uninstall", args=[application_name], trailing_flags=[
        "--silent",
        "--accept-source-agreements"]
                                  )

    return await winget(command, False)
