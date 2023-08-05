# resfmt

A ReScript helper for code formatter. This script enables code
formatting with `bsc -format` with stdin so that it can be used
with [emacs-format-all-the-code](https://github.com/lassik/emacs-format-all-the-code).

This is a workaround for `bsc` not supporting stdin, see this
[issue](https://github.com/rescript-lang/rescript-compiler/issues/4846).
