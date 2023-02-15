# LaTeX Template for Academic Papers

This repository contains a minimalist template to write academic papers with LaTeX.

## Template documentation

The template is documented at https://pascalmichaillat.org/d2/.

## Template overview

+ The font for text, roman math, and numbers is [Source Serif Pro](https://fonts.google.com/specimen/Source+Serif+Pro).
+ The font for Greek and calligraphic math is [Euler](http://luc.devroye.org/fonts-26139.html).
+ No colors are used in the text (only black) to reduce distraction, and so papers print well.
+ Colors are reserved for graphs.
+ Margins, spacing, and font size are set for comfortable reading.
+ Headings are designed so the paper is easy to scan.
+ Formatting is also specified for figures, tables, appendix, and online appendix.

## Template files

The repository contains files to produce a minimalist paper with LaTeX. The template was developed with the MacTeX-2021 distribution.

+ `paper.tex` –  LaTeX file containing the skeleton of the paper. Fill it out with the content of your paper. Compile it with pdfTeX.
+ `paper.sty` –  LaTeX style file collecting all the formatting commands. Must be included in the same folder as `paper.tex`.
+ `figures.pdf` – PDF file with all the figures included in the paper. Replace the figures with your own figures—one per page.
+ `bibliography.bib` – BibTeX file with all the references included in the paper. Replace these references with your own.
+ `bibliography.bst` – BibTeX style file to format the references.  Must be included in the same folder as `paper.tex`. This style file is based on `econ.bst`, which was created by [Shiro Takeda](https://shirotakeda.github.io) and is [available on GitHub](https://github.com/ShiroTakeda/econ-bst).
+ `paper.pdf` – PDF file produced by compiling `paper.tex` with pdfTeX. This file is not required to use the template; it only illustrate the output of the template.

## Online appendix

The repository also includes files to produce an online appendix—in case the paper's appendix must be carved out into a separate, online appendix. 

+ `appendix.tex` –  LaTeX file containing the skeleton of the online appendix. Fill it out with the content of your online appendix. Compile it with pdfTeX. The equation and section labels from `paper.tex` can be used in `appendix.tex` thanks to the `xr` package. [This requires the following](https://www.ctan.org/pkg/xr):
	* `appendix.tex` is be in the same folder as `paper.tex`.
	* `paper.tex` is compiled first.
	* The auxiliary file `paper.aux` is available when `appendix.tex` is compiled.
+ `appendix.sty` –  LaTeX style file collecting additional formatting commands for the online appendix. Must be included in the same folder as `appendix.tex`. This style file must be used in conjunction with `paper.sty`, which must also be included in the folder. 
+ `appendix.pdf` – PDF file produced by compiling `appendix.tex` with pdfTeX. This file is not required to use the template; it only illustrate the output of the template.

## Related resources

+ [This LaTeX template](https://github.com/pmichaillat/latex-presentation) produces minimalist academic presentations following the same principles, and with a similar general appearance, as this paper template. 
+ [This LaTeX style file](https://github.com/pmichaillat/latex-math) contains commands to easily typeset mathematical expressions. It can be used in combination with this paper template to make it easier to type and read math.

## License

The content of this repository is licensed under the terms of the [MIT License](https://opensource.org/license/mit-license-php/).
