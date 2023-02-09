import asyncio

from ProcessManagement import run_shell_process, ShellProcessException
from ProcessManagement.NpmManagement.NpmCITypes import NpmInstallSuccessResponse, NpmInstallErrorResponse, \
    NpmInstallResponse, NpmAuditResponse
from ProcessManagement.NpmManagement.NPMExceptions import NpmError, find_error


async def npm(command: str, process_returns_code_1_even_though_success: bool):

    try:
        response = await run_shell_process(command, process_returns_code_1_even_though_success)
    except ShellProcessException as e:
        raise find_error(e.processResponse.json_success_output(), e.processResponse.decoded_error_output())

    return response

async def npm_ci(path: str, folder: str) -> NpmInstallResponse:
    response = await npm("npm ci --prefix " + path + folder + " --json")

    success_response: NpmInstallSuccessResponse = NpmInstallSuccessResponse(response.json_success_output())
    error_response: NpmInstallErrorResponse = NpmInstallErrorResponse(response.decoded_error_output())

    return NpmInstallResponse(success_response, error_response)


async def npm_i(path :str, folder: str) -> NpmInstallResponse:
    response = await npm("cd " + path + folder + " && npm install --prefix " + path + folder + " --json")

    success_response: NpmInstallSuccessResponse = NpmInstallSuccessResponse(response.json_success_output())
    error_response: NpmInstallErrorResponse = NpmInstallErrorResponse(response.decoded_error_output())

    return NpmInstallResponse(success_response, error_response)



async def npm_audit(path:str, folder: str):
    response = await npm("cd " + path + folder + " && npm audit --json", True)
    return NpmAuditResponse(response.json_success_output())
