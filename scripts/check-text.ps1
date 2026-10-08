<#
.SYNOPSIS
    Checks the style and hygiene of the text in LaTeX sources. Changes nothing; prints findings only.

.DESCRIPTION
    Reads the .tex files of a project (or a given file or folder) and reports:
      - phrases from the phrase list (categories filler, wordy, hype, hedge, meta, ai-tic, grammar, spelling),
      - [long]        a sentence longer than MaxWords words,
      - [dup]         the same word twice in a row ("the the"),
      - [latex]       $$; a space instead of ~ before \ref, \eqref, \cite; a lowercase name before a reference
                      (theorem~\ref); a sentence that starts with math; straight quotes "; a \label with an unknown
                      prefix or a name that is not lowercase words with hyphens; e.g./i.e. without a comma;
                      et al without a period,
      - [todo]        TODO, FIXME, XXX, \fillin, ??,
      - [contraction] don't, can't, it's ...,
      - [spelling]    British forms in American text (optimise, capitalise, colour, modelling, licence, catalogue,
                      programme ...); the list is built in, the phrase list holds only typos.

    Skipped: the preamble (everything before \begin{document} in a file with \documentclass), definition lines
    (\newcommand, \usepackage, ...), the environments verbatim, lstlisting, algorithmic, tikzpicture, equation,
    align and similar, and \[ ... \] blocks. Lines that are mostly Slovak or Czech are skipped by the phrase checks.
    Of several phrase hits that overlap, only the longest is reported.

    The summary table at the end lists words, sentences, mean sentence length and the number of findings per
    category (categories without findings are omitted). Word and sentence counts are approximate: commands,
    math and comments are not counted.

    The phrase list is a UTF-8 TSV file: category<TAB>regex<TAB>suggestion. Lines that start with # and blank lines
    are ignored. The regex uses .NET syntax and is matched case-insensitively against each paragraph (the
    consecutive text lines of one paragraph, comments removed, joined by a space), so that a phrase broken by a
    line end is found; a hit is reported on the line where it starts. Write (?-i:...) around the part that must
    match case-sensitively. If the phrase list is missing, the script says so and runs the built-in checks only.

    Plain text from pdftotext (.txt) is supported: a bare capital A and a single-letter variable are not treated
    as articles there.

    The exit code is 0 even when there are findings; 2 for invalid parameters.

.PARAMETER Project
    Name of a folder in projects/. All .tex files in it are checked (recursively), except the folder preamble/.

.PARAMETER Path
    A .tex or .txt file, or a folder with such files. A relative path is tried from the current folder, then
    from the workspace root.

.PARAMETER PhraseList
    Path to the phrase list. Default: knowledge/writing/phrase-list.tsv.

.PARAMETER MaxWords
    Longest allowed sentence in words (default 40).

.PARAMETER Summary
    Print only the summary table, without the individual findings.

.EXAMPLE
    .\scripts\check-text.ps1 -Project clanok-1-min-cut-path
    .\scripts\check-text.ps1 -Path projects\clanok-1-min-cut-path\sections\01-introduction.tex -MaxWords 30
    .\scripts\check-text.ps1 -Path knowledge\sources\diplomova-praca-2025-min-cut-path.txt -Summary
#>
param(
    [Parameter(Position = 0)]
    [string]$Project,

    [string]$Path,

    [string]$PhraseList,

    [int]$MaxWords = 40,

    [switch]$Summary
)

$workspace = Split-Path -Parent $PSScriptRoot
$projectsRoot = Join-Path $workspace "projects"
$defaultPhraseList = Join-Path $workspace "knowledge\writing\phrase-list.tsv"

function Stop-InvalidParameter([string]$Message) {
    $Host.UI.WriteErrorLine("check-text: $Message")
    exit 2
}

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

if ($Project -and $Path) {
    Stop-InvalidParameter "Pass either -Project or -Path, not both."
}
if (-not $Project -and -not $Path) {
    Stop-InvalidParameter "Missing -Project <name> or -Path <file-or-folder>."
}
if ($MaxWords -lt 1) {
    Stop-InvalidParameter "-MaxWords must be a positive integer."
}

function Test-InPreambleFolder([string]$FullName, [string]$Root) {
    $relative = $FullName.Substring($Root.TrimEnd('\').Length)
    return ($relative -match '(?i)[\\/]preamble[\\/]')
}

$files = New-Object System.Collections.Generic.List[string]
if ($Project) {
    $sourceDirectory = Join-Path $projectsRoot $Project
    if (-not (Test-Path -LiteralPath $sourceDirectory -PathType Container)) {
        $available = (Get-ChildItem -LiteralPath $projectsRoot -Directory | ForEach-Object { $_.Name }) -join ", "
        Stop-InvalidParameter "Project does not exist: $sourceDirectory. Available projects: $available"
    }
    $sourceDirectory = (Get-Item -LiteralPath $sourceDirectory).FullName
    foreach ($item in (Get-ChildItem -LiteralPath $sourceDirectory -Recurse -File | Sort-Object FullName)) {
        # .cls, .sty, .bst and .bib hold no prose; only .tex outside preamble/ is read
        if ($item.Extension -ne ".tex") { continue }
        if (Test-InPreambleFolder $item.FullName $sourceDirectory) { continue }
        $files.Add($item.FullName)
    }
    if ($files.Count -eq 0) {
        Stop-InvalidParameter "Project $Project contains no .tex file."
    }
}
else {
    $candidate = $Path
    if (-not (Test-Path -LiteralPath $candidate)) {
        $candidate = Join-Path $workspace $Path
    }
    if (-not (Test-Path -LiteralPath $candidate)) {
        Stop-InvalidParameter "Path does not exist: $Path"
    }
    $target = Get-Item -LiteralPath $candidate
    if ($target.PSIsContainer) {
        foreach ($item in (Get-ChildItem -LiteralPath $target.FullName -Recurse -File | Sort-Object FullName)) {
            if ($item.Extension -ne ".tex" -and $item.Extension -ne ".txt") { continue }
            if (Test-InPreambleFolder $item.FullName $target.FullName) { continue }
            $files.Add($item.FullName)
        }
        if ($files.Count -eq 0) {
            Stop-InvalidParameter "Folder $($target.FullName) contains no .tex or .txt file."
        }
    }
    else {
        if ($target.Extension -ne ".tex" -and $target.Extension -ne ".txt") {
            Stop-InvalidParameter "Only .tex and .txt files are supported: $($target.FullName)"
        }
        $files.Add($target.FullName)
    }
}

$phraseListExplicit = [bool]$PhraseList
if (-not $phraseListExplicit) {
    $PhraseList = $defaultPhraseList
}
elseif (-not (Test-Path -LiteralPath $PhraseList -PathType Leaf)) {
    $alternative = Join-Path $workspace $PhraseList
    if (Test-Path -LiteralPath $alternative -PathType Leaf) {
        $PhraseList = $alternative
    }
    else {
        Stop-InvalidParameter "Phrase list does not exist: $PhraseList"
    }
}

# The output quotes the source (for example Erdos with a long o), hence UTF-8.
$previousOutputEncoding = $null
try {
    $previousOutputEncoding = [Console]::OutputEncoding
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false
}
catch {
    $previousOutputEncoding = $null
}

# ---------------------------------------------------------------------------
# Constants and regular expressions
# ---------------------------------------------------------------------------

$utf8 = New-Object System.Text.UTF8Encoding $false
$ordinal = [System.StringComparison]::Ordinal
$rxIgnoreCase = [System.Text.RegularExpressions.RegexOptions]"IgnoreCase, CultureInvariant"
$rxNone = [System.Text.RegularExpressions.RegexOptions]"CultureInvariant"

# Placeholders (Unicode private use area) keep this script ASCII.
$MATH = [string][char]0xE000      # inline math
$DISP = [string][char]0xE001      # display math (ends the sentence)
$MACRO = [string][char]0xE002     # custom macro in the text, counted as one word
$EMPH = [string][char]0xE003      # start of an emphasized span (stops "chain \emph{chain paths}" from being a duplicate)

$builtinCategories = @("long", "dup", "latex", "todo", "contraction", "spelling")
$phraseCategories = @("filler", "wordy", "hype", "hedge", "meta", "ai-tic", "grammar")

# Prefixes of knowledge/writing/latex-conventions.md, section 7.
$labelPrefixes = @("sec", "def", "thm", "lem", "clm", "cor", "prop", "rem", "ex", "fig", "tab", "alg", "line", "eq", "prob")

function New-StringSet([string[]]$Items) {
    $set = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    foreach ($entry in $Items) { [void]$set.Add($entry) }
    return , $set
}

# Environments whose content is not prose.
$verbatimEnvironments = New-StringSet @("verbatim", "verbatim*", "Verbatim", "lstlisting", "minted", "comment", "filecontents", "filecontents*")
$skippedEnvironments = New-StringSet @(
    "verbatim", "verbatim*", "Verbatim", "lstlisting", "minted", "comment", "filecontents", "filecontents*",
    "algorithmic", "tikzpicture", "tikzcd", "thebibliography",
    "equation", "equation*", "align", "align*", "alignat", "alignat*", "flalign", "flalign*",
    "gather", "gather*", "multline", "multline*", "eqnarray", "eqnarray*", "displaymath", "math"
)

# Commands whose argument is running text.
$unwrapCommands = New-StringSet @(
    "emph", "textbf", "textit", "textsc", "textsf", "texttt", "textrm", "textup", "textsl", "textmd",
    "textnormal", "underline", "mbox", "text", "caption", "title", "enquote"
)
$emphasisCommands = New-StringSet @("emph", "textbf", "textit", "textsc", "textsf", "texttt", "textsl", "underline")
# Headings are not counted as prose.
$headingCommands = New-StringSet @("part", "chapter", "section", "subsection", "subsubsection", "paragraph", "subparagraph")
# Commands without an argument that are not words.
$silentCommands = New-StringSet @(
    "item", "noindent", "indent", "par", "medskip", "smallskip", "bigskip", "centering", "raggedright",
    "maketitle", "tableofcontents", "qedhere", "qed", "newline", "linebreak", "pagebreak", "newpage",
    "clearpage", "hfill", "vfill", "quad", "qquad", "dots", "ldots", "cdots", "appendix", "small", "large",
    "Large", "LARGE", "huge", "Huge", "footnotesize", "scriptsize", "tiny", "normalsize", "bfseries",
    "itshape", "mdseries", "rmfamily", "sffamily", "ttfamily", "em", "bf", "it", "toprule", "midrule",
    "bottomrule", "hline", "relax", "protect", "linewidth", "textwidth", "columnwidth", "displaystyle",
    "sloppy", "fussy", "null", "break", "nobreak", "allowbreak", "nolinebreak", "leavevmode", "strut"
)

$rxComment = [regex]::new('(?<=(?:^|[^\\])(?:\\\\)*)%.*$', $rxNone)
$rxDocumentClass = [regex]::new('^\s*\\documentclass\b', $rxNone)
$rxBeginEnvironment = [regex]::new('\\begin\{([A-Za-z]+\*?)\}', $rxNone)
$rxBeginEnd = [regex]::new('\\(?:begin|end)\{[^{}]*\}(?:\s*\[[^\[\]]*\]|\s*\{(?:[^{}]|\{[^{}]*\})*\})*', $rxNone)
$rxItem = [regex]::new('\\item\b(?:\s*\[[^\[\]]*\])?', $rxNone)
$rxCommandWithArgument = [regex]::new('\\([A-Za-z]+)\*?(?:\s*\[[^\[\]{}]*\])*\{([^{}]*)\}', $rxNone)
$rxCommandNoArgument = [regex]::new('\\([A-Za-z]+)\*?', $rxNone)
$rxReferenceCommands = [regex]::new('\\(?:label|ref|eqref|pageref|cref|Cref|autoref|nameref|cite[A-Za-z]*|includegraphics|input|include|bibliography|bibliographystyle|url|href|usepackage|lstinline|verb)\*?(?:\s*\[[^\[\]]*\])*\{[^{}]*\}', $rxNone)
$rxAccent = [regex]::new('\\[`''"^~=.](?=\{?\p{L})', $rxNone)
$rxSpacingCommand = [regex]::new('\\[,;:! /]', $rxNone)
$rxDashes = [regex]::new('-{2,}', $rxNone)
$rxSpaces = [regex]::new('\s+', $rxNone)
$rxStartsBoundary = [regex]::new('^\\(?:begin|end|item|part|chapter|section|subsection|subsubsection|paragraph|subparagraph|caption|label|centering|includegraphics|maketitle|bibliography|bibliographystyle|medskip|smallskip|bigskip|noindent|title|author|date|input|include)\b', $rxNone)
$rxHeadingLine = [regex]::new('^\\(?:part|chapter|section|subsection|subsubsection|paragraph|subparagraph|caption)\b', $rxNone)
$rxBoldOnlyLine = [regex]::new('^(?:\\item\b(?:\s*\[[^\[\]]*\])?\s*)?\\(?:textbf|textit|emph|textsc)\{[^{}]*\}\s*[.:]?\s*$', $rxNone)
$rxDefinitionLine = [regex]::new('^\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand|DeclareMathOperator|def|let|newtheorem|theoremstyle|usepackage|RequirePackage|setlength|setcounter|newcounter|newenvironment|renewenvironment|newif|hypersetup|crefname|Crefname|addtolength|renewcommand)\b', $rxNone)
$rxRowBreak = [regex]::new('\\\\\s*(?:\[[^\[\]]*\])?\s*$', $rxNone)
$rxSentenceEnd = [regex]::new('[.!?][)''"\u2019\u201D\]]*$', $rxNone)

$rxWordTex = [regex]::new('[\p{L}\p{Nd}]+(?:[''\u2019\-][\p{L}\p{Nd}]+)*|\uE002', $rxNone)
$rxWordTxt = [regex]::new('\p{L}{2,}(?:[''\u2019\-]\p{L}+)*|\b[aAI]\b', $rxNone)
$rxHasLetter = [regex]::new('\p{L}{2,}|\uE002', $rxNone)
$rxSentenceBreak = [regex]::new('[.!?]+[)''"\u2019\u201D\]]*\s+(?=\uE003?[\p{Lu}\uE000\uE002])', $rxNone)
$rxTokenBeforeBreak = [regex]::new('([\p{L}.]+)$', $rxNone)
$abbreviations = New-StringSet @(
    "e.g", "i.e", "cf", "etc", "al", "vs", "resp", "approx", "ca", "fig", "figs", "eq", "eqs", "sec", "thm",
    "def", "alg", "tab", "no", "nos", "vol", "pp", "p", "ed", "eds", "prof", "dr", "mr", "mrs", "ms", "st",
    "jr", "sr", "w.l.o.g", "w.r.t", "rndr", "csc", "phd", "ph.d", "mgr", "bc", "ing", "doc", "wlog", "viz"
)

$rxDup = [regex]::new('\b(\p{L}+)\s+\1\b', $rxIgnoreCase)
$dupAllowed = New-StringSet @("that", "had", "log", "bla", "is")

$rxDoubleDollar = [regex]::new('\$\$', $rxNone)
$rxSpaceBeforeRef = [regex]::new('(\S+) +(\\(?:ref|eqref|pageref|cite|citep)\*?(?:\[[^\[\]]*\])*\{[^{}]*\})', $rxNone)
$rxAttachedCite = [regex]::new('[\p{L}\}]\\cite[a-z]*\*?(?:\[[^\[\]]*\])*\{[^{}]*\}', $rxNone)
$rxLowercaseRef = [regex]::new('\b(theorem|lemma|section|subsection|figure|definition|corollary|proposition|algorithm|table|claim|remark|appendix|chapter)(s?)(?:~|\s+)\\(?:ref|eqref|cref)\{', $rxNone)
$rxLabel = [regex]::new('\\label\{([^{}]*)\}', $rxNone)
$rxLabelName = [regex]::new('^[a-z0-9]+(?:-[a-z0-9]+)*$', $rxNone)
$rxEgIe = [regex]::new('(?<![\p{L}.])(?:e\.g|i\.e)\.(?!,)', $rxIgnoreCase)
$rxEgIeNoPeriod = [regex]::new('(?<![\p{L}.])(?:e\.g|i\.e)(?=[\s,~])', $rxIgnoreCase)
$rxEtAl = [regex]::new('\bet\.?\s+al\b(?!\.)|\bet\.\s*al\b\.?', $rxIgnoreCase)
$rxStraightQuote = [regex]::new('"[^"]{0,60}"?', $rxNone)
$rxMathAtStart = [regex]::new('^(?:\$(?!\$)|\\\()', $rxNone)

$rxTodoWords = [regex]::new('\b(?:TODO|FIXME|XXX)\b|\\fillin\b|\\todo\b', $rxNone)
$rxQuestionMarks = [regex]::new('\?\?+', $rxNone)

# Lines in Slovak or Czech are not checked against the English phrase list.
$rxSlovakLetters = [regex]::new('[\u00E1\u00E4\u010D\u010F\u00E9\u00ED\u013A\u013E\u0148\u00F3\u00F4\u0155\u0161\u0165\u00FA\u00FD\u017E\u00C1\u00C4\u010C\u010E\u00C9\u00CD\u0139\u013D\u0147\u00D3\u00D4\u0154\u0160\u0164\u00DA\u00DD\u017D\u011B\u0159\u016F\u011A\u0158\u016E]', $rxNone)
$rxSlovakWords = [regex]::new('\b(?:sa|je|pre|alebo|ako|ale|som|boli|bola|bolo|lebo|preto|medzi|v\u0161ak|ktor\p{L}+|\u017Ee|nie|aj|s\u00FA|se|pro|jako|nebo|aby|tedy)\b', $rxIgnoreCase)

$rxContraction = [regex]::new('\b(?:\p{L}+n[''\u2019]t|(?:it|that|there|here|what|let|who)[''\u2019]s|(?:we|you|they|i|he|she|it|that)[''\u2019](?:ll|re|ve|d)|i[''\u2019]m)\b', $rxIgnoreCase)
$contractionExpansions = @{
    "don't" = "do not"; "can't" = "cannot"; "isn't" = "is not"; "it's" = "it is"; "we'll" = "we will"
    "doesn't" = "does not"; "won't" = "will not"; "let's" = "let us"; "aren't" = "are not"
    "didn't" = "did not"; "wasn't" = "was not"; "weren't" = "were not"; "hasn't" = "has not"
    "haven't" = "have not"; "couldn't" = "could not"; "wouldn't" = "would not"; "shouldn't" = "should not"
    "that's" = "that is"; "there's" = "there is"; "we're" = "we are"; "we've" = "we have"; "i'm" = "I am"
}

$britishIse = '(?:optimi|formali|generali|minimi|maximi|characteri|reali|recogni|summari|parametri|parameteri|randomi|normali|initiali|synchroni|utili|visuali|organi|speciali|categori|lineari|discreti|penali|prioriti|standardi|symmetri|factori|locali|finali|stabili|emphasi|critici|hypothesi|diagonali|regulari|centrali|equali|vectori|paralleli|capitali|customi|authori|itemi|tokeni|saniti|rationali|harmoni|hybridi|ideali|legitimi|materiali|memori|memoi|neutrali|polari|quanti|rasteri|seriali|systemati|theori|contextuali|conceptuali|individuali|triviali|digiti|mobili|plurali)s(?:e|es|ed|ing|er|ers|ation|ations|able)'
$rxBritish = [regex]::new(
    '\b(?:(?<ise>' + $britishIse + ')' +
    '|(?<isation>(?!improvis)\p{L}{3,}isations?)' +
    '|(?<analyse>analys(?:e|ed|ing|er|ers))' +
    '|(?<our>(?:colou|neighbou|behaviou|favou|honou|flavou|labou|harbou|rigou|vigou|humou|rumou)r\p{L}*)' +
    '|(?<centre>cent(?:re|res|red))' +
    '|(?<re>(?:fib|met|calib)res?)' +
    '|(?<ll>(?:model|label|travel|cancel|signal|channel|level|fuel|tunnel|total|marshal|dial|pencil|counsel)l(?:ed|ing|er|ers))' +
    '|(?<misc>acknowledgements?|judgements?|artefacts?|whilst|amongst|fulfil|fulfilment|defence|offences?' +
    '|licences?|licenced|licencing|catalogues?|catalogued|cataloguing|programmes?|analogues?|grey|learnt' +
    '|practis(?:e|es|ed|ing)|ageing|enrolments?|scepti(?:c|cs|cal|cally|cism)))\b',
    $rxIgnoreCase)
$britishMisc = @{
    "acknowledgement" = "acknowledgment"; "acknowledgements" = "acknowledgments"; "judgement" = "judgment"
    "judgements" = "judgments"; "artefact" = "artifact"; "artefacts" = "artifacts"; "whilst" = "while"
    "amongst" = "among"; "fulfil" = "fulfill"; "fulfilment" = "fulfillment"; "defence" = "defense"
    "offence" = "offense"; "offences" = "offenses"
    "licence" = "license"; "licences" = "licenses"; "licenced" = "licensed"; "licencing" = "licensing"
    "catalogue" = "catalog"; "catalogues" = "catalogs"; "catalogued" = "cataloged"; "cataloguing" = "cataloging"
    "programme" = "program"; "programmes" = "programs"; "analogue" = "analog"; "analogues" = "analogs"
    "grey" = "gray"; "learnt" = "learned"; "ageing" = "aging"; "enrolment" = "enrollment"; "enrolments" = "enrollments"
    "practise" = "practice"; "practises" = "practices"; "practised" = "practiced"; "practising" = "practicing"
    "sceptic" = "skeptic"; "sceptics" = "skeptics"; "sceptical" = "skeptical"; "sceptically" = "skeptically"
    "scepticism" = "skepticism"
}

function Get-AmericanForm($Match) {
    $value = $Match.Value
    if ($Match.Groups["ise"].Success) { return ($value -replace '(?i)is(e|es|ed|ing|er|ers|ation|ations|able)$', 'iz$1') }
    if ($Match.Groups["isation"].Success) { return ($value -replace '(?i)isation', 'ization') }
    if ($Match.Groups["analyse"].Success) { return ($value -replace '(?i)analys', 'analyz') }
    if ($Match.Groups["our"].Success) { return ($value -replace '(?i)our', 'or') }
    if ($Match.Groups["centre"].Success) {
        $lower = $value.ToLowerInvariant()
        if ($lower -eq "centre") { return "center" }
        if ($lower -eq "centres") { return "centers" }
        return "centered"
    }
    if ($Match.Groups["re"].Success) { return ($value -replace '(?i)re(s?)$', 'er$1') }
    if ($Match.Groups["ll"].Success) { return ($value -replace '(?i)ll', 'l') }
    $key = $value.ToLowerInvariant()
    if ($britishMisc.ContainsKey($key)) { return $britishMisc[$key] }
    return "American form"
}

# ---------------------------------------------------------------------------
# Phrase list
# ---------------------------------------------------------------------------

$phraseRules = New-Object System.Collections.Generic.List[object]
$phraseListNote = ""
if (Test-Path -LiteralPath $PhraseList -PathType Leaf) {
    $phraseLines = [System.IO.File]::ReadAllLines((Get-Item -LiteralPath $PhraseList).FullName, $utf8)
    for ($index = 0; $index -lt $phraseLines.Length; $index++) {
        $phraseLine = $phraseLines[$index]
        if ($phraseLine.Trim() -eq "" -or $phraseLine.TrimStart().StartsWith("#")) { continue }
        $fields = $phraseLine.Split([char[]]@([char]9), 3)
        if ($fields.Length -lt 2 -or $fields[0].Trim() -eq "" -or $fields[1].Trim() -eq "") {
            Write-Warning "Phrase list, line $($index + 1): expected category<TAB>regex<TAB>suggestion; line skipped."
            continue
        }
        $suggestion = ""
        if ($fields.Length -ge 3) { $suggestion = $fields[2].Trim() }
        try {
            $compiled = [regex]::new($fields[1].Trim(), $rxIgnoreCase)
        }
        catch {
            Write-Warning "Phrase list, line $($index + 1): invalid regex '$($fields[1].Trim())'; line skipped."
            continue
        }
        $phraseRules.Add([pscustomobject]@{
                Category   = $fields[0].Trim().ToLowerInvariant()
                Regex      = $compiled
                Suggestion = $suggestion
            })
    }
    $phraseListNote = "$PhraseList ($($phraseRules.Count) rules)"
}
else {
    $phraseListNote = "missing ($PhraseList) - built-in checks only"
    Write-Warning "Phrase list does not exist: $PhraseList. Continuing with the built-in checks only."
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

$script:findings = New-Object System.Collections.Generic.List[object]
$script:currentFile = ""
$script:mathState = ""
$script:isTxt = $false
$script:skippedLines = 0

function Get-DisplayPath([string]$FullName) {
    $root = $workspace.TrimEnd('\') + '\'
    if ($FullName.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $FullName.Substring($root.Length).Replace('\', '/')
    }
    return $FullName.Replace('\', '/')
}

function Add-Finding([int]$Line, [int]$Column, [string]$Category, [string]$Text, [string]$Suggestion) {
    $clean = $rxSpaces.Replace($Text.Replace($EMPH, ''), ' ').Trim()
    if ($clean.Length -gt 90) { $clean = $clean.Substring(0, 87) + "..." }
    $script:findings.Add([pscustomobject]@{
            File       = $script:currentFile
            Line       = $Line
            Column     = $Column
            Category   = $Category
            Text       = $clean
            Suggestion = $Suggestion
        })
}

# True for a line that is mostly Slovak or Czech: the English phrase list does not apply to it.
function Test-NonEnglish([string]$Text) {
    if ($rxSlovakLetters.Matches($Text).Count -ge 3) { return $true }
    if ($rxSlovakWords.Matches($Text).Count -ge 2) { return $true }
    return $false
}

# Replaces math with a placeholder. The state (open math) is carried across lines in
# $script:mathState: display = \[, dollars = $$, inline = $, paren = \(.
function Convert-MathToPlaceholder([string]$Text) {
    $builder = New-Object System.Text.StringBuilder
    $position = 0
    $length = $Text.Length
    while ($position -lt $length) {
        if ($script:mathState -ne "") {
            $closing = '$'
            if ($script:mathState -eq "display") { $closing = '\]' }
            elseif ($script:mathState -eq "dollars") { $closing = '$$' }
            elseif ($script:mathState -eq "paren") { $closing = '\)' }
            $found = $Text.IndexOf($closing, $position, $ordinal)
            if ($found -lt 0) { return $builder.ToString() }
            $position = $found + $closing.Length
            $script:mathState = ""
            continue
        }
        $openDisplay = $Text.IndexOf('\[', $position, $ordinal)
        $openParen = $Text.IndexOf('\(', $position, $ordinal)
        $openDollar = $Text.IndexOf('$', $position, $ordinal)
        $next = -1
        foreach ($candidatePosition in @($openDisplay, $openParen, $openDollar)) {
            if ($candidatePosition -ge 0 -and ($next -lt 0 -or $candidatePosition -lt $next)) { $next = $candidatePosition }
        }
        if ($next -lt 0) {
            [void]$builder.Append($Text.Substring($position))
            break
        }
        [void]$builder.Append($Text.Substring($position, $next - $position))
        if ($next -eq $openDollar) {
            if ($next + 1 -lt $length -and $Text[$next + 1] -eq '$') {
                $script:mathState = "dollars"
                [void]$builder.Append($DISP)
                $position = $next + 2
            }
            else {
                $script:mathState = "inline"
                [void]$builder.Append($MATH)
                $position = $next + 1
            }
        }
        elseif ($next -eq $openDisplay) {
            $script:mathState = "display"
            [void]$builder.Append($DISP)
            $position = $next + 2
        }
        else {
            $script:mathState = "paren"
            [void]$builder.Append($MATH)
            $position = $next + 2
        }
    }
    return $builder.ToString()
}

$commandEvaluator = [System.Text.RegularExpressions.MatchEvaluator] {
    param($match)
    $name = $match.Groups[1].Value
    $argument = $match.Groups[2].Value
    if ($script:emphasisCommands.Contains($name)) { return ($script:EMPH + $argument) }
    if ($script:unwrapCommands.Contains($name)) { return $argument }
    if ($script:headingCommands.Contains($name)) { return " " }
    if ($argument.Trim() -eq "") { return $script:MACRO }
    return " "
}
$noArgumentEvaluator = [System.Text.RegularExpressions.MatchEvaluator] {
    param($match)
    if ($script:silentCommands.Contains($match.Groups[1].Value)) { return " " }
    return $script:MACRO
}

# Turns a line with math already masked into plain sentence text.
function Convert-ToProse([string]$Masked) {
    $text = $rxBeginEnd.Replace($Masked, ' ')
    $text = $rxItem.Replace($text, ' ')
    for ($pass = 0; $pass -lt 12; $pass++) {
        $replaced = $rxCommandWithArgument.Replace($text, $commandEvaluator)
        if ($replaced -eq $text) { break }
        $text = $replaced
    }
    $text = $rxAccent.Replace($text, '')
    $text = $text.Replace('\-', '')
    $text = $rxSpacingCommand.Replace($text, ' ')
    $text = $rxCommandNoArgument.Replace($text, $noArgumentEvaluator)
    $text = $text.Replace('~', ' ')
    $text = $rxDashes.Replace($text, ' ')
    $text = $text -replace '[{}&\\]', ' '
    return $rxSpaces.Replace($text, ' ').Trim()
}

# --- sentence assembly --------------------------------------------------------

$script:unitBuilder = New-Object System.Text.StringBuilder
$script:unitOffsets = New-Object System.Collections.Generic.List[int]
$script:unitLines = New-Object System.Collections.Generic.List[int]
$script:statWords = 0
$script:statSentences = 0
$script:statSentenceWords = 0

function Get-UnitLine([int]$Offset) {
    $line = $script:unitLines[0]
    for ($segment = 0; $segment -lt $script:unitOffsets.Count; $segment++) {
        if ($script:unitOffsets[$segment] -le $Offset) { $line = $script:unitLines[$segment] } else { break }
    }
    return $line
}

function Test-UnitOpen {
    # True if the buffer holds an unfinished sentence.
    if ($script:unitBuilder.Length -eq 0) { return $false }
    return (-not $rxSentenceEnd.IsMatch($script:unitBuilder.ToString().TrimEnd()))
}

function Complete-Unit {
    if ($script:unitBuilder.Length -eq 0) { return }
    $text = $script:unitBuilder.ToString()

    foreach ($dup in $rxDup.Matches($text)) {
        $word = $dup.Groups[1].Value.ToLowerInvariant()
        if ($dupAllowed.Contains($word)) { continue }
        if ($script:isTxt -and $word.Length -lt 2) { continue }
        Add-Finding (Get-UnitLine $dup.Index) 0 "dup" $dup.Value "delete the repeated word"
    }

    # Sentence boundaries: a period, a space and a capital letter (or math); abbreviations do not end a sentence.
    $starts = New-Object System.Collections.Generic.List[int]
    $starts.Add(0)
    foreach ($break in $rxSentenceBreak.Matches($text)) {
        $before = $rxTokenBeforeBreak.Match($text.Substring(0, $break.Index))
        if ($before.Success) {
            $token = $before.Groups[1].Value.TrimEnd('.').ToLowerInvariant()
            if ($abbreviations.Contains($token)) { continue }
            # initials (M. Loebl); in .txt single letters are variables, so the sentence is split there
            if (-not $script:isTxt -and $token.Length -eq 1 -and $before.Groups[1].Value -cmatch '^\p{Lu}$') { continue }
        }
        $starts.Add($break.Index + $break.Length)
    }
    for ($sentence = 0; $sentence -lt $starts.Count; $sentence++) {
        $from = $starts[$sentence]
        $to = $text.Length
        if ($sentence + 1 -lt $starts.Count) { $to = $starts[$sentence + 1] }
        $piece = $text.Substring($from, $to - $from)
        if ($script:isTxt) { $count = $rxWordTxt.Matches($piece).Count } else { $count = $rxWordTex.Matches($piece).Count }
        if ($count -eq 0) { continue }
        $script:statWords += $count
        if ($count -ge 3) {
            # spans shorter than 3 words (a run-in head such as "Formally:", a list label) are not sentences
            $script:statSentences++
            $script:statSentenceWords += $count
        }
        if ($count -gt $MaxWords) {
            $shown = $piece.Replace($EMPH, '').Replace($MATH, '$..$').Replace($MACRO, '\..').Trim()
            $opening = ($shown -split '\s+' | Select-Object -First 9) -join ' '
            Add-Finding (Get-UnitLine $from) 0 "long" "$opening ..." "$count words (limit $MaxWords): split or shorten"
        }
    }
    [void]$script:unitBuilder.Clear()
    $script:unitOffsets.Clear()
    $script:unitLines.Clear()
}

function Add-UnitText([string]$Text, [int]$Line) {
    if ($Text -eq "") { return }
    if ($script:unitBuilder.Length -gt 0) {
        $current = $script:unitBuilder.ToString()
        if ($script:isTxt -and $current -cmatch '\p{Ll}-$' -and $Text -cmatch '^\p{Ll}') {
            # a word hyphenated at the end of a line (pdftotext)
            $script:unitBuilder.Length = $script:unitBuilder.Length - 1
        }
        else {
            [void]$script:unitBuilder.Append(' ')
        }
    }
    $script:unitOffsets.Add($script:unitBuilder.Length)
    $script:unitLines.Add($Line)
    [void]$script:unitBuilder.Append($Text)
}

# --- checks on one line -------------------------------------------------------

# In pdftotext output a bare capital A or a single-letter variable is not an article.
function Test-SuppressedHit([string]$Category, [string]$Value) {
    if (-not $script:isTxt -or $Category -ne "grammar") { return $false }
    if ($Value -cmatch '^A\s') { return $true }
    if ($Value -match '^(?i:a)\s+(?i:and|or|is|are|in|if|to|of|as|at|on|be|then|with|such|we)\b') { return $true }
    return $false
}

function Get-RuleHits([string]$Text) {
    $hits = New-Object System.Collections.Generic.List[object]
    foreach ($rule in $phraseRules) {
        foreach ($match in $rule.Regex.Matches($Text)) {
            if ($match.Length -eq 0) { continue }
            if (Test-SuppressedHit $rule.Category $match.Value) { continue }
            $hits.Add([pscustomobject]@{ Rule = $rule; Start = $match.Index; End = ($match.Index + $match.Length); Value = $match.Value })
        }
    }
    return , $hits
}

# Of several overlapping hits keep the longest one (the first rule in the file wins a tie).
function Select-LongestHits($Hits) {
    if ($Hits.Count -le 1) { return , $Hits }
    $ordered = @($Hits | Sort-Object @{ Expression = { $_.End - $_.Start }; Descending = $true }, Start)
    $kept = New-Object System.Collections.Generic.List[object]
    foreach ($hit in $ordered) {
        $overlaps = $false
        foreach ($other in $kept) {
            if ($hit.Start -lt $other.End -and $other.Start -lt $hit.End) { $overlaps = $true; break }
        }
        if (-not $overlaps) { $kept.Add($hit) }
    }
    return , $kept
}

function Format-HitText([string]$Value) {
    # a hit of a sentence-start rule begins with the previous sentence's period
    return ($Value -replace '^[.!?:\s]+', '').Trim()
}

# Phrase checks run on blocks: consecutive prose lines of one paragraph are joined with a space, so that a phrase
# broken by a line end is found and "^" means the start of a paragraph. A hit is reported on the line where it starts.
$script:blockText = New-Object System.Text.StringBuilder
$script:blockOffsets = New-Object System.Collections.Generic.List[int]
$script:blockLines = New-Object System.Collections.Generic.List[int]

function Complete-PhraseBlock {
    if ($script:blockText.Length -eq 0) { return }
    $text = $script:blockText.ToString()
    foreach ($hit in (Select-LongestHits (Get-RuleHits $text))) {
        $shown = Format-HitText $hit.Value
        $position = $hit.Start + ($hit.Value.Length - ($hit.Value -replace '^[.!?:\s]+', '').Length)
        $segment = 0
        for ($i = 0; $i -lt $script:blockOffsets.Count; $i++) {
            if ($script:blockOffsets[$i] -le $position) { $segment = $i } else { break }
        }
        Add-Finding $script:blockLines[$segment] ($position - $script:blockOffsets[$segment]) $hit.Rule.Category $shown $hit.Rule.Suggestion
    }
    [void]$script:blockText.Clear()
    $script:blockOffsets.Clear()
    $script:blockLines.Clear()
}

# Ends the block only if it ends a sentence (a formula line in .txt does not end the sentence around it).
function Complete-PhraseBlockAtSentenceEnd {
    $length = $script:blockText.Length
    if ($length -eq 0) { return }
    $last = $script:blockText[$length - 1]
    if ($last -eq '.' -or $last -eq '!' -or $last -eq '?' -or $last -eq ':') { Complete-PhraseBlock }
}

function Add-PhraseLine([string]$Text, [int]$Line) {
    if ($phraseRules.Count -eq 0) { return }
    if (Test-NonEnglish $Text) {
        $script:skippedLines++
        Complete-PhraseBlock
        return
    }
    $piece = $Text.Trim()
    if ($piece -eq "") { return }
    $length = $script:blockText.Length
    if ($length -gt 0) {
        if ($script:isTxt -and $length -ge 2 -and $script:blockText[$length - 1] -eq '-' -and [char]::IsLower($script:blockText[$length - 2]) -and [char]::IsLower($piece[0])) {
            $script:blockText.Length = $length - 1     # a word hyphenated at the end of a line (pdftotext)
        }
        else {
            [void]$script:blockText.Append(' ')
        }
    }
    $script:blockOffsets.Add($script:blockText.Length)
    $script:blockLines.Add($Line)
    [void]$script:blockText.Append($piece)
}

function Test-Wording([string]$Text, [int]$Line) {
    foreach ($hit in $rxContraction.Matches($Text)) {
        $key = $hit.Value.ToLowerInvariant().Replace([string][char]0x2019, "'")
        $expansion = "spell out the contraction"
        if ($contractionExpansions.ContainsKey($key)) { $expansion = $contractionExpansions[$key] }
        Add-Finding $Line $hit.Index "contraction" $hit.Value $expansion
    }
    foreach ($hit in $rxBritish.Matches($Text)) {
        Add-Finding $Line $hit.Index "spelling" $hit.Value (Get-AmericanForm $hit)
    }
}

function Test-Todo([string]$RawLine, [string]$WithoutComment, [int]$Line) {
    foreach ($hit in $rxTodoWords.Matches($RawLine)) {
        Add-Finding $Line $hit.Index "todo" $hit.Value "finish or remove"
    }
    foreach ($hit in $rxQuestionMarks.Matches($WithoutComment)) {
        Add-Finding $Line $hit.Index "todo" $hit.Value "unresolved reference or note"
    }
}

function Test-Labels([string]$WithoutComment, [int]$Line) {
    foreach ($hit in $rxLabel.Matches($WithoutComment)) {
        $name = $hit.Groups[1].Value
        $separator = $name.IndexOf(':')
        $prefix = ""
        $rest = $name
        if ($separator -gt 0) { $prefix = $name.Substring(0, $separator); $rest = $name.Substring($separator + 1) }
        if ($labelPrefixes -cnotcontains $prefix) {
            Add-Finding $Line $hit.Index "latex" $hit.Value ("label prefix must be one of: " + ($labelPrefixes -join ", "))
        }
        elseif (-not $rxLabelName.IsMatch($rest)) {
            Add-Finding $Line $hit.Index "latex" $hit.Value "label name: lowercase words with hyphens"
        }
    }
}

function Test-LatexLine([string]$WithoutComment, [int]$Line) {
    foreach ($hit in $rxSpaceBeforeRef.Matches($WithoutComment)) {
        $before = $hit.Groups[1].Value
        $last = $before[$before.Length - 1]
        if ($last -eq '(' -or $last -eq '~' -or $last -eq '[' -or $last -eq '{') { continue }
        Add-Finding $Line $hit.Index "latex" $hit.Value "use ~ before the reference, not a space"
    }
    foreach ($hit in $rxAttachedCite.Matches($WithoutComment)) {
        Add-Finding $Line $hit.Index "latex" $hit.Value "missing ~ before \cite"
    }
    foreach ($hit in $rxLowercaseRef.Matches($WithoutComment)) {
        $name = $hit.Groups[1].Value
        $capital = $name.Substring(0, 1).ToUpperInvariant() + $name.Substring(1) + $hit.Groups[2].Value
        Add-Finding $Line $hit.Index "latex" ($hit.Value.TrimEnd('{')) "capitalize: $capital"
    }
    foreach ($hit in $rxEgIe.Matches($WithoutComment)) {
        Add-Finding $Line $hit.Index "latex" $hit.Value ($hit.Value + ",")
    }
    foreach ($hit in $rxEgIeNoPeriod.Matches($WithoutComment)) {
        Add-Finding $Line $hit.Index "latex" $hit.Value ($hit.Value + ".,")
    }
    foreach ($hit in $rxEtAl.Matches($WithoutComment)) {
        Add-Finding $Line $hit.Index "latex" $hit.Value "et al."
    }
}

# ---------------------------------------------------------------------------
# .tex files
# ---------------------------------------------------------------------------

function Invoke-TexCheck([string[]]$Lines) {
    $inPreamble = $false
    foreach ($candidateLine in $Lines) {
        if ($rxDocumentClass.IsMatch($candidateLine)) { $inPreamble = $true; break }
    }
    $skipEnvironment = ""
    $script:mathState = ""

    for ($index = 0; $index -lt $Lines.Length; $index++) {
        $raw = $Lines[$index]
        $line = $index + 1

        if ($inPreamble) {
            if ($raw.Contains('\begin{document}')) { $inPreamble = $false }
            continue
        }

        if ($skipEnvironment -ne "") {
            if ($verbatimEnvironments.Contains($skipEnvironment)) {
                if ($raw.Contains("\end{$skipEnvironment}")) { $skipEnvironment = "" }
                continue
            }
            $inside = $rxComment.Replace($raw, '')
            Test-Labels $inside $line
            Test-Todo $raw "" $line
            if ($inside.Contains("\end{$skipEnvironment}")) { $skipEnvironment = "" }
            continue
        }

        $withoutComment = $rxComment.Replace($raw, '')
        $trimmed = $withoutComment.Trim()

        if ($trimmed -eq "") {
            if ($raw.Trim() -eq "") {
                # a blank line ends the paragraph; inline math does not continue across it
                Complete-Unit
                Complete-PhraseBlock
                if ($script:mathState -eq "inline" -or $script:mathState -eq "paren") { $script:mathState = "" }
            }
            else {
                Test-Todo $raw "" $line
            }
            continue
        }

        if ($trimmed.Contains('\end{document}')) { break }

        if ($rxDefinitionLine.IsMatch($trimmed)) {
            # macro definitions and package lines are not prose
            Test-Todo $raw "" $line
            Complete-Unit
            Complete-PhraseBlock
            continue
        }

        $skipHere = ""
        foreach ($begin in $rxBeginEnvironment.Matches($withoutComment)) {
            if ($skippedEnvironments.Contains($begin.Groups[1].Value)) { $skipHere = $begin.Groups[1].Value; break }
        }
        if ($skipHere -ne "") {
            Complete-Unit
            Complete-PhraseBlock
            if (-not $verbatimEnvironments.Contains($skipHere)) {
                Test-Labels $withoutComment $line
                Test-Todo $raw "" $line
            }
            if (-not $withoutComment.Contains("\end{$skipHere}")) { $skipEnvironment = $skipHere }
            continue
        }

        $mathOpenAtStart = ($script:mathState -ne "")
        $normalized = $withoutComment.Replace('\\', '  ').Replace('\$', '  ').Replace('\%', '  ').Replace('\&', '  ').Replace('\#', '  ').Replace('\_', '  ')
        $masked = Convert-MathToPlaceholder $normalized

        Test-Labels $withoutComment $line
        $plainDollars = $withoutComment.Replace('\$', '  ')
        if ($rxDoubleDollar.IsMatch($plainDollars)) {
            Add-Finding $line $plainDollars.IndexOf('$$') "latex" '$$' 'use \[ ... \]'
        }

        $visible = $masked.Replace($MATH, ' ').Replace($DISP, ' ')
        if (-not $rxHasLetter.IsMatch($rxReferenceCommands.Replace($rxBeginEnd.Replace($visible, ' '), ' '))) {
            # the line is all math, \begin/\end or references only: no prose
            Test-Todo $raw "" $line
            if ($rxStartsBoundary.IsMatch($trimmed) -or $masked.Contains($DISP) -or $mathOpenAtStart) {
                Complete-Unit
                Complete-PhraseBlock
            }
            continue
        }

        Test-Todo $raw $visible $line
        Test-LatexLine $withoutComment $line

        $startsBoundary = $rxStartsBoundary.IsMatch($trimmed)
        if ($startsBoundary) { Complete-PhraseBlock }
        Add-PhraseLine $withoutComment $line

        $checkText = $rxReferenceCommands.Replace($rxBeginEnd.Replace($masked, ' '), ' ')
        Test-Wording $checkText $line
        $quoteText = $rxAccent.Replace($checkText, '')
        $quote = $rxStraightQuote.Match($quoteText)
        if ($quote.Success) {
            Add-Finding $line $quote.Index "latex" $quote.Value 'straight quotes: use \enquote{...} (csquotes)'
        }

        if ($startsBoundary) { Complete-Unit }

        $isHeading = ($rxHeadingLine.IsMatch($trimmed) -or $rxBoldOnlyLine.IsMatch($trimmed))
        $prose = Convert-ToProse $masked

        if (-not $mathOpenAtStart -and $rxMathAtStart.IsMatch($trimmed) -and -not (Test-UnitOpen)) {
            $opening = ($trimmed -split '\s+' | Select-Object -First 4) -join ' '
            Add-Finding $line 0 "latex" "$opening ..." "do not start a sentence with a symbol; start with a word"
        }

        if ($rxBoldOnlyLine.IsMatch($trimmed)) {
            # a stand-alone bold head (Reduction., Case ...) is not a sentence
            Complete-Unit
            Complete-PhraseBlock
            continue
        }

        $parts = $prose.Split([char[]]$DISP.ToCharArray())
        for ($part = 0; $part -lt $parts.Length; $part++) {
            if ($part -gt 0) { Complete-Unit }
            $piece = $parts[$part].Trim()
            if ($piece -eq "") { continue }
            if ((-not (Test-UnitOpen)) -and $script:unitBuilder.Length -gt 0) { Complete-Unit }
            Add-UnitText $piece $line
        }

        if ($isHeading -or $rxRowBreak.IsMatch($trimmed)) {
            Complete-Unit
            Complete-PhraseBlock
        }
    }
    Complete-Unit
    Complete-PhraseBlock
}

# ---------------------------------------------------------------------------
# .txt files (for example pdftotext output)
# ---------------------------------------------------------------------------

$rxTxtPageNumber = [regex]::new('^\d{1,4}$', $rxNone)
$rxTxtDottedLine = [regex]::new('(?:\.\s){4,}', $rxNone)
$rxTxtCodeLine = [regex]::new('^\d+:\s', $rxNone)
$rxTxtHeading = [regex]::new('^(?:\d+(?:\.\d+)*|[A-Z])\s+\p{Lu}[^.!?]*$', $rxNone)
$rxTxtBullet = [regex]::new('^[\u2022\u2013\u2014*-]\s', $rxNone)
$rxTxtStartsNew = [regex]::new('^(?:\p{Lu}|\d|[\u2022\u2013\u2014*(-])', $rxNone)
$rxTxtEndsBlock = [regex]::new('[.!?:][)''"\u2019\u201D\]]*$', $rxNone)
$rxLetters = [regex]::new('\p{L}', $rxNone)
$rxNonSpace = [regex]::new('\S', $rxNone)

function Invoke-TxtCheck([string[]]$Lines) {
    $blankPending = $false

    for ($index = 0; $index -lt $Lines.Length; $index++) {
        $raw = $Lines[$index]
        $line = $index + 1
        $trimmed = $raw.Trim()

        if ($trimmed -eq "") { $blankPending = $true; continue }
        Test-Todo $raw $raw $line

        if ($raw.Contains([string][char]12)) {     # new page
            Complete-Unit
            Complete-PhraseBlock
        }
        $nonSpace = $rxNonSpace.Matches($trimmed).Count
        $letters = $rxLetters.Matches($trimmed).Count
        $indent = $raw.Length - $raw.TrimStart().Length
        $words = $rxWordTxt.Matches($trimmed).Count
        $isNoise = $rxTxtPageNumber.IsMatch($trimmed) -or $rxTxtDottedLine.IsMatch($trimmed) -or $rxTxtCodeLine.IsMatch($trimmed)
        if (-not $isNoise -and ($letters -lt 0.6 * $nonSpace)) { $isNoise = $true }                  # formula
        if (-not $isNoise -and $indent -ge 12 -and $words -le 8) { $isNoise = $true }              # centered formula or caption
        if ($isNoise) {
            Complete-PhraseBlockAtSentenceEnd
            $blankPending = $true
            continue
        }

        Test-Wording $trimmed $line

        $isHeading = ($rxTxtHeading.IsMatch($trimmed) -and $words -le 12)
        if ($isHeading -or $rxTxtBullet.IsMatch($trimmed)) {
            Complete-Unit
            Complete-PhraseBlock
        }
        elseif ($blankPending) {
            Complete-PhraseBlockAtSentenceEnd
            if ($script:unitBuilder.Length -gt 0) {
                $current = $script:unitBuilder.ToString().TrimEnd()
                if ($rxTxtEndsBlock.IsMatch($current) -or $rxTxtStartsNew.IsMatch($trimmed)) { Complete-Unit }
            }
        }
        $blankPending = $false

        Add-PhraseLine $trimmed $line
        if ($isHeading) {
            Complete-PhraseBlock
            continue
        }
        Add-UnitText ($rxSpaces.Replace($trimmed, ' ')) $line
    }
    Complete-Unit
    Complete-PhraseBlock
}

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

$fileStats = New-Object System.Collections.Generic.List[object]

foreach ($fullName in $files) {
    $script:currentFile = Get-DisplayPath $fullName
    $script:isTxt = ([System.IO.Path]::GetExtension($fullName) -eq ".txt")
    $script:statWords = 0
    $script:statSentences = 0
    $script:statSentenceWords = 0
    $firstFinding = $script:findings.Count

    try {
        $content = [System.IO.File]::ReadAllLines($fullName, $utf8)
    }
    catch {
        Write-Warning "Cannot read the file: $fullName ($($_.Exception.Message))"
        continue
    }

    if ($script:isTxt) { Invoke-TxtCheck $content } else { Invoke-TexCheck $content }

    $counts = @{}
    for ($position = $firstFinding; $position -lt $script:findings.Count; $position++) {
        $category = $script:findings[$position].Category
        if ($counts.ContainsKey($category)) { $counts[$category]++ } else { $counts[$category] = 1 }
    }
    $average = 0.0
    if ($script:statSentences -gt 0) { $average = [math]::Round($script:statSentenceWords / $script:statSentences, 1) }
    $fileStats.Add([pscustomobject]@{
            File          = $script:currentFile
            Words         = $script:statWords
            Sentences     = $script:statSentences
            SentenceWords = $script:statSentenceWords
            Average       = $average
            Counts        = $counts
            Total         = ($script:findings.Count - $firstFinding)
        })
}

# --- findings -----------------------------------------------------------------

if (-not $Summary) {
    $order = @{}
    for ($position = 0; $position -lt $fileStats.Count; $position++) { $order[$fileStats[$position].File] = $position }
    $sorted = $script:findings | Sort-Object @{ Expression = { $order[$_.File] } }, Line, Column, Category
    foreach ($finding in $sorted) {
        $text = "{0}:{1}: [{2}] ""{3}""" -f $finding.File, $finding.Line, $finding.Category, $finding.Text
        if ($finding.Suggestion -ne "") { $text += " -> " + $finding.Suggestion }
        Write-Output $text
    }
    if ($script:findings.Count -gt 0) { Write-Output "" }
}

# --- summary ------------------------------------------------------------------

# Columns: built-in categories, then phrase-list categories, then any other category found; empty ones are omitted.
$candidateCategories = New-Object System.Collections.Generic.List[string]
foreach ($category in $builtinCategories) { $candidateCategories.Add($category) }
foreach ($category in $phraseCategories) { if (-not $candidateCategories.Contains($category)) { $candidateCategories.Add($category) } }
foreach ($finding in $script:findings) {
    if (-not $candidateCategories.Contains($finding.Category)) { $candidateCategories.Add($finding.Category) }
}
$categories = New-Object System.Collections.Generic.List[string]
foreach ($category in $candidateCategories) {
    foreach ($finding in $script:findings) {
        if ($finding.Category -eq $category) { $categories.Add($category); break }
    }
}

$nameWidth = 5
foreach ($stat in $fileStats) { if ($stat.File.Length -gt $nameWidth) { $nameWidth = $stat.File.Length } }

function Format-Row([string]$Name, [string]$Words, [string]$Sentences, [string]$Average, [string[]]$Cells, [string]$Total) {
    $row = $Name.PadRight($nameWidth) + "  " + $Words.PadLeft(6) + "  " + $Sentences.PadLeft(5) + "  " + $Average.PadLeft(6)
    for ($column = 0; $column -lt $categories.Count; $column++) {
        $width = [math]::Max($categories[$column].Length, 4)
        $row += "  " + $Cells[$column].PadLeft($width)
    }
    return $row + "  " + $Total.PadLeft(5)
}

Write-Output "Phrase list: $phraseListNote"
Write-Output "Sentence limit: $MaxWords words. Words and sentences are approximate (commands, math and comments are not counted)."
if ($script:skippedLines -gt 0) {
    Write-Output "Skipped by the phrase checks as non-English: $($script:skippedLines) lines."
}
Write-Output ""
Write-Output (Format-Row "File" "words" "sent." "mean" $categories.ToArray() "total")

$totalWords = 0
$totalSentences = 0
$totalSentenceWords = 0
$totalCounts = @{}
foreach ($stat in $fileStats) {
    $cells = New-Object System.Collections.Generic.List[string]
    foreach ($category in $categories) {
        $value = 0
        if ($stat.Counts.ContainsKey($category)) { $value = $stat.Counts[$category] }
        $cells.Add([string]$value)
        if ($totalCounts.ContainsKey($category)) { $totalCounts[$category] += $value } else { $totalCounts[$category] = $value }
    }
    $totalWords += $stat.Words
    $totalSentences += $stat.Sentences
    $totalSentenceWords += $stat.SentenceWords
    Write-Output (Format-Row $stat.File ([string]$stat.Words) ([string]$stat.Sentences) ($stat.Average.ToString("0.0", [System.Globalization.CultureInfo]::InvariantCulture)) $cells.ToArray() ([string]$stat.Total))
}
if ($fileStats.Count -ne 1) {
    $cells = New-Object System.Collections.Generic.List[string]
    foreach ($category in $categories) {
        $value = 0
        if ($totalCounts.ContainsKey($category)) { $value = $totalCounts[$category] }
        $cells.Add([string]$value)
    }
    $totalAverage = 0.0
    if ($totalSentences -gt 0) { $totalAverage = [math]::Round($totalSentenceWords / $totalSentences, 1) }
    Write-Output (Format-Row "TOTAL" ([string]$totalWords) ([string]$totalSentences) ($totalAverage.ToString("0.0", [System.Globalization.CultureInfo]::InvariantCulture)) $cells.ToArray() ([string]$script:findings.Count))
}

if ($null -ne $previousOutputEncoding) {
    try { [Console]::OutputEncoding = $previousOutputEncoding } catch { }
}
exit 0
