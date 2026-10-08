#!/bin/bash
# usage: check.sh <variant> <jobname>
cd /c/Users/norom/Documents/latex/tmp/thesis-build/$1
J=${2:-main}
echo "--- latex warnings/errors"; grep -n -i -E "warning|^!|error" out/$J.log | grep -v infwarerr
echo "--- overfull/underfull"; grep -n -A2 -E "^(Overfull|Underfull)" out/$J.log | head -40
echo "--- bibtex"; grep -E "^Warning|error message|Warning--" out/$J.blg
echo "--- pdfinfo"; pdfinfo out/$J.pdf | grep -E "Title|Author|Keywords|Pages|Page size|PDF version"
echo "--- unresolved in text"; pdftotext -enc UTF-8 out/$J.pdf - | grep -n -E "\?\?|\[\?\]"
echo "--- fonts not embedded / Type 3"; pdffonts out/$J.pdf | awk 'NR>2 && ($5!="yes" || $2=="Type" ) {print}' | head; pdffonts out/$J.pdf | grep -c "Type 3"
echo "--- page labels (PDF /PageLabels)"
python - "$J" <<'PY'
import sys, pypdf
r=pypdf.PdfReader(f"out/{sys.argv[1]}.pdf")
labs=r.page_labels
print(len(labs), "pages; labels:", ",".join(labs[:6]), "...", ",".join(labs[-3:]))
PY
