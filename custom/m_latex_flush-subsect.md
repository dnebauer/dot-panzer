---
header-includes:
  - \usepackage[section]{placeins}
  - \makeatletter
  - \AtBeginDocument{\expandafter\expandafter\renewcommand\expandafter\expandafter\subsection\expandafter\expandafter{\expandafter\expandafter\@fb@secFB\subsection}}
  - \makeatother
---
From a [StackExchange question](https://tex.stackexchange.com/a/118667).

Need to double \expandafter commands because one *level* of them is *consumed*
during metadata extraction.
