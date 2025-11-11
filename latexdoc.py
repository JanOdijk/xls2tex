

docend = '\n' + r'\end{exe}' + '\n\n' + r'\end{document}'

docbegin = \
r"""
%\documentclass[output=paper,colorlinks,citecolor=brown]{langscibook}
\documentclass[output=paper,colorlinks,citecolor=brown]{article}

\input{multilingual-mwe-examples.tex} % PMWE-specific commands for MWE examples

%\newfontfamily\Parsifont[Script=Arabic]{ScheherazadeRegOT_Jazm.ttf} % Fonts for Farsi
%\newcommand{\PRL}[1]{\RL{\Parsifont #1}} % Shortcut for right-to-left (\RL) Farsi text
\newcommand\blfootnote[1]{%
  \begingroup
  \renewcommand\thefootnote{}\footnote{#1}%
  \addtocounter{footnote}{-1}%
  \endgroup
}
    
\usepackage{enumitem}
\usepackage{spverbatim}

\bibliography{localbibliography}

%\frontmatter

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\title{Canonical Forms for MWEs from the PARSEME Guidelines 2.0}

\author{
 Jan Odijk \affiliation{Institute for Language Sciences, Utrecht, the Netherlands}\and 
 Kilian Evang \affiliation{Düsseldorf University, Germany}\and 
 Dan Zeman \affiliation{Charles University, Prague, Czech Republic}\lastand
}

%\abstract{}
\papernote{}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\begin{document}

\maketitle
\rohead{{\small Canonical Forms for MWEs}}
\lehead{{\small the authors}}

\blfootnote{Published under the Creative Commons Attribution 4.0 Licence (CC BY 4.0):
http://creativecommons.org/licenses/by/4.0/}




"""