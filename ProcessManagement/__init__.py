import asyncio
from asyncio.subprocess import Process


class ProcessResponse:
    def __init__(self, success_output: str, error_output: str):
        self.success_output = success_output
        self.error_output = error_output


async def extract_stdout_and_err_as_string(process: Process) -> ProcessResponse:
    response = await process.communicate()

    success_output = response[0].decode('utf-8')
    error_output = response[1].decode('utf-8')

    return ProcessResponse(success_output, error_output)


async def run_shell_process(command: str) -> ProcessResponse:
    result = await asyncio.create_subprocess_shell(command,
                                                   stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE)

    return await extract_stdout_and_err_as_string(result)