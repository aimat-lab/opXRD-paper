# LaTeX template for academic papers

This repository contains a minimalist template to write academic papers with LaTeX.

## Included files and how to use them

- `paper.tex` –  Skeleton of the paper. Fill it out with the content of your paper.
- `paper.sty` –  LaTeX style file collecting all the formatting commands. Must be included in the same folder as `paper.tex`.
- `figures.pdf` – PDF file with all the figures included in the paper. Replace the figures with your own figures---one per page. An easy way to do that is to create a Keynote or Powerpoint presentation; insert each figure as a slide background; and save the resulting presentation as PDF. With this method, all the figures have the exact same size. It is also possible to use Keynote or Powerpoint to annotate the figures created with an external software (Matlab, R, and so on).
- `bibliography.bib` – BibTeX file with all the references included in the paper. Replace the references with your own.
- `bibliography.bst` – BibTeX style file to format the entries into the reference section. This style file is [hosted in this GitHub repository](https://github.com/pmichaillat/latex-bibliography). 
- `paper.pdf` – PDF file produced by compiling `paper.tex` (with PDFTeX). This file is not required to use the template; it only illustrate the output of the template.

## Additional files for online appendix

The repository also includes an additional template and style file in case the appendix of the paper must be carved out into a separate online appendix. 

- `appendix.tex` –  Skeleton of the online appendix. Fill it out with the content of your online appendix. The appendix must be in the same folder as the paper so the equation and section labels from the paper can be used in the online appendix.
- `appendix.sty` –  LaTeX style file collecting additional formatting commands for the online appendix. Must be included in the same folder as `appendix.tex`. This style file must be used in conjonction with `paper.sty`, which must also be included in the folder. 
- `appendix.pdf` – PDF file produced by compiling `appendix.tex` (with PDFTeX). This file is not required to use the template; it only illustrate the output of the template.

## Key features

- The font for text, roman math, and numbers is [Source Serif Pro](https://fonts.google.com/specimen/Source+Serif+Pro).
- The font for Greek and calligraphic math is [Euler](http://luc.devroye.org/fonts-26139.html).
- No colors are used in the text (only black) to reduce distraction, and so papers print well.
- Colors are reserved for graphs.
- Margins, spacing, and font size are set for comfortable reading.
- Formating is also specified for appendix and online appendix.

## Reference

As much as possible the style file follows Matthew Butterick's wonderful typographical advice in [Practical Typography](https://practicaltypography.com).

## Related LaTeX resources

- [This LaTeX template](https://github.com/pmichaillat/latex-presentation) produces minimalist academic presentations following the same principles and with a similar general appearance as this paper template. 
- [This LaTeX style file](https://github.com/pmichaillat/latex-math) contains commands to easily typeset mathematical expressions. It can be used in combination with this paper template to make it easier to type and read math.
