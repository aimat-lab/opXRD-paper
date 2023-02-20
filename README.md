# LaTeX Template for Academic Papers

This repository contains a minimalist template to write academic papers with LaTeX.

## Documentation

The template's documentation is available at https://pascalmichaillat.org/d2/.

## Features

+ The font for text, roman math, and numbers is [Source Serif Pro](https://fonts.google.com/specimen/Source+Serif+Pro).
+ The font for Greek and calligraphic math is [Euler](http://luc.devroye.org/fonts-26139.html).
+ No colors are used in the text to reduce distraction and to guarantee quality printing.
+ Margins, spacing, and font size are set for comfortable reading.
+ Headings are designed for easy scanning.
+ Formatting is also specified for figures, tables, appendix, and online appendix.

## Included files

+ `paper.tex` –  LaTeX file containing the skeleton of the paper.
+ `paper.sty` –  LaTeX style file collecting all the formatting commands.
+ `figures.pdf` – PDF file with all the figures included in the paper.
+ `bibliography.bib` – BibTeX file with all the references included in the paper.
+ `bibliography.bst` – BibTeX style file to format the references. This style file is based on `econ.bst`, which was created by [Shiro Takeda](https://shirotakeda.github.io) and is [available on GitHub](https://github.com/ShiroTakeda/econ-bst).
+ `paper.pdf` – PDF file produced by compiling `paper.tex` with pdfTeX.

## Usage

+ Fill out `paper.tex` with the content of your paper. Compile the file with pdfTeX.
+ `paper.sty` must be included in the same folder as `paper.tex`. It can be modified to alter the paper's format.
+ `bibliography.bst` must be included in the same folder as `paper.tex`. It can be modified to alter the bibliography's format.
+ Replace the figures in `figures.pdf` with your own figures—one per page.
+ Replace the references in `bibliography.bib` with your own references.
+ `paper.pdf` is not required to use the template. It only illustrate the output of the template, and will be overridden once `paper.tex` is compiled.
+ The template was developed with the MacTeX-2021 distribution but should hopefully also work with more recent distributions. 

## Online appendix

The repository also includes files to produce an online appendix (in case the paper's appendix must be carved out into a separate, online appendix): 

+ `appendix.tex` –  LaTeX file containing the skeleton of the online appendix.
+ `appendix.sty` –  LaTeX style file collecting additional formatting commands for the online appendix.
+ `appendix.pdf` – PDF file produced by compiling `appendix.tex` with pdfTeX.

These files should be used as follows:

+ Fill out `appendix.tex` with the content of your online appendix. Compile it with pdfTeX. The equation and section labels from `paper.tex` can be used in `appendix.tex` thanks to the `xr` package. [This requires the following](https://www.ctan.org/pkg/xr):
	* `appendix.tex` is in the same folder as `paper.tex`.
	* `paper.tex` is compiled first.
	* The auxiliary file `paper.aux` is available when `appendix.tex` is compiled.
+ `appendix.sty` must be included in the same folder as `appendix.tex`. It can be modified to alter the format of the online appendix. It works in conjunction with `paper.sty`, which must also be included in the folder. 
+ `appendix.pdf` is not required to use the template. It only illustrate the output of the template, and will be overridden once `appendix.tex` is compiled.

## Related resources

+ [This LaTeX template](https://github.com/pmichaillat/latex-presentation) produces minimalist academic presentations following the same principles, and with a similar general appearance, as this paper template. 
+ [This LaTeX style file](https://github.com/pmichaillat/latex-math) contains commands to easily typeset mathematical expressions. It can be used in combination with this paper template to make it easier to type and read math.

## License

The content of this repository is licensed under the terms of the [MIT License](https://opensource.org/license/mit-license-php/).
