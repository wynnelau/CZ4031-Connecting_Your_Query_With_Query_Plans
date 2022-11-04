# CZ4031_Project2

## Suggested Git workflow

Each new feature should reside in its own branch. When a feature is complete, it gets merged into master via a pull request.

### Creating a new feature branch

```sh
git branch <branch_name>
git checkout <branch_name>
```

When done with development on fthat eature, make sure that your repo is up-to-date.

```sh
git checkout master
git pull
```

Then, rebase your feature branch on master and push.

```sh
git checkout <branch_name>
git rebase master
git push
```

After resolving merge conflicts(if any) submit a pull request on GitHub.

### Submitting a pull request

1. Go to the repo on GitHub.
2. Click on [Pull Requests]([github.com/pehweihang/cryspbook/pulls](https://github.com/akshitkaranam/CZ4031_Project1/pulls))
3. Click on New pull request.
4. Request a merge to master branch.

Once a pull requested is created, every member checks it to see if there are any part of his code that has been accidentally changed. Once we confirm there
