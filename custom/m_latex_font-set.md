---
header-includes:
  - \usepackage{fontspec}
  - \setmainfont{Junicode}
  - \newfontfamily\myregularfont{Junicode}
  - \newfontfamily\mychinesefont{IPAexMincho}
  - \usepackage[CJK]{ucharclasses}
  - \setTransitionsForCJK{\mychinesefont}{\myregularfont}
---
From Michael Franzl's blog at
[https://michaelfranzl.com/2014/12/10/xelatex-unicode-font-fallback-unsupported-characters/]()

Font IPAexMincho provided in debian by package `texlive-lang-cjk`
