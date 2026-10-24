# ruff: file-ignore[undocumented-public-module, undocumented-public-function]
from __future__ import annotations

from github import Auth, Github
from github.InputGitTreeElement import InputGitTreeElement
from operator import attrgetter, methodcaller
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
	from github.Commit import Commit
	from github.ContentFile import ContentFile
	from github.GitCommit import GitCommit
	from github.GitRef import GitRef
	from github.GitTree import GitTree
	from github.Repository import Repository

def check_asdl() -> None:
	githubToken: str | None = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
	if githubToken:
		githubClient: Github = Github(auth=Auth.Token(githubToken))
	else:
		githubClient: Github = Github()
	repositoryCpython: Repository = githubClient.get_repo('python/cpython')
	listPathRelativeFilenamesWritten: list[PurePosixPath] = []
	listPathRelativeFilenamesDeleted: list[PurePosixPath] = []

	for path_asdl in Path(__file__).parent.glob('3.*'):
		filesUpdated, filesDeleted = checkBranch(repositoryCpython, path_asdl.relative_to(Path.cwd()))
		listPathRelativeFilenamesWritten.extend(filesUpdated)
		listPathRelativeFilenamesDeleted.extend(filesDeleted)

	if githubToken and 'GITHUB_REPOSITORY' in os.environ:
		GitHubActionPushFiles(githubClient.get_repo(os.environ['GITHUB_REPOSITORY']), listPathRelativeFilenamesWritten, listPathRelativeFilenamesDeleted)

def checkBranch(repositoryCpython: Repository, pathRelative_asdl: Path) -> tuple[list[PurePosixPath], list[PurePosixPath]]:
	pathRelative_asdl.mkdir(parents=True, exist_ok=True)
	listFilenames: frozenset[str] = frozenset(map(attrgetter('name'), filter(methodcaller('is_file'), pathRelative_asdl.iterdir())))  # pyright: ignore[reportUnknownArgumentType]

	listPathRelativeFilenamesWritten: list[PurePosixPath] = []
	listPathRelativeFilenamesDeleted: list[PurePosixPath] = []
	setCommitSHA: set[str] = set()

	for filename in ('Python.asdl', 'asdl.py'):
		commit: Commit = repositoryCpython.get_commits(sha=pathRelative_asdl.name, path=f"Parser/{filename}")[0]
		if commit.sha not in listFilenames or filename not in listFilenames:
			contents: list[ContentFile] | ContentFile = repositoryCpython.get_contents(f"Parser/{filename}", ref=commit.sha)
			if isinstance(contents, list):
				raise ValueError
			pathFilename: Path = pathRelative_asdl / filename
			pathFilename.write_bytes(contents.decoded_content)
			listPathRelativeFilenamesWritten.append(PurePosixPath(pathFilename))

		if commit.sha not in listFilenames and commit.sha not in setCommitSHA:
			(pathRelative_asdl / commit.sha).touch()
			listPathRelativeFilenamesWritten.append(PurePosixPath(pathRelative_asdl / commit.sha))
		setCommitSHA.add(commit.sha)

	for condemnedPathFilename in pathRelative_asdl.glob('[0-9a-f]' * 40):
		if condemnedPathFilename.name not in setCommitSHA:
			condemnedPathFilename.unlink()
			listPathRelativeFilenamesDeleted.append(PurePosixPath(condemnedPathFilename))

	return listPathRelativeFilenamesWritten, listPathRelativeFilenamesDeleted

def GitHubActionPushFiles(repository: Repository, listPathRelativeFilenamesWritten: list[PurePosixPath], listPathRelativeFilenamesDeleted: list[PurePosixPath], branchPullRequest: str = 'update-cpython-asdl') -> None:
	if not listPathRelativeFilenamesWritten and not listPathRelativeFilenamesDeleted:
		return

	message: str = 'Update CPython ASDL files'
	gitCommitParent: GitCommit = repository.get_git_commit(repository.get_branch(repository.default_branch).commit.sha)

	gitTreeUpdated: GitTree = repository.create_git_tree([
			*(InputGitTreeElement(pathRelativeFilenameDeleted.as_posix(), mode='100644', type='blob', sha=None)
				for pathRelativeFilenameDeleted in listPathRelativeFilenamesDeleted
			),
			*(InputGitTreeElement(pathRelativeFilenameWritten.as_posix(), mode='100644', type='blob'
					, content=Path(pathRelativeFilenameWritten).read_text(encoding='utf-8'))
				for pathRelativeFilenameWritten in listPathRelativeFilenamesWritten
			),
		], base_tree=gitCommitParent.tree)
	gitReferencePullRequest: GitRef | None = None
	if branchPullRequest in map(attrgetter('name'), repository.get_branches()):
		gitReferencePullRequest = repository.get_git_ref(f'heads/{branchPullRequest}')

	if gitReferencePullRequest is None or gitTreeUpdated.sha != repository.get_git_commit(gitReferencePullRequest.object.sha).tree.sha:
		gitCommitUpdated: GitCommit = repository.create_git_commit(message, gitTreeUpdated, [gitCommitParent])
		if gitReferencePullRequest is None:
			repository.create_git_ref(ref=f"refs/heads/{branchPullRequest}", sha=gitCommitUpdated.sha)
		else:
			gitReferencePullRequest.edit(gitCommitUpdated.sha, force=True)

	if repository.get_pulls(state='open', base=repository.default_branch, head=f'{repository.owner.login}:{branchPullRequest}').totalCount == 0:
		repository.create_pull(base=repository.default_branch, head=branchPullRequest, title=message)

if __name__ == '__main__':
	check_asdl()
