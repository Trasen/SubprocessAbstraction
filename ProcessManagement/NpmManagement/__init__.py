
from ProcessManagement import run_shell_process, ShellProcessCommand, BaseShellProcessException
from ProcessManagement.NpmManagement.NpmCITypes import NpmInstallSuccessResponse, NpmInstallErrorResponse, \
    NpmInstallResponse, NpmAuditResponse
from ProcessManagement.NpmManagement.NPMExceptions import NpmException, find_exception


async def npm(command: ShellProcessCommand, process_returns_code_1_even_though_success: bool = False):
    try:
        response = await run_shell_process(command, process_returns_code_1_even_though_success)
    except BaseShellProcessException as e:
        raise find_exception(e.response.json_success_output(), e.response.decoded_error_output())

    return response


async def npm_ci(path: str, folder: str) -> NpmInstallResponse:

    command = ShellProcessCommand(application="npm", command="ci", args=["--prefix " + path + folder], trailing_flags=["--json"])
    response = await npm(command)

    success_response: NpmInstallSuccessResponse = NpmInstallSuccessResponse(response.json_success_output())
    error_response: NpmInstallErrorResponse = NpmInstallErrorResponse(response.decoded_error_output())

    return NpmInstallResponse(success_response, error_response)


async def npm_i(path: str, folder: str) -> NpmInstallResponse:

    command = ShellProcessCommand(application="cd " + path + folder + " && npm", command="install", args=[], trailing_flags=["--json"])
    response = await npm(command)

    success_response: NpmInstallSuccessResponse = NpmInstallSuccessResponse(response.json_success_output())
    error_response: NpmInstallErrorResponse = NpmInstallErrorResponse(response.decoded_error_output())

    return NpmInstallResponse(success_response, error_response)


async def npm_audit(path: str, folder: str):

    command = ShellProcessCommand(application="cd " + path + folder + " && npm", command="audit", args=[], trailing_flags=["--json"])
    response = await npm(command, True)

    return NpmAuditResponse(response.json_success_output())
