import json


class Dependencies:
    def __init__(
            self,
            json_data: json
    ):
        self.prod: int = json_data['prod']
        self.dev: int = json_data['dev']
        self.optional: int = json_data['optional']
        self.peer: int = json_data['peer']
        self.peerOptional: int = json_data['peerOptional']
        self.total: int = json_data['total']


class Vulnerabilities:
    def __init__(self, json_data: json):
        self.info: int = json_data['info']
        self.low: int = json_data['low']
        self.moderate: int = json_data['moderate']
        self.high: int = json_data['high']
        self.critical: int = json_data['critical']
        self.total: int = json_data['total']


class Audit:
    def __init__(self, json_data: json):
        self.vulnerabilities: Vulnerabilities = Vulnerabilities(json_data['vulnerabilities'])
        self.dependencies: Dependencies = Dependencies(json_data['dependencies'])


class NpmInstallSuccessResponse:
    def __init__(self, json_data: json):
        self.added: int = json_data["added"]
        self.removed: int = json_data["removed"]
        self.changed: int = json_data["changed"]
        self.audited: int = json_data["audited"]
        self.funding: int = json_data["funding"]
        self.audit: Audit = Audit(json_data["audit"])


class DeprecatedPackage:
    def __init__(self,
                 name,
                 version,
                 description
                 ):
        self.name: str = name
        self.version: str = version
        self.description: str = description


class NpmInstallErrorResponse:
    def __init__(self,
                 data: str
                 ):

        self.deprecated_packages: [DeprecatedPackage] = []

        all_rows = data.splitlines()
        for row in all_rows:
            words = row.split(' ')
            could_be_deprecated = words[2]

            if (could_be_deprecated == 'deprecated'):
                name_and_version = words[3].split('@')
                package_name = name_and_version[0]
                version = name_and_version[1].split(':')[0]
                description = ''
                description_array = words[4:len(words)]
                for value in description_array:
                    description += value + ' '

                self.deprecated_packages.append(DeprecatedPackage(package_name, version, description))




class NpmInstallResponse:
    def __init__(self, successResponse: NpmInstallSuccessResponse, errorResponse: NpmInstallErrorResponse):
        self.successResponse = successResponse
        self.errorResponse = errorResponse


class NpmAuditVulnerability:
    def __init__(self, data:json):
        self.name: str = data["name"]
        self.severity: str = data["severity"]
        self.isDirect: bool = data["isDirect"]
        self.via: json = data["via"] # This can be basically anything, so for now just gonna dump the json data stored in via
        self.effects: [str] = data["effects"]
        self.range: str = data["range"]
        self.nodes: [str] = data["nodes"]
        self.fixAvailable: bool = data["fixAvailable"]


class NpmAuditMetadata:
    def __init__(self, data: json):
        self.dependencies:Dependencies = data["dependencies"]
        self.vulnerabilities:Vulnerabilities = data["vulnerabilities"]


class NpmAuditResponse:
    def __init__(self, data: json):
        self.auditReportVersion: int = data["auditReportVersion"]

        self.vulnerabilities: [NpmAuditVulnerability] = []
        vulnerabilities = data["vulnerabilities"]
        for vuln in vulnerabilities:
            self.vulnerabilities.append(NpmAuditVulnerability(vulnerabilities[vuln]))

        self.metadata: NpmAuditMetadata = NpmAuditMetadata(data["metadata"])
