<#
.SYNOPSIS
    Checks the bibliography of a LaTeX project against its citations and against the canonical .bib.
    Changes nothing; prints findings only.

.DESCRIPTION
    Project mode (-Project or -Path): reads every .tex file of the project, finds the .bib files it uses
    (\bibliography{...} for BibTeX, \addbibresource{...} for biblatex; otherwise every .bib in the folder) and reports:
      [cite-missing]       a cited key that is not in the project .bib
      [cite-case]          a cited key that differs from the .bib key only in letter case
      [unused]             a .bib entry that is never cited (skipped after \nocite{*})
      [duplicate-key]      the same key twice (BibTeX compares keys case-insensitively)
      [duplicate-doi]      the same DOI in two entries
      [duplicate-entry]    two entries with the same title and year
      [canonical-missing]  a project entry that is not in the canonical .bib
      [canonical-diff]     a project entry whose type or fields differ from the canonical entry
      [status]             status line problems of the canonical entry (see below)
      [required]           a field the entry type requires is missing
      [recommended]        a recommended field is missing (doi, number, isbn ...)
      [doi]                DOI with a URL or "doi:" prefix, or with implausible syntax
      [isbn]               ISBN-10 or ISBN-13 with a wrong check digit or format
      [pages]              page range without "--", or an odd page format
      [year]               year that is not four digits
      [non-ascii]          non-ASCII character in a field (BibTeX projects and the canonical file) with the LaTeX escape
      [field]              field that does not belong in the file (abstract, keywords, file, month, language, tool fields)
      [biblatex]           biblatex-only field or entry type in a BibTeX project or in the canonical file
      [author]             author list not in "Surname, Given and ..." form, or "and others"
      [title-case]         unprotected capitals in a title that a BibTeX style would lowercase
      [key-style]          key with characters outside A-Z a-z 0-9 (BibTeX projects and the canonical file)
      [syntax]             .bib syntax that BibTeX cannot parse (unbalanced braces, repeated fields, unknown entry type)
      [bib-file]           a .bib file that is missing or not found

    Canonical mode (-CanonicalOnly): checks only the canonical file with the entry checks above plus the status
    line check: every entry has a status comment directly above it:
        % VERIFIED 2026-10-08 (where it was checked)
        % PARTIAL 2026-10-08: what is and is not verified
        % TODO: what has to be resolved
    The legacy tags OVERENE and CIASTOCNE are accepted and counted in one note per file.

    A project that uses biblatex (\addbibresource, \printbibliography) is checked with biblatex rules: UTF-8 and
    biblatex fields are allowed, and entries missing from the canonical file are reported as a note.

    The exit code is 0 even when there are findings; 2 for invalid parameters.

.PARAMETER Project
    Name of a folder in projects/.

.PARAMETER Path
    A folder with .tex and .bib files (for example a copy in tmp/). Relative paths are tried from the current
    folder, then from the workspace root.

.PARAMETER Canonical
    Path to the canonical bibliography. Default: knowledge/bibliography/references.bib.

.PARAMETER CanonicalOnly
    Check only the canonical file; -Project and -Path are not used.

.PARAMETER Summary
    Print only the summary, without the individual findings.

.EXAMPLE
    .\scripts\check-bib.ps1 -Project clanok-1-min-cut-path
    .\scripts\check-bib.ps1 -Project cv -Summary
    .\scripts\check-bib.ps1 -CanonicalOnly
    .\scripts\check-bib.ps1 -Path tmp\style-bibtest\project -Canonical tmp\style-bibtest\canonical.bib
#>
param(
    [Parameter(Position = 0)]
    [string]$Project,

    [string]$Path,

    [string]$Canonical,

    [switch]$CanonicalOnly,

    [switch]$Summary
)

$workspace = Split-Path -Parent $PSScriptRoot
$projectsRoot = Join-Path $workspace "projects"
$defaultCanonical = Join-Path $workspace "knowledge\bibliography\references.bib"

function Stop-InvalidParameter([string]$Message) {
    $Host.UI.WriteErrorLine("check-bib: $Message")
    exit 2
}

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

if ($CanonicalOnly) {
    if ($Project -or $Path) { Stop-InvalidParameter "-CanonicalOnly does not take -Project or -Path." }
}
else {
    if ($Project -and $Path) { Stop-InvalidParameter "Pass either -Project or -Path, not both." }
    if (-not $Project -and -not $Path) { Stop-InvalidParameter "Missing -Project <name>, -Path <folder> or -CanonicalOnly." }
}

$projectDirectory = ""
if (-not $CanonicalOnly) {
    if ($Project) {
        $projectDirectory = Join-Path $projectsRoot $Project
        if (-not (Test-Path -LiteralPath $projectDirectory -PathType Container)) {
            $available = (Get-ChildItem -LiteralPath $projectsRoot -Directory | ForEach-Object { $_.Name }) -join ", "
            Stop-InvalidParameter "Project does not exist: $projectDirectory. Available projects: $available"
        }
    }
    else {
        $projectDirectory = $Path
        if (-not (Test-Path -LiteralPath $projectDirectory -PathType Container)) {
            $projectDirectory = Join-Path $workspace $Path
        }
        if (-not (Test-Path -LiteralPath $projectDirectory -PathType Container)) {
            Stop-InvalidParameter "Folder does not exist: $Path"
        }
    }
    $projectDirectory = (Get-Item -LiteralPath $projectDirectory).FullName
}

$canonicalPath = $defaultCanonical
if ($Canonical) {
    $canonicalPath = $Canonical
    if (-not (Test-Path -LiteralPath $canonicalPath -PathType Leaf)) {
        $canonicalPath = Join-Path $workspace $Canonical
    }
}
$canonicalFound = (Test-Path -LiteralPath $canonicalPath -PathType Leaf)
if (-not $canonicalFound) {
    if ($CanonicalOnly -or $Canonical) { Stop-InvalidParameter "Canonical file does not exist: $canonicalPath" }
}
else {
    $canonicalPath = (Get-Item -LiteralPath $canonicalPath).FullName
}

# The output quotes the source, hence UTF-8.
$previousOutputEncoding = $null
try {
    $previousOutputEncoding = [Console]::OutputEncoding
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false
}
catch {
    $previousOutputEncoding = $null
}

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

$utf8 = New-Object System.Text.UTF8Encoding $false
$rxNone = [System.Text.RegularExpressions.RegexOptions]"CultureInvariant"
$rxIgnoreCase = [System.Text.RegularExpressions.RegexOptions]"IgnoreCase, CultureInvariant"

function New-StringSet([string[]]$Items) {
    $set = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    foreach ($entry in $Items) { [void]$set.Add($entry) }
    return , $set
}

# Entry types of classic BibTeX.
$bibtexTypes = New-StringSet @("article", "book", "booklet", "conference", "inbook", "incollection", "inproceedings",
    "manual", "mastersthesis", "misc", "phdthesis", "proceedings", "techreport", "unpublished")
$ignoredTypes = New-StringSet @("comment", "preamble", "string")

# Required and recommended fields per type (alternatives separated by |). Same table as knowledge/bibliography/README.md.
$requiredFields = @{
    "article"       = @{ Required = @("author", "title", "journal", "year", "volume", "pages|eid|articleno"); Recommended = @("number", "doi") }
    "inproceedings" = @{ Required = @("author", "title", "booktitle", "year", "pages|eid|articleno"); Recommended = @("publisher", "doi") }
    "conference"    = @{ Required = @("author", "title", "booktitle", "year", "pages|eid|articleno"); Recommended = @("publisher", "doi") }
    "book"          = @{ Required = @("author|editor", "title", "publisher", "year"); Recommended = @("isbn") }
    "incollection"  = @{ Required = @("author", "title", "booktitle", "publisher", "year", "pages"); Recommended = @("editor", "doi") }
    "inbook"        = @{ Required = @("author|editor", "title", "publisher", "year", "chapter|pages"); Recommended = @("isbn") }
    "phdthesis"     = @{ Required = @("author", "title", "school", "year"); Recommended = @() }
    "mastersthesis" = @{ Required = @("author", "title", "school", "year"); Recommended = @() }
    "techreport"    = @{ Required = @("author", "title", "institution", "year"); Recommended = @("number") }
    "unpublished"   = @{ Required = @("author", "title", "note"); Recommended = @("year") }
    "proceedings"   = @{ Required = @("title", "year"); Recommended = @("publisher", "isbn") }
    "manual"        = @{ Required = @("title"); Recommended = @("year") }
    "booklet"       = @{ Required = @("title"); Recommended = @() }
}
# @misc is split by use: a preprint has eprint; everything else (software, data, model, web page) needs a url.
$miscPreprint = @{ Required = @("author", "title", "year", "eprint", "archivePrefix"); Recommended = @("primaryClass") }
$miscOther = @{ Required = @("author|organization", "title", "year", "url|howpublished"); Recommended = @("note") }

# Fields that do not belong in the knowledge base (README, section 6) and fields added by reference managers.
$forbiddenFields = New-StringSet @("abstract", "keywords", "file", "month", "language", "annote", "timestamp", "owner",
    "groups", "comment", "review", "date-added", "date-modified", "mendeley-tags", "mendeley-groups", "bdsk-url-1",
    "bdsk-file-1", "rating", "read", "priority", "citeulike-article-id", "posted-at")
$biblatexFields = New-StringSet @("date", "journaltitle", "location", "urldate", "eprinttype", "eprintclass", "langid",
    "shortjournal", "issuetitle", "maintitle", "origdate", "sortname", "pubstate", "entrysubtype", "options", "ids",
    "xdata", "related", "annotator", "shorthand", "shorttitle", "subtitle", "titleaddon", "booktitleaddon", "usera",
    "userb", "userc", "userd", "usere", "verba", "verbb", "verbc")
$biblatexTypes = New-StringSet @("online", "report", "thesis", "software", "dataset", "patent", "mvbook", "bookinbook",
    "suppbook", "collection", "reference", "mvcollection", "inreference", "periodical", "suppperiodical", "review",
    "standard", "legislation", "jurisdiction", "video", "music", "audio", "movie", "image", "artwork", "commentary",
    "letter", "set", "xdata", "mvproceedings", "mvreference", "suppcollection", "unpublished_biblatex")

# LaTeX escapes for the non-ASCII characters that occur in names and titles.
$escapeTable = @{}
function Add-Accents([string]$Command, [string]$Pairs) {
    foreach ($pair in ($Pairs -split ' ')) {
        $code = [Convert]::ToInt32($pair.Substring(0, 4), 16)
        $letter = $pair.Substring(5)
        if ($Command.Length -eq 1 -and $Command -notmatch '[A-Za-z]') { $escapeTable[$code] = '{\' + $Command + $letter + '}' }
        else { $escapeTable[$code] = '{\' + $Command + '{' + $letter + '}}' }
    }
}
Add-Accents "'" "00E1:a 00E9:e 00ED:i 00F3:o 00FA:u 00FD:y 0107:c 013A:l 0144:n 0155:r 015B:s 017A:z 00C1:A 00C9:E 00CD:I 00D3:O 00DA:U 00DD:Y 0106:C 0139:L 0143:N 0154:R 015A:S 0179:Z"
Add-Accents '"' "00E4:a 00EB:e 00EF:i 00F6:o 00FC:u 00FF:y 00C4:A 00CB:E 00CF:I 00D6:O 00DC:U"
Add-Accents "``" "00E0:a 00E8:e 00EC:i 00F2:o 00F9:u 00C0:A 00C8:E 00CC:I 00D2:O 00D9:U"
Add-Accents "^" "00E2:a 00EA:e 00EE:i 00F4:o 00FB:u 00C2:A 00CA:E 00CE:I 00D4:O 00DB:U"
Add-Accents "~" "00F1:n 00E3:a 00F5:o 00D1:N 00C3:A 00D5:O"
Add-Accents "." "017C:z 017B:Z 0117:e"
Add-Accents "=" "0101:a 0113:e 012B:i 014D:o 016B:u"
Add-Accents "v" "010D:c 010F:d 011B:e 013E:l 0148:n 0159:r 0161:s 0165:t 017E:z 010C:C 010E:D 011A:E 013D:L 0147:N 0158:R 0160:S 0164:T 017D:Z"
Add-Accents "c" "00E7:c 00C7:C 015F:s 0163:t 015E:S 0162:T"
Add-Accents "r" "016F:u 016E:U"
Add-Accents "H" "0151:o 0171:u 0150:O 0170:U"
Add-Accents "k" "0105:a 0119:e 0104:A 0118:E"
Add-Accents "u" "0103:a 011F:g 0102:A 011E:G"
$escapeTable[0x0142] = '{\l}'; $escapeTable[0x0141] = '{\L}'; $escapeTable[0x00DF] = '{\ss}'
$escapeTable[0x00F8] = '{\o}'; $escapeTable[0x00D8] = '{\O}'; $escapeTable[0x00E6] = '{\ae}'; $escapeTable[0x00C6] = '{\AE}'
$escapeTable[0x00E5] = '{\aa}'; $escapeTable[0x00C5] = '{\AA}'; $escapeTable[0x0131] = '{\i}'
$escapeTable[0x2013] = '--'; $escapeTable[0x2014] = '---'; $escapeTable[0x2018] = '`'; $escapeTable[0x2019] = "'"
$escapeTable[0x201C] = '``'; $escapeTable[0x201D] = "''"; $escapeTable[0x00A0] = '~'; $escapeTable[0x00D7] = '$\times$'

$rxStatus = [regex]::new('^\s*%+\s*(VERIFIED|PARTIAL|TODO|OVERENE|CIASTOCNE)\b(.*)$', $rxNone)
$rxStatusVerified = [regex]::new('^\s*(\d{4}-\d{2}-\d{2})\s+\(.+\)', $rxNone)
$rxStatusPartial = [regex]::new('^\s*(\d{4}-\d{2}-\d{2}):\s*\S', $rxNone)
$rxStatusTodo = [regex]::new('^:\s*\S', $rxNone)
$rxDate = [regex]::new('(\d{4}-\d{2}-\d{2})', $rxNone)
$rxComment = [regex]::new('(?<=(?:^|[^\\])(?:\\\\)*)%.*$', $rxNone)
$rxCite = [regex]::new('\\(?:[Cc]ite(?:t|p|alt|alp|author|year|yearpar|num|title|url|date)?|[Pp]arencite|[Tt]extcite|[Aa]utocite|[Ff]ootcite|[Ss]martcite|[Ss]upercite|[Ff]ullcite|[Ff]ootfullcite|nocite)\*?(?:\s*\[[^\]]*\]){0,2}\s*\{([^{}]*)\}', $rxNone)
$rxBibliography = [regex]::new('\\bibliography\s*\{([^{}]*)\}', $rxNone)
$rxAddResource = [regex]::new('\\addbibresource\s*(?:\[[^\]]*\])?\s*\{([^{}]*)\}', $rxNone)
$rxBiblatexUse = [regex]::new('\\(?:usepackage\s*(?:\[[^\]]*\])?\s*\{biblatex\}|printbibliography|addbibresource)', $rxNone)
$rxEntryStart = [regex]::new('\G\s*([A-Za-z]+)\s*([{(])', $rxNone)
$rxKey = [regex]::new('\G\s*([^\s,{}()=]+)\s*(,|\}|\))', $rxNone)
$rxFieldName = [regex]::new('\G([A-Za-z][A-Za-z0-9_:.\-]*)\s*=\s*', $rxNone)
$rxDoi = [regex]::new('^10\.\d{4,9}/\S+$', $rxNone)
$rxAllCaps = [regex]::new('(?<![\p{L}\\])[A-Z]{2,}(?![\p{L}])', $rxNone)
$rxCamelCase = [regex]::new('(?<![\p{L}\\])[A-Z][a-z]+[A-Z][A-Za-z]*(?![\p{L}])', $rxNone)
$romanNumerals = New-StringSet @("II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII")

# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------

$script:findings = New-Object System.Collections.Generic.List[object]
$categoryOrder = @("bib-file", "syntax", "cite-missing", "cite-case", "unused", "duplicate-key", "duplicate-doi", "duplicate-entry",
    "canonical-missing", "canonical-diff", "status", "required", "recommended", "doi", "isbn", "pages", "year",
    "non-ascii", "field", "biblatex", "author", "title-case", "key-style")

function Get-DisplayPath([string]$FullName) {
    $root = $workspace.TrimEnd('\') + '\'
    if ($FullName.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $FullName.Substring($root.Length).Replace('\', '/')
    }
    return $FullName.Replace('\', '/')
}

function Add-Finding([string]$File, [int]$Line, [string]$Category, [string]$Key, [string]$Message) {
    $script:findings.Add([pscustomobject]@{
            File     = $File
            Line     = $Line
            Category = $Category
            Key      = $Key
            Message  = $Message
        })
}

function Format-Short([string]$Text, [int]$Limit = 60) {
    $clean = ($Text -replace '\s+', ' ').Trim()
    if ($clean.Length -gt $Limit) { return $clean.Substring(0, $Limit - 3) + "..." }
    return $clean
}

# ---------------------------------------------------------------------------
# .bib parser
# ---------------------------------------------------------------------------

function Get-LineNumber([int[]]$LineStarts, [int]$Offset) {
    $index = [Array]::BinarySearch($LineStarts, $Offset)
    if ($index -lt 0) { $index = (-bnot $index) - 1 }
    return $index + 1
}

# Index of the brace that closes the one at $Open (unescaped braces are counted), or -1.
function Find-ClosingBrace([string]$Text, [int]$Open) {
    $depth = 0
    for ($i = $Open; $i -lt $Text.Length; $i++) {
        $c = $Text[$i]
        if ($c -eq '\') { $i++; continue }
        if ($c -eq '{') { $depth++ }
        elseif ($c -eq '}') {
            $depth--
            if ($depth -eq 0) { return $i }
        }
    }
    return -1
}

# Index of the quote that closes the one at $Open (quotes inside braces do not count), or -1.
function Find-ClosingQuote([string]$Text, [int]$Open) {
    $depth = 0
    for ($i = $Open + 1; $i -lt $Text.Length; $i++) {
        $c = $Text[$i]
        if ($c -eq '\') { $i++; continue }
        if ($c -eq '{') { $depth++ }
        elseif ($c -eq '}') { $depth-- }
        elseif ($c -eq '"' -and $depth -le 0) { return $i }
    }
    return -1
}

function Read-BibFile([string]$FullName) {
    $display = Get-DisplayPath $FullName
    $text = [System.IO.File]::ReadAllText($FullName, $utf8)
    $lines = $text -split "`r?`n"
    $starts = New-Object System.Collections.Generic.List[int]
    $starts.Add(0)
    for ($i = 0; $i -lt $text.Length; $i++) {
        if ($text[$i] -eq "`n") { $starts.Add($i + 1) }
    }
    $lineStarts = $starts.ToArray()

    $entries = New-Object System.Collections.Generic.List[object]
    $position = 0
    while ($position -lt $text.Length) {
        $at = $text.IndexOf('@', $position)
        if ($at -lt 0) { break }
        $atLine = Get-LineNumber $lineStarts $at
        $before = $text.Substring($lineStarts[$atLine - 1], $at - $lineStarts[$atLine - 1])
        if ($before.TrimStart().StartsWith('%')) { $position = $at + 1; continue }    # "@" inside a % comment line

        $start = $rxEntryStart.Match($text, $at + 1)
        if (-not $start.Success) {
            Add-Finding $display $atLine "syntax" "" "cannot read an entry type after '@'"
            $position = $at + 1
            continue
        }
        $type = $start.Groups[1].Value.ToLowerInvariant()
        $open = $start.Groups[2].Value
        $close = if ($open -eq '{') { '}' } else { ')' }
        $cursor = $start.Index + $start.Length

        if ($ignoredTypes.Contains($type)) {
            $end = Find-ClosingBrace $text ($cursor - 1)
            if ($open -eq '(') { $end = $text.IndexOf(')', $cursor) }
            if ($end -lt 0) { $position = $cursor; continue }
            $position = $end + 1
            continue
        }

        $keyMatch = $rxKey.Match($text, $cursor)
        if (-not $keyMatch.Success) {
            Add-Finding $display $atLine "syntax" "" "entry of type @$type has no readable key"
            $position = $cursor
            continue
        }
        $key = $keyMatch.Groups[1].Value
        $cursor = $keyMatch.Index + $keyMatch.Length
        $fields = New-Object 'System.Collections.Specialized.OrderedDictionary'
        $fieldLines = @{}
        $repeated = New-Object System.Collections.Generic.List[string]
        $ended = ($keyMatch.Groups[2].Value -ne ',')
        $broken = $false

        while (-not $ended) {
            while ($cursor -lt $text.Length -and ($text[$cursor] -match '[\s,]')) { $cursor++ }
            if ($cursor -ge $text.Length) { $broken = $true; break }
            if ($text[$cursor] -eq $close) { $cursor++; $ended = $true; break }
            $nameMatch = $rxFieldName.Match($text, $cursor)
            if (-not $nameMatch.Success) { $broken = $true; break }
            $name = $nameMatch.Groups[1].Value.ToLowerInvariant()
            $fieldLine = Get-LineNumber $lineStarts $nameMatch.Index
            $cursor = $nameMatch.Index + $nameMatch.Length

            $pieces = 0
            $value = New-Object System.Text.StringBuilder
            while ($true) {
                while ($cursor -lt $text.Length -and [char]::IsWhiteSpace($text[$cursor])) { $cursor++ }
                if ($cursor -ge $text.Length) { $broken = $true; break }
                $c = $text[$cursor]
                if ($c -eq '{') {
                    $closing = Find-ClosingBrace $text $cursor
                    if ($closing -lt 0) { $broken = $true; break }
                    [void]$value.Append($text.Substring($cursor + 1, $closing - $cursor - 1))
                    $cursor = $closing + 1
                }
                elseif ($c -eq '"') {
                    $closing = Find-ClosingQuote $text $cursor
                    if ($closing -lt 0) { $broken = $true; break }
                    [void]$value.Append($text.Substring($cursor + 1, $closing - $cursor - 1))
                    $cursor = $closing + 1
                }
                else {
                    $bare = [regex]::Match($text.Substring($cursor, [math]::Min(80, $text.Length - $cursor)), '^[^\s,#{}"()]+')
                    if (-not $bare.Success) { $broken = $true; break }
                    [void]$value.Append($bare.Value)
                    $cursor += $bare.Length
                }
                $pieces++
                while ($cursor -lt $text.Length -and [char]::IsWhiteSpace($text[$cursor])) { $cursor++ }
                if ($cursor -lt $text.Length -and $text[$cursor] -eq '#') { $cursor++; [void]$value.Append(' # '); continue }
                break
            }
            if ($broken) { break }
            if ($fields.Contains($name)) { $repeated.Add($name) } else { $fields.Add($name, $value.ToString()); $fieldLines[$name] = $fieldLine }
        }

        if ($broken) {
            Add-Finding $display $atLine "syntax" $key "entry cannot be parsed (unbalanced braces or quotes, or a missing comma); the rest of the file may be affected"
            $nextEntry = [regex]::Match($text.Substring([math]::Min($cursor, $text.Length)), '\r?\n\s*@')
            if ($nextEntry.Success) { $position = $cursor + $nextEntry.Index + 1 } else { $position = $text.Length }
            continue
        }
        foreach ($name in $repeated) {
            Add-Finding $display $atLine "syntax" $key "field '$name' is given twice; BibTeX uses the first"
        }

        # Comment block directly above the entry (contiguous lines that start with %).
        $comments = New-Object System.Collections.Generic.List[object]
        $above = $atLine - 2
        while ($above -ge 0 -and $lines[$above].TrimStart().StartsWith('%')) {
            $comments.Insert(0, [pscustomobject]@{ Line = ($above + 1); Text = $lines[$above] })
            $above--
        }

        $entries.Add([pscustomobject]@{
                Key        = $key
                Type       = $type
                Line       = $atLine
                Fields     = $fields
                FieldLines = $fieldLines
                Comments   = $comments
                File       = $display
            })
        $position = $cursor
    }
    return [pscustomobject]@{ Path = $FullName; Display = $display; Lines = $lines; Entries = $entries }
}

# ---------------------------------------------------------------------------
# Field checks
# ---------------------------------------------------------------------------

function Test-IsbnValue([string]$Value) {
    $digits = ($Value -replace '[-\s]', '')
    if ($digits -match '^\d{13}$') {
        $sum = 0
        for ($i = 0; $i -lt 12; $i++) {
            $weight = 1
            if ($i % 2 -eq 1) { $weight = 3 }
            $sum += [int][string]$digits[$i] * $weight
        }
        $expected = (10 - ($sum % 10)) % 10
        if ($expected -ne [int][string]$digits[12]) { return "ISBN-13 check digit is $($digits[12]); expected $expected" }
        return $null
    }
    if ($digits -match '^\d{9}[\dXx]$') {
        $sum = 0
        for ($i = 0; $i -lt 9; $i++) { $sum += [int][string]$digits[$i] * (10 - $i) }
        $expected = (11 - ($sum % 11)) % 11
        $expectedText = [string]$expected
        if ($expected -eq 10) { $expectedText = "X" }
        $actual = ([string]$digits[9]).ToUpperInvariant()
        if ($actual -ne $expectedText) { return "ISBN-10 check digit is $actual; expected $expectedText" }
        return $null
    }
    return "not an ISBN-10 or ISBN-13 (found '$Value')"
}

function Test-PagesValue([string]$Value) {
    $pages = $Value.Trim()
    $single = '^[A-Za-z]{0,2}\d+(?::\d+)?$'
    $range = '^[A-Za-z]{0,2}\d+(?::\d+)?--[A-Za-z]{0,2}\d+(?::\d+)?$'
    if ($pages -match $single -or $pages -match $range) { return $null }
    if ($pages -match '^\S+\s*(?:-|\u2013|\u2014|---)\s*\S+$' -and $pages -notmatch '--') {
        return "page range '$pages': use '--' (en dash), for example 151--158"
    }
    if ($pages -match '^\s*pp?\.') { return "page range '$pages': drop the 'p.' prefix" }
    if ($pages -match '\s--\s|--\s|\s--') { return "page range '$pages': no spaces around '--'" }
    return "page format '$pages' is not a number, a range 151--158 or an article number 12:1--12:17"
}

# Splits an author or editor list at " and " outside braces.
function Split-Names([string]$Value) {
    $names = New-Object System.Collections.Generic.List[string]
    $depth = 0
    $current = New-Object System.Text.StringBuilder
    $i = 0
    while ($i -lt $Value.Length) {
        $c = $Value[$i]
        if ($c -eq '{') { $depth++ }
        elseif ($c -eq '}') { $depth-- }
        if ($depth -eq 0 -and $Value.Length - $i -ge 5 -and $Value.Substring($i, 5) -match '^\s[Aa][Nn][Dd]\s') {
            $names.Add($current.ToString().Trim())
            [void]$current.Clear()
            $i += 5
            continue
        }
        [void]$current.Append($c)
        $i++
    }
    $names.Add($current.ToString().Trim())
    return , $names
}

function Get-UnprotectedText([string]$Title) {
    # The title with everything inside braces removed.
    $builder = New-Object System.Text.StringBuilder
    $depth = 0
    foreach ($c in $Title.ToCharArray()) {
        if ($c -eq '{') { $depth++; continue }
        if ($c -eq '}') { if ($depth -gt 0) { $depth-- }; continue }
        if ($depth -eq 0) { [void]$builder.Append($c) } else { [void]$builder.Append(' ') }
    }
    return $builder.ToString()
}

function Get-FieldLine($Entry, [string]$Name) {
    if ($Entry.FieldLines.ContainsKey($Name)) { return $Entry.FieldLines[$Name] }
    return $Entry.Line
}

# $Biblatex: the file belongs to a biblatex project (UTF-8 and biblatex fields are fine).
function Test-Entry($Entry, [bool]$Biblatex) {
    $file = $Entry.File
    $key = $Entry.Key
    $fields = $Entry.Fields
    $type = $Entry.Type

    # entry type
    if (-not $bibtexTypes.Contains($type) -and -not $Biblatex) {
        if ($biblatexTypes.Contains($type)) {
            Add-Finding $file $Entry.Line "biblatex" $key "entry type @$type exists only in biblatex; use a BibTeX type (@misc, @techreport, @mastersthesis)"
        }
        else {
            Add-Finding $file $Entry.Line "syntax" $key "unknown entry type @$type"
        }
    }

    # key style
    if (-not $Biblatex -and $key -notmatch '^[A-Za-z0-9]+$') {
        Add-Finding $file $Entry.Line "key-style" $key "key has characters outside A-Z a-z 0-9"
    }

    # required and recommended fields
    $spec = $null
    if ($type -eq "misc") {
        if ($fields.Contains("eprint")) { $spec = $miscPreprint } else { $spec = $miscOther }
    }
    elseif ($requiredFields.ContainsKey($type)) { $spec = $requiredFields[$type] }
    if ($null -ne $spec) {
        foreach ($need in $spec.Required) {
            $present = $false
            foreach ($alternative in ($need -split '\|')) {
                if ($fields.Contains($alternative.ToLowerInvariant()) -and $fields[$alternative.ToLowerInvariant()].Trim() -ne "") { $present = $true; break }
            }
            if (-not $present) {
                $alternatives = $need -split '\|'
                if ($alternatives.Count -gt 1) { $needText = "one of the fields: " + ($alternatives -join ", ") }
                else { $needText = "the field '$need'" }
                Add-Finding $file $Entry.Line "required" $key "@$type needs $needText"
            }
        }
        foreach ($want in $spec.Recommended) {
            $present = $false
            foreach ($alternative in ($want -split '\|')) {
                if ($fields.Contains($alternative.ToLowerInvariant()) -and $fields[$alternative.ToLowerInvariant()].Trim() -ne "") { $present = $true; break }
            }
            if (-not $present) { Add-Finding $file $Entry.Line "recommended" $key "field '$want' is missing (add it, or accept that it is not available)" }
        }
    }

    # fields that do not belong
    foreach ($name in $fields.Keys) {
        if ($forbiddenFields.Contains($name) -or $name -like "mendeley-*" -or $name -like "bdsk-*") {
            Add-Finding $file (Get-FieldLine $Entry $name) "field" $key "field '$name' does not belong in the bibliography; delete it"
        }
        elseif (-not $Biblatex -and $biblatexFields.Contains($name)) {
            $hint = ""
            if ($name -eq "date") { $hint = " (use year)" }
            elseif ($name -eq "journaltitle") { $hint = " (use journal)" }
            elseif ($name -eq "location") { $hint = " (use address)" }
            elseif ($name -eq "urldate") { $hint = " (put the access date in note)" }
            elseif ($name -eq "eprinttype") { $hint = " (use archivePrefix)" }
            elseif ($name -eq "eprintclass") { $hint = " (use primaryClass)" }
            Add-Finding $file (Get-FieldLine $Entry $name) "biblatex" $key "field '$name' exists only in biblatex$hint"
        }
    }

    # year
    if ($fields.Contains("year") -and $fields["year"].Trim() -notmatch '^\d{4}$') {
        Add-Finding $file (Get-FieldLine $Entry "year") "year" $key "year '$($fields["year"].Trim())' is not four digits"
    }

    # DOI
    if ($fields.Contains("doi")) {
        $doi = $fields["doi"].Trim()
        if ($doi -match '^(?i:https?://(?:dx\.)?doi\.org/|doi:\s*)') {
            Add-Finding $file (Get-FieldLine $Entry "doi") "doi" $key "write the bare DOI without 'https://doi.org/' or 'doi:' (found '$(Format-Short $doi)')"
        }
        elseif ($doi -notmatch $rxDoi) {
            Add-Finding $file (Get-FieldLine $Entry "doi") "doi" $key "'$(Format-Short $doi)' is not a plausible DOI (10.<registrant>/<suffix>, no spaces)"
        }
        elseif ($doi -match '[.,;]$') {
            Add-Finding $file (Get-FieldLine $Entry "doi") "doi" $key "DOI ends with punctuation: '$(Format-Short $doi)'"
        }
    }
    if ($fields.Contains("url") -and $fields["url"].Trim() -match '^(?i:https?://(?:dx\.)?doi\.org/)') {
        Add-Finding $file (Get-FieldLine $Entry "url") "doi" $key "url repeats a DOI; move it to the 'doi' field"
    }

    # ISBN
    if ($fields.Contains("isbn")) {
        foreach ($part in (($fields["isbn"] -replace '\([^)]*\)', '') -split '[;,]')) {
            if ($part.Trim() -eq "") { continue }
            $problem = Test-IsbnValue $part.Trim()
            if ($null -ne $problem) { Add-Finding $file (Get-FieldLine $Entry "isbn") "isbn" $key $problem }
        }
    }

    # pages
    if ($fields.Contains("pages")) {
        $problem = Test-PagesValue $fields["pages"]
        if ($null -ne $problem) { Add-Finding $file (Get-FieldLine $Entry "pages") "pages" $key $problem }
    }

    # authors and editors
    foreach ($role in @("author", "editor")) {
        if (-not $fields.Contains($role)) { continue }
        $names = Split-Names $fields[$role]
        foreach ($name in $names) {
            if ($name -match '^(?i:others)$') {
                Add-Finding $file (Get-FieldLine $Entry $role) "author" $key "'and others' in ${role}: list all authors"
            }
            elseif ($name -match ';|\s&\s') {
                Add-Finding $file (Get-FieldLine $Entry $role) "author" $key "separate names with ' and ', not ';' or '&'"
            }
            elseif ($name -ne "" -and -not $name.StartsWith('{') -and $name -notmatch ',') {
                Add-Finding $file (Get-FieldLine $Entry $role) "author" $key "name '$(Format-Short $name 40)' is not in 'Surname, Given' form"
            }
        }
    }

    # title capitals
    if ($fields.Contains("title") -and -not $Biblatex) {
        $title = $fields["title"].Trim()
        if ($title.StartsWith('{') -and $title.EndsWith('}') -and (Find-ClosingBrace $title 0) -eq $title.Length - 1) {
            Add-Finding $file (Get-FieldLine $Entry "title") "title-case" $key "do not wrap the whole title in braces; protect single words"
        }
        else {
            $plain = Get-UnprotectedText $title
            $words = New-Object System.Collections.Generic.List[string]
            foreach ($m in $rxAllCaps.Matches($plain)) { if (-not $romanNumerals.Contains($m.Value) -and $m.Value -ne "I") { $words.Add($m.Value) } }
            foreach ($m in $rxCamelCase.Matches($plain)) { $words.Add($m.Value) }
            if ($words.Count -gt 0) {
                Add-Finding $file (Get-FieldLine $Entry "title") "title-case" $key ("protect capitals a style may lowercase: " + (($words | Select-Object -Unique | ForEach-Object { '{' + $_ + '}' }) -join ", "))
            }
        }
    }

    # non-ASCII characters (BibTeX only)
    if (-not $Biblatex) {
        foreach ($name in $fields.Keys) {
            $value = $fields[$name]
            $found = New-Object System.Collections.Generic.List[string]
            foreach ($c in $value.ToCharArray()) {
                if ([int]$c -gt 127) {
                    $code = [int]$c
                    $suggestion = "no known escape"
                    if ($escapeTable.ContainsKey($code)) { $suggestion = $escapeTable[$code] }
                    $label = "U+{0:X4} -> {1}" -f $code, $suggestion
                    if (-not $found.Contains($label)) { $found.Add($label) }
                }
            }
            if ($found.Count -gt 0) {
                Add-Finding $file (Get-FieldLine $Entry $name) "non-ascii" $key "field '$name' contains non-ASCII characters: $($found -join '; ')"
            }
        }
    }
}

# ---------------------------------------------------------------------------
# Status line of canonical entries
# ---------------------------------------------------------------------------

# Returns an object { Tag; Text; Line; Count } for the weakest status line above the entry, or $null.
function Get-EntryStatus($Entry) {
    $found = New-Object System.Collections.Generic.List[object]
    foreach ($comment in $Entry.Comments) {
        $m = $rxStatus.Match($comment.Text)
        if ($m.Success) {
            $found.Add([pscustomobject]@{ Tag = $m.Groups[1].Value; Rest = $m.Groups[2].Value; Line = $comment.Line })
        }
    }
    if ($found.Count -eq 0) { return $null }
    $rank = @{ "TODO" = 0; "PARTIAL" = 1; "CIASTOCNE" = 1; "VERIFIED" = 2; "OVERENE" = 2 }
    $weakest = $found[0]
    foreach ($candidate in $found) { if ($rank[$candidate.Tag] -lt $rank[$weakest.Tag]) { $weakest = $candidate } }
    return [pscustomobject]@{ Tag = $weakest.Tag; Rest = $weakest.Rest; Line = $weakest.Line; Count = $found.Count }
}

# $Report: add findings (canonical mode); returns the status object either way.
function Test-Status($Entry, [bool]$Report, $LegacyCounter) {
    $status = Get-EntryStatus $Entry
    if ($null -eq $status) {
        if ($Report) { Add-Finding $Entry.File $Entry.Line "status" $Entry.Key "no status line above the entry (% VERIFIED <date> (<where>) | % PARTIAL <date>: <what> | % TODO: <what>)" }
        return $null
    }
    if (-not $Report) { return $status }
    if ($status.Count -gt 1) {
        Add-Finding $Entry.File $status.Line "status" $Entry.Key "$($status.Count) status lines above the entry; keep one (the weakest is used)"
    }
    $tag = $status.Tag
    if ($tag -eq "OVERENE" -or $tag -eq "CIASTOCNE") { $LegacyCounter.Value++; return $status }
    $ok = $true
    if ($tag -eq "VERIFIED") { $ok = $rxStatusVerified.IsMatch($status.Rest) }
    elseif ($tag -eq "PARTIAL") { $ok = $rxStatusPartial.IsMatch($status.Rest) }
    elseif ($tag -eq "TODO") { $ok = $rxStatusTodo.IsMatch($status.Rest) }
    if (-not $ok) {
        $form = "% VERIFIED 2026-10-08 (<where>)"
        if ($tag -eq "PARTIAL") { $form = "% PARTIAL 2026-10-08: <what is and is not verified>" }
        elseif ($tag -eq "TODO") { $form = "% TODO: <what>" }
        Add-Finding $Entry.File $status.Line "status" $Entry.Key "status line is not in the form '$form'"
    }
    $date = $rxDate.Match($status.Rest)
    if ($date.Success) {
        $parsed = [datetime]::MinValue
        if (-not [datetime]::TryParseExact($date.Groups[1].Value, "yyyy-MM-dd", [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::None, [ref]$parsed)) {
            Add-Finding $Entry.File $status.Line "status" $Entry.Key "'$($date.Groups[1].Value)' is not a valid ISO date"
        }
        elseif ($parsed.Date -gt (Get-Date).Date) {
            Add-Finding $Entry.File $status.Line "status" $Entry.Key "status date $($date.Groups[1].Value) is in the future"
        }
    }
    return $status
}

# ---------------------------------------------------------------------------
# File-level checks
# ---------------------------------------------------------------------------

# Comment lines are read as text by 8-bit BibTeX; non-ASCII there breaks the run.
function Test-CommentsAscii($BibFile) {
    for ($i = 0; $i -lt $BibFile.Lines.Length; $i++) {
        $text = $BibFile.Lines[$i]
        if ($text.TrimStart().StartsWith('%') -and $text -match '[^\x00-\x7F]') {
            Add-Finding $BibFile.Display ($i + 1) "non-ascii" "" "comment line has non-ASCII characters (8-bit BibTeX fails on them); write it without diacritics"
        }
    }
}

function Test-Duplicates($Entries) {
    $exact = New-Object 'System.Collections.Generic.Dictionary[string,object]' ([System.StringComparer]::Ordinal)
    $folded = @{}
    $dois = @{}
    $titles = @{}
    foreach ($entry in $Entries) {
        $key = $entry.Key
        if ($exact.ContainsKey($key)) {
            Add-Finding $entry.File $entry.Line "duplicate-key" $key "key already used at line $($exact[$key].Line) of $($exact[$key].File)"
        }
        elseif ($folded.ContainsKey($key.ToLowerInvariant())) {
            $other = $folded[$key.ToLowerInvariant()]
            Add-Finding $entry.File $entry.Line "duplicate-key" $key "BibTeX treats this key as '$($other.Key)' (line $($other.Line)): keys are case-insensitive"
        }
        else {
            $exact[$key] = $entry
            $folded[$key.ToLowerInvariant()] = $entry
        }
        if ($entry.Fields.Contains("doi")) {
            $doi = $entry.Fields["doi"].Trim().ToLowerInvariant() -replace '^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)', ''
            if ($doi -ne "") {
                if ($dois.ContainsKey($doi)) {
                    Add-Finding $entry.File $entry.FieldLines["doi"] "duplicate-doi" $key "DOI $doi is also the DOI of '$($dois[$doi].Key)' (line $($dois[$doi].Line))"
                }
                else { $dois[$doi] = $entry }
            }
        }
        if ($entry.Fields.Contains("title") -and $entry.Fields.Contains("year")) {
            $normalized = (($entry.Fields["title"] -replace '[^\p{L}\p{Nd}]', '').ToLowerInvariant()) + "|" + $entry.Fields["year"].Trim()
            if ($titles.ContainsKey($normalized) -and $titles[$normalized].Key -ne $key) {
                Add-Finding $entry.File $entry.Line "duplicate-entry" $key "same title and year as '$($titles[$normalized].Key)' (line $($titles[$normalized].Line))"
            }
            elseif (-not $titles.ContainsKey($normalized)) { $titles[$normalized] = $entry }
        }
    }
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

$script:filesRead = New-Object System.Collections.Generic.List[object]
$legacyCount = 0
$citedCount = 0
$texCount = 0
$projectKind = ""

if ($CanonicalOnly) {
    $canonicalFile = Read-BibFile $canonicalPath
    $script:filesRead.Add($canonicalFile)
    Test-Duplicates $canonicalFile.Entries
    foreach ($entry in $canonicalFile.Entries) {
        Test-Entry $entry $false
        [void](Test-Status $entry $true ([ref]$legacyCount))
    }
    Test-CommentsAscii $canonicalFile
    if ($legacyCount -gt 0) {
        Add-Finding $canonicalFile.Display 0 "status" "" "$legacyCount entries carry legacy status tags (OVERENE/CIASTOCNE); they are accepted, convert them to VERIFIED/PARTIAL"
    }
}
else {
    # --- sources
    $texFiles = @(Get-ChildItem -LiteralPath $projectDirectory -Recurse -File -Filter *.tex | Sort-Object FullName)
    $texCount = $texFiles.Count
    $citations = New-Object System.Collections.Generic.List[object]
    $bibNames = New-Object System.Collections.Generic.List[string]
    $biblatex = $false
    $nociteAll = $false
    $bibliographyDeclared = $false
    foreach ($tex in $texFiles) {
        $display = Get-DisplayPath $tex.FullName
        $lines = [System.IO.File]::ReadAllLines($tex.FullName, $utf8)
        for ($i = 0; $i -lt $lines.Length; $i++) {
            $line = $rxComment.Replace($lines[$i], '')
            if ($line.IndexOf('cite', [System.StringComparison]::Ordinal) -ge 0) {
                foreach ($m in $rxCite.Matches($line)) {
                    foreach ($part in $m.Groups[1].Value.Split(',')) {
                        $citeKey = $part.Trim()
                        if ($citeKey -eq "") { continue }
                        if ($citeKey -eq "*") { $nociteAll = $true; continue }
                        if ($citeKey.Contains('#')) { continue }          # macro argument in a \newcommand
                        $citations.Add([pscustomobject]@{ Key = $citeKey; File = $display; Line = ($i + 1) })
                    }
                }
            }
            if ($line.IndexOf('bib', [System.StringComparison]::Ordinal) -ge 0) {
                foreach ($m in $rxBibliography.Matches($line)) {
                    $bibliographyDeclared = $true
                    foreach ($part in $m.Groups[1].Value.Split(',')) { if ($part.Trim() -ne "") { $bibNames.Add($part.Trim()) } }
                }
                foreach ($m in $rxAddResource.Matches($line)) {
                    $bibliographyDeclared = $true
                    $biblatex = $true
                    $bibNames.Add($m.Groups[1].Value.Trim())
                }
            }
            if ($rxBiblatexUse.IsMatch($line)) { $biblatex = $true }
        }
    }
    # preamble and class files may load biblatex too
    foreach ($sty in @(Get-ChildItem -LiteralPath $projectDirectory -Recurse -File | Where-Object { $_.Extension -eq ".sty" -or $_.Extension -eq ".cls" })) {
        if (Select-String -LiteralPath $sty.FullName -Pattern '\\RequirePackage\s*(?:\[[^\]]*\])?\s*\{biblatex\}' -Quiet) { $biblatex = $true }
    }
    $projectKind = "BibTeX"
    if ($biblatex) { $projectKind = "biblatex" }

    # --- .bib files of the project
    $allBib = @(Get-ChildItem -LiteralPath $projectDirectory -Recurse -File -Filter *.bib | Sort-Object FullName)
    $bibFiles = New-Object System.Collections.Generic.List[string]
    foreach ($name in $bibNames) {
        $file = $name
        if ([System.IO.Path]::GetExtension($file) -ne ".bib") { $file = $file + ".bib" }
        $candidate = Join-Path $projectDirectory $file
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
            $leaf = [System.IO.Path]::GetFileName($file)
            $match = $allBib | Where-Object { $_.Name -eq $leaf } | Select-Object -First 1
            if ($null -ne $match) { $candidate = $match.FullName }
        }
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $full = (Get-Item -LiteralPath $candidate).FullName
            if (-not $bibFiles.Contains($full)) { $bibFiles.Add($full) }
        }
        else {
            Add-Finding (Get-DisplayPath $projectDirectory) 0 "bib-file" "" "the source names '$name' but there is no such .bib file in the project"
        }
    }
    if ($bibFiles.Count -eq 0 -and -not $bibliographyDeclared) {
        foreach ($bib in $allBib) { $bibFiles.Add($bib.FullName) }
    }
    if ($bibFiles.Count -eq 0) {
        Add-Finding (Get-DisplayPath $projectDirectory) 0 "bib-file" "" "the project has no .bib file"
    }

    $projectEntries = New-Object System.Collections.Generic.List[object]
    foreach ($bibPath in $bibFiles) {
        $parsed = Read-BibFile $bibPath
        $script:filesRead.Add($parsed)
        if (-not $biblatex) { Test-CommentsAscii $parsed }
        foreach ($entry in $parsed.Entries) { $projectEntries.Add($entry) }
    }
    Test-Duplicates $projectEntries

    # --- canonical file
    $canonicalEntries = New-Object 'System.Collections.Generic.Dictionary[string,object]' ([System.StringComparer]::Ordinal)
    if ($canonicalFound) {
        $canonicalFile = Read-BibFile $canonicalPath
        foreach ($entry in $canonicalFile.Entries) {
            if (-not $canonicalEntries.ContainsKey($entry.Key)) { $canonicalEntries[$entry.Key] = $entry }
        }
    }
    else {
        Add-Finding (Get-DisplayPath $canonicalPath) 0 "bib-file" "" "canonical file not found; the comparison with it is skipped"
    }
    $canonicalFolded = @{}
    foreach ($name in $canonicalEntries.Keys) { $canonicalFolded[$name.ToLowerInvariant()] = $canonicalEntries[$name] }

    # --- citations against entries
    $byKey = New-Object 'System.Collections.Generic.Dictionary[string,object]' ([System.StringComparer]::Ordinal)
    $byFolded = @{}
    foreach ($entry in $projectEntries) {
        if (-not $byKey.ContainsKey($entry.Key)) { $byKey[$entry.Key] = $entry }
        if (-not $byFolded.ContainsKey($entry.Key.ToLowerInvariant())) { $byFolded[$entry.Key.ToLowerInvariant()] = $entry }
    }
    $cited = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    $reported = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    foreach ($citation in $citations) {
        [void]$cited.Add($citation.Key)
        if ($byKey.ContainsKey($citation.Key)) { continue }
        if (-not $reported.Add($citation.Key)) { continue }
        if ($byFolded.ContainsKey($citation.Key.ToLowerInvariant())) {
            Add-Finding $citation.File $citation.Line "cite-case" $citation.Key "the .bib key is '$($byFolded[$citation.Key.ToLowerInvariant()].Key)'; write it with exactly that case"
        }
        else {
            $hint = ""
            if ($canonicalEntries.ContainsKey($citation.Key)) { $hint = " (it is in the canonical file: copy the entry)" }
            Add-Finding $citation.File $citation.Line "cite-missing" $citation.Key "no entry with this key in the project .bib$hint"
        }
    }
    $citedCount = $cited.Count

    # --- entry checks
    foreach ($entry in $projectEntries) {
        if (-not $nociteAll -and -not $cited.Contains($entry.Key)) {
            $caseCited = $false
            foreach ($c in $cited) { if ($c.ToLowerInvariant() -eq $entry.Key.ToLowerInvariant()) { $caseCited = $true; break } }
            if (-not $caseCited) { Add-Finding $entry.File $entry.Line "unused" $entry.Key "entry is never cited" }
        }
        Test-Entry $entry $biblatex

        if (-not $canonicalFound) { continue }
        $reference = $null
        if ($canonicalEntries.ContainsKey($entry.Key)) { $reference = $canonicalEntries[$entry.Key] }
        elseif ($canonicalFolded.ContainsKey($entry.Key.ToLowerInvariant())) {
            $reference = $canonicalFolded[$entry.Key.ToLowerInvariant()]
            Add-Finding $entry.File $entry.Line "canonical-diff" $entry.Key "key differs in letter case from the canonical key '$($reference.Key)'"
        }
        if ($null -eq $reference) {
            $note = ""
            if ($biblatex) { $note = " (biblatex project: own entries may stay local)" }
            Add-Finding $entry.File $entry.Line "canonical-missing" $entry.Key "no entry with this key in the canonical file; add it there first$note"
            continue
        }
        if ($reference.Type -ne $entry.Type) {
            Add-Finding $entry.File $entry.Line "canonical-diff" $entry.Key "entry type @$($entry.Type) differs from canonical @$($reference.Type)"
        }
        $names = New-Object System.Collections.Generic.List[string]
        foreach ($name in $entry.Fields.Keys) { $names.Add($name) }
        foreach ($name in $reference.Fields.Keys) { if (-not $names.Contains($name)) { $names.Add($name) } }
        foreach ($name in $names) {
            $mine = $null
            $theirs = $null
            if ($entry.Fields.Contains($name)) { $mine = ($entry.Fields[$name] -replace '\s+', ' ').Trim() }
            if ($reference.Fields.Contains($name)) { $theirs = ($reference.Fields[$name] -replace '\s+', ' ').Trim() }
            $line = $entry.Line
            if ($entry.FieldLines.ContainsKey($name)) { $line = $entry.FieldLines[$name] }
            if ($null -eq $mine) {
                Add-Finding $entry.File $line "canonical-diff" $entry.Key "field '$name' is missing; canonical has '$(Format-Short $theirs)'"
            }
            elseif ($null -eq $theirs) {
                Add-Finding $entry.File $line "canonical-diff" $entry.Key "field '$name' is not in the canonical entry (project '$(Format-Short $mine)')"
            }
            elseif ($mine -cne $theirs) {
                Add-Finding $entry.File $line "canonical-diff" $entry.Key "field '$name' differs: project '$(Format-Short $mine)' vs canonical '$(Format-Short $theirs)'"
            }
        }
        # status of the canonical entry: only VERIFIED entries go into a submission
        $status = Test-Status $reference $false ([ref]$legacyCount)
        if ($null -eq $status) {
            Add-Finding $entry.File $entry.Line "status" $entry.Key "the canonical entry has no status line"
        }
        elseif ($status.Tag -eq "PARTIAL" -or $status.Tag -eq "CIASTOCNE") {
            Add-Finding $entry.File $entry.Line "status" $entry.Key "canonical status is $($status.Tag): finish the verification, or drop the unverified field, before submission"
        }
        elseif ($status.Tag -eq "TODO") {
            Add-Finding $entry.File $entry.Line "status" $entry.Key "canonical status is TODO: resolve it before submission"
        }
    }
}

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

$fileOrder = @{}
$position = 0
foreach ($file in $script:filesRead) { $fileOrder[$file.Display] = $position; $position++ }
foreach ($finding in $script:findings) {
    if (-not $fileOrder.ContainsKey($finding.File)) { $fileOrder[$finding.File] = $position; $position++ }
}

if (-not $Summary) {
    $sorted = $script:findings | Sort-Object @{ Expression = { $fileOrder[$_.File] } }, Line, Category, Key
    foreach ($finding in $sorted) {
        $label = ""
        if ($finding.Key -ne "") { $label = $finding.Key + ": " }
        Write-Output ("{0}:{1}: [{2}] {3}{4}" -f $finding.File, $finding.Line, $finding.Category, $label, $finding.Message)
    }
    if ($script:findings.Count -gt 0) { Write-Output "" }
}

if ($CanonicalOnly) {
    Write-Output "Mode: canonical file only"
}
else {
    $citeNote = "$citedCount distinct keys cited"
    if ($nociteAll) { $citeNote += ', \nocite{*} present' }
    Write-Output "Project: $(Get-DisplayPath $projectDirectory) ($projectKind; $texCount .tex files, $citeNote)"
}
foreach ($file in $script:filesRead) {
    Write-Output ("File: {0} ({1} entries)" -f $file.Display, $file.Entries.Count)
}
if (-not $CanonicalOnly -and $canonicalFound) { Write-Output "Canonical: $(Get-DisplayPath $canonicalPath)" }

$counts = @{}
foreach ($finding in $script:findings) {
    if ($counts.ContainsKey($finding.Category)) { $counts[$finding.Category]++ } else { $counts[$finding.Category] = 1 }
}
Write-Output ""
if ($script:findings.Count -eq 0) {
    Write-Output "Findings: 0"
}
else {
    Write-Output "Findings: $($script:findings.Count)"
    $listed = New-Object System.Collections.Generic.List[string]
    foreach ($category in $categoryOrder) { $listed.Add($category) }
    foreach ($category in $counts.Keys) { if (-not $listed.Contains($category)) { $listed.Add($category) } }
    foreach ($category in $listed) {
        if ($counts.ContainsKey($category)) { Write-Output ("  {0,-18} {1,4}" -f $category, $counts[$category]) }
    }
}

if ($null -ne $previousOutputEncoding) {
    try { [Console]::OutputEncoding = $previousOutputEncoding } catch { }
}
exit 0
