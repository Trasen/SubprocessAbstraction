import json


class ShellProcessCommand:
    def __init__(self, application: str, command: str, args: [str], trailing_flags: [str]):
        self.application: str = application
        self.command: str = command
        self.args: [str] = args
        self.trailing_flags: [str] = trailing_flags

    def combine(self) -> str:
        return self.application + " " + self.command + " " + " ".join(self.args) + " " + " ".join(self.trailing_flags)


class ProcessResponse:
    default_decoding_format = "utf-8"

    def __init__(self, original_command: ShellProcessCommand, success_output: bytes, error_output: bytes, return_code: int):
        self.command = original_command
        self.return_code: int = return_code
        self.success_output: bytes = success_output
        self.error_output: bytes = error_output

    def decoded_success_output(self, codec: str = default_decoding_format) -> str:
        return self.success_output.decode(codec)

    def decoded_error_output(self, codec: str = default_decoding_format) -> str:
        return self.error_output.decode(codec)

    def json_success_output(self, codec: str = default_decoding_format) -> json:
        return json.loads(self.success_output.decode(codec))

    def json_error_output(self, codec: str = default_decoding_format) -> json:
        return json.loads(self.error_output.decode(codec))
