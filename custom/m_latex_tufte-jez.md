---
documentclass: tufte-handout
fontsize: 12pt
mainfont: TeX Gyre Pagella
monofont: Menlo for Powerline
newtxmathoptions:
- cmintegrals
- cmbraces
colorlinks: true
linkcolor: RoyalBlue
urlcolor: RoyalBlue
---

# Source #

From [sample markdown file][file] at github repo [jez/pandoc-starter][repo].

# Currently fails #

Fails with this error message if documentclass=`tufte-handout`:

```bash
ERROR:     !Error producing PDF.
ERROR:     !! Argument of \MakeTextLowercase has an extra }.
ERROR:     !<inserted text>
ERROR:     !                \par
ERROR:     !l.265 \begin{Shaded}
```

[comment]: # (URLs)

   [file]:
   https://github.com/jez/pandoc-starter/blob/master/tufte-handout/src/sample.md

   [repo]:
   https://github.com/jez/pandoc-starter
