import click
import re
from pathlib import Path

import invoke
from external import External
import settings

class Git(External):

    @classmethod
    def clean(cls, folder='.'):
        context = invoke.Context()
        with context.cd(folder):
            context.run('git clean -xdf')

    @classmethod
    def get_editor(cls):
        return invoke.Context().run('git config --get core.editor', pty=True, hide=True).stdout.strip()

    @classmethod
    def clone(cls, repository, branch, directory, bare=False):
        bare_option = '--bare' if bare else ''
        cls.run(f'git clone {bare_option} --branch {branch} --single-branch {repository} {directory}')

    @classmethod
    def add_remote(cls, name, url, path):
        context = invoke.Context()
        with context.cd(path):
            context.run(f'git remote add {name} {url}')

    @classmethod
    def status(cls, path, extended=False, name=False):
        context = invoke.Context()
        with context.cd(path):
            if extended:
                print()
                if name:
                    print(f"   {name}/")
                context.run('git log --format="   %s (%h)" -n 1')
                return context.run('git -c color.status=always status -sb', pty=True)
            else:
                try:
                    return context.run('git status -s', pty=True, hide='out')
                except invoke.UnexpectedExit as ue:
                    print(ue.streams_for_display()[0].strip())

    @classmethod
    def stash(cls, path):
        context = invoke.Context()
        with context.cd(path):
            context.run('git stash -a')

    @classmethod
    def checkout(cls, path, branch, options=None):
        context = invoke.Context()
        with context.cd(path):
            current_branch = cls.get_current_branch(path)
            if branch != current_branch:
                context.run('git checkout %s %s' % (options or '', branch))

    @classmethod
    def get_current_branch(cls, path):
        context = invoke.Context()
        with context.cd(path):
            return context.run('git branch --show-current', pty=True, hide='out').stdout.strip()

    @classmethod
    def get_remote_branches(cls, path, remote=None, worktree=False):
        context = invoke.Context()
        with context.cd(path):
            if worktree:
                command = f'git ls-remote --heads {remote}'
            else:
                command = 'git branch -r' + (('l "' + remote + '/*"') if remote else '')
            entries = context.run(command, pty=False, hide='out').stdout
            if worktree:
                return re.findall('refs/heads/(.*)\n', entries)
            else:
                len_remote = len(remote) + 1 if remote else 0
                return [x.strip()[len_remote:] for x in entries.split('\n')]

    @classmethod
    def diff(cls, path, repo_name=None):
        context = invoke.Context()
        with context.cd(path):
            print(f'{(repo_name + ":: ") if repo_name else ""}:: {"-" * (80 - len(repo_name or ""))}')
            context.run('git diff')

    @classmethod
    def fetch(cls, path, repo_name, remote_name, branch_name):
        context = invoke.Context()
        with context.cd(path):
            context.run('git fetch %s %s' % (remote_name, branch_name))

    @classmethod
    def push(cls, path, force=False):
        context = invoke.Context()
        with context.cd(path):
            context.run(f'git push {"-ff" if force else ""}')

    @classmethod
    def pull(cls, path, remote, branch_name):
        context = invoke.Context()
        with context.cd(path):
            context.run(f'git pull {remote} {branch_name}')

    @classmethod
    def update_master_branch(cls, base_path, repo_name):
        path = Path(base_path) / repo_name
        cls.fetch(base_path, repo_name, 'origin', 'master')
        context = invoke.Context()
        with context.cd(path):
            context.run('git checkout master')
        cls.pull(path, 'origin', 'master')

    @classmethod
    def worktree_add(cls, branch, path, new=False):
        context = invoke.Context()
        with context.cd(path):
            context.run(f'git worktree add ../{branch} {branch}')

@click.group(name='git')
@click.pass_context
def git_group(ctx):
    pass

@git_group.command(name='diff')
@click.argument('path', required=False)
@click.argument('repo_name', required=False)
@click.pass_context
def diff_command(ctx, path=None, repo_name=None):
    Git.diff(path or settings.paths.starting, repo_name=repo_name)

@git_group.command()
@click.argument('path', required=False)
@click.pass_context
def status(ctx, path=None):
    Git.status(path or settings.paths.starting, extended=True, name=None)
