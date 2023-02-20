import json


class NpmException(BaseException):
    code = "NOT_YET_IMPLEMENTED_ERROR"

    def __init__(self, raw_text: str, json_data: json):
        self.raw_text: str = raw_text
        self.json_data: json = json_data


class NoPackageLock(NpmException):
    code = 'EUSAGE'

    def __init__(self, summary: str):
        self.summary = summary


class NoSuchFileOrDirectory(NpmException):
    code = 'ENOENT'

    def __init__(self, summary: str):
        self.summary = summary


def _get_all_npm_exceptions() -> [str, NpmException]:
    errors: [str, BaseException] = {}

    for cls in NpmException.__subclasses__():
        errors.__setitem__(cls.code, cls)

    return errors


def find_exception(data: json, raw_text: str) -> NpmException or None:
    code: str = ""
    summary: str = ""
    error: NpmException = None
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
        error = _get_all_npm_exceptions()[code](summary)
    except KeyError:
        raise NpmException(data, raw_text)

    return error
