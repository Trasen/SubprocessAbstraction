import asyncio
from asyncio.subprocess import Process

from ProcessManagement import ProcessResponse
from ProcessManagement.ProcessResponse import ProcessResponse
from ProcessManagement.ShellProcessExceptions import ShellProcessException, EmptyCommand, NonRecognizeableCommand


async def extract_process_response(process: Process, command: str) -> ProcessResponse:
    response = await process.communicate()

    return_code = process.returncode
    success_output = response[0]
    error_output = response[1]

    return ProcessResponse(command, success_output, error_output, return_code)


async def run_shell_process(command: str, process_returns_code_1_on_success: bool = False) -> ProcessResponse:
    if command == '':
        raise EmptyCommand()

    result = await asyncio.create_subprocess_shell(command,
                                                   stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE,
                                                   )

    process_response = await extract_process_response(result, command)

    if process_response.return_code == 1 and not process_returns_code_1_on_success:
        if process_response.error_output.__contains__(b"is not recognized as an internal or external command"):
            raise NonRecognizeableCommand(command)
        else:
            raise ShellProcessException(process_response)

    return process_response


