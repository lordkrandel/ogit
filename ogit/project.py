import json

from .json_mixin import JsonMixin


TEMPLATE = """{
    "name": "master",
    "repos": {}
}"""


class Project(JsonMixin):

    def __init__(self, name, path, last_used):
        self.name = name
        self.path = path
        self.last_used = last_used

    @classmethod
    def from_json(cls, data):
        return Project(
            name=data.get('name'),
            path=str(data.get('path')),
            last_used=data.get('last_used'))

    def to_json(self):
        data = {
            'name': self.name,
            'path': str(self.path),
            'last_used': self.last_used}
        return json.dumps(data, indent=4)


class Projects(JsonMixin, dict):

    def __init__(self, projects=None):
        super().__init__()
        self.update(projects or {})

    @classmethod
    def from_json(cls, data):
        projects = {k: Project.from_json(v) for k, v in data.items()
                    if isinstance(v, dict)}
        return Projects(projects)

    def to_json(self):
        data = {k: v.__dict__ for k, v in self.items()}
        return json.dumps(data, indent=4)
