from ProcessManagement import run_shell_process


async def winget_install(application_name: str):
    return await run_shell_process("winget install " + application_name + " --silent --accept-package-agreements --accept-source-agreements")


async def winget_uninstall(application_name: str):
    return await run_shell_process("winget uninstall " + application_name + " --silent --accept-source-agreements")
