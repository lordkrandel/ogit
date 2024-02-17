import json

import click
import settings
from git import Git
from json_mixin import JsonMixin

TEMPLATE = """{
    "name": "master",
    "repos": {}
}"""


class Project(JsonMixin):

    def __init__(self, name=None, path=None, last_used=None):
        path = path or settings.paths.starting
        self.path = str(path)
        self.name = name or path.name
        self.last_used = last_used or Git.get_current_branch(self.path)

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
        self.update(projects or {settings.paths.starting.name: Project()})

    @classmethod
    def from_json(cls, data):
        projects = {k: Project.from_json(v) for k, v in data.items()
                    if isinstance(v, dict)}
        return Projects(projects)

    def to_json(self):
        data = {k: v.__dict__ for k, v in self.items()}
        return json.dumps(data, indent=4)

@click.group(invoke_without_command=True, name='projects')
@click.pass_context
def projects_group(ctx):
    if ctx.invoked_subcommand is None:
        print(settings.projects)

@projects_group.command(name='init')
@click.pass_context
def projects_init(ctx):
    if not settings.projects:
        settings.projects = Projects({settings.project.name: settings.project} if settings.project else {})
        print(f"{settings.paths.projects} created")
    settings.projects.save_json(settings.paths.projects)

@projects_group.command(name='status')
@click.pass_context
def projects_status(ctx):
    for project in settings.projects.values():
        ctx.invoke(project_status, project)


@click.group(invoke_without_command=True, name='project')
@click.pass_context
def project_group(ctx):
    if ctx.invoked_subcommand is None:
        print(settings.project)

@project_group.command(name='status')
@click.pass_context
def project_status(ctx, _project=None):
    _project = _project or settings.project
    Git.status(_project.path, extended=True, name=_project.name)

@project_group.command(name='init')
@click.pass_context
def project_init(ctx):
    if not settings.project:
        settings.project = Project()
        print(f"{settings.project.path} created")
        if settings.projects:
            settings.projects[settings.project.name] = settings.project
        else:
            ctx.forward(projects_init)
