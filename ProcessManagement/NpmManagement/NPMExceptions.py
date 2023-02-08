import json


class NpmError(BaseException):
    code = "NOT_YET_IMPLEMENTED_ERROR"

    def __init__(self, raw_text: str, json_data: json):
        self.raw_text: str = raw_text
        self.json_data: json = json_data


class NoPackageLock(NpmError):
    code = 'EUSAGE'

    def __init__(self, summary: str):
        self.summary = summary


class NoSuchFileOrDirectory(NpmError):
    code = 'ENOENT'

    def __init__(self, summary: str):
        self.summary = summary


def _get_all_npm_errors() -> [str, NpmError]:
    errors: [str, BaseException] = {}

    for cls in NpmError.__subclasses__():
        errors.__setitem__(cls.code, cls)

    return errors


error_dictionary: [str, BaseException] = _get_all_npm_errors()


def find_error(data: json, raw_text: str) -> NpmError or None:
    code: str = ""
    summary: str = ""
    error: NpmError = None
    if data:
        try:
            code = data['error']["code"]
            summary = data['error']["summary"]
        except KeyError:
            pass
    elif raw_text:
        rows: [str] = raw_text.splitlines()
        line_split = rows[0].split("! ")
        code = line_split[1].split(" ")[1]
        summary = raw_text
    try:
        error = error_dictionary[code](summary)
    except BaseException:
        pass

    return error
