import sys
src=sys.argv[1]
def sub(path, old, new):
    p=f"{src}/{path}"; s=open(p,encoding="utf-8",newline="").read(); assert old in s,(path,old)
    open(p,"w",encoding="utf-8",newline="").write(s.replace(old,new,1))
sub("settings.tex", r"{large language models, algorithm design, combinatorial optimization}", r"{only, two}")
sub("settings.tex", r"{keyword one, keyword two, keyword three}", r"{a, b, c, d, e, f}")
words=" ".join(["word"]*520)
open(f"{src}/frontmatter/abstract-en.tex","w",encoding="utf-8").write(words+"\n")
open(f"{src}/frontmatter/abstract-sk.tex","w",encoding="utf-8").write("First paragraph of the Slovak abstract that has a number of words.\n\nSecond paragraph.\n")
sub("chapters/03-first-result.tex", r"%\chapterbasedon{Key2026}", r"\chapterbasedon{Diestel2025}")
