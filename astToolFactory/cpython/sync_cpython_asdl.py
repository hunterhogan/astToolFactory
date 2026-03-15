# ruff: noqa: D100, D103
from __future__ import annotations

from github import Auth, Github
from github.Commit import Commit
from github.ContentFile import ContentFile
from github.InputGitTreeElement import InputGitTreeElement
from operator import attrgetter, methodcaller
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
	from collections.abc import Iterable
	from github.Commit import Commit
	from github.ContentFile import ContentFile
	from github.GitCommit import GitCommit
	from github.GitRef import GitRef
	from github.PaginatedList import PaginatedList
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

def checkBranch(repositoryCpython: Repository, pathRelative_asdl: Path) -> tuple[list[PurePosixPath], Iterable[PurePosixPath]]:
	listFilenames: frozenset[str] = frozenset(map(attrgetter('name'), filter(methodcaller('is_file'), pathRelative_asdl.iterdir()))) # pyright: ignore[reportUnknownArgumentType]

	listPathRelativeFilenamesWritten: list[PurePosixPath] = []
	listPathRelativeFilenamesDeleted: Iterable[PurePosixPath] = []

	for filename in listFilenames:
		listPathRelativeFilenamesDeleted.append(PurePosixPath(pathRelative_asdl / filename))
		paginatedList: PaginatedList[Commit] = repositoryCpython.get_commits(sha=pathRelative_asdl.name, path=f"Parser/{filename}")
		if 0 < paginatedList.totalCount:
			listCommit: list[Commit] = paginatedList.get_page(0)
			if listCommit:
				commit: Commit = listCommit[0]
				if commit.sha not in listFilenames:

					contents: list[ContentFile] | ContentFile = repositoryCpython.get_contents(f"Parser/{filename}", ref=pathRelative_asdl.name)
					if isinstance(contents, list):
						raise ValueError
					pathFilename: Path = pathRelative_asdl / filename
					pathFilename.write_bytes(contents.decoded_content)
					listPathRelativeFilenamesWritten.append(PurePosixPath(pathFilename))

					(pathRelative_asdl / commit.sha).touch()
					listPathRelativeFilenamesWritten.append(PurePosixPath(pathRelative_asdl / commit.sha))

	if listPathRelativeFilenamesWritten:
		listPathRelativeFilenamesDeleted = set(listPathRelativeFilenamesDeleted).difference(listPathRelativeFilenamesWritten)
		for condemnedPathFilename in listPathRelativeFilenamesDeleted:
			Path(condemnedPathFilename).unlink()
	else:
		listPathRelativeFilenamesDeleted = []

	return listPathRelativeFilenamesWritten, listPathRelativeFilenamesDeleted

def GitHubActionPushFiles(repository: Repository, listPathRelativeFilenamesWritten: list[PurePosixPath], listPathRelativeFilenamesDeleted: list[PurePosixPath], branchPullRequest: str = 'update-cpython-asdl') -> None:
	message: str = 'Update CPython ASDL files'
	gitCommitParent: GitCommit = repository.get_git_commit(repository.get_branch(repository.default_branch).commit.sha)
	repository.create_git_ref(ref=f"refs/heads/{branchPullRequest}", sha=gitCommitParent.sha)

	gitCommitUpdated: GitCommit = repository.create_git_commit(message, repository.create_git_tree([
			*(InputGitTreeElement(pathRelativeFilenameDeleted.as_posix(), mode='100644', type='blob', sha=None)
				for pathRelativeFilenameDeleted in listPathRelativeFilenamesDeleted
			),
			*(InputGitTreeElement(pathRelativeFilenameWritten.as_posix(), mode='100644', type='blob'
					, content=Path(pathRelativeFilenameWritten).read_text(encoding='utf-8'))
				for pathRelativeFilenameWritten in listPathRelativeFilenamesWritten
			),
		], base_tree=gitCommitParent.tree), [gitCommitParent])
	gitReferencePullRequest: GitRef = repository.get_git_ref(f'heads/{branchPullRequest}')
	gitReferencePullRequest.edit(gitCommitUpdated.sha)
	repository.create_pull(base=repository.default_branch, head=branchPullRequest, title=message)

if __name__ == '__main__':
	check_asdl()
