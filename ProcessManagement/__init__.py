import asyncio
from asyncio.subprocess import Process

from ProcessManagement import ProcessResponse
from ProcessManagement.ProcessResponse import ProcessResponse, ShellProcessCommand
from ProcessManagement.ShellProcessExceptions import EmptyCommand, NonRecognizableCommand, BaseShellProcessException


async def extract_process_response(process: Process, command: ShellProcessCommand) -> ProcessResponse:
    response = await process.communicate()

    return_code = process.returncode
    success_output = response[0]
    error_output = response[1]

    return ProcessResponse(command, success_output, error_output, return_code)


async def run_shell_process(command: ShellProcessCommand, process_returns_code_1_even_though_success: bool = False) -> ProcessResponse:
    if command.command == '':
        raise EmptyCommand()

    result = await asyncio.create_subprocess_shell(command.combine(),
                                                   stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE,
                                                   )

    process_response = await extract_process_response(result, command)

    if process_response.return_code > 0 and not process_returns_code_1_even_though_success:
        if process_response.error_output.__contains__(b"is not recognized as an internal or external command"):
            raise NonRecognizableCommand(command.command)
        else:
            raise BaseShellProcessException(command, process_response)

    return process_response
