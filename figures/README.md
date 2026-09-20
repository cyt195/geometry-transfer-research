# Figures

`figure1_overview.tex` is a conceptual TikZ figure, not empirical evidence. It contains no headline numbers.

Include it in a LaTeX document that loads:

```tex
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
```

Future empirical figures must be generated from supplied authoritative data with `scripts/reproduce_figures.py` or an independently audited successor. Generated outputs belong in a new result namespace and should carry input hashes and source keys.
