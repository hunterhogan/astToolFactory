# noqa: INP001
from github import Auth, Github
from github.ContentFile import ContentFile
from github.InputGitTreeElement import InputGitTreeElement
from pathlib import Path
from typing import Any, TYPE_CHECKING
import sys

if TYPE_CHECKING:
	from github.Repository import Repository

def main() -> None:
	settings: dict[str, Any] = {
		'githubToken': sys.argv[1],
		'repositoryNameThis': sys.argv[2],
		'cpythonRepo': 'python/cpython',
		'branches': ['3.9', '3.10', '3.11', '3.12', '3.13', '3.14'],
		'files': ['Parser/Python.asdl', 'Parser/asdl.py'],
		'localBase': 'astToolFactory/cpython',
		'localPrefix': '_py',
		'notifyUser': 'hunterhogan'
	}

	authToken: Auth.Token = Auth.Token(settings['githubToken'])
	githubClient: Github = Github(auth=authToken)
	repositoryCPython: Repository = githubClient.get_repo(settings['cpythonRepo'])

	listBranches: list[str] = settings['branches']
	listPathFilenamesTarget: list[str] = settings['files']

	listPathFilenameChanged: list[Path] = []
	for branch in listBranches:
		pathDirectory: Path = Path(settings['localBase']) / f"{settings['localPrefix']}{branch.replace('.', '')}"
		for relativePathFilename in listPathFilenamesTarget:
			content = repositoryCPython.get_contents(relativePathFilename, ref=branch)
			if isinstance(content, ContentFile):
				decodedContent: bytes = content.decoded_content
				pathFilename: Path = pathDirectory / Path(relativePathFilename).name
				if not pathFilename.exists() or pathFilename.read_bytes() != decodedContent:
					pathFilename.parent.mkdir(parents=True, exist_ok=True)
					pathFilename.write_bytes(decodedContent)
					listPathFilenameChanged.append(pathFilename)

	if listPathFilenameChanged:
		branchName: str = "update-cpython-asdl"
		repository = githubClient.get_repo(settings['repositoryNameThis'])

		# Get the current main branch SHA
		mainBranch = repository.get_branch("main")
		mainSha: str = mainBranch.commit.sha

		# Create a new branch
		repository.create_git_ref(ref=f"refs/heads/{branchName}", sha=mainSha)

		# Create blobs and tree entries for each changed file
		listTreeElements: list[InputGitTreeElement] = []
		for pathFilename in listPathFilenameChanged:
			contentBytes: bytes = pathFilename.read_bytes()

			# Create blob
			blob = repository.create_git_blob(content=contentBytes.decode('utf-8'), encoding='utf-8')

			# Create tree element
			treeElement = InputGitTreeElement(
				path=str(pathFilename),
				mode='100644',
				type='blob',
				sha=blob.sha
			)
			listTreeElements.append(treeElement)

		# Create tree
		tree = repository.create_git_tree(listTreeElements, base_tree=repository.get_git_commit(mainSha).tree)

		# Create commit
		commit = repository.create_git_commit(
			message=f"Update CPython ASDL files: {', '.join(str(pathFilename) for pathFilename in listPathFilenameChanged)}",
			tree=tree,
			parents=[repository.get_git_commit(mainSha)]
		)

		# Update branch reference
		repository.get_git_ref(f"heads/{branchName}").edit(sha=commit.sha)

		# Create pull request
		pullRequest = repository.create_pull(
			title=f"Update CPython ASDL files ({branchName})",
			body=f"Automated update. cc @{settings['notifyUser']}",
			head=branchName,
			base="main"
		)
		pullRequest.create_issue_comment(f"@{settings['notifyUser']} CPython ASDL files updated in astToolFactory.")

if __name__ == "__main__":
	main()
