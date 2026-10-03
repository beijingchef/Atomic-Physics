# English Quarto edition

This folder contains the English edition of the source manuscript, with one QMD file per original chapter, plus `index.qmd` and the Quarto book configuration.

From this folder, run:

```sh
quarto preview
quarto render --to html
```

The HTML book is written to `_book/index.html`. A PDF configuration is also supplied (`quarto render --to pdf`); PDF rendering requires an appropriate TeX installation.

## Conversion details

- All 2,597 embedded MathType equations were converted to LaTeX. Inline equations use `$...$`; displayed equations use `$$...$$` with Quarto equation labels and automatic chapter-based numbering.
- Native Word mathematics and additional formula pictures were also converted. The two grouped measurement diagrams were rebuilt in LaTeX.
- Word equation references have been replaced by linked Quarto references. Equation numbers are regenerated, so they may differ from the Word edition.
- Tables, exercises, solutions, footnotes, references, and the original chapter order are retained. The original Word manuscript is unchanged.
- Original scientific illustrations are retained. In a few original raster illustrations, the short labels for “source” and “eigenvalue” remain in Chinese; the surrounding English descriptions explain them.
- Sections 10.1, 10.2, and the Chapter 6 solutions heading have no substantive content in the source; no missing material has been invented. The repeated Exercise 4.5 heading in the solutions is retained from the manuscript.
- Minor editorial repairs include a missing equation bookmark, split Word reference fields, and the obvious z-component typo in the spin expectation-value vector. The preface's discussion of optical refraction/interference has been phrased without classifying these specifically as quantum effects. This is a translation and format conversion, not a comprehensive scientific revision.

The extraction, English paragraph translations, equation normalization, and validation records are in the adjacent `conversion_work` folder. `build_book.py` recreates the QMD files from those records.

## Validation

All 13 QMD files rendered successfully with Quarto 1.10.18. All 2,871 converted math expressions passed a MathJax syntax check. Browser checks of all 12 chapters found no math-rendering errors or missing images. The HTML edition bundles MathJax 3.2.2 locally (license included). The PDF format has not been rendered.

