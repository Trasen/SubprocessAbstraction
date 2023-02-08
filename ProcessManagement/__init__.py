import asyncio
from asyncio.subprocess import Process

from ProcessManagement import ProcessResponse
from ProcessManagement.ProcessResponse import ProcessResponse
from ProcessManagement.ShellProcessExceptions import ShellProcessException, EmptyCommand, NonRecognizeableCommand


async def extract_process_response(process: Process) -> ProcessResponse:
    response = await process.communicate()

    return_code = process.returncode
    success_output = response[0]
    error_output = response[1]

    return ProcessResponse(success_output, error_output, return_code)


async def run_shell_process(command: str) -> ProcessResponse:
    if command == '':
        raise EmptyCommand()

    result = await asyncio.create_subprocess_shell(command,
                                                   stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE,
                                                   )

    process_response = await extract_process_response(result)

    if process_response.return_code == 1:
        if process_response.error_output.__contains__(b"is not recognized as an internal or external command"):
            raise NonRecognizeableCommand(command)
        else:
            raise ShellProcessException(process_response)

    return process_response

