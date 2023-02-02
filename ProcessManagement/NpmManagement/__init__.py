import json

from ProcessManagement import run_shell_process
from ProcessManagement.NpmManagement.NpmCITypes import NpmCiSuccessResponse, NpmCiErrorResponse, NpmCiResponse


async def npm_i(path: str, folder: str):
    return await run_shell_process("npm i --prefix" + path + folder + " --json")


async def npm_ci(path: str, folder: str) -> NpmCiResponse:
    response = await run_shell_process("npm ci --prefix " + path + folder + " --json")
    sucess_output = json.loads(response.success_output)

    success_response: NpmCiSuccessResponse = NpmCiSuccessResponse(sucess_output)
    error_response: NpmCiErrorResponse = NpmCiErrorResponse(response.error_output)
    return NpmCiResponse(success_response, error_response)
