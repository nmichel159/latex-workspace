import sys, re, shutil
src = sys.argv[1]
def sub(path, old, new, count=1):
    p = f"{src}/{path}"
    s = open(p, encoding="utf-8", newline="").read()
    assert old in s, (path, old)
    s = s.replace(old, new, count)
    open(p, "w", encoding="utf-8", newline="").write(s)
st = "settings.tex"
sub(st, r"\newcommand{\ThesisSides}{oneside}", r"\newcommand{\ThesisSides}{twoside}")
sub(st, r"%\thesislabelsenglishtrue", r"\thesislabelsenglishtrue")
sub(st, r"\thesisdeclarationfalse", r"\thesisdeclarationtrue")
sub(st, r"\thesisglossaryfalse", r"\thesisglossarytrue")
sub(st, r"\thesisbackmatterfalse", r"\thesisbackmattertrue")
sub(st, r"\thesisindexfalse", r"\thesisindextrue")
sub(st, r"\newcommand{\ThesisConsultant}{}", r"\newcommand{\ThesisConsultant}{doc. RNDr. Consultant Name, PhD.}")
sub(st, r"\newcommand{\ThesisRegNo}{}", r"\newcommand{\ThesisRegNo}{PF-2029-001}")
sub(st, r"\newcommand{\ThesisSubtitle}{}", r"\newcommand{\ThesisSubtitle}{A Sample Subtitle}")
sub(st, r"\newif\ifthesiscovercounts ", r"\newif\ifthesiscovercounts \thesiscovercountstrue ")
sub(st, r"\newcommand{\ThesisAssignmentPages}{1}", r"\newcommand{\ThesisAssignmentPages}{1,2}")
sub(st, r"\newcommand{\ThesisFooter}{\fancyfoot[C]{\thepage}}", r"\newcommand{\ThesisFooter}{\fancyfoot[RO,LE]{\thepage}}")
if len(sys.argv) > 2 and sys.argv[2] == "pdfa":
    sub(st, r"\newif\ifthesispdfa ", r"\newif\ifthesispdfa \thesispdfatrue ")
# enable the examples
def uncomment_block(path, start, end):
    p = f"{src}/{path}"
    lines = open(p, encoding="utf-8", newline="").read().split("\n")
    out, on = [], False
    for l in lines:
        if start in l: on = True
        if on and l.startswith("% ") and not l.startswith("% ---") and not l.startswith("% Labels") and not l.startswith("% Caption") and not l.startswith("% Lines"):
            l = l[2:]
        elif on and l == "%":
            l = ""
        out.append(l)
    open(p, "w", encoding="utf-8", newline="").write("\n".join(out))
uncomment_block("chapters/02-preliminaries.tex", r"% \begin{definition}[Cut-path]", "")
uncomment_block("chapters/03-first-result.tex", r"% \begin{algorithm}[tb]", "")
shutil.copy("C:/Users/norom/Documents/latex/tmp/thesis-build/dummy/assignment.pdf", f"{src}/assignment.pdf")
shutil.copy("C:/Users/norom/Documents/latex/tmp/thesis-build/dummy/example.pdf", f"{src}/img/example.pdf")
