# Minimalist LaTeX Template for Academic Papers

This repository contains a LaTeX template for academic papers. The template carefully follows typographical best practices and has a minimalist design.

## Documentation

The template's documentation is available at https://pascalmichaillat.org/d2/.

## Features

+ The font for text, roman math, and numbers is [Source Serif Pro](https://fonts.google.com/specimen/Source+Serif+Pro).
+ The font for Greek and calligraphic math is [Euler](http://luc.devroye.org/fonts-26139.html).
+ No colors are used in the text to reduce distraction and to guarantee quality printing.
+ Margins, spacing, and font size are set for comfortable reading.
+ Headings are designed for easy scanning.
+ Formatting is also specified for figures, tables, appendix, and a separate online appendix.

## Usage

+ Clone the repository to your local machine.
+ Start editing the LaTeX file `paper.tex` to replace the boilerplate content with the content of your paper. 
+ Replace the figures in the PDF file `figures.pdf` with the figures that will be included in the paper. There should be one figure per page.
+ Replace the references in the BibTeX file `bibliography.bib` with the references that will be included in the paper.
+ Compile `paper.tex` with pdfTeX. This will generate a PDF file of your paper named `paper.pdf`.
+ The LaTeX style file `paper.sty` collects all the commands to format the paper. The file must be included in the same folder as `paper.tex`. It can be modified to alter the paper's format.
+ The BibTeX style file `bibliography.bst` collects all the commands to format the bibliography. It must be included in the same folder as `paper.tex`. It can be modified to alter the bibliography's format. This style file is based on `econ.bst`, which was created by Shiro Takeda and is [available on GitHub](https://github.com/ShiroTakeda/econ-bst).
+ The file `paper.pdf` is not required to use the template. It only illustrate the output of the template. It will be overridden once `paper.tex` is compiled.

### Online appendix

The repository also includes files to produce an online appendix—in case the paper's appendix must be carved out into a separate, online appendix upon publication. An online appendix can be produced as follows:

+ Start editing the LaTeX file `appendix.tex` to replace the boilerplate content with the content of your online appendix. 
+ The equation and section labels from `paper.tex` can be used in `appendix.tex`. [This requires the following](https://www.ctan.org/pkg/xr):
	+ The file `appendix.tex` is in the same folder as `paper.tex`.
	+ The file `paper.tex` is compiled first.
	+ The auxiliary file `paper.aux` is available when `appendix.tex` is compiled.
+ Compile `appendix.tex` with pdfTeX. This will generate a PDF file of your appendix named `appendix.pdf`.
+ The LaTeX style file `appendix.sty` collects additional commands to format the online appendix. It must be included in the same folder as `appendix.tex`. It can be modified to alter the format of the online appendix. It works in conjunction with `paper.sty`, which must be included in the same folder. 
+ The file `appendix.pdf` is not required to use the template. It only illustrate the output of the template, and will be overridden once `appendix.tex` is compiled.

## Software

The template was developed on a Mac running macOS Ventura 13.2 with the MacTeX-2021 distribution. Hopefully, it should also work on other machines and with more recent distributions.

## License

The content of this repository is licensed under the terms of the MIT License.

## Related resources

+ [LaTeX template for academic presentations](https://github.com/pmichaillat/latex-presentation) – This template produces academic presentations following the same principles, and with a similar appearance, as this paper template. 
+ [LaTeX commands to write math](https://github.com/pmichaillat/latex-math) – These commands make it easy to write mathematical expressions. They can be used in combination with this paper template.
<!-- + [These Matlab scripts](https://github.com/pmichaillat/matlab-graph) produce clean 4:3 graphs that can be directly imported into slides and then into the paper. They can be used to generate graphs that can be inserted into `figures.pdf` in combination with this paper template. -->
