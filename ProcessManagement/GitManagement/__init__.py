from ProcessManagement import run_shell_process, ShellProcessCommand


async def git_clone(path: str, url: str):

    command = ShellProcessCommand(application="git", command="clone", args=[url], trailing_flags=[path])
    return await run_shell_process(command)
