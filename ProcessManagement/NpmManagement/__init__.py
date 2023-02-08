from ProcessManagement import run_shell_process, ShellProcessException
from ProcessManagement.NpmManagement.NpmCITypes import NpmCiSuccessResponse, NpmCiErrorResponse, NpmCiResponse
from ProcessManagement.NpmManagement.NPMExceptions import NpmError, find_error


async def npm(command: str):

    try:
        response = await run_shell_process(command)
    except ShellProcessException as e:
        raise find_error(e.processResponse.json_success_output(), e.processResponse.decoded_error_output())

    return response

async def npm_ci(path: str, folder: str) -> NpmCiResponse:
    response = await npm("npm ci --prefix " + path + folder + " --json")

    success_response: NpmCiSuccessResponse = NpmCiSuccessResponse(response.json_success_output())
    error_response: NpmCiErrorResponse = NpmCiErrorResponse(response.decoded_error_output())

    return NpmCiResponse(success_response, error_response)
