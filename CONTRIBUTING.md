# Contribution Guidelines

When contributing to `PujoAtlasKol-Backend`, whether on GitHub or in other community spaces:

- Be respectful, civil, and open-minded.
- Before opening a new pull request, try searching through the [issue tracker](https://github.com/Pujo-Atlas-Kolkata/PujoAtlasKol-Backend/issues) for known issues or fixes.
- If you want to make code changes based on your personal opinion(s), make sure you open an issue first describing the changes you want to make, and open a pull request only when your suggestions get approved by maintainers.

## How to Contribute

### Prerequisites

In order to not waste your time implementing a change that has already been declined, or is generally not needed, start by [opening an issue](https://github.com/Pujo-Atlas-Kolkata/PujoAtlasKol-Backend/issues/new) describing the problem you would like to solve.

### Local Environment Setup

Please follow the [Contributing Guidelines](README.md) to setup the project.

### Create a branch
Create a new branch from the corresponding feature branch that will be mentioned in the issue as a tag, in the below format. This will get the feature branch tagged to the issue itself.

```bash
git checkout -b <commit-type>/[<issue-number>]/{<change-title>}
example - "feat/12/add-event-api"
```



### Implement your changes

When making commits, make sure to follow the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) guidelines, i.e. prepending the message with `feat:`, `fix:`, `chore:`, `docs:`. You can use `git status` to double check which files have not yet been staged for commit:

```bash
git add <file> && git commit -m "feat/fix/chore/docs: commit message"
```

Please keep in mind that you will not be able to push commits if you're not following the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) guidelines or Lint check is failing.

### When you're done

When you're done implementing your changes, please also make a manual, functional test of your changes. When all that's done, it's time to open a pull request to upstream, and fill out the title and body appropriately. Again, make sure to follow the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) guidelines for your title.

### Community

For help, discussion about best practices, or any other conversation that would benefit this project: [Join the Pujo Atlas Discord Server.](https://discord.com/invite/xxSXWYf6d4)
