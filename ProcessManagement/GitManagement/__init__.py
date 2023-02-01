from ProcessManagement import run_shell_process


async def git_clone(path: str, url: str):
    return await run_shell_process("git clone " + url + " " + path)
