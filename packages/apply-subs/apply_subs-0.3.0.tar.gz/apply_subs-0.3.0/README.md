# apply-subs
![PyPI](https://img.shields.io/pypi/v/apply-subs)
![PyPI](https://img.shields.io/pypi/pyversions/apply_subs?logo=python&logoColor=white&label=Python)
[![codecov](https://codecov.io/gh/neutrinoceros/apply_subs/branch/main/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/apply_subs)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/neutrinoceros/apply_subs/main.svg)](https://results.pre-commit.ci/latest/github/neutrinoceros/apply_subs/main)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Apply a dictionnary (json) of substitutions to a text file.
## Installing

```shell
$ pip install apply-subs
```

# Examples

## minimal
```shell
$ echo "Lorem ipsum dolor sit amet, consectetur adipiscing elit" > mytext.txt
$ echo '{"Hello": "Lorem ipsum", "goodbye": "adipiscing elit"}' > mysubs.json
$ apply-subs mytext.txt -s mysubs.json
```
will print the patched content
```
Hello dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore goodbye.
```

## patch mode


In patch mode (`-p/--patch`),
print a patch diff instead of the end result
```patch
--- mytext.txt
+++ mytext.txt (patched)
@@ -1 +1 @@
-Lorem ipsum dolor sit amet, consectetur adipiscing elit
+Hello dolor sit amet, consectetur goodbye
```

Use `-cp/--cpatch/--colored-patch` for a colored output (when supported).

## inplace substitutions
`-i/--inplace`
```
apply-subs --inplace mytext.txt -s mysubs.json
```
is equivalent to
```
apply-subs mytext.txt -s mysubs.json > mytext.txt
```
