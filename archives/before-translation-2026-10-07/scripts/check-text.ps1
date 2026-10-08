<#
.SYNOPSIS
    Skontroluje styl a hygienu textu v LaTeX zdrojoch. Nic nemeni, len vypise nalezy.

.DESCRIPTION
    Prejde .tex subory projektu (alebo zadany subor ci priecinok) a hlasi:
      - frazy zo zoznamu fraz (kategorie filler, wordy, hype, hedge, meta, ai-tic, grammar, spelling),
      - [long]        vetu dlhsiu nez MaxWords slov,
      - [dup]         to iste slovo dvakrat za sebou ("the the"),
      - [latex]       $$; medzeru namiesto ~ pred \ref, \eqref, \cite; male pismeno pred odkazom
                      (theorem~\ref); vetu zacinajucu matematikou; rovne uvodzovky "; \label
                      s neznamym prefixom; e.g./i.e. bez ciarky; et al bez bodky,
      - [todo]        TODO, FIXME, XXX, \fillin, ??,
      - [contraction] don't, can't, it's ...,
      - [spelling]    britske tvary v americkom texte (optimise, colour, modelling ...).

    Preskakuje preambulu (vsetko pred \begin{document} v subore s \documentclass), prostredia
    verbatim, lstlisting, algorithmic, tikzpicture, equation, align a bloky \[ ... \].
    Na konci vypise tabulku: slova, vety, priemerna dlzka vety a pocty nalezov podla kategorii.
    Pocty slov su priblizne (bez prikazov, matematiky a komentarov).

    Zoznam fraz je UTF-8 TSV: kategoria<TAB>regex<TAB>navrh. Riadky zacinajuce # a prazdne riadky
    sa ignoruju. Regex je v syntaxi .NET a hlada sa bez ohladu na velkost pismen v kazdom riadku
    zdroja po odstraneni LaTeX komentarov. Ak predvoleny zoznam chyba, skript to oznami a pokracuje
    len so vstavanymi kontrolami.

    Navratovy kod je 0, aj ked su nalezy; 2 pri neplatnych parametroch.

.PARAMETER Project
    Nazov priecinka v projects/. Skontroluju sa vsetky .tex subory v nom (rekurzivne) okrem
    priecinka preamble/.

.PARAMETER Path
    Subor alebo priecinok s .tex alebo .txt subormi (napr. text z pdftotext). Relativna cesta sa
    berie od aktualneho priecinka, potom od korena pracovneho priestoru.

.PARAMETER PhraseList
    Cesta k zoznamu fraz. Predvolene knowledge/writing/phrase-list.tsv.

.PARAMETER MaxWords
    Najvacsi povoleny pocet slov vo vete (predvolene 40).

.PARAMETER Summary
    Vypise len suhrnnu tabulku, bez jednotlivych nalezov.

.EXAMPLE
    .\scripts\check-text.ps1 -Project clanok-1-min-cut-path
    .\scripts\check-text.ps1 -Path projects\clanok-1-min-cut-path\sections\introduction.tex -MaxWords 30
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
# Parametre
# ---------------------------------------------------------------------------

if ($Project -and $Path) {
    Stop-InvalidParameter "Zadaj bud -Project, alebo -Path, nie oboje."
}
if (-not $Project -and -not $Path) {
    Stop-InvalidParameter "Chyba -Project <nazov> alebo -Path <subor-alebo-priecinok>."
}
if ($MaxWords -lt 1) {
    Stop-InvalidParameter "-MaxWords musi byt kladne cele cislo."
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
        Stop-InvalidParameter "Projekt neexistuje: $sourceDirectory. Dostupne projekty: $available"
    }
    $sourceDirectory = (Get-Item -LiteralPath $sourceDirectory).FullName
    foreach ($item in (Get-ChildItem -LiteralPath $sourceDirectory -Recurse -File | Sort-Object FullName)) {
        # .cls, .sty, .bst a .bib neobsahuju prozu; berie sa len .tex mimo preamble/
        if ($item.Extension -ne ".tex") { continue }
        if (Test-InPreambleFolder $item.FullName $sourceDirectory) { continue }
        $files.Add($item.FullName)
    }
    if ($files.Count -eq 0) {
        Stop-InvalidParameter "V projekte $Project nie je ziadny .tex subor."
    }
}
else {
    $candidate = $Path
    if (-not (Test-Path -LiteralPath $candidate)) {
        $candidate = Join-Path $workspace $Path
    }
    if (-not (Test-Path -LiteralPath $candidate)) {
        Stop-InvalidParameter "Cesta neexistuje: $Path"
    }
    $target = Get-Item -LiteralPath $candidate
    if ($target.PSIsContainer) {
        foreach ($item in (Get-ChildItem -LiteralPath $target.FullName -Recurse -File | Sort-Object FullName)) {
            if ($item.Extension -ne ".tex" -and $item.Extension -ne ".txt") { continue }
            if (Test-InPreambleFolder $item.FullName $target.FullName) { continue }
            $files.Add($item.FullName)
        }
        if ($files.Count -eq 0) {
            Stop-InvalidParameter "V priecinku $($target.FullName) nie je ziadny .tex ani .txt subor."
        }
    }
    else {
        if ($target.Extension -ne ".tex" -and $target.Extension -ne ".txt") {
            Stop-InvalidParameter "Podporovane su len subory .tex a .txt: $($target.FullName)"
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
        Stop-InvalidParameter "Zoznam fraz neexistuje: $PhraseList"
    }
}

# Vystup obsahuje citaty zo zdroja (napr. Erdos s dlhym o), preto UTF-8.
$previousOutputEncoding = $null
try {
    $previousOutputEncoding = [Console]::OutputEncoding
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false
}
catch {
    $previousOutputEncoding = $null
}

# ---------------------------------------------------------------------------
# Konstanty a regularne vyrazy
# ---------------------------------------------------------------------------

$utf8 = New-Object System.Text.UTF8Encoding $false
$ordinal = [System.StringComparison]::Ordinal
$rxIgnoreCase = [System.Text.RegularExpressions.RegexOptions]"IgnoreCase, CultureInvariant"
$rxNone = [System.Text.RegularExpressions.RegexOptions]"CultureInvariant"

# Zastupne znaky (sukromna oblast Unicode), aby skript ostal v ASCII.
$MATH = [string][char]0xE000      # matematika v riadku
$DISP = [string][char]0xE001      # vysadena matematika (ukoncuje vetu)
$MACRO = [string][char]0xE002     # vlastne makro v texte, pocita sa ako jedno slovo

$builtinCategories = @("long", "dup", "latex", "todo", "contraction", "spelling")
$phraseCategories = @("filler", "wordy", "hype", "hedge", "meta", "ai-tic", "grammar")

$labelPrefixes = @("sec", "def", "thm", "lem", "clm", "cor", "prop", "rem", "ex", "fig", "tab", "alg", "eq", "prob", "app")

function New-StringSet([string[]]$Items) {
    $set = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    foreach ($entry in $Items) { [void]$set.Add($entry) }
    return , $set
}

# Prostredia, ktorych obsah nie je proza.
$verbatimEnvironments = New-StringSet @("verbatim", "verbatim*", "Verbatim", "lstlisting", "minted", "comment", "filecontents", "filecontents*")
$skippedEnvironments = New-StringSet @(
    "verbatim", "verbatim*", "Verbatim", "lstlisting", "minted", "comment", "filecontents", "filecontents*",
    "algorithmic", "tikzpicture", "tikzcd", "thebibliography",
    "equation", "equation*", "align", "align*", "alignat", "alignat*", "flalign", "flalign*",
    "gather", "gather*", "multline", "multline*", "eqnarray", "eqnarray*", "displaymath", "math"
)

# Prikazy, ktorych argument je text vety.
$unwrapCommands = New-StringSet @(
    "emph", "textbf", "textit", "textsc", "textsf", "texttt", "textrm", "textup", "textsl", "textmd",
    "textnormal", "underline", "mbox", "text", "caption", "title", "enquote"
)
# Nadpisy sa do prozy nerataju.
$headingCommands = New-StringSet @("part", "chapter", "section", "subsection", "subsubsection", "paragraph", "subparagraph")
# Prikazy bez argumentu, ktore nie su slovom.
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
$rxRowBreak = [regex]::new('\\\\\s*(?:\[[^\[\]]*\])?\s*$', $rxNone)
$rxSentenceEnd = [regex]::new('[.!?][)''"\u2019\u201D\]]*$', $rxNone)

$rxWordTex = [regex]::new('[\p{L}\p{Nd}]+(?:[''\u2019\-][\p{L}\p{Nd}]+)*|\uE002', $rxNone)
$rxWordTxt = [regex]::new('\p{L}{2,}(?:[''\u2019\-]\p{L}+)*|\b[aAI]\b', $rxNone)
$rxHasLetter = [regex]::new('\p{L}{2,}|\uE002', $rxNone)
$rxSentenceBreak = [regex]::new('[.!?]+[)''"\u2019\u201D\]]*\s+(?=[\p{Lu}\uE000\uE002])', $rxNone)
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
$rxEgIe = [regex]::new('(?<![\p{L}.])(?:e\.g|i\.e)\.(?!,)', $rxIgnoreCase)
$rxEgIeNoPeriod = [regex]::new('(?<![\p{L}.])(?:e\.g|i\.e)(?=[\s,~])', $rxIgnoreCase)
$rxEtAl = [regex]::new('\bet\.?\s+al\b(?!\.)|\bet\.\s*al\b\.?', $rxIgnoreCase)
$rxStraightQuote = [regex]::new('"[^"]{0,60}"?', $rxNone)
$rxMathAtStart = [regex]::new('^(?:\$(?!\$)|\\\()', $rxNone)

$rxTodoWords = [regex]::new('\b(?:TODO|FIXME|XXX)\b|\\fillin\b|\\todo\b', $rxNone)
$rxQuestionMarks = [regex]::new('\?\?+', $rxNone)

$rxContraction = [regex]::new('\b(?:\p{L}+n[''\u2019]t|(?:it|that|there|here|what|let|who)[''\u2019]s|(?:we|you|they|i|he|she|it|that)[''\u2019](?:ll|re|ve|d)|i[''\u2019]m)\b', $rxIgnoreCase)
$contractionExpansions = @{
    "don't" = "do not"; "can't" = "cannot"; "isn't" = "is not"; "it's" = "it is"; "we'll" = "we will"
    "doesn't" = "does not"; "won't" = "will not"; "let's" = "let us"; "aren't" = "are not"
    "didn't" = "did not"; "wasn't" = "was not"; "weren't" = "were not"; "hasn't" = "has not"
    "haven't" = "have not"; "couldn't" = "could not"; "wouldn't" = "would not"; "shouldn't" = "should not"
    "that's" = "that is"; "there's" = "there is"; "we're" = "we are"; "we've" = "we have"; "i'm" = "I am"
}

$britishIse = '(?:optimi|formali|generali|minimi|maximi|characteri|reali|recogni|summari|parametri|parameteri|randomi|normali|initiali|synchroni|utili|visuali|organi|speciali|categori|lineari|discreti|penali|prioriti|standardi|symmetri|factori|locali|finali|stabili|emphasi|critici|hypothesi|diagonali|regulari|centrali|equali|vectori|paralleli)s(?:e|es|ed|ing|er|ers|ation|ations|able)'
$rxBritish = [regex]::new(
    '\b(?:(?<ise>' + $britishIse + ')' +
    '|(?<isation>(?!improvis)\p{L}{3,}isations?)' +
    '|(?<analyse>analys(?:e|ed|ing|er|ers))' +
    '|(?<our>(?:colou|neighbou|behaviou|favou|honou)r\p{L}*)' +
    '|(?<centre>cent(?:re|res|red))' +
    '|(?<ll>(?:model|label|travel|cancel|signal|channel|level)l(?:ed|ing|er|ers))' +
    '|(?<misc>acknowledgements?|judgements?|artefacts?|whilst|amongst|fulfil|fulfilment|defence))\b',
    $rxIgnoreCase)
$britishMisc = @{
    "acknowledgement" = "acknowledgment"; "acknowledgements" = "acknowledgments"; "judgement" = "judgment"
    "judgements" = "judgments"; "artefact" = "artifact"; "artefacts" = "artifacts"; "whilst" = "while"
    "amongst" = "among"; "fulfil" = "fulfill"; "fulfilment" = "fulfillment"; "defence" = "defense"
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
    if ($Match.Groups["ll"].Success) { return ($value -replace '(?i)ll', 'l') }
    $key = $value.ToLowerInvariant()
    if ($britishMisc.ContainsKey($key)) { return $britishMisc[$key] }
    return "americky tvar"
}

# ---------------------------------------------------------------------------
# Zoznam fraz
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
            Write-Warning "Zoznam fraz, riadok $($index + 1): ocakavam kategoria<TAB>regex<TAB>navrh; riadok preskakujem."
            continue
        }
        $suggestion = ""
        if ($fields.Length -ge 3) { $suggestion = $fields[2].Trim() }
        try {
            $compiled = [regex]::new($fields[1].Trim(), $rxIgnoreCase)
        }
        catch {
            Write-Warning "Zoznam fraz, riadok $($index + 1): neplatny regex '$($fields[1].Trim())'; riadok preskakujem."
            continue
        }
        $phraseRules.Add([pscustomobject]@{
                Category   = $fields[0].Trim().ToLowerInvariant()
                Regex      = $compiled
                Suggestion = $suggestion
            })
    }
    $phraseListNote = "$PhraseList ($($phraseRules.Count) pravidiel)"
}
else {
    $phraseListNote = "chyba ($PhraseList) - bezia len vstavane kontroly"
    Write-Warning "Zoznam fraz neexistuje: $PhraseList. Pokracujem len so vstavanymi kontrolami."
}

# ---------------------------------------------------------------------------
# Pomocne funkcie
# ---------------------------------------------------------------------------

$script:findings = New-Object System.Collections.Generic.List[object]
$script:currentFile = ""
$script:mathState = ""

function Get-DisplayPath([string]$FullName) {
    $root = $workspace.TrimEnd('\') + '\'
    if ($FullName.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $FullName.Substring($root.Length).Replace('\', '/')
    }
    return $FullName.Replace('\', '/')
}

function Add-Finding([int]$Line, [int]$Column, [string]$Category, [string]$Text, [string]$Suggestion) {
    $clean = $rxSpaces.Replace($Text, ' ').Trim()
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

# Nahradi matematiku zastupnym znakom. Stav (otvorena matematika) sa prenasa medzi riadkami
# v $script:mathState: display = \[, dollars = $$, inline = $, paren = \(.
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

# Z riadku s uz zamaskovanou matematikou urobi cisty text vety.
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

# --- stavba viet ------------------------------------------------------------

$script:unitBuilder = New-Object System.Text.StringBuilder
$script:unitOffsets = New-Object System.Collections.Generic.List[int]
$script:unitLines = New-Object System.Collections.Generic.List[int]
$script:isTxt = $false
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
    # True, ak v zasobniku je rozpisana (neukoncena) veta.
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
        Add-Finding (Get-UnitLine $dup.Index) 0 "dup" $dup.Value "vymaz zdvojene slovo"
    }

    # hranice viet: bodka, medzera a velke pismeno (alebo matematika); skratky vetu nekoncia
    $starts = New-Object System.Collections.Generic.List[int]
    $starts.Add(0)
    foreach ($break in $rxSentenceBreak.Matches($text)) {
        $before = $rxTokenBeforeBreak.Match($text.Substring(0, $break.Index))
        if ($before.Success) {
            $token = $before.Groups[1].Value.TrimEnd('.').ToLowerInvariant()
            if ($abbreviations.Contains($token)) { continue }
            # inicialy (M. Loebl); v .txt su jednopismenove premenne, tam sa veta deli
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
            # useky kratsie nez 3 slova (Formally:, nadpisy poloziek) nie su vety
            $script:statSentences++
            $script:statSentenceWords += $count
        }
        if ($count -gt $MaxWords) {
            $shown = $piece.Replace($MATH, '$..$').Replace($MACRO, '\..').Trim()
            $opening = ($shown -split '\s+' | Select-Object -First 9) -join ' '
            Add-Finding (Get-UnitLine $from) 0 "long" "$opening ..." "$count slov (limit $MaxWords): rozdel alebo skrat vetu"
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
            # slovo rozdelene na konci riadku (pdftotext)
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

# --- kontroly na riadku -----------------------------------------------------

function Test-Phrases([string]$Text, [int]$Line, [string]$Previous, [int]$PreviousLine) {
    if ($phraseRules.Count -eq 0) { return }
    foreach ($rule in $phraseRules) {
        foreach ($hit in $rule.Regex.Matches($Text)) {
            if ($hit.Length -eq 0) { continue }
            Add-Finding $Line $hit.Index $rule.Category $hit.Value $rule.Suggestion
        }
    }
    if ($Previous -ne "") {
        # fraza rozdelena koncom riadku: hlada sa v spojeni dvoch susednych riadkov
        $head = $Previous.TrimEnd()
        $joined = $head + " " + $Text.TrimStart()
        foreach ($rule in $phraseRules) {
            foreach ($hit in $rule.Regex.Matches($joined)) {
                if ($hit.Length -eq 0) { continue }
                if ($hit.Index -lt $head.Length -and ($hit.Index + $hit.Length) -gt ($head.Length + 1)) {
                    Add-Finding $PreviousLine (1000 + $hit.Index) $rule.Category $hit.Value $rule.Suggestion
                }
            }
        }
    }
}

function Test-Wording([string]$Text, [int]$Line) {
    foreach ($hit in $rxContraction.Matches($Text)) {
        $key = $hit.Value.ToLowerInvariant().Replace([string][char]0x2019, "'")
        $expansion = "rozpis skrateny tvar"
        if ($contractionExpansions.ContainsKey($key)) { $expansion = $contractionExpansions[$key] }
        Add-Finding $Line $hit.Index "contraction" $hit.Value $expansion
    }
    foreach ($hit in $rxBritish.Matches($Text)) {
        Add-Finding $Line $hit.Index "spelling" $hit.Value (Get-AmericanForm $hit)
    }
}

function Test-Todo([string]$RawLine, [string]$WithoutComment, [int]$Line) {
    foreach ($hit in $rxTodoWords.Matches($RawLine)) {
        Add-Finding $Line $hit.Index "todo" $hit.Value "dokonci alebo odstran"
    }
    foreach ($hit in $rxQuestionMarks.Matches($WithoutComment)) {
        Add-Finding $Line $hit.Index "todo" $hit.Value "nevyrieseny odkaz alebo poznamka"
    }
}

function Test-Labels([string]$WithoutComment, [int]$Line) {
    foreach ($hit in $rxLabel.Matches($WithoutComment)) {
        $name = $hit.Groups[1].Value
        $separator = $name.IndexOf(':')
        $prefix = ""
        if ($separator -gt 0) { $prefix = $name.Substring(0, $separator) }
        if ($labelPrefixes -cnotcontains $prefix) {
            Add-Finding $Line $hit.Index "latex" $hit.Value ("prefix navestia ma byt jeden z: " + ($labelPrefixes -join ", "))
        }
    }
}

function Test-LatexLine([string]$WithoutComment, [int]$Line) {
    $plain = $WithoutComment.Replace('\$', '  ')
    if ($rxDoubleDollar.IsMatch($plain)) {
        Add-Finding $Line $plain.IndexOf('$$') "latex" '$$' 'pouzi \[ ... \]'
    }
    foreach ($hit in $rxSpaceBeforeRef.Matches($WithoutComment)) {
        $before = $hit.Groups[1].Value
        $last = $before[$before.Length - 1]
        if ($last -eq '(' -or $last -eq '~' -or $last -eq '[' -or $last -eq '{') { continue }
        Add-Finding $Line $hit.Index "latex" $hit.Value "pred odkazom pouzi ~ namiesto medzery"
    }
    foreach ($hit in $rxAttachedCite.Matches($WithoutComment)) {
        Add-Finding $Line $hit.Index "latex" $hit.Value "pred \cite chyba ~"
    }
    foreach ($hit in $rxLowercaseRef.Matches($WithoutComment)) {
        $name = $hit.Groups[1].Value
        $capital = $name.Substring(0, 1).ToUpperInvariant() + $name.Substring(1) + $hit.Groups[2].Value
        Add-Finding $Line $hit.Index "latex" ($hit.Value.TrimEnd('{')) "$capital s velkym pismenom"
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
# Spracovanie .tex
# ---------------------------------------------------------------------------

function Invoke-TexCheck([string[]]$Lines) {
    $inPreamble = $false
    foreach ($candidateLine in $Lines) {
        if ($rxDocumentClass.IsMatch($candidateLine)) { $inPreamble = $true; break }
    }
    $skipEnvironment = ""
    $script:mathState = ""
    $previousProse = ""
    $previousProseLine = -1

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
                # prazdny riadok konci odsek; matematika v riadku cez odsek nepokracuje
                Complete-Unit
                if ($script:mathState -eq "inline" -or $script:mathState -eq "paren") { $script:mathState = "" }
            }
            else {
                Test-Todo $raw "" $line
            }
            continue
        }

        if ($trimmed.Contains('\end{document}')) { break }

        $skipHere = ""
        foreach ($begin in $rxBeginEnvironment.Matches($withoutComment)) {
            if ($skippedEnvironments.Contains($begin.Groups[1].Value)) { $skipHere = $begin.Groups[1].Value; break }
        }
        if ($skipHere -ne "") {
            Complete-Unit
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
            Add-Finding $line $plainDollars.IndexOf('$$') "latex" '$$' 'pouzi \[ ... \]'
        }

        $visible = $masked.Replace($MATH, ' ').Replace($DISP, ' ')
        if (-not $rxHasLetter.IsMatch($rxReferenceCommands.Replace($rxBeginEnd.Replace($visible, ' '), ' '))) {
            # riadok je cely matematika, \begin/\end alebo len odkazy: ziadna proza
            Test-Todo $raw "" $line
            if ($rxStartsBoundary.IsMatch($trimmed) -or $masked.Contains($DISP) -or $mathOpenAtStart) { Complete-Unit }
            continue
        }

        Test-Todo $raw $visible $line
        Test-LatexLineBody $withoutComment $line

        if ($previousProseLine -eq ($line - 1)) {
            Test-Phrases $withoutComment $line $previousProse $previousProseLine
        }
        else {
            Test-Phrases $withoutComment $line "" -1
        }
        $previousProse = $withoutComment
        $previousProseLine = $line

        $checkText = $rxReferenceCommands.Replace($rxBeginEnd.Replace($masked, ' '), ' ')
        Test-Wording $checkText $line
        $quoteText = $rxAccent.Replace($checkText, '')
        $quote = $rxStraightQuote.Match($quoteText)
        if ($quote.Success) {
            Add-Finding $line $quote.Index "latex" $quote.Value 'rovne uvodzovky: pouzi ``...'''''
        }

        $startsBoundary = $rxStartsBoundary.IsMatch($trimmed)
        if ($startsBoundary) { Complete-Unit }

        $isHeading = ($rxHeadingLine.IsMatch($trimmed) -or $rxBoldOnlyLine.IsMatch($trimmed))
        $prose = Convert-ToProse $masked

        if (-not $mathOpenAtStart -and $rxMathAtStart.IsMatch($trimmed) -and -not (Test-UnitOpen)) {
            $opening = ($trimmed -split '\s+' | Select-Object -First 4) -join ' '
            Add-Finding $line 0 "latex" "$opening ..." "veta nema zacinat symbolom; zacni slovom"
        }

        if ($rxBoldOnlyLine.IsMatch($trimmed)) {
            # samostatny tucny nadpis (Reduction., Case ...) nie je veta
            Complete-Unit
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

        if ($isHeading -or $rxRowBreak.IsMatch($trimmed)) { Complete-Unit }
    }
    Complete-Unit
}

function Test-LatexLineBody([string]$WithoutComment, [int]$Line) {
    foreach ($hit in $rxSpaceBeforeRef.Matches($WithoutComment)) {
        $before = $hit.Groups[1].Value
        $last = $before[$before.Length - 1]
        if ($last -eq '(' -or $last -eq '~' -or $last -eq '[' -or $last -eq '{') { continue }
        Add-Finding $Line $hit.Index "latex" $hit.Value "pred odkazom pouzi ~ namiesto medzery"
    }
    foreach ($hit in $rxAttachedCite.Matches($WithoutComment)) {
        Add-Finding $Line $hit.Index "latex" $hit.Value "pred \cite chyba ~"
    }
    foreach ($hit in $rxLowercaseRef.Matches($WithoutComment)) {
        $name = $hit.Groups[1].Value
        $capital = $name.Substring(0, 1).ToUpperInvariant() + $name.Substring(1) + $hit.Groups[2].Value
        Add-Finding $Line $hit.Index "latex" ($hit.Value.TrimEnd('{')) "$capital s velkym pismenom"
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
# Spracovanie .txt (napr. vystup pdftotext)
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
    $previousProse = ""
    $previousProseLine = -1

    for ($index = 0; $index -lt $Lines.Length; $index++) {
        $raw = $Lines[$index]
        $line = $index + 1
        $trimmed = $raw.Trim()

        if ($trimmed -eq "") { $blankPending = $true; continue }
        Test-Todo $raw $raw $line

        if ($raw.Contains([string][char]12)) { Complete-Unit }     # novy list
        $nonSpace = $rxNonSpace.Matches($trimmed).Count
        $letters = $rxLetters.Matches($trimmed).Count
        $indent = $raw.Length - $raw.TrimStart().Length
        $words = $rxWordTxt.Matches($trimmed).Count
        $isNoise = $rxTxtPageNumber.IsMatch($trimmed) -or $rxTxtDottedLine.IsMatch($trimmed) -or $rxTxtCodeLine.IsMatch($trimmed)
        if (-not $isNoise -and ($letters -lt 0.6 * $nonSpace)) { $isNoise = $true }                  # vzorec
        if (-not $isNoise -and $indent -ge 12 -and $words -le 8) { $isNoise = $true }              # vycentrovany vzorec alebo popis
        if ($isNoise) {
            # vzorec uprostred vety vetu neprerusuje, ak dalsi riadok pokracuje malym pismenom
            $blankPending = $true
            continue
        }

        if ($previousProseLine -ge ($line - 2)) {
            Test-Phrases $trimmed $line $previousProse $previousProseLine
        }
        else {
            Test-Phrases $trimmed $line "" -1
        }
        $previousProse = $trimmed
        $previousProseLine = $line
        Test-Wording $trimmed $line

        $isHeading = ($rxTxtHeading.IsMatch($trimmed) -and $words -le 12)
        if ($isHeading -or $rxTxtBullet.IsMatch($trimmed)) { Complete-Unit }
        elseif ($blankPending -and $script:unitBuilder.Length -gt 0) {
            $current = $script:unitBuilder.ToString().TrimEnd()
            if ($rxTxtEndsBlock.IsMatch($current) -or $rxTxtStartsNew.IsMatch($trimmed)) { Complete-Unit }
        }
        $blankPending = $false

        if ($isHeading) { continue }
        Add-UnitText ($rxSpaces.Replace($trimmed, ' ')) $line
    }
    Complete-Unit
}

# ---------------------------------------------------------------------------
# Hlavny cyklus
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
        Write-Warning "Subor sa neda precitat: $fullName ($($_.Exception.Message))"
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
            File      = $script:currentFile
            Words     = $script:statWords
            Sentences = $script:statSentences
            SentenceWords = $script:statSentenceWords
            Average   = $average
            Counts    = $counts
            Total     = ($script:findings.Count - $firstFinding)
        })
}

# --- nalezy -----------------------------------------------------------------

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

# --- suhrn ------------------------------------------------------------------

$categories = New-Object System.Collections.Generic.List[string]
foreach ($category in $builtinCategories) { $categories.Add($category) }
foreach ($category in $phraseCategories) {
    $used = $false
    foreach ($rule in $phraseRules) { if ($rule.Category -eq $category) { $used = $true; break } }
    if ($used) { $categories.Add($category) }
}
foreach ($finding in $script:findings) {
    if (-not $categories.Contains($finding.Category)) { $categories.Add($finding.Category) }
}

$nameWidth = 5
foreach ($stat in $fileStats) { if ($stat.File.Length -gt $nameWidth) { $nameWidth = $stat.File.Length } }

function Format-Row([string]$Name, [string]$Words, [string]$Sentences, [string]$Average, [string[]]$Cells, [string]$Total) {
    $row = $Name.PadRight($nameWidth) + "  " + $Words.PadLeft(6) + "  " + $Sentences.PadLeft(5) + "  " + $Average.PadLeft(7)
    for ($column = 0; $column -lt $categories.Count; $column++) {
        $width = [math]::Max($categories[$column].Length, 4)
        $row += "  " + $Cells[$column].PadLeft($width)
    }
    return $row + "  " + $Total.PadLeft(6)
}

Write-Output "Zoznam fraz: $phraseListNote"
Write-Output "Limit dlzky vety: $MaxWords slov. Slova a vety su priblizne (bez prikazov, matematiky a komentarov)."
Write-Output ""
Write-Output (Format-Row "Subor" "slova" "vety" "priemer" $categories.ToArray() "spolu")

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
    Write-Output (Format-Row "SPOLU" ([string]$totalWords) ([string]$totalSentences) ($totalAverage.ToString("0.0", [System.Globalization.CultureInfo]::InvariantCulture)) $cells.ToArray() ([string]$script:findings.Count))
}

if ($null -ne $previousOutputEncoding) {
    try { [Console]::OutputEncoding = $previousOutputEncoding } catch { }
}
exit 0
