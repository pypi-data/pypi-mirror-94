# IBIS Microsoft SQL Backend


## Releasing

This project uses Rever and GitHub actions for releasing a new package version.

Make sure your current environment has [rever](https://regro.github.io/rever-docs/) installed. You can create an environment just for the package releasing:

```bash
conda env create -n ibis-mssql-release --file envs/release.yaml
```

Activate your new environment:

```sh
conda activate ibis-mssql-release
```

Run `rever check` to check your `rever` configuration is correct.

```bash
rever check
```

Delete the rever folder to start a clean release.

```bash
rm -rf rever/
```

Lets start the releasing process!

```
Note: Maybe you want to have a fresh clone just for releasing.
```

```
Note: For releasing, you probably want to clone directly from the upstream repository.
```

```
Note: Ensure you have permissions to push changes to the repository.
```

Ensure you are using the latest version of the master branch:

```sh
git fetch --all
# if the repository is set as origin
git checkout origin/master
# or, if the repository is set as upstream
git checkout upstream/master
```

Now, if you want to release the version `0.1.5`
(please, first check the latest version released), run:

```sh
rever 0.1.5
```

After that, you can push the changes to upstream:

```sh
git push
```
