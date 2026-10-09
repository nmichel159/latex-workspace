<#
.SYNOPSIS
    Checks that an article project follows its venue template and builds on its own, then packs it into a zip
    that compiles at the recipient (journal, reviewer, co-author, arXiv) without anything from this workspace.

.DESCRIPTION
    Turns "the project is self-contained and follows the template" from a convention into a check with proof.
    Reads projects/<Project>, writes only to tmp/package-<Project>/ (staging, build logs) and
    outputs/<Project>/package/ (zip and PDF). Nothing under projects/, templates/, knowledge/ or archives/ is changed.

    A. Template conformance (static). The class of \documentclass{X} is searched as X.cls in templates/ (or
       -Template). Findings:
         [template-file]   FAIL: a .cls .bst .sty .clo .bbx .cbx .cfg .def of the project differs from the venue's
                           file of the same name (SHA-256), or the project uses X.cls but does not contain it
         [template-bst]    \bibliographystyle in the project names a style the template does not ship (the template
                           ships .bst files); a project without the command (the class sets the style) is not a finding
         [layout]          a command that overrides the venue's layout (geometry, setspace, spacing commands,
                           \setlength or assignment of page dimensions, \vspace{-...}, \pagestyle, \fontsize,
                           \titleformat, \setlist, redefined \section ... \maketitle); only when a template folder exists.
                           The list is fixed: an override written another way is not found. Files that are identical
                           to a template file are not checked. Remove the command or justify it in the project README.
         [template-origin] provenance of the template folder that ships the class, from templates/SOURCES.tsv
                           (columns folder kind version official_url linked_from archive sha256 retrieved note).
                           FAIL: no row for the folder (or no SOURCES.tsv); a row of kind venue whose official_url is
                           not https, whose archive file does not exist in the workspace, or whose archive has another
                           SHA-256 than the recorded one; an unknown kind; a class file in the project that no folder
                           of templates/ ships (its origin is not recorded at all). Note: kind other ("not a publisher
                           template"). Kind house: nothing. The report prints
                           "Template origin: <folder> (<kind>, <version>, <official_url>)".
       A standard class (no X.cls in the project or in templates/, but found in the TeX distribution) has no
       template folder: "Template: none (standard class X)" and A3-A5 are skipped.
    B. Self-containedness (static). \input \include \includegraphics \bibliography \addbibresource \documentclass
       \usepackage \RequirePackage \bibliographystyle \graphicspath are read from the .tex files (comments, verbatim
       and \verb removed):
         [outside]    FAIL: absolute path, or a path with ".." (the file is not inside the project folder)
         [missing]    FAIL: the target exists neither in the project nor (class, package, style, \input and
                      \includegraphics without a path) in the TeX distribution; targets that a \IfFileExists test
                      guards (optional files) and paths built from macros (# or \) are not checked
         [case]       FAIL: the file name differs from the name on disk in letter case; the build breaks on a
                      case-sensitive system (a journal server, Overleaf), which the round trip on Windows cannot show
         [filename]   a project file whose path has a space or a non-ASCII character
    T. No traces. Nothing that is sent may carry a trace of this workspace, of its tools or of an AI tool outside
       the disclosure the venue asks for. Scanned: (a) before staging (also with -CheckOnly), every project file that
       would be packaged, as it will be staged (comment lines that staging removes are skipped), and its path;
       (b) before the zip is written, every staged file as it will be zipped, the .bbl included; (c) metadata of
       images, in (a) and (b): PNG tEXt, zTXt, iTXt, eXIf chunks and the iCCP name; JPEG APPn segments (EXIF, XMP)
       and COM; EPS comment lines, pdfmark lines and XMP packet; SVG as text; PDF figures through pdfinfo, pdfinfo
       -meta and a byte search of the PDF objects outside streams, of object streams and of metadata streams;
       (d) the staged PDF the same way; (e) the zip entry names. A file identical to a file of the template folder
       (the publisher's class, style, icons) is not scanned when the folder's row in templates/SOURCES.tsv is of
       kind venue or other, unless it is a .tex or .bib file. Patterns are case-insensitive and match whole words
       only:
         workspace traces (always FAIL): TODO, FIXME (also TODO(verify), \todo{...}); claude.ai, claude.com,
           anthropic.com; Co-Authored-By; "Generated with [" and "Generated with Claude" (the commit trailer; plain
           "generated with" is ordinary prose); noreply@; CLAUDE.md, .claude/; the Windows user name of this machine
           (from USERNAME, at least 4 characters and not a generic name) and its profile path (USERPROFILE); an
           absolute Windows path (X:/dir/ anywhere; X:\dir\ everywhere except TeX code, where f:\R\to\R is math, so
           in TeX files only in comments and verbatim lines, and with $...$ masked); a path into this workspace
           (knowledge/, archives/, outputs/, inbox/, scripts/, tmp/, projects/ followed by a name that exists there)
         AI tool and vendor names: Claude (and "Claude Code"), Anthropic, ChatGPT, OpenAI, Copilot, Gemini,
           GPT-<digit>, "AI-generated", "generated by AI"
         [trace]      FAIL: a workspace trace, or an AI tool name that neither exemption covers: (i) the hit is in a
                      .tex file whose name matches *ai-declaration*.tex or *ai-statement*.tex (the disclosure the venue
                      requires; articles: sections/91-ai-declaration.tex); (ii) a regular expression in
                      projects/<Project>/submission/package-allow.txt matches a span of the same line that overlaps
                      the hit (one regex per line, case-insensitive; a line starting with # and the text after
                      " #" are comments giving the reason; for papers whose research uses LLMs, or a name such as
                      Claude Berge). An invalid regex there fails as well. Hits allowed by (i) or (ii) are listed
                      as [trace] notes, so they stay visible.
       Duplicates are reported once: a hit already reported for the project file is not repeated for its staged
       copy, and a binary file reports each term once. The report gives "Trace scan: <n> files, <m> hits (<k>
       allowed)", where a project file and its staged copy count as one file and the staged PDF and the zip as
       one each.
    I. AI declaration (advisory, never FAIL):
         [ai-declaration] no command argument (\section{...}, \section*{...}, \chapter*{...}, a thesis macro) in the
                      packaged .tex files is a heading with "Declaration of generative AI", "Use of AI tools" or
                      "AI-assisted technologies"; the note says whether projects/<Project>/submission/
                      *ai-declaration*.tex holds a draft (never packaged) and where the venue policies are. The
                      line "AI declaration: ..." just before the verdict repeats it on every run.
    C. Staging (not with -CheckOnly). The project is copied to tmp/package-<Project>/stage/ without the
       workspace-only material listed under LEFT OUT below. Unless -KeepComments, full-line
       comments of the .tex files are removed (not inside verbatim, Verbatim, lstlisting, minted, comment,
       filecontents, alltt; magic comments "%!" in the first five lines stay) and the remaining end-of-line comments are
       listed as [comment] notes, so a human can read them before the zip is sent. .tex files are written as UTF-8
       without BOM. Unless -KeepComments, the .bib files lose the lines that start with % outside entries and the
       @comment{...} blocks (a header that names the canonical .bib or a verification status is workspace
       information); a .bib that is not valid UTF-8 is copied unchanged ([encoding] note).
       With -Flat all files move into one directory and the path arguments are rewritten (see -Flat).
    D. Build in the stage the way a recipient would (latexmk -pdf, pdflatex with the installer disabled,
       -halt-on-error). A failure is [build] FAIL with the first error lines.
    E. Verification of the staged PDF:
         [undefined]  FAIL: "??" or "[?]" in the text of the PDF
         [fonts]      a font that is not embedded, or a Type 3 font
         [pages]      FAIL: more pages than -MaxPages (the limit of the venue)
         [text-diff]  FAIL: the text differs from the text of a reference build of the untouched project (the
                      files copied byte for byte, with the same exclusions, into tmp/package-<Project>/reference/
                      and built in the same run, so \today and other build-time values agree); proves that
                      comment stripping and flattening changed nothing
         [unused]     a file in the package that the build did not read (it would confuse a submission system)
    F. Package: build products are removed (the .bbl stays: journals and arXiv build without BibTeX), the staged
       files are scanned for traces (T b, c; a FAIL stops the run before the zip is written) and the zip is
       written with forward slashes in the entry names and no top-level folder:
         outputs/<Project>/package/<Project>-<yyyyMMdd>.zip   (-Flat: <Project>-<yyyyMMdd>-flat.zip)
         outputs/<Project>/package/<Project>-<yyyyMMdd>.pdf
       A second main file beside main.tex (-MainFile exam.tex) adds its name: <Project>-exam-<yyyyMMdd>.zip.
       The zip entry names are scanned (T e); a FAIL there removes the zip and the PDF again.
    G. Round trip: the zip is extracted to tmp/package-<Project>/roundtrip/ and built there; [roundtrip] FAIL unless
       the build succeeds, the extracted files equal the stage and the text equals the text of E.
    H. Report: findings as "path:line: [category] message" (FAIL: before the message of a failing finding), the
       files in the zip, page count, paths and links of zip and PDF, the lines "Trace scan: ..." and
       "AI declaration: ...", and the last line "Verdict: PASS" or "Verdict: FAIL (<categories>)". A category fails
       when one of its findings fails ([trace] and [template-origin] also have notes that do not).

    LEFT OUT of the package (workspace-only material; every report lists it as "Excluded from the package"):
      every *.md file (README.md, LICENSE.md, notes; anywhere in the project); response-to-reviewers.tex and
      main-marked.tex in the project root; the folders submission/ and
      experiments/ in the project root; *.zip; every file or folder whose name starts with a dot; pdfa.xmpi
      (pdfx scratch file); editor backups (*~, *.bak, *.swp); LaTeX build products (*.aux *.log *.out *.toc
      *.fls *.fdb_latexmk *.synctex.gz *.blg). Everything else goes into the package: .tex, .bib, images, the
      venue's .cls/.bst/.sty, a ready .bbl. The main file may be a wrapper that reads another file (exam.tex
      reads main.tex): the class is found by following \input from the main file.

    Static FAIL findings (A, B, T a) stop the run before staging: a package that is known to be wrong is not built.
    FAIL findings of the verification (E: [undefined], [text-diff], [trace] in the staged PDF) and of the trace scan
    of the staged files stop it before the zip is written, and a failed round trip or a [trace] FAIL in the zip
    entry names deletes the zip and the PDF again ("Stopped:" in the report says why). Stale output of an earlier
    run with the same name is deleted first, so a FAIL never leaves a valid-looking zip.

    Exit code: 0 = PASS (findings may exist), 1 = FAIL, 2 = invalid parameters.

.PARAMETER Project
    Name of a folder in projects/.

.PARAMETER MainFile
    Main .tex file in the project root. If omitted, main.tex is used, otherwise the only .tex with \documentclass
    (files excluded from the package are ignored).

.PARAMETER Template
    Name of a folder in templates/. Default: the folder that contains X.cls for the main file's \documentclass{X}.

.PARAMETER Flat
    Package with all files in one directory (Elsevier Editorial Manager and Springer build from a single directory).
    Rewrites the path arguments of \input, \include, \includeonly, \includegraphics, \bibliography,
    \addbibresource, removes \graphicspath, and rewrites every other {folder/file} group that names a project file,
    so paths passed to project macros (the thesis template's \thesisfrontpart{...}{frontmatter/x}) are handled too.
    [flat] FAIL: two files with the same name in different folders, or a reference to a folder of the project
    (folder/...) that remains after the rewrite (for example a path assembled from macros). \include is safe in
    this layout: the chapter files and their .aux files are in the same directory. Under -CheckOnly only the name
    clashes are checked.

.PARAMETER KeepComments
    Do not remove comment lines (.tex full-line comments, .bib comment lines and @comment blocks). The comments
    are then part of the package and are scanned for traces like the rest.

.PARAMETER CheckOnly
    Run only the static checks (A and B): no staging, no build, no zip, nothing written.

.PARAMETER MaxPages
    Page limit of the venue; the staged PDF is checked against it.

.EXAMPLE
    .\scripts\package-project.ps1 -Project clanok-1-min-cut-path
    .\scripts\package-project.ps1 -Project clanok-1-min-cut-path -Flat -MaxPages 20
    .\scripts\package-project.ps1 -Project clanok-1-min-cut-path -CheckOnly
#>
param(
    [Parameter(Position = 0)]
    [string]$Project,

    [Parameter(Position = 1)]
    [string]$MainFile,

    [string]$Template,

    [switch]$Flat,

    [switch]$KeepComments,

    [switch]$CheckOnly,

    [int]$MaxPages = 0
)

$workspace = Split-Path -Parent $PSScriptRoot
$projectsRoot = Join-Path $workspace "projects"
$templatesRoot = Join-Path $workspace "templates"
$outputsRoot = Join-Path $workspace "outputs"
$tmpRoot = Join-Path $workspace "tmp"

function Stop-InvalidParameter([string]$Message) {
    $Host.UI.WriteErrorLine("package-project: $Message")
    exit 2
}

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

if (-not $Project) { Stop-InvalidParameter "Missing -Project <name>." }
if ($Project -match '[\\/:]') { Stop-InvalidParameter "-Project is the name of a folder in projects/, not a path: $Project" }
$projectDirectory = Join-Path $projectsRoot $Project
if (-not (Test-Path -LiteralPath $projectDirectory -PathType Container)) {
    $available = (Get-ChildItem -LiteralPath $projectsRoot -Directory | ForEach-Object { $_.Name }) -join ", "
    Stop-InvalidParameter "Project does not exist: $projectDirectory. Available projects: $available"
}
$projectDirectory = (Get-Item -LiteralPath $projectDirectory).FullName.TrimEnd('\')

if ($PSBoundParameters.ContainsKey('MaxPages') -and $MaxPages -lt 1) { Stop-InvalidParameter "-MaxPages must be a positive number of pages." }

$templateDirectory = $null
$templateExplicit = $false
if ($Template) {
    if ($Template -match '[\\/:]') { Stop-InvalidParameter "-Template is the name of a folder in templates/, not a path: $Template" }
    $templateDirectory = Join-Path $templatesRoot $Template
    if (-not (Test-Path -LiteralPath $templateDirectory -PathType Container)) {
        $available = (Get-ChildItem -LiteralPath $templatesRoot -Directory | ForEach-Object { $_.Name }) -join ", "
        Stop-InvalidParameter "Template does not exist: $templateDirectory. Available templates: $available"
    }
    $templateDirectory = (Get-Item -LiteralPath $templateDirectory).FullName.TrimEnd('\')
    $templateExplicit = $true
}
if ($MainFile) {
    if ($MainFile -match '[\\/]') { Stop-InvalidParameter "-MainFile must be a file in the project root: $MainFile" }
    if (-not (Test-Path -LiteralPath (Join-Path $projectDirectory $MainFile) -PathType Leaf)) {
        Stop-InvalidParameter "Main LaTeX file does not exist: $(Join-Path $projectDirectory $MainFile)"
    }
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

$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

$utf8 = New-Object System.Text.UTF8Encoding $false
$utf8Strict = New-Object System.Text.UTF8Encoding($false, $true)
$rxNone = [System.Text.RegularExpressions.RegexOptions]"CultureInvariant"
$rxIgnoreCase = [System.Text.RegularExpressions.RegexOptions]"IgnoreCase, CultureInvariant"
$stamp = Get-Date -Format "yyyyMMdd"

$workRoot = Join-Path $tmpRoot "package-$Project"
$stageDirectory = Join-Path $workRoot "stage"
$roundtripDirectory = Join-Path $workRoot "roundtrip"
$packageDirectory = Join-Path $outputsRoot "$Project\package"
$zipName = $(if ($Flat) { "$Project-$stamp-flat.zip" } else { "$Project-$stamp.zip" })
$pdfName = "$Project-$stamp.pdf"
$zipPath = Join-Path $packageDirectory $zipName
$packagePdfPath = Join-Path $packageDirectory $pdfName

function New-StringSet([string[]]$Items) {
    $set = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($entry in $Items) { [void]$set.Add($entry) }
    return , $set
}

# Categories whose findings fail by default; [trace] and [template-origin] also report notes (Add-Finding -Fail $false).
$failCategories = New-StringSet @("template-file", "template-origin", "outside", "missing", "case", "trace", "flat", "build", "undefined", "pages", "text-diff", "roundtrip", "internal")
$categoryOrder = @("template-file", "template-origin", "template-bst", "layout", "outside", "missing", "case", "filename", "trace",
    "flat", "build", "undefined", "fonts", "pages", "text-diff", "unused", "comment", "ai-declaration", "encoding", "roundtrip", "internal")

$layoutPackages = New-StringSet @("geometry", "fullpage", "a4wide", "setspace", "titlesec", "sectsty", "fancyhdr", "savetrees", "parskip")
$venueFileExtensions = New-StringSet @(".cls", ".bst", ".sty", ".clo", ".bbx", ".cbx", ".cfg", ".def")
$verbatimEnvironments = "verbatim|Verbatim|lstlisting|minted|comment|filecontents|alltt"

# Regular expressions on the code view of a .tex file (comments, verbatim and \verb removed)
$rxComment = [regex]::new('(?<=(?:^|[^\\])(?:\\\\)*)%.*$', $rxNone)
$rxVerbInline = [regex]::new('\\verb\*?([^A-Za-z*\s])[^\n]*?\1', $rxNone)
$rxVerbBegin = [regex]::new('\\begin\s*\{(' + $verbatimEnvironments + ')\*?\}', $rxNone)
$rxDocumentClass = [regex]::new('\\documentclass\s*(?:\[[^\]]*\])?\s*\{([^{}]*)\}', $rxNone)
$rxUsePackage = [regex]::new('\\(?:usepackage|RequirePackage)\s*(?:\[[^\]]*\])?\s*\{([^{}]*)\}', $rxNone)
$rxInputInclude = [regex]::new('\\(input|include)\s*\{([^{}]*)\}', $rxNone)
$rxGraphics = [regex]::new('\\includegraphics\*?\s*(?:\[[^\]]*\])?\s*\{([^{}]*)\}', $rxNone)
$rxBibliography = [regex]::new('\\bibliography\s*\{([^{}]*)\}', $rxNone)
$rxAddResource = [regex]::new('\\addbibresource\s*(?:\[([^\]]*)\])?\s*\{([^{}]*)\}', $rxNone)
$rxBibStyle = [regex]::new('\\bibliographystyle\s*\{([^{}]*)\}', $rxNone)
$rxGraphicsPath = [regex]::new('\\graphicspath\s*\{(?:\s*\{[^{}]*\}\s*)*\}', $rxNone)
$rxIfFileExists = [regex]::new('\\(?:IfFileExists|InputIfFileExists)\*?\s*\{([^{}]*)\}', $rxNone)
$rxLayoutSetlength = [regex]::new('\\(?:setlength|addtolength)\s*\{?\s*\\(textwidth|textheight|topmargin|oddsidemargin|evensidemargin|columnsep|parskip|parindent|headsep|footskip)\b', $rxNone)
$rxLayoutStretch = [regex]::new('\\(linespread|baselinestretch|setstretch|onehalfspacing|doublespacing|singlespacing)\b', $rxNone)
$rxLayoutVspace = [regex]::new('\\(vspace\*?)\s*\{\s*-', $rxNone)
$rxLayoutPage = [regex]::new('\\(enlargethispage|pagestyle|thispagestyle|newgeometry|geometry|fontsize|titleformat|titlespacing|setlist)\b', $rxNone)
$rxLayoutAssign = [regex]::new('\\(pdfpagewidth|pdfpageheight|paperwidth|paperheight|textwidth|textheight|columnsep)\s*=', $rxNone)
$rxLayoutHeading = [regex]::new('\\(?:renewcommand\*?|def|let)\s*\{?\s*\\(section|subsection|subsubsection|paragraph|subparagraph|maketitle)\b', $rxNone)

# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------

$script:findings = New-Object System.Collections.Generic.List[object]

function Get-DisplayPath([string]$FullName) {
    $root = $workspace.TrimEnd('\') + '\'
    if ($FullName.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $FullName.Substring($root.Length).Replace('\', '/')
    }
    return $FullName.Replace('\', '/')
}

# $Fail overrides the default of the category ($null: the category decides).
function Add-Finding([string]$File, [int]$Line, [string]$Category, [string]$Message, [object]$Fail = $null) {
    $isFail = $failCategories.Contains($Category)
    if ($null -ne $Fail) { $isFail = [bool]$Fail }
    $script:findings.Add([pscustomobject]@{
            File     = $File
            Line     = $Line
            Category = $Category
            Fail     = $isFail
            Message  = $Message
        })
}

# Finding in a source file of the project; $Rel is relative to the project folder.
function Add-ProjectFinding([string]$Rel, [int]$Line, [string]$Category, [string]$Message, [object]$Fail = $null) {
    Add-Finding "projects/$Project/$Rel" $Line $Category $Message $Fail
}

function Format-Short([string]$Text, [int]$Limit = 70) {
    $clean = ($Text -replace '\s+', ' ').Trim()
    if ($clean.Length -gt $Limit) { return $clean.Substring(0, $Limit - 3) + "..." }
    return $clean
}

function Format-Size([long]$Bytes) {
    if ($Bytes -ge 1MB) { return ("{0,8:N2} MB" -f ($Bytes / 1MB)) }
    if ($Bytes -lt 1KB) { return ("{0,8:N0}  B" -f $Bytes) }
    return ("{0,8:N1} kB" -f ($Bytes / 1KB))
}

# ---------------------------------------------------------------------------
# Helpers: TeX source model
# ---------------------------------------------------------------------------

function Get-LineNumber([int[]]$LineStarts, [int]$Offset) {
    $index = [Array]::BinarySearch($LineStarts, $Offset)
    if ($index -lt 0) { $index = (-bnot $index) - 1 }
    return $index + 1
}

# Text of a source file; $null when it is not valid UTF-8 (such a file is copied unchanged).
function Read-SourceText([string]$FullName) {
    $bytes = [System.IO.File]::ReadAllBytes($FullName)
    try { $text = $utf8Strict.GetString($bytes) } catch { return $null }
    if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) { $text = $text.Substring(1) }
    return $text
}

$verbMask = [System.Text.RegularExpressions.MatchEvaluator] { param($m) ('_' * $m.Length) }

# Lines of a .tex text with their code view. Raw keeps the line end (CR); Code has comments, verbatim material and
# \verb arguments removed; CommentAt is the index of the first unescaped % (or -1); Keep marks lines inside
# verbatim-like environments, which are never rewritten. CodeText joins the code lines for multi-line regexes.
function Get-TexModel([string]$Text) {
    $raw = $Text -split "`n"
    $count = $raw.Count
    $code = New-Object string[] $count
    $commentAt = New-Object int[] $count
    $keep = New-Object bool[] $count
    $environment = $null
    for ($i = 0; $i -lt $count; $i++) {
        $line = $raw[$i]
        $commentAt[$i] = -1
        if ($null -ne $environment) {
            $keep[$i] = $true
            $end = [regex]::Match($line, '\\end\s*\{' + [regex]::Escape($environment) + '\*?\}')
            if ($end.Success) {
                $environment = $null
                $rest = $rxVerbInline.Replace($line.Substring($end.Index + $end.Length), $verbMask)
                $at = $rxComment.Match($rest)
                if ($at.Success) { $rest = $rest.Substring(0, $at.Index) }
                $code[$i] = $rest
            }
            else { $code[$i] = "" }
            continue
        }
        $masked = $rxVerbInline.Replace($line, $verbMask)
        $comment = $rxComment.Match($masked)
        $codePart = $masked
        if ($comment.Success) { $commentAt[$i] = $comment.Index; $codePart = $masked.Substring(0, $comment.Index) }
        $begin = $rxVerbBegin.Match($codePart)
        if ($begin.Success) {
            $keep[$i] = $true
            $commentAt[$i] = -1
            $name = $begin.Groups[1].Value
            $after = $codePart.Substring($begin.Index + $begin.Length)
            if ($after -match ('\\end\s*\{' + [regex]::Escape($name) + '\*?\}')) {
                $code[$i] = $codePart.Substring(0, $begin.Index)
            }
            else {
                $environment = $name
                $code[$i] = $codePart.Substring(0, $begin.Index)
            }
            continue
        }
        $code[$i] = $codePart
    }
    $starts = New-Object int[] $count
    $position = 0
    for ($i = 0; $i -lt $count; $i++) { $starts[$i] = $position; $position += $code[$i].Length + 1 }
    return [pscustomobject]@{
        Raw        = $raw
        Code       = $code
        CommentAt  = $commentAt
        Keep       = $keep
        CodeText   = ($code -join "`n")
        LineStarts = $starts
    }
}

# ---------------------------------------------------------------------------
# Helpers: external tools (no PowerShell error records, no hidden prompts)
# ---------------------------------------------------------------------------

$script:toolPaths = @{}
function Get-ToolPath([string]$Tool) {
    if (-not $script:toolPaths.ContainsKey($Tool)) {
        $command = Get-Command $Tool -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($null -eq $command) { throw "Tool not found on PATH: $Tool" }
        $script:toolPaths[$Tool] = $command.Source
    }
    return $script:toolPaths[$Tool]
}

function ConvertTo-ArgumentString([string[]]$Arguments) {
    $parts = foreach ($argument in $Arguments) {
        if ($argument -eq "") { '""' }
        elseif ($argument -match '[\s"]') { '"' + (($argument -replace '(\\*)"', '$1$1\"') -replace '(\\+)$', '$1$1') + '"' }
        else { $argument }
    }
    return ($parts -join ' ')
}

function Invoke-Tool([string]$Tool, [string[]]$Arguments, [string]$WorkingDirectory) {
    $info = New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName = Get-ToolPath $Tool
    $info.Arguments = ConvertTo-ArgumentString $Arguments
    $info.WorkingDirectory = $WorkingDirectory
    $info.UseShellExecute = $false
    $info.CreateNoWindow = $true
    $info.RedirectStandardInput = $true
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    $info.StandardOutputEncoding = $utf8
    $info.StandardErrorEncoding = $utf8
    $process = [System.Diagnostics.Process]::Start($info)
    $process.StandardInput.Close()
    $outputTask = $process.StandardOutput.ReadToEndAsync()
    $errorTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    return [pscustomobject]@{ ExitCode = $process.ExitCode; Output = $outputTask.Result; Error = $errorTask.Result }
}

# ---------------------------------------------------------------------------
# The project: files, exclusions
# ---------------------------------------------------------------------------

$script:included = New-Object System.Collections.Generic.List[object]    # Rel, Full, Length, Time
$script:excluded = New-Object System.Collections.Generic.List[object]    # Rel, Reason, IsFolder
$script:excludedFiles = @{}                                              # lowercase Rel -> reason

function Get-FileExclusionReason([string]$Name, [bool]$AtRoot) {
    if ($Name.StartsWith('.')) { return "name starts with a dot" }
    if ($Name -like '*.zip') { return "archive" }
    if ($Name -ieq 'pdfa.xmpi') { return "pdfx scratch file" }
    if ($Name -match '(~|\.bak|\.swp)$') { return "editor backup" }
    if ($Name -match '\.(aux|log|out|toc|fls|fdb_latexmk|blg)$' -or $Name -like '*.synctex.gz') { return "LaTeX build product" }
    if ($Name -like '*.md') { return "workspace-only" }
    if ($AtRoot -and ($Name -ieq 'response-to-reviewers.tex' -or $Name -ieq 'main-marked.tex')) { return "workspace-only" }
    return $null
}

function Scan-ProjectFolder([string]$Directory, [string]$Prefix) {
    $atRoot = ($Prefix -eq "")
    foreach ($item in @(Get-ChildItem -LiteralPath $Directory -Force | Sort-Object Name)) {
        $rel = $Prefix + $item.Name
        if ($item.PSIsContainer) {
            $reason = $null
            if ($item.Name.StartsWith('.')) { $reason = "name starts with a dot" }
            elseif ($atRoot -and ($item.Name -ieq 'submission' -or $item.Name -ieq 'experiments')) { $reason = "workspace-only" }
            if ($null -ne $reason) { $script:excluded.Add([pscustomobject]@{ Rel = $rel + "/"; Reason = $reason; IsFolder = $true }) }
            else { Scan-ProjectFolder $item.FullName ($rel + "/") }
        }
        else {
            $reason = Get-FileExclusionReason $item.Name $atRoot
            if ($null -ne $reason) {
                $script:excluded.Add([pscustomobject]@{ Rel = $rel; Reason = $reason; IsFolder = $false })
                $script:excludedFiles[$rel] = $reason
            }
            else {
                $script:included.Add([pscustomobject]@{ Rel = $rel; Full = $item.FullName; Length = $item.Length; Time = $item.LastWriteTime })
            }
        }
    }
}
Scan-ProjectFolder $projectDirectory ""

$fileIndex = @{}                         # Rel -> Rel (the name on disk); lookups ignore case
foreach ($file in $script:included) { $fileIndex[$file.Rel] = $file.Rel }
$texFiles = @($script:included | Where-Object { $_.Rel -like '*.tex' })

function Test-ExcludedPath([string]$Rel) {
    if ($script:excludedFiles.ContainsKey($Rel)) { return $script:excludedFiles[$Rel] }
    $first = $Rel.Split('/')[0]
    foreach ($item in $script:excluded) {
        if ($item.IsFolder -and $item.Rel.TrimEnd('/') -ieq $first -and (Test-Path -LiteralPath (Join-Path $projectDirectory $Rel))) { return $item.Reason }
    }
    return $null
}

# TeX models of every .tex file
$texModels = @{}
foreach ($file in $texFiles) {
    $text = Read-SourceText $file.Full
    if ($null -eq $text) {
        $texModels[$file.Rel] = $null
        Add-ProjectFinding $file.Rel 1 "encoding" "not valid UTF-8: not parsed, copied unchanged (comments are not removed, paths are not rewritten)"
    }
    else { $texModels[$file.Rel] = Get-TexModel $text }
}

# Main file
if (-not $MainFile) {
    if ($fileIndex.ContainsKey("main.tex")) { $MainFile = "main.tex" }
    else {
        $candidates = @($texFiles | Where-Object { $_.Rel -notlike '*/*' -and $null -ne $texModels[$_.Rel] -and $rxDocumentClass.IsMatch($texModels[$_.Rel].CodeText) })
        if ($candidates.Count -ne 1) {
            $names = ($candidates | ForEach-Object { $_.Rel }) -join ", "
            Stop-InvalidParameter "Cannot determine the main file automatically (candidates: $names). Pass -MainFile."
        }
        $MainFile = $candidates[0].Rel
    }
}
if (-not $fileIndex.ContainsKey($MainFile)) {
    Stop-InvalidParameter "The main file $MainFile is excluded from the package ($(Test-ExcludedPath $MainFile)) or is not a project file."
}
$MainFile = $fileIndex[$MainFile]
if ($MainFile -notlike '*.tex') { Stop-InvalidParameter "The main file must be a .tex file: $MainFile" }
$mainBase = [IO.Path]::GetFileNameWithoutExtension($MainFile)
# A second main file of the same project (exam.tex beside main.tex) gets its own package names.
if ($mainBase -ne "main" -and $fileIndex.ContainsKey("main.tex")) {
    $zipName = $(if ($Flat) { "$Project-$mainBase-$stamp-flat.zip" } else { "$Project-$mainBase-$stamp.zip" })
    $pdfName = "$Project-$mainBase-$stamp.pdf"
    $zipPath = Join-Path $packageDirectory $zipName
    $packagePdfPath = Join-Path $packageDirectory $pdfName
}
$mainModel = $texModels[$MainFile]
if ($null -eq $mainModel) { Stop-InvalidParameter "The main file is not valid UTF-8: $MainFile" }

# Findings of the file level that need the project listing
foreach ($file in $script:included) {
    if ($file.Rel -match '[^\x21-\x7E/]') {
        Add-ProjectFinding $file.Rel 1 "filename" "the path contains a space or a non-ASCII character; rename the file (a recipient's system or submission form may reject it)"
    }
}

# ---------------------------------------------------------------------------
# A. Template conformance
# ---------------------------------------------------------------------------

# \documentclass of the main file; when it has none (exam.tex reads main.tex), of the files it \input (depth 3).
function Find-DocumentClass([string]$Rel, [int]$Depth) {
    $model = $texModels[$Rel]
    if ($null -eq $model) { return $null }
    $match = $rxDocumentClass.Match($model.CodeText)
    if ($match.Success) {
        return [pscustomobject]@{ Name = $match.Groups[1].Value.Trim(); Rel = $Rel; Line = (Get-LineNumber $model.LineStarts $match.Index) }
    }
    if ($Depth -ge 3) { return $null }
    foreach ($input in $rxInputInclude.Matches($model.CodeText)) {
        $target = $input.Groups[2].Value.Trim()
        foreach ($candidate in @($target, ($target + ".tex"))) {
            if ($fileIndex.ContainsKey($candidate) -and $candidate -like '*.tex') {
                $found = Find-DocumentClass $fileIndex[$candidate] ($Depth + 1)
                if ($null -ne $found) { return $found }
                break
            }
        }
    }
    return $null
}

$classInfo = Find-DocumentClass $MainFile 0
$className = $null
$classIsLocal = $false
$standardClass = $false
$templateNote = ""
$templateFilesIdentical = New-Object System.Collections.Generic.List[string]
$templateFiles = @()                      # all files of the template folder
$templateHashes = $null                   # set of SHA-256 of all template files

if ($null -eq $classInfo) {
    Add-ProjectFinding $MainFile 1 "missing" "no \documentclass found in the main file or in the files it reads: the class and the template cannot be determined"
}
else {
    $className = $classInfo.Name
    $classRelative = $className.Replace('\', '/')
    if ($classRelative -notlike '*.cls') { $classRelative += ".cls" }
    $classIsLocal = $fileIndex.ContainsKey($classRelative)
    $classLeaf = [IO.Path]::GetFileName($classRelative)

    if (-not $templateExplicit) {
        $matches = New-Object System.Collections.Generic.List[string]
        foreach ($directory in @(Get-ChildItem -LiteralPath $templatesRoot -Directory | Sort-Object Name)) {
            $hit = @(Get-ChildItem -LiteralPath $directory.FullName -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -ieq $classLeaf })
            if ($hit.Count -gt 0) { $matches.Add($directory.FullName) }
        }
        if ($matches.Count -gt 0) { $templateDirectory = $matches[0] }
        if ($matches.Count -gt 1) {
            $others = ($matches | Select-Object -Skip 1 | ForEach-Object { Get-DisplayPath $_ }) -join ", "
            $templateNote = "several template folders contain ${classLeaf}: $others; using the first"
        }
    }
    if ($null -eq $templateDirectory) {
        # No template folder: a standard class of the TeX distribution (or a class that only the project has).
        $standardClass = $true
    }
}
if ($null -ne $templateDirectory) {
    $templateFiles = @(Get-ChildItem -LiteralPath $templateDirectory -Recurse -File)
    if ($templateExplicit -and $null -ne $classLeaf -and @($templateFiles | Where-Object { $_.Name -ieq $classLeaf }).Count -eq 0) {
        $templateNote = "the template does not contain $classLeaf (the class comes from the project or from the TeX distribution)"
    }
    $templateHashes = New-Object 'System.Collections.Generic.HashSet[string]'
    foreach ($file in $templateFiles) { [void]$templateHashes.Add((Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash) }
}

# --- Distribution lookups (kpsewhich, installer disabled), batched ---------------------------------------------
$script:distributionCache = @{}
function Find-InDistribution([string[]]$Names) {
    $todo = @($Names | Where-Object { $_ -and -not $script:distributionCache.ContainsKey($_) } | Select-Object -Unique)
    for ($start = 0; $start -lt $todo.Count; $start += 30) {
        $chunk = @($todo[$start..([Math]::Min($start + 29, $todo.Count - 1))])
        $result = Invoke-Tool "kpsewhich" (@("--miktex-disable-installer") + $chunk) $env:TEMP
        $found = @{}
        foreach ($line in ($result.Output -split "`r?`n")) {
            if ($line.Trim().Length -gt 0) { $found[[IO.Path]::GetFileName($line.Trim())] = $true }
        }
        foreach ($name in $chunk) { $script:distributionCache[$name] = $found.ContainsKey([IO.Path]::GetFileName($name)) }
    }
}
function Test-InDistribution([string]$Name) {
    return ($script:distributionCache.ContainsKey($Name) -and $script:distributionCache[$Name])
}

# --- B. References of the .tex files ------------------------------------------------------------------------------
$refs = New-Object System.Collections.Generic.List[object]
$graphicsDirectories = New-Object System.Collections.Generic.List[string]
$optionalTargets = New-StringSet @()
$layoutHits = New-Object System.Collections.Generic.List[object]

function Add-Ref([string]$Kind, [string]$Arg, [string]$Rel, [int]$Line) {
    $refs.Add([pscustomobject]@{ Kind = $Kind; Arg = $Arg.Trim(); Rel = $Rel; Line = $Line })
}

foreach ($file in $texFiles) {
    $model = $texModels[$file.Rel]
    if ($null -eq $model) { continue }
    $code = $model.CodeText
    $starts = $model.LineStarts
    foreach ($m in $rxDocumentClass.Matches($code)) { Add-Ref "documentclass" $m.Groups[1].Value $file.Rel (Get-LineNumber $starts $m.Index) }
    foreach ($m in $rxUsePackage.Matches($code)) {
        foreach ($name in $m.Groups[1].Value.Split(',')) { if ($name.Trim().Length -gt 0) { Add-Ref "usepackage" $name $file.Rel (Get-LineNumber $starts $m.Index) } }
    }
    foreach ($m in $rxInputInclude.Matches($code)) { Add-Ref $m.Groups[1].Value $m.Groups[2].Value $file.Rel (Get-LineNumber $starts $m.Index) }
    foreach ($m in $rxGraphics.Matches($code)) { Add-Ref "graphics" $m.Groups[1].Value $file.Rel (Get-LineNumber $starts $m.Index) }
    foreach ($m in $rxBibliography.Matches($code)) {
        foreach ($name in $m.Groups[1].Value.Split(',')) { if ($name.Trim().Length -gt 0) { Add-Ref "bibliography" $name $file.Rel (Get-LineNumber $starts $m.Index) } }
    }
    foreach ($m in $rxAddResource.Matches($code)) {
        if ($m.Groups[1].Value -notmatch 'location\s*=\s*remote') { Add-Ref "addbibresource" $m.Groups[2].Value $file.Rel (Get-LineNumber $starts $m.Index) }
    }
    foreach ($m in $rxBibStyle.Matches($code)) { Add-Ref "bibliographystyle" $m.Groups[1].Value $file.Rel (Get-LineNumber $starts $m.Index) }
    foreach ($m in $rxGraphicsPath.Matches($code)) {
        $line = Get-LineNumber $starts $m.Index
        foreach ($entry in [regex]::Matches($m.Value, '\{([^{}]*)\}')) {
            if ($entry.Index -gt 0) {
                $directory = $entry.Groups[1].Value.Trim()
                if ($directory.Length -gt 0) { Add-Ref "graphicspath" $directory $file.Rel $line; $graphicsDirectories.Add($directory.Replace('\', '/').TrimEnd('/')) }
            }
        }
    }
    foreach ($m in $rxIfFileExists.Matches($code)) { [void]$optionalTargets.Add($m.Groups[1].Value.Trim()) }
}

# Classes and packages of the project itself that name a style: the template check needs \bibliographystyle from .cls
$classStyleRefs = New-Object System.Collections.Generic.List[object]
foreach ($file in @($script:included | Where-Object { $_.Rel -like '*.cls' })) {
    $text = [System.IO.File]::ReadAllText($file.Full, $utf8)
    $model = Get-TexModel $text
    foreach ($m in $rxBibStyle.Matches($model.CodeText)) {
        $classStyleRefs.Add([pscustomobject]@{ Kind = "bibliographystyle"; Arg = $m.Groups[1].Value.Trim(); Rel = $file.Rel; Line = (Get-LineNumber $model.LineStarts $m.Index) })
    }
}

$graphicsExtensions = @(".pdf", ".png", ".jpg", ".jpeg", ".eps", ".mps", ".PDF", ".PNG", ".JPG", ".JPEG")
$graphicsKnown = '\.(pdf|png|jpe?g|eps|mps|jbig2|jb2)$'

function Test-OutsidePath([string]$Path) {
    if ($Path -match '^[A-Za-z]:') { return "absolute path" }
    # a control sequence (\ThesisBibStyle) or a macro parameter (#1) is not a path: the build is the proof
    if ($Path -match '#' -or $Path -match '\\[A-Za-z@]') { return $null }
    if ($Path -match '^[\\/~]') { return "absolute path" }
    foreach ($segment in ($Path -split '[\\/]')) { if ($segment -eq '..') { return "path with a .. segment" } }
    return $null
}

# Resolves one reference. State: found (Actual, CaseMismatch), missing, outside (Reason), skip, distribution (Names).
function Resolve-Reference($Ref) {
    $arg = $Ref.Arg
    if ($arg.Length -eq 0) { return [pscustomobject]@{ State = "skip" } }
    $outside = Test-OutsidePath $arg
    if ($null -ne $outside) { return [pscustomobject]@{ State = "outside"; Reason = $outside } }
    if ($arg -match '[#\\$]' -or $arg -match '^[A-Za-z]+://') { return [pscustomobject]@{ State = "skip" } }
    $path = $arg
    while ($path.StartsWith('./')) { $path = $path.Substring(2) }
    if ($path.Length -eq 0) { return [pscustomobject]@{ State = "skip" } }

    $extensions = @("")
    $distributionKind = $null
    switch ($Ref.Kind) {
        "input" { if ($path -notmatch '\.[A-Za-z0-9]+$') { $extensions = @(".tex", "") } else { $extensions = @("", ".tex") }; $distributionKind = "input" }
        "include" { $extensions = @(".tex") }
        "graphics" { if ($path -match $graphicsKnown) { $extensions = @("") } else { $extensions = $graphicsExtensions }; $distributionKind = "graphics" }
        "bibliography" { if ($path -like '*.bib') { $extensions = @("") } else { $extensions = @(".bib") } }
        "addbibresource" { $extensions = @("") }
        "documentclass" { if ($path -like '*.cls') { $extensions = @("") } else { $extensions = @(".cls") }; $distributionKind = "class" }
        "usepackage" { if ($path -like '*.sty') { $extensions = @("") } else { $extensions = @(".sty") }; $distributionKind = "package" }
        "bibliographystyle" { if ($path -like '*.bst') { $extensions = @("") } else { $extensions = @(".bst") }; $distributionKind = "style" }
        "graphicspath" {
            if (Test-Path -LiteralPath (Join-Path $projectDirectory $path) -PathType Container) { return [pscustomobject]@{ State = "found"; Actual = $path; CaseMismatch = $false } }
            return [pscustomobject]@{ State = "skip" }
        }
    }
    $bases = @("")
    if ($Ref.Kind -eq "graphics") { foreach ($base in $graphicsDirectories) { if ($base.Length -gt 0 -and $base -notmatch '^[\\/~]|^[A-Za-z]:|\.\.') { $bases += ($base + "/") } } }
    $tried = New-Object System.Collections.Generic.List[string]
    foreach ($base in $bases) {
        foreach ($extension in $extensions) {
            $candidate = $base + $path + $extension
            $tried.Add($candidate)
            if ($fileIndex.ContainsKey($candidate)) {
                $actual = $fileIndex[$candidate]
                $typed = $base + $path
                $compare = $actual
                if ($extension.Length -gt 0) { $compare = $actual.Substring(0, $actual.Length - $extension.Length) }
                $mismatch = -not ($compare -ceq $typed)
                if ($extension.Length -eq 0) { $mismatch = -not ($actual -ceq $typed) }
                return [pscustomobject]@{ State = "found"; Actual = $actual; CaseMismatch = $mismatch; Typed = $typed }
            }
        }
    }
    $names = @()
    $isPlainName = ($path -notmatch '/')
    switch ($distributionKind) {
        "input" { if ($isPlainName) { $names = @($(if ($path -match '\.[A-Za-z0-9]+$') { $path } else { $path + ".tex" })) } }
        "graphics" { if ($isPlainName) { $names = @($(if ($path -match $graphicsKnown) { $path } else { foreach ($e in @(".pdf", ".png", ".jpg", ".jpeg", ".eps")) { $path + $e } })) } }
        "class" { if ($isPlainName) { $names = @($path + $(if ($path -like '*.cls') { "" } else { ".cls" })) } }
        "package" { if ($isPlainName) { $names = @($path + $(if ($path -like '*.sty') { "" } else { ".sty" })) } }
        "style" { if ($isPlainName) { $names = @($path + $(if ($path -like '*.bst') { "" } else { ".bst" })) } }
    }
    return [pscustomobject]@{ State = "missing"; Names = $names; Tried = $tried }
}

$resolved = New-Object System.Collections.Generic.List[object]
$wantedNames = New-Object System.Collections.Generic.List[string]
$allRefs = New-Object System.Collections.Generic.List[object]
foreach ($ref in $refs) { $allRefs.Add($ref) }
foreach ($ref in $classStyleRefs) { $allRefs.Add($ref) }
foreach ($ref in $allRefs) {
    $result = Resolve-Reference $ref
    $resolved.Add([pscustomobject]@{ Ref = $ref; Result = $result })
    if ($result.State -eq "missing") { foreach ($name in $result.Names) { $wantedNames.Add($name) } }
}
if ($wantedNames.Count -gt 0) { Find-InDistribution $wantedNames.ToArray() }
# The class of the main file is also looked up when it is neither local nor in a template (standard class).
$classLeafName = $null
if ($null -ne $className) { $classLeafName = [IO.Path]::GetFileName($className.Replace('\', '/')); if ($classLeafName -notlike '*.cls') { $classLeafName += ".cls" } }

$staticReferenceTargets = New-StringSet @()    # leaf names of the .bib and .bst files named in the sources
$distributionClass = $false
foreach ($entry in $resolved) {
    $ref = $entry.Ref
    $result = $entry.Result
    $label = "\" + $(switch ($ref.Kind) { "graphics" { "includegraphics" } "bibliography" { "bibliography" } default { $ref.Kind } }) + "{" + $ref.Arg + "}"
    switch ($result.State) {
        "outside" {
            Add-ProjectFinding $ref.Rel $ref.Line "outside" "${label}: $($result.Reason); the file is not inside the project folder, so it is missing in the package. Copy it into the project."
        }
        "found" {
            if ($ref.Kind -in @("bibliography", "addbibresource", "bibliographystyle")) { [void]$staticReferenceTargets.Add([IO.Path]::GetFileName($result.Actual)) }
            if ($result.CaseMismatch) {
                Add-ProjectFinding $ref.Rel $ref.Line "case" "${label}: the file on disk is $($result.Actual); the letter case differs, so it is not found on a case-sensitive system. Use the exact name."
            }
        }
        "missing" {
            if ($ref.Kind -eq "graphicspath") { continue }
            $inDistribution = $false
            foreach ($name in $result.Names) { if (Test-InDistribution $name) { $inDistribution = $true } }
            if ($inDistribution) {
                if ($ref.Kind -eq "documentclass" -and $ref.Rel -eq $MainFile) { $distributionClass = $true }
                continue
            }
            if ($optionalTargets.Contains($ref.Arg)) { continue }
            if ($ref.Kind -eq "documentclass" -and $null -ne $templateDirectory -and $ref.Rel -eq $MainFile) { continue }   # reported as [template-file]
            $reason = Test-ExcludedPath ($ref.Arg)
            $where = "in the project"
            if ($result.Names.Count -gt 0) { $where = "in the project or in the TeX distribution" }
            $detail = ""
            if ($null -ne $reason) { $detail = " (a file of this name exists but is excluded from the package: $reason)" }
            elseif ($ref.Kind -eq "graphics") { $detail = " (tried: " + (($result.Tried.ToArray() | Select-Object -First 5) -join ", ") + ")" }
            Add-ProjectFinding $ref.Rel $ref.Line "missing" "${label}: no such file $where$detail."
        }
    }
}

# A3. Venue files must be byte-identical to the template's.
$templateRelative = ""
if ($null -ne $templateDirectory) {
    $templateRelative = Get-DisplayPath $templateDirectory
    $templateByName = @{}
    foreach ($file in $templateFiles) {
        if (-not $templateByName.ContainsKey($file.Name)) { $templateByName[$file.Name] = New-Object System.Collections.Generic.List[object] }
        $templateByName[$file.Name].Add($file)
    }
    foreach ($file in $script:included) {
        $extension = [IO.Path]::GetExtension($file.Rel)
        if (-not $venueFileExtensions.Contains($extension)) { continue }
        $leaf = [IO.Path]::GetFileName($file.Rel)
        if (-not $templateByName.ContainsKey($leaf)) { continue }
        $hash = (Get-FileHash -LiteralPath $file.Full -Algorithm SHA256).Hash
        $same = $false
        foreach ($candidate in $templateByName[$leaf]) {
            if ((Get-FileHash -LiteralPath $candidate.FullName -Algorithm SHA256).Hash -eq $hash) { $same = $true; break }
        }
        if ($same) { $templateFilesIdentical.Add($file.Rel) }
        else {
            $first = $templateByName[$leaf][0]
            $other = (Get-FileHash -LiteralPath $first.FullName -Algorithm SHA256).Hash
            Add-ProjectFinding $file.Rel 1 "template-file" "differs from $(Get-DisplayPath $first.FullName) (SHA-256 $($hash.Substring(0, 12)) against $($other.Substring(0, 12))); the venue's files must not be edited. Restore the file from the template."
        }
    }
    if ($null -ne $className -and -not $classIsLocal) {
        $inTemplate = $templateByName.ContainsKey($classLeafName)
        if ($inTemplate) {
            Add-ProjectFinding $MainFile $classInfo.Line "template-file" "\documentclass{$className} needs $classLeafName, which is in $templateRelative but not in the project: the folder is not self-contained. Copy the venue's files into the project."
        }
        elseif ($templateExplicit) {
            # explicit -Template without this class: the class must come from the distribution (checked above)
        }
    }

    # A4. Bibliography style
    $templateStyles = @($templateFiles | Where-Object { $_.Extension -ieq ".bst" } | ForEach-Object { [IO.Path]::GetFileNameWithoutExtension($_.Name) })
    if ($templateStyles.Count -gt 0) {
        # Only a \bibliographystyle command of the project is checked; without one the class sets the style (no finding).
        $styleRefs = @($refs | Where-Object { $_.Kind -eq "bibliographystyle" })
        foreach ($styleRef in $styleRefs) {
            if ($styleRef.Arg -match '[#\\]') { continue }
            $styleName = [IO.Path]::GetFileNameWithoutExtension($styleRef.Arg.Replace('\', '/'))
            if ($templateStyles -notcontains $styleName) {
                Add-ProjectFinding $styleRef.Rel $styleRef.Line "template-bst" "\bibliographystyle{$($styleRef.Arg)}: the template ships $($templateStyles -join ', ').bst; use the venue's style."
            }
        }
    }

    # A5. Commands that override the venue's layout
    $layoutText = " must not be changed; remove it or justify it in the project README"
    foreach ($file in $texFiles) {
        $model = $texModels[$file.Rel]
        if ($null -eq $model) { continue }
        $hash = (Get-FileHash -LiteralPath $file.Full -Algorithm SHA256).Hash
        if ($templateHashes.Contains($hash)) { continue }
        $code = $model.CodeText
        $starts = $model.LineStarts
        $hits = New-Object System.Collections.Generic.List[object]
        foreach ($m in $rxUsePackage.Matches($code)) {
            foreach ($name in $m.Groups[1].Value.Split(',')) {
                if ($layoutPackages.Contains($name.Trim())) { $hits.Add([pscustomobject]@{ Index = $m.Index; Text = "\usepackage{$($name.Trim())}" }) }
            }
        }
        foreach ($m in $rxLayoutStretch.Matches($code)) { $hits.Add([pscustomobject]@{ Index = $m.Index; Text = "\" + $m.Groups[1].Value }) }
        foreach ($m in $rxLayoutSetlength.Matches($code)) { $hits.Add([pscustomobject]@{ Index = $m.Index; Text = "length \" + $m.Groups[1].Value + " is set" }) }
        foreach ($m in $rxLayoutVspace.Matches($code)) { $hits.Add([pscustomobject]@{ Index = $m.Index; Text = "\" + $m.Groups[1].Value + "{-...}" }) }
        foreach ($m in $rxLayoutPage.Matches($code)) { $hits.Add([pscustomobject]@{ Index = $m.Index; Text = "\" + $m.Groups[1].Value }) }
        foreach ($m in $rxLayoutAssign.Matches($code)) { $hits.Add([pscustomobject]@{ Index = $m.Index; Text = "length \" + $m.Groups[1].Value + " is set" }) }
        foreach ($m in $rxLayoutHeading.Matches($code)) { $hits.Add([pscustomobject]@{ Index = $m.Index; Text = "\" + $m.Groups[1].Value + " is redefined" }) }
        foreach ($hit in ($hits | Sort-Object Index)) {
            Add-ProjectFinding $file.Rel (Get-LineNumber $starts $hit.Index) "layout" "$($hit.Text) found: the venue's layout must not be changed; remove it or justify it in the project README."
        }
    }
}
elseif ($null -ne $classInfo -and $distributionClass) {
    $standardClass = $true
}
elseif ($null -ne $classInfo -and $classIsLocal) {
    $templateNote = "class $className is a file of the project, no template folder contains it"
}
elseif ($null -ne $classInfo) {
    # not local, not in a template, not in the distribution: already reported as [missing] above
    $standardClass = $true
}

# Flat: name clashes are a static check as well
function Test-FlatClashes {
    $byLeaf = @{}
    foreach ($file in $script:included) {
        $leaf = [IO.Path]::GetFileName($file.Rel).ToLowerInvariant()
        if (-not $byLeaf.ContainsKey($leaf)) { $byLeaf[$leaf] = New-Object System.Collections.Generic.List[string] }
        $byLeaf[$leaf].Add($file.Rel)
    }
    $clash = $false
    foreach ($leaf in ($byLeaf.Keys | Sort-Object)) {
        if ($byLeaf[$leaf].Count -gt 1) {
            $clash = $true
            Add-ProjectFinding $byLeaf[$leaf][1] 1 "flat" "name clash in the flat layout: $($byLeaf[$leaf] -join ' and ') both become '$leaf'. Rename one of the files."
        }
    }
    return $clash
}
if ($Flat) { [void](Test-FlatClashes) }

# ---------------------------------------------------------------------------
# A6. Origin of the template (templates/SOURCES.tsv)
# ---------------------------------------------------------------------------

$script:templateOrigin = $null          # report line "Template origin: ..."
$originKind = $null                     # kind of the row in SOURCES.tsv (venue, house, other)
$templateShipsClass = ($null -ne $templateDirectory -and $null -ne $classLeafName -and
    @($templateFiles | Where-Object { $_.Name -ieq $classLeafName }).Count -gt 0)
# A class that only the project has: nothing records where it came from (a hand-made or unfiled template).
if ($null -eq $templateDirectory -and $classIsLocal) {
    Add-ProjectFinding $fileIndex[$classRelative] 1 "template-origin" "the class $classLeafName is a file of the project, but no folder of templates/ ships it, so its origin is not recorded. File the publisher's download under templates/<venue>/ with its row in templates/SOURCES.tsv (skill process-inbox)"
}
if ($templateShipsClass) {
    $originFolder = Split-Path -Leaf $templateDirectory
    $sourcesPath = Join-Path $templatesRoot "SOURCES.tsv"
    $sourcesDisplay = "templates/SOURCES.tsv"
    if (-not (Test-Path -LiteralPath $sourcesPath -PathType Leaf)) {
        Add-Finding $sourcesDisplay 1 "template-origin" "the file is missing, so the origin of templates/$originFolder is not recorded; a venue template must be the publisher's download (templates/README.md, section Provenance)"
    }
    else {
        $sourceLines = [System.IO.File]::ReadAllLines($sourcesPath, $utf8)
        $columns = @{}
        if ($sourceLines.Count -gt 0) {
            $names = $sourceLines[0].Split("`t")
            for ($k = 0; $k -lt $names.Count; $k++) { $columns[$names[$k].Trim()] = $k }
        }
        $missingColumns = @(@("folder", "kind", "version", "official_url", "archive", "sha256") | Where-Object { -not $columns.ContainsKey($_) })
        if ($missingColumns.Count -gt 0) {
            Add-Finding $sourcesDisplay 1 "template-origin" "the header lacks the column(s) $($missingColumns -join ', '): the origin of templates/$originFolder cannot be checked"
        }
        else {
            $row = $null
            $rowLine = 0
            for ($k = 1; $k -lt $sourceLines.Count; $k++) {
                $cells = $sourceLines[$k].Split("`t")
                if ($cells.Count -gt $columns["folder"] -and $cells[$columns["folder"]].Trim() -ieq $originFolder) { $row = $cells; $rowLine = $k + 1; break }
            }
            if ($null -eq $row) {
                Add-Finding $sourcesDisplay 1 "template-origin" "no row for templates/${originFolder}: its origin is not recorded. A venue template is the publisher's download, recorded with URL, archive and SHA-256 (templates/README.md, section Provenance)"
            }
            else {
                $cell = { param($name) if ($row.Count -gt $columns[$name]) { return $row[$columns[$name]].Trim() } return "" }
                $kind = & $cell "kind"
                $version = & $cell "version"
                $officialUrl = & $cell "official_url"
                $archive = & $cell "archive"
                $recordedHash = & $cell "sha256"
                $script:templateOrigin = "$originFolder ($kind, $version, $officialUrl)"
                $originKind = $kind
                switch ($kind) {
                    "venue" {
                        if ($officialUrl -notmatch '^https://\S+$') {
                            Add-Finding $sourcesDisplay $rowLine "template-origin" "templates/${originFolder}: official_url '$officialUrl' is not an https address of the publisher's download"
                        }
                        $archiveFull = $null
                        if ($archive -eq "" -or $archive -eq "-") {
                            Add-Finding $sourcesDisplay $rowLine "template-origin" "templates/${originFolder}: no archive recorded; keep the downloaded zip under archives/ and record its path and SHA-256"
                        }
                        elseif ($archive -match '^[A-Za-z]:|^[\\/]' -or ($archive -split '[\\/]') -contains '..') {
                            Add-Finding $sourcesDisplay $rowLine "template-origin" "templates/${originFolder}: archive '$archive' must be a path inside the workspace (relative, no ..)"
                        }
                        else {
                            $archiveFull = Join-Path $workspace $archive.Replace('/', '\')
                            if (-not (Test-Path -LiteralPath $archiveFull -PathType Leaf)) {
                                Add-Finding $sourcesDisplay $rowLine "template-origin" "templates/${originFolder}: the archive $archive does not exist; the download cannot be proved"
                            }
                            else {
                                $actualHash = (Get-FileHash -LiteralPath $archiveFull -Algorithm SHA256).Hash
                                if ($actualHash -ine $recordedHash) {
                                    Add-Finding $sourcesDisplay $rowLine "template-origin" "templates/${originFolder}: SHA-256 of $archive is $($actualHash.ToLowerInvariant().Substring(0, 16))..., the row records '$(Format-Short $recordedHash 20)'; the archive is not the recorded download"
                                }
                            }
                        }
                    }
                    "other" {
                        Add-Finding $sourcesDisplay $rowLine "template-origin" "templates/$originFolder is not a publisher template (other): $(Format-Short (& $cell 'note') 90)" $false
                    }
                    "house" { }
                    default {
                        Add-Finding $sourcesDisplay $rowLine "template-origin" "templates/${originFolder}: unknown kind '$kind' (venue, house or other)"
                    }
                }
            }
        }
    }
}

# ---------------------------------------------------------------------------
# I. AI declaration (advisory)
# ---------------------------------------------------------------------------

$sectionSign = [string][char]0x00A7
$aiPolicyText = "venue policy: knowledge/writing/submission.md ${sectionSign}1 - Elsevier, Springer Nature, SIAM, Wiley and others require the statement in the manuscript when AI tools were used beyond grammar checking"
$rxHeadingArgument = [regex]::new('\\([A-Za-z@]+)\*?\s*(?:\[[^\]]*\]\s*)?\{((?:[^{}]|\{[^{}]*\})*)\}', $rxNone)
$rxDeclarationTitle = [regex]::new('Declaration\s+of\s+generative\s+AI|Use\s+of\s+AI\s+tools|AI-assisted\s+technologies', $rxIgnoreCase)
$aiDeclarationFound = $null
foreach ($file in $texFiles) {
    $model = $texModels[$file.Rel]
    if ($null -eq $model) { continue }
    foreach ($m in $rxHeadingArgument.Matches($model.CodeText)) {
        if ($rxDeclarationTitle.IsMatch($m.Groups[2].Value)) {
            $aiDeclarationFound = [pscustomobject]@{ Rel = $file.Rel; Line = (Get-LineNumber $model.LineStarts $m.Index); Title = (Format-Short $m.Groups[2].Value 60) }
            break
        }
    }
    if ($null -ne $aiDeclarationFound) { break }
}
if ($null -ne $aiDeclarationFound) {
    $script:aiDeclarationLine = "AI declaration: '$($aiDeclarationFound.Title)' in projects/$Project/$($aiDeclarationFound.Rel):$($aiDeclarationFound.Line) (packaged)"
}
else {
    $draftNames = @()
    $submissionDirectory = Join-Path $projectDirectory "submission"
    if (Test-Path -LiteralPath $submissionDirectory -PathType Container) {
        $draftNames = @(Get-ChildItem -LiteralPath $submissionDirectory -File -Filter '*ai-declaration*.tex' | Sort-Object Name | ForEach-Object { "projects/$Project/submission/$($_.Name)" })
    }
    if ($draftNames.Count -gt 0) {
        $draftText = "a draft exists at $($draftNames -join ', ') and was not packaged (if AI tools were used, insert it as sections/91-ai-declaration.tex, directly before the references)"
    }
    else { $draftText = "no draft in projects/$Project/submission/" }
    Add-ProjectFinding $MainFile 1 "ai-declaration" "no section 'Declaration of generative AI ...', 'Use of AI tools' or '... AI-assisted technologies ...' in the packaged .tex files; $draftText; $aiPolicyText"
    $script:aiDeclarationLine = "AI declaration: none in the manuscript; $draftText; $aiPolicyText"
}

# ---------------------------------------------------------------------------
# T. Trace scan: workspace, tool and AI traces in everything that is sent
# ---------------------------------------------------------------------------

$latin1 = [System.Text.Encoding]::GetEncoding(28591)
$script:traceRules = New-Object System.Collections.Generic.List[object]
$script:traceSeen = New-Object 'System.Collections.Generic.HashSet[string]'
$script:traceFiles = New-StringSet @()
$script:traceSkipped = New-StringSet @()      # project files identical to a template file (the publisher's): not scanned
$script:traceHitCount = 0
$script:traceAllowedCount = 0
$script:allowRules = New-Object System.Collections.Generic.List[object]
$script:workspaceEntryCache = @{}

# Check: "" = everywhere; "backslash" = not in TeX code, $...$ masked; "exists" = groups 1 and 2 name an entry of the workspace
function Add-TraceRule([string]$Id, [string]$Group, [string]$Label, [string]$Pattern, [string]$Check) {
    $script:traceRules.Add([pscustomobject]@{ Id = $Id; Group = $Group; Label = $Label; Regex = [regex]::new($Pattern, $rxIgnoreCase); Check = $Check })
}

Add-TraceRule "todo" "workspace" "unfinished-work marker" '(?<![A-Za-z0-9])(?:todo|fixme)s?(?![A-Za-z])' ""
Add-TraceRule "vendor-address" "workspace" "AI vendor address" '(?<![A-Za-z0-9])(?:claude\.(?:ai|com)|anthropic\.com)(?![A-Za-z0-9])' ""
Add-TraceRule "trailer" "workspace" "tool trailer" '(?<![A-Za-z0-9])(?:co-authored-by|generated\s+with\s+(?:\[|claude(?![A-Za-z]))|noreply@)' ""
Add-TraceRule "tool-config" "workspace" "AI tool configuration path" '(?<![A-Za-z0-9])claude\.md(?![A-Za-z0-9])|(?<![A-Za-z0-9])\.claude[\\/]' ""
$traceUser = ("" + $env:USERNAME).Trim()
$genericUsers = New-StringSet @("user", "users", "admin", "administrator", "owner", "guest", "home", "test", "default", "public", "student", "author")
if ($traceUser.Length -ge 4 -and -not $genericUsers.Contains($traceUser)) {
    Add-TraceRule "user-name" "workspace" "Windows user name of this machine" ('(?<![A-Za-z0-9])' + [regex]::Escape($traceUser) + '(?![A-Za-z0-9])') ""
}
$traceProfile = ("" + $env:USERPROFILE).Trim().TrimEnd('\')
if ($traceProfile -match '^[A-Za-z]:\\[^\\]+') {
    $profileSegments = @($traceProfile.Split('\') | ForEach-Object { [regex]::Escape($_) })
    Add-TraceRule "user-profile" "workspace" "user profile path" ('(?<![A-Za-z0-9])' + ($profileSegments -join '(?:\\{1,2}|/)') + '(?![A-Za-z0-9])') ""
}
# A drive letter preceded by a letter, digit, dot, slash or hyphen is part of a word or URL (https://x.org/a:/b/),
# except after file:///.
Add-TraceRule "abs-path" "workspace" "absolute Windows path" '(?:(?<=file:///)|(?<![A-Za-z0-9_./\\-]))[A-Za-z]:/(?=[A-Za-z0-9_.$~-])[^\s/\\:*?"<>|{}%]{1,64}/' ""
Add-TraceRule "abs-path" "workspace" "absolute Windows path" '(?<![A-Za-z0-9_./\\-])[A-Za-z]:\\{1,2}(?=[A-Za-z0-9_.~-])[^\s/\\:*?"<>|{}%$]{1,64}\\' "backslash"
Add-TraceRule "workspace-path" "workspace" "path into this workspace" '(?<![A-Za-z0-9_.\-])(knowledge|archives|outputs|inbox|scripts|tmp|projects)[\\/]{1,2}([A-Za-z0-9_.\-]+)' "exists"
Add-TraceRule "ai-name" "ai" "AI tool name" '(?<![A-Za-z0-9])(?:claude(?:\s+code)?|anthropic|chat-?gpt|openai|copilot|gemini)(?![A-Za-z])|(?<![A-Za-z0-9])gpt-?\d' ""
Add-TraceRule "ai-generated" "ai" "AI-generation statement" '(?<![A-Za-z0-9])(?:ai[- ]generated|generated\s+by\s+(?:an?\s+)?ai)(?![A-Za-z])' ""

$rxMathSpan = [regex]::new('\$[^$\r\n]*\$', $rxNone)
$traceMask = [System.Text.RegularExpressions.MatchEvaluator] { param($m) (' ' * $m.Length) }
$texLikeExtensions = New-StringSet @(".sty", ".cls", ".clo", ".def", ".cfg", ".ltx", ".dtx", ".ins", ".bbx", ".cbx", ".lbx", ".tikz", ".pgf", ".bbl", ".xmpdata")

function Test-WorkspaceEntry([string]$Folder, [string]$Name) {
    $leaf = $Name.TrimEnd('.')
    if ($leaf.Length -eq 0) { return $false }
    $key = ($Folder + '/' + $leaf).ToLowerInvariant()
    if (-not $script:workspaceEntryCache.ContainsKey($key)) {
        $script:workspaceEntryCache[$key] = Test-Path -LiteralPath (Join-Path (Join-Path $workspace $Folder) $leaf)
    }
    return $script:workspaceEntryCache[$key]
}

# Hits of all rules in one line of text; overlapping hits: a workspace trace wins over an AI name, then the
# earlier and the longer hit. The "backslash" rule only counts from $BackslashPathFrom on (TeX: the comment).
function Find-TraceHits([string]$Text, [int]$BackslashPathFrom) {
    $found = New-Object System.Collections.Generic.List[object]
    $accepted = New-Object System.Collections.Generic.List[object]
    if ([string]::IsNullOrEmpty($Text)) { return , $accepted }
    $masked = $null
    foreach ($rule in $script:traceRules) {
        $subject = $Text
        if ($rule.Check -eq "backslash") {
            if ($BackslashPathFrom -ge $Text.Length) { continue }
            if ($null -eq $masked) { $masked = $rxMathSpan.Replace($Text, $traceMask) }
            $subject = $masked
        }
        foreach ($m in $rule.Regex.Matches($subject)) {
            if ($rule.Check -eq "backslash" -and $m.Index -lt $BackslashPathFrom) { continue }
            if ($rule.Check -eq "exists" -and -not (Test-WorkspaceEntry $m.Groups[1].Value $m.Groups[2].Value)) { continue }
            $found.Add([pscustomobject]@{ Rule = $rule; Index = $m.Index; Length = $m.Length; Value = $Text.Substring($m.Index, $m.Length) })
        }
    }
    if ($found.Count -eq 0) { return , $accepted }
    $ordered = @($found | Sort-Object @{ Expression = { if ($_.Rule.Group -eq "workspace") { 0 } else { 1 } } }, Index, @{ Expression = { - $_.Length } })
    foreach ($hit in $ordered) {
        $overlap = $false
        foreach ($other in $accepted) {
            if ($hit.Index -lt $other.Index + $other.Length -and $other.Index -lt $hit.Index + $hit.Length) { $overlap = $true; break }
        }
        if (-not $overlap) { $accepted.Add($hit) }
    }
    return , $accepted
}

function Get-TraceSnippet([string]$Text, [int]$Index, [int]$Length) {
    $start = [Math]::Max(0, $Index - 30)
    $end = [Math]::Min($Text.Length, $Index + $Length + 30)
    $snippet = ($Text.Substring($start, $end - $start) -replace '\s+', ' ').Trim()
    if ($start -gt 0) { $snippet = "..." + $snippet }
    if ($end -lt $Text.Length) { $snippet += "..." }
    return $snippet
}

# Scans one line and records its hits. $CommentFrom >= 0: hits from there on are in a TeX comment.
# $KeySource and $KeyText identify the place across the phases (project file and its staged copy are one place),
# so a hit is reported once. $Once (binary files) reports each term once per file.
function Register-TraceText([string]$File, [int]$Line, [string]$Text, [int]$BackslashPathFrom, [int]$CommentFrom,
    [string]$Where, [string]$KeySource, [string]$KeyText, [bool]$Declaration, [hashtable]$Once) {
    $hits = Find-TraceHits $Text $BackslashPathFrom
    if ($hits.Count -eq 0) { return }
    $context = $KeyText
    if ([string]::IsNullOrEmpty($context)) { $context = ($Text -replace '\s+', ' ').Trim() }
    foreach ($hit in $hits) {
        $valueKey = ($hit.Value -replace '\s+', ' ').ToLowerInvariant()
        if ($null -ne $Once) {
            $onceKey = $hit.Rule.Id + "|" + $valueKey
            if ($Once.ContainsKey($onceKey)) { continue }
            $Once[$onceKey] = $true
        }
        if (-not $script:traceSeen.Add("$KeySource|$($hit.Rule.Id)|$valueKey|$context")) { continue }
        $script:traceHitCount++
        $place = $Where
        if ($CommentFrom -ge 0 -and $hit.Index -ge $CommentFrom) { $place = "comment" }
        $snippet = Get-TraceSnippet $Text $hit.Index $hit.Length
        $allowedBy = $null
        if ($hit.Rule.Group -eq "ai") {
            if ($Declaration) { $allowedBy = "the AI declaration file" }
            else {
                foreach ($allow in $script:allowRules) {
                    foreach ($m in $allow.Regex.Matches($Text)) {
                        if ($m.Index -lt $hit.Index + $hit.Length -and $hit.Index -lt $m.Index + [Math]::Max(1, $m.Length)) {
                            $allowedBy = "submission/package-allow.txt line $($allow.Line)"
                            if ($allow.Reason -ne "") { $allowedBy += " ($(Format-Short $allow.Reason 50))" }
                            break
                        }
                    }
                    if ($null -ne $allowedBy) { break }
                }
            }
        }
        if ($null -ne $allowedBy) {
            $script:traceAllowedCount++
            Add-Finding $File $Line "trace" "allowed by ${allowedBy}: $($hit.Rule.Label) '$($hit.Value)' in ${place}: $snippet" $false
        }
        elseif ($hit.Rule.Group -eq "workspace") {
            Add-Finding $File $Line "trace" "$($hit.Rule.Label) '$($hit.Value)' in ${place}: $snippet; remove it in the project (workspace traces cannot be allowed)"
        }
        else {
            Add-Finding $File $Line "trace" "$($hit.Rule.Label) '$($hit.Value)' in ${place}: $snippet; name a tool only in the AI declaration (sections/91-ai-declaration.tex), or allow the term with a reason in submission/package-allow.txt"
        }
    }
}

# Every line of a block of text (metadata value, XMP packet, PDF objects) as one place.
function Register-TraceBlock([string]$File, [string]$Where, [string]$Text, [string]$KeySource, [hashtable]$Once) {
    if ([string]::IsNullOrEmpty($Text)) { return }
    foreach ($part in ($Text -split '[\r\n\x00]+')) {
        if ($part.Trim().Length -lt 3) { continue }
        Register-TraceText $File 1 $part 0 -1 $Where $KeySource "" $false $Once
    }
}

# Printable runs (ASCII and UTF-16LE) of a byte range, as lines.
function Get-PrintableRuns([byte[]]$Bytes, [int]$Offset, [int]$Count) {
    $runs = New-Object System.Text.StringBuilder
    $text = $latin1.GetString($Bytes, $Offset, $Count)
    [void]$runs.Append(([regex]::Replace($text, '[^\x20-\x7E\t]+', "`n")))
    foreach ($shift in @(0, 1)) {
        if ($Count - $shift -lt 8) { continue }
        $wide = [System.Text.Encoding]::Unicode.GetString($Bytes, $Offset + $shift, ($Count - $shift) - (($Count - $shift) % 2))
        [void]$runs.Append("`n").Append(([regex]::Replace($wide, '[^\x20-\x7E\t]+', "`n")))
    }
    return (($runs.ToString() -split "`n") | Where-Object { $_.Trim().Length -ge 4 }) -join "`n"
}

# zlib data (2-byte header, deflate, Adler-32) to bytes; $null when it cannot be inflated. At most 32 MB.
function Expand-Zlib([byte[]]$Bytes, [int]$Offset, [int]$Count) {
    if ($Count -lt 3) { return $null }
    try {
        $source = New-Object System.IO.MemoryStream($Bytes, ($Offset + 2), ($Count - 2))
        $inflater = New-Object System.IO.Compression.DeflateStream($source, [System.IO.Compression.CompressionMode]::Decompress)
        $target = New-Object System.IO.MemoryStream
        $buffer = New-Object byte[] 65536
        while ($true) {
            $read = $inflater.Read($buffer, 0, $buffer.Length)
            if ($read -le 0) { break }
            $target.Write($buffer, 0, $read)
            if ($target.Length -gt 32MB) { break }
        }
        $inflater.Dispose()
        return $target.ToArray()
    }
    catch { return $null }
}

function Get-BigEndian32([byte[]]$Bytes, [int]$At) {
    return ([int]$Bytes[$At] -shl 24) -bor ([int]$Bytes[$At + 1] -shl 16) -bor ([int]$Bytes[$At + 2] -shl 8) -bor [int]$Bytes[$At + 3]
}

function Invoke-TracePng([byte[]]$Bytes, [string]$File, [string]$KeySource) {
    $once = @{}
    $signature = @(137, 80, 78, 71, 13, 10, 26, 10)
    $valid = ($Bytes.Length -ge 8)
    for ($k = 0; $valid -and $k -lt 8; $k++) { if ($Bytes[$k] -ne $signature[$k]) { $valid = $false } }
    if (-not $valid) { Register-TraceBlock $File "binary content (not a valid PNG)" (Get-PrintableRuns $Bytes 0 $Bytes.Length) $KeySource $once; return }
    $position = 8
    while ($position + 12 -le $Bytes.Length) {
        $length = Get-BigEndian32 $Bytes $position
        $type = [System.Text.Encoding]::ASCII.GetString($Bytes, $position + 4, 4)
        $start = $position + 8
        if ($length -lt 0 -or $start + $length -gt $Bytes.Length) { break }
        if ($type -in @("tEXt", "zTXt", "iTXt", "iCCP", "eXIf")) {
            $zero = [Array]::IndexOf($Bytes, [byte]0, $start, $length)
            $keyword = ""
            if ($zero -ge 0) { $keyword = $latin1.GetString($Bytes, $start, $zero - $start) }
            $where = "PNG $type chunk '$keyword'"
            $value = $null
            if ($type -eq "tEXt" -and $zero -ge 0) { $value = $keyword + ": " + $latin1.GetString($Bytes, $zero + 1, $start + $length - $zero - 1) }
            elseif ($type -eq "zTXt" -and $zero -ge 0) {
                $inflated = Expand-Zlib $Bytes ($zero + 2) ($start + $length - $zero - 2)
                if ($null -ne $inflated) { $value = $keyword + ": " + $latin1.GetString($inflated) }
            }
            elseif ($type -eq "iTXt" -and $zero -ge 0 -and $zero + 3 -le $start + $length) {
                $compressed = $Bytes[$zero + 1]
                $languageEnd = [Array]::IndexOf($Bytes, [byte]0, $zero + 3, $start + $length - $zero - 3)
                $translatedEnd = -1
                if ($languageEnd -ge 0) { $translatedEnd = [Array]::IndexOf($Bytes, [byte]0, $languageEnd + 1, $start + $length - $languageEnd - 1) }
                if ($translatedEnd -ge 0) {
                    $textStart = $translatedEnd + 1
                    $textBytes = $null
                    if ($compressed -eq 1) { $textBytes = Expand-Zlib $Bytes $textStart ($start + $length - $textStart) }
                    else { $textBytes = New-Object byte[] ($start + $length - $textStart); [Array]::Copy($Bytes, $textStart, $textBytes, 0, $textBytes.Length) }
                    if ($null -ne $textBytes) { $value = $keyword + ": " + $utf8.GetString($textBytes) }
                }
            }
            elseif ($type -eq "iCCP") { $value = $keyword }
            else { $value = Get-PrintableRuns $Bytes $start $length }
            Register-TraceBlock $File $where $value $KeySource $once
        }
        if ($type -eq "IEND") { break }
        $position = $start + $length + 4
    }
}

function Invoke-TraceJpeg([byte[]]$Bytes, [string]$File, [string]$KeySource) {
    $once = @{}
    if ($Bytes.Length -lt 4 -or $Bytes[0] -ne 0xFF -or $Bytes[1] -ne 0xD8) {
        Register-TraceBlock $File "binary content (not a valid JPEG)" (Get-PrintableRuns $Bytes 0 $Bytes.Length) $KeySource $once
        return
    }
    $position = 2
    while ($position + 4 -le $Bytes.Length) {
        if ($Bytes[$position] -ne 0xFF) { break }
        $marker = [int]$Bytes[$position + 1]
        if ($marker -eq 0xFF) { $position++; continue }
        if ($marker -eq 0xD9 -or $marker -eq 0xDA) { break }
        if (($marker -ge 0xD0 -and $marker -le 0xD7) -or $marker -eq 0x01) { $position += 2; continue }
        $length = ([int]$Bytes[$position + 2] -shl 8) -bor [int]$Bytes[$position + 3]
        if ($length -lt 2 -or $position + 2 + $length -gt $Bytes.Length) { break }
        if (($marker -ge 0xE0 -and $marker -le 0xEF) -or $marker -eq 0xFE) {
            $where = $(if ($marker -eq 0xFE) { "JPEG comment" } else { "JPEG APP$($marker - 0xE0) segment" })
            Register-TraceBlock $File $where (Get-PrintableRuns $Bytes ($position + 4) ($length - 2)) $KeySource $once
        }
        $position += 2 + $length
    }
}

$rxPdfStream = [regex]::new('(?<![A-Za-z])stream(?:\r\n|\n|\r)', $rxNone)
function Invoke-TracePdf([string]$Full, [byte[]]$Bytes, [string]$File, [string]$KeySource) {
    $once = @{}
    $info = Invoke-Tool "pdfinfo" @("-enc", "UTF-8", $Full) $workspace
    if ($info.ExitCode -eq 0) {
        foreach ($line in ($info.Output -split "`r?`n")) {
            if ($line -match '^(Title|Author|Subject|Keywords|Creator|Producer):\s*(.*)$') {
                Register-TraceBlock $File ("PDF info " + $Matches[1]) $Matches[2] $KeySource $once
            }
        }
        $meta = Invoke-Tool "pdfinfo" @("-meta", $Full) $workspace
        if ($meta.ExitCode -eq 0) { Register-TraceBlock $File "XMP metadata" $meta.Output $KeySource $once }
    }
    # Byte search: the objects outside streams, object streams and metadata streams (Flate or unfiltered).
    $raw = $latin1.GetString($Bytes)
    $outside = New-Object System.Text.StringBuilder
    $previous = 0
    $search = 0
    while ($search -lt $raw.Length) {
        $m = $rxPdfStream.Match($raw, $search)
        if (-not $m.Success) { break }
        $dataStart = $m.Index + $m.Length
        $dataEnd = $raw.IndexOf("endstream", $dataStart, [System.StringComparison]::Ordinal)
        if ($dataEnd -lt 0) { break }
        [void]$outside.Append($raw, $previous, $dataStart - $previous).Append("`n")
        $dictionaryStart = [Math]::Max($previous, $m.Index - 2048)
        $dictionary = $raw.Substring($dictionaryStart, $m.Index - $dictionaryStart)
        $objectAt = $dictionary.LastIndexOf(" obj")
        if ($objectAt -ge 0) { $dictionary = $dictionary.Substring($objectAt) }
        if ($dictionary -match '/Type\s*/(ObjStm|Metadata)\b' -or $dictionary -match '/Subtype\s*/XML\b') {
            $kind = $(if ($dictionary -match '/Type\s*/ObjStm\b') { "PDF object stream" } else { "PDF metadata stream" })
            $count = $dataEnd - $dataStart
            $decoded = $null
            if ($dictionary -notmatch '/Filter') { $decoded = $raw.Substring($dataStart, $count) }
            elseif ($dictionary -match '/Filter\s*(?:\[\s*)?/FlateDecode\s*\]?' -and $dictionary -notmatch '/DecodeParms') {
                $inflated = Expand-Zlib $Bytes $dataStart $count
                if ($null -ne $inflated) {
                    try { $decoded = $utf8Strict.GetString($inflated) } catch { $decoded = $latin1.GetString($inflated) }
                }
            }
            if ($null -ne $decoded) { Register-TraceBlock $File $kind $decoded $KeySource $once }
        }
        $previous = $dataEnd
        $search = $dataEnd + 9
    }
    if ($previous -lt $raw.Length) { [void]$outside.Append($raw, $previous, $raw.Length - $previous) }
    Register-TraceBlock $File "PDF objects" $outside.ToString() $KeySource $once
}

function Invoke-TraceEps([byte[]]$Bytes, [string]$File, [string]$KeySource) {
    $start = 0
    $count = $Bytes.Length
    if ($count -ge 30 -and $Bytes[0] -eq 0xC5 -and $Bytes[1] -eq 0xD0 -and $Bytes[2] -eq 0xD3 -and $Bytes[3] -eq 0xC6) {
        $start = [BitConverter]::ToInt32($Bytes, 4)
        $count = [BitConverter]::ToInt32($Bytes, 8)
        if ($start -lt 0 -or $count -lt 0 -or $start + $count -gt $Bytes.Length) { $start = 0; $count = $Bytes.Length }
    }
    $lines = $latin1.GetString($Bytes, $start, $count) -split "\r\n|\r|\n"
    $inPacket = $false
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line -match '<\?xpacket begin') { $inPacket = $true }
        if ($inPacket -or $line.StartsWith('%') -or $line -match 'pdfmark') {
            Register-TraceText $File ($i + 1) $line 0 -1 "EPS header or metadata" $KeySource "" $false $null
        }
        if ($line -match '<\?xpacket end') { $inPacket = $false }
    }
}

$rxBibEntryStart = [regex]::new('\G@\s*([A-Za-z]+)\s*([{(])', $rxNone)
$bibTopLevelStops = [char[]]@('@', "`n")
$bibBraces = [char[]]@('{', '}', '(', ')')

# Index of the delimiter that closes the entry opened at $Open ('{' or '('); -1 when unbalanced.
function Find-BibEntryEnd([string]$Text, [int]$Open, [string]$Delimiter) {
    $depth = 0
    $parens = 0
    $k = $Open
    while ($k -lt $Text.Length) {
        $k = $Text.IndexOfAny($bibBraces, $k)
        if ($k -lt 0) { return -1 }
        $ch = $Text[$k]
        if ($Delimiter -eq '{') {
            if ($ch -eq '{') { $depth++ }
            elseif ($ch -eq '}') { $depth--; if ($depth -eq 0) { return $k } }
        }
        else {
            if ($ch -eq '{') { $depth++ }
            elseif ($ch -eq '}') { $depth-- }
            elseif ($ch -eq '(' -and $depth -eq 0) { $parens++ }
            elseif ($ch -eq ')' -and $depth -eq 0) { $parens--; if ($parens -eq 0) { return $k } }
        }
        $k++
    }
    return -1
}

# A .bib text as staged without -KeepComments: lines that start with % outside entries and @comment blocks removed.
# Returns Lines (Number = line in the project file, Text without the line feed), Changed, Text (the staged text).
function Get-BibStagedLines([string]$Text) {
    $n = $Text.Length
    $ranges = New-Object System.Collections.Generic.List[int[]]     # removed [start, end) ranges, in order
    $i = 0
    $lineStart = $true
    while ($i -lt $n) {
        if ($lineStart) {
            $j = $i
            while ($j -lt $n -and ($Text[$j] -eq [char]' ' -or $Text[$j] -eq [char]"`t")) { $j++ }
            if ($j -lt $n -and $Text[$j] -eq [char]'%') {
                $end = $Text.IndexOf("`n", $j)
                if ($end -lt 0) { $end = $n - 1 }
                $ranges.Add([int[]]@($i, ($end + 1)))
                $i = $end + 1
                continue
            }
            $lineStart = $false
        }
        $next = $Text.IndexOfAny($bibTopLevelStops, $i)
        if ($next -lt 0) { break }
        if ($Text[$next] -eq [char]"`n") { $i = $next + 1; $lineStart = $true; continue }
        $m = $rxBibEntryStart.Match($Text, $next)
        if (-not $m.Success) { $i = $next + 1; continue }
        $close = Find-BibEntryEnd $Text ($m.Index + $m.Length - 1) $m.Groups[2].Value
        if ($close -lt 0) { break }     # unbalanced entry: the rest stays as it is
        if ($m.Groups[1].Value -ieq 'comment') { $ranges.Add([int[]]@($next, ($close + 1))) }
        $i = $close + 1
    }
    $lines = New-Object System.Collections.Generic.List[object]
    $kept = New-Object System.Collections.Generic.List[string]
    $changed = ($ranges.Count -gt 0)
    $rangeIndex = 0
    $start = 0
    $number = 1
    while ($start -le $n) {
        $end = $Text.IndexOf("`n", $start)
        $stop = $(if ($end -lt 0) { $n } else { $end + 1 })
        while ($rangeIndex -lt $ranges.Count -and $ranges[$rangeIndex][1] -le $start) { $rangeIndex++ }
        $content = $null
        $removed = $false
        if ($rangeIndex -lt $ranges.Count -and $ranges[$rangeIndex][0] -lt $stop) {
            $removed = $true
            $builder = New-Object System.Text.StringBuilder
            for ($k = $start; $k -lt $stop; $k++) {
                $inRange = $false
                for ($r = $rangeIndex; $r -lt $ranges.Count -and $ranges[$r][0] -le $k; $r++) { if ($k -lt $ranges[$r][1]) { $inRange = $true; break } }
                if (-not $inRange -and $Text[$k] -ne [char]"`n") { [void]$builder.Append($Text[$k]) }
            }
            $content = $builder.ToString()
        }
        else { $content = $Text.Substring($start, $stop - $start).TrimEnd([char]"`n") }
        if (-not ($removed -and $content.Trim().Length -eq 0)) {
            $lines.Add([pscustomobject]@{ Number = $number; Text = $content })
            $kept.Add($content)
        }
        if ($end -lt 0) { break }
        $start = $end + 1
        $number++
    }
    return [pscustomobject]@{ Lines = $lines; Changed = $changed; Text = ($kept -join "`n") }
}

# Scans one file. $PredictStage: a project file, scanned as staging will write it (comment lines that staging
# removes are skipped); otherwise the file as it is (a staged file). A file that cannot be scanned fails: nothing
# proves that it is clean.
function Invoke-TraceFile([string]$Full, [string]$Rel, [string]$File, [string]$KeySource, [bool]$PredictStage) {
    [void]$script:traceFiles.Add($KeySource)        # a project file and its staged copy count once
    try { Invoke-TraceFileContent $Full $Rel $File $KeySource $PredictStage }
    catch {
        Add-Finding $File 1 "trace" "the file could not be scanned ($($_.Exception.Message)); nothing proves that it carries no trace. Export it again or remove it from the project"
    }
}

function Invoke-TraceFileContent([string]$Full, [string]$Rel, [string]$File, [string]$KeySource, [bool]$PredictStage) {
    $extension = [IO.Path]::GetExtension($Rel).ToLowerInvariant()
    $leaf = [IO.Path]::GetFileName($Rel)
    $bytes = [System.IO.File]::ReadAllBytes($Full)
    if ($extension -eq ".png") { Invoke-TracePng $bytes $File $KeySource; return }
    if ($extension -eq ".jpg" -or $extension -eq ".jpeg") { Invoke-TraceJpeg $bytes $File $KeySource; return }
    if ($extension -eq ".pdf") { Invoke-TracePdf $Full $bytes $File $KeySource; return }
    if ($extension -eq ".eps" -or $extension -eq ".ps") { Invoke-TraceEps $bytes $File $KeySource; return }
    if ([Array]::IndexOf($bytes, [byte]0) -ge 0) {
        Register-TraceBlock $File "binary content" (Get-PrintableRuns $bytes 0 $bytes.Length) $KeySource @{}
        return
    }
    $valid = $true
    try { $text = $utf8Strict.GetString($bytes) } catch { $text = $latin1.GetString($bytes); $valid = $false }
    if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) { $text = $text.Substring(1) }
    $declaration = ($extension -eq ".tex" -and ($leaf -like '*ai-declaration*' -or $leaf -like '*ai-statement*'))
    if ($extension -eq ".tex" -or $texLikeExtensions.Contains($extension)) {
        $strip = ($PredictStage -and $extension -eq ".tex" -and $valid -and -not $KeepComments)
        $model = Get-TexModel $text
        for ($i = 0; $i -lt $model.Raw.Count; $i++) {
            $line = $model.Raw[$i].TrimEnd([char]"`r")
            $at = $model.CommentAt[$i]
            $from = 0
            $commentFrom = -1
            if (-not $model.Keep[$i]) {
                if ($at -ge 0 -and $at -le $line.Length) {
                    if ($strip -and $line.Substring(0, $at).Trim().Length -eq 0 -and -not ($i -lt 5 -and $line -match '^\s*%\s*!')) { continue }
                    $from = $at
                    $commentFrom = $at
                }
                else { $from = $line.Length }
            }
            Register-TraceText $File ($i + 1) $line $from $commentFrom "text" $KeySource "" $declaration $null
        }
        return
    }
    if ($extension -eq ".bib") {
        $entries = $null
        if ($PredictStage -and $valid -and -not $KeepComments) { $entries = (Get-BibStagedLines $text).Lines }
        else {
            $entries = New-Object System.Collections.Generic.List[object]
            $number = 1
            foreach ($line in ($text -split "`n")) { $entries.Add([pscustomobject]@{ Number = $number; Text = $line }); $number++ }
        }
        foreach ($entry in $entries) {
            Register-TraceText $File $entry.Number $entry.Text.TrimEnd([char]"`r") 0 -1 "text" $KeySource "" $false $null
        }
        return
    }
    if ($extension -eq ".svg") { $text = [regex]::Replace($text, '(?i)base64,[A-Za-z0-9+/=\s]+', 'base64,') }
    $number = 1
    foreach ($line in ($text -split "`n")) {
        Register-TraceText $File $number $line.TrimEnd([char]"`r") 0 -1 "text" $KeySource "" $false $null
        $number++
    }
}

# Allowed AI tool names of this project
$allowFile = Join-Path $projectDirectory "submission\package-allow.txt"
if (Test-Path -LiteralPath $allowFile -PathType Leaf) {
    $allowLines = [System.IO.File]::ReadAllLines($allowFile, $utf8)
    for ($i = 0; $i -lt $allowLines.Count; $i++) {
        $line = $allowLines[$i]
        if ($line.Trim().Length -eq 0 -or $line.Trim().StartsWith('#')) { continue }
        $pattern = $line
        $reason = ""
        $cut = [regex]::Match($line, '\s#')
        if ($cut.Success) { $pattern = $line.Substring(0, $cut.Index); $reason = $line.Substring($cut.Index).Trim().TrimStart('#').Trim() }
        $pattern = $pattern.Trim()
        try { $allowRegex = [regex]::new($pattern, $rxIgnoreCase) }
        catch {
            Add-ProjectFinding "submission/package-allow.txt" ($i + 1) "trace" "invalid regular expression '$pattern': the allowlist cannot be applied; fix the line"
            continue
        }
        $script:allowRules.Add([pscustomobject]@{ Regex = $allowRegex; Line = ($i + 1); Reason = $reason })
    }
}

# T (a): every file that would be packaged, as it will be staged, and its path
foreach ($file in $script:included) {
    $extension = [IO.Path]::GetExtension($file.Rel).ToLowerInvariant()
    # files of a publisher or third-party template (venue, other) are theirs; files of a house template are ours
    if ($null -ne $templateHashes -and ($originKind -eq "venue" -or $originKind -eq "other") -and $extension -ne ".tex" -and $extension -ne ".bib") {
        if ($templateHashes.Contains((Get-FileHash -LiteralPath $file.Full -Algorithm SHA256).Hash)) { [void]$script:traceSkipped.Add($file.Rel); continue }
    }
    if ($extension -eq ".bib" -and -not $KeepComments -and $null -eq (Read-SourceText $file.Full)) {
        Add-ProjectFinding $file.Rel 1 "encoding" "not valid UTF-8: copied unchanged (comment lines are not removed)"
    }
    $display = "projects/$Project/$($file.Rel)"
    Register-TraceText $display 1 $file.Rel 0 -1 "file name" $file.Rel "<file name>" $false $null
    Invoke-TraceFile $file.Full $file.Rel $display $file.Rel $true
}

# ---------------------------------------------------------------------------
# Report (H)
# ---------------------------------------------------------------------------

$script:run = [pscustomobject]@{
    Stopped    = $null      # why staging did not happen
    Pages      = $null
    ZipEntries = $null      # list of Name, Length
    ZipBuilt   = $false
    PdfBuilt   = $false
    CommentNotes = 0
}

function Complete-Run {
    $fileOrder = @{}
    $position = 0
    foreach ($file in $script:included) { $fileOrder["projects/$Project/$($file.Rel)"] = $position; $position++ }
    foreach ($finding in $script:findings) {
        if (-not $fileOrder.ContainsKey($finding.File)) { $fileOrder[$finding.File] = $position; $position++ }
    }
    $categoryRank = @{}
    for ($i = 0; $i -lt $categoryOrder.Count; $i++) { $categoryRank[$categoryOrder[$i]] = $i }
    $sorted = $script:findings | Sort-Object @{ Expression = { $fileOrder[$_.File] } }, Line, @{ Expression = { $categoryRank[$_.Category] } }
    foreach ($finding in $sorted) {
        $prefix = ""
        if ($finding.Fail) { $prefix = "FAIL: " }
        Write-Output ("{0}:{1}: [{2}] {3}{4}" -f $finding.File, $finding.Line, $finding.Category, $prefix, $finding.Message)
    }
    if ($script:findings.Count -gt 0) { Write-Output "" }

    Write-Output "Project: $Project (projects/$Project, main file $MainFile)"
    if ($null -ne $className) { Write-Output "Class: $className" }
    if ($null -ne $templateDirectory) {
        $how = $(if ($templateExplicit) { "-Template" } else { "found by $classLeafName" })
        Write-Output "Template: $(Get-DisplayPath $templateDirectory) ($how)"
        if ($templateFilesIdentical.Count -gt 0) { Write-Output "Venue files identical to the template: $($templateFilesIdentical -join ', ')" }
    }
    elseif ($null -ne $className -and $standardClass) { Write-Output "Template: none (standard class $className)" }
    elseif ($null -ne $className) { Write-Output "Template: none ($templateNote)" }
    else { Write-Output "Template: unknown (no \documentclass found)" }
    if ($null -ne $script:templateOrigin) { Write-Output "Template origin: $($script:templateOrigin)" }
    if ($templateNote -ne "" -and $null -ne $templateDirectory) { Write-Output "Note: $templateNote" }

    $layout = $(if ($Flat) { "flat (all files in one directory)" } else { "folders as in the project" })
    Write-Output "Layout: $layout$(if ($KeepComments) { '; comments kept' })"
    if ($CheckOnly) { Write-Output "Mode: static checks only (-CheckOnly)" }
    if ($null -ne $script:run.Stopped) { Write-Output "Stopped: $($script:run.Stopped)" }
    if ($script:excluded.Count -gt 0) {
        $items = $script:excluded | ForEach-Object { "$($_.Rel) ($($_.Reason))" }
        Write-Output "Excluded from the package ($($script:excluded.Count)): $($items -join ', ')"
    }
    if ($null -ne $script:run.ZipEntries) {
        $total = ($script:run.ZipEntries | Measure-Object Length -Sum).Sum
        Write-Output "Files in the zip ($($script:run.ZipEntries.Count), $(([string](Format-Size $total)).Trim()) uncompressed):"
        foreach ($entry in $script:run.ZipEntries) { Write-Output ("  {0}  {1}" -f (Format-Size $entry.Length), $entry.Name) }
    }

    $counts = @{}
    $failCounts = @{}
    foreach ($finding in $script:findings) {
        if ($counts.ContainsKey($finding.Category)) { $counts[$finding.Category]++ } else { $counts[$finding.Category] = 1 }
        if ($finding.Fail) {
            if ($failCounts.ContainsKey($finding.Category)) { $failCounts[$finding.Category]++ } else { $failCounts[$finding.Category] = 1 }
        }
    }
    Write-Output ""
    if ($script:findings.Count -eq 0) { Write-Output "Findings: 0" }
    else {
        $failCount = @($script:findings | Where-Object { $_.Fail }).Count
        Write-Output "Findings: $($script:findings.Count) ($failCount FAIL)"
        $listed = New-Object System.Collections.Generic.List[string]
        foreach ($category in $categoryOrder) { $listed.Add($category) }
        foreach ($category in $counts.Keys) { if (-not $listed.Contains($category)) { $listed.Add($category) } }
        foreach ($category in $listed) {
            if ($counts.ContainsKey($category)) {
                $mark = $(if ($failCounts.ContainsKey($category)) { "  FAIL" } else { "" })
                Write-Output ("  {0,-14} {1,4}{2}" -f $category, $counts[$category], $mark)
            }
        }
    }
    if ($script:run.CommentNotes -gt 0 -and $KeepComments) { Write-Output "Comments kept: $($script:run.CommentNotes) comment lines" }
    if ($null -ne $script:run.Pages) {
        $limit = $(if ($MaxPages -gt 0) { " (limit $MaxPages)" } else { "" })
        Write-Output "Pages: $($script:run.Pages)$limit"
    }
    if ($script:run.ZipBuilt) {
        Write-Output "Zip:  $zipPath"
        Write-Output "Link: $(Get-DisplayPath $zipPath)"
    }
    if ($script:run.PdfBuilt) {
        Write-Output "PDF:  $packagePdfPath"
        Write-Output "Link: $(Get-DisplayPath $packagePdfPath)"
    }
    if ($null -ne $script:traceFiles) {
        $skippedText = ""
        if ($script:traceSkipped.Count -gt 0) { $skippedText = "; $($script:traceSkipped.Count) files identical to the template not scanned" }
        Write-Output "Trace scan: $($script:traceFiles.Count) files, $($script:traceHitCount) hits ($($script:traceAllowedCount) allowed)$skippedText"
    }
    if ($null -ne $script:aiDeclarationLine) { Write-Output $script:aiDeclarationLine }

    $reasons = @()
    foreach ($category in $categoryOrder) { if ($failCounts.ContainsKey($category)) { $reasons += $category } }
    foreach ($category in $failCounts.Keys) { if ($categoryOrder -notcontains $category) { $reasons += $category } }
    if ($null -ne $previousOutputEncoding) {
        try { [Console]::OutputEncoding = $previousOutputEncoding } catch { }
    }
    if ($reasons.Count -eq 0) {
        Write-Output "Verdict: PASS"
        exit 0
    }
    Write-Output "Verdict: FAIL ($($reasons -join ', '))"
    exit 1
}

# ---------------------------------------------------------------------------
# Stop after the static checks?
# ---------------------------------------------------------------------------

# An unexpected error in the stages ends the run with a verdict instead of a bare PowerShell error.
trap {
    Add-Finding (Get-DisplayPath $PSCommandPath) $_.InvocationInfo.ScriptLineNumber "internal" "unexpected error: $($_.Exception.Message)"
    $script:run.Stopped = "internal error: the package must not be sent"
    Complete-Run
}

if ($CheckOnly) { Complete-Run }

# Output of an earlier run with the same name is stale from here on: a FAIL never leaves a valid-looking zip.
foreach ($stale in @($zipPath, $packagePdfPath)) {
    if (Test-Path -LiteralPath $stale) { Remove-Item -LiteralPath $stale -Force }
}
if (@($script:findings | Where-Object { $_.Fail }).Count -gt 0) {
    $script:run.Stopped = "static FAIL findings (A, B, T): nothing was staged, built or packed"
    Complete-Run
}

function Test-NewFail([int]$Before) {
    return (@($script:findings | Where-Object { $_.Fail }).Count -gt $Before)
}
function Get-FailCount { return @($script:findings | Where-Object { $_.Fail }).Count }

# ---------------------------------------------------------------------------
# Helpers for the stages
# ---------------------------------------------------------------------------

Add-Type -AssemblyName System.IO.Compression

function Write-Step([string]$Text) { Write-Host "-- $Text" }

# Deletes a work folder; only folders named tmp/package-* can be deleted.
function Remove-WorkDirectory([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path).TrimEnd('\')
    $guard = [IO.Path]::GetFullPath($tmpRoot).TrimEnd('\') + '\package-'
    if (-not $full.StartsWith($guard, [System.StringComparison]::OrdinalIgnoreCase)) { throw "Refusing to delete outside tmp/package-*: $full" }
    if (Test-Path -LiteralPath $full) { Remove-Item -LiteralPath $full -Recurse -Force }
}

# Relative paths (forward slashes) of all files of a folder.
function Get-RelativeFiles([string]$Directory) {
    $root = $Directory.TrimEnd('\') + '\'
    $list = New-Object System.Collections.Generic.List[string]
    foreach ($file in @(Get-ChildItem -LiteralPath $Directory -Recurse -File -Force)) {
        $list.Add($file.FullName.Substring($root.Length).Replace('\', '/'))
    }
    return $list.ToArray()
}

function Get-TreeSnapshot([string]$Directory) {
    $snapshot = @{}
    foreach ($rel in (Get-RelativeFiles $Directory)) {
        $snapshot[$rel] = (Get-FileHash -LiteralPath (Join-Path $Directory $rel.Replace('/', '\')) -Algorithm SHA256).Hash
    }
    return $snapshot
}

function Get-BuildErrors([string]$Directory, [string]$Main, $Result) {
    # Lines of the TeX log that report an error, with their line numbers in the log.
    $lines = New-Object System.Collections.Generic.List[object]
    $logPath = Join-Path $Directory ([IO.Path]::ChangeExtension($Main, ".log"))
    if (Test-Path -LiteralPath $logPath) {
        $log = [System.IO.File]::ReadAllLines($logPath)
        for ($i = 0; $i -lt $log.Count -and $lines.Count -lt 8; $i++) {
            if ($log[$i] -match '^(!|\S+:\d+:)\s') {
                $lines.Add([pscustomobject]@{ Line = ($i + 1); Text = $log[$i].Trim() })
                if ($i + 1 -lt $log.Count -and $log[$i + 1] -match '^l\.\d+') { $lines.Add([pscustomobject]@{ Line = ($i + 2); Text = $log[$i + 1].Trim() }) }
            }
        }
    }
    if ($lines.Count -eq 0) {
        $tail = @((($Result.Output + "`n" + $Result.Error) -split "`r?`n") | Where-Object { $_.Trim().Length -gt 0 } | Select-Object -Last 8)
        $number = 1
        foreach ($line in $tail) { $number++; $lines.Add([pscustomobject]@{ Line = $number; Text = $line.Trim() }) }
    }
    return , $lines
}

# The build of a recipient: latexmk, pdfLaTeX with the installer disabled, no outdir, in place.
function Invoke-LatexBuild([string]$Directory, [string]$Main, [string]$LogFile) {
    $arguments = @("-pdf", "-pdflatex=pdflatex -disable-installer %O %S", "-interaction=nonstopmode", "-file-line-error",
        "-halt-on-error", "-recorder", $Main)
    $result = Invoke-Tool "latexmk" $arguments $Directory
    [System.IO.File]::WriteAllText($LogFile, ("latexmk exit code $($result.ExitCode)`r`n" + $result.Output + "`r`n" + $result.Error), $utf8)
    $pdf = Join-Path $Directory ([IO.Path]::ChangeExtension($Main, ".pdf"))
    $ok = ($result.ExitCode -eq 0 -and (Test-Path -LiteralPath $pdf))
    $errors = $null
    if (-not $ok) { $errors = Get-BuildErrors $Directory $Main $result }
    return [pscustomobject]@{ Ok = $ok; Pdf = $pdf; Errors = $errors; ExitCode = $result.ExitCode; Directory = $Directory }
}

function Add-BuildFindings($Build, [string]$Label) {
    $logDisplay = Get-DisplayPath (Join-Path $Build.Directory ([IO.Path]::ChangeExtension($MainFile, ".log")))
    Add-Finding $logDisplay 1 "build" "$Label did not build (latexmk exit code $($Build.ExitCode)); first errors follow"
    foreach ($entry in $Build.Errors) { Add-Finding $logDisplay ([Math]::Max(2, $entry.Line)) "build" $entry.Text }
}

function Get-PdfText([string]$Pdf, [string]$TextFile) {
    $result = Invoke-Tool "pdftotext" @("-enc", "UTF-8", $Pdf, $TextFile) $workRoot
    if ($result.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $TextFile)) { throw "pdftotext failed on $Pdf : $($result.Error)" }
    return ([System.IO.File]::ReadAllText($TextFile, $utf8) -replace "`r`n", "`n")
}

function Get-PageCount([string]$Pdf) {
    $result = Invoke-Tool "pdfinfo" @($Pdf) $workRoot
    $match = [regex]::Match($result.Output, '(?m)^Pages:\s+(\d+)')
    if (-not $match.Success) { throw "pdfinfo did not report the page count of $Pdf" }
    return [int]$match.Groups[1].Value
}

# Fonts that are not embedded, or Type 3 fonts (columns are located from the dashed header line of pdffonts).
function Get-FontProblems([string]$Pdf) {
    $problems = New-Object System.Collections.Generic.List[string]
    $result = Invoke-Tool "pdffonts" @($Pdf) $workRoot
    $lines = $result.Output -split "`r?`n"
    if ($lines.Count -lt 3) { return , $problems }
    $columns = [regex]::Matches($lines[1], '-+')
    if ($columns.Count -lt 6) { return , $problems }
    $cell = {
        param($line, $k)
        $start = $columns[$k].Index
        if ($line.Length -le $start) { return "" }
        return $line.Substring($start, [Math]::Min($columns[$k].Length, $line.Length - $start)).Trim()
    }
    for ($i = 2; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line.Trim().Length -eq 0) { continue }
        $name = & $cell $line 0
        $type = & $cell $line 1
        $embedded = & $cell $line 3
        if ($embedded -eq "no") { $problems.Add("font $name ($type) is not embedded") }
        elseif ($type -match 'Type 3') { $problems.Add("font $name is a Type 3 (bitmap) font") }
    }
    return , $problems
}

# First differing lines of two texts, or $null when they are equal.
function Get-TextDifference([string]$Expected, [string]$Actual) {
    if ($Expected -ceq $Actual) { return $null }
    $left = $Expected -split "`n"
    $right = $Actual -split "`n"
    $found = New-Object System.Collections.Generic.List[string]
    $count = [Math]::Max($left.Count, $right.Count)
    for ($i = 0; $i -lt $count -and $found.Count -lt 3; $i++) {
        $a = $(if ($i -lt $left.Count) { $left[$i] } else { "<end of text>" })
        $b = $(if ($i -lt $right.Count) { $right[$i] } else { "<end of text>" })
        if ($a -cne $b) { $found.Add("text line $($i + 1): '$(Format-Short $a 60)' against '$(Format-Short $b 60)'") }
    }
    return ($found -join "; ")
}

function New-PackageZip([string]$Directory, [string]$ZipFile) {
    $names = [string[]](Get-RelativeFiles $Directory)
    [Array]::Sort($names, [System.StringComparer]::Ordinal)
    $stream = [System.IO.File]::Open($ZipFile, [System.IO.FileMode]::Create)
    try {
        $archive = New-Object System.IO.Compression.ZipArchive($stream, [System.IO.Compression.ZipArchiveMode]::Create, $false, [System.Text.Encoding]::UTF8)
        try {
            foreach ($name in $names) {
                $source = Join-Path $Directory $name.Replace('/', '\')
                $entry = $archive.CreateEntry($name, [System.IO.Compression.CompressionLevel]::Optimal)
                $time = (Get-Item -LiteralPath $source).LastWriteTime
                if ($time.Year -ge 1980) { $entry.LastWriteTime = New-Object System.DateTimeOffset($time) }
                $entryStream = $entry.Open()
                try {
                    $input = [System.IO.File]::OpenRead($source)
                    try { $input.CopyTo($entryStream) } finally { $input.Dispose() }
                }
                finally { $entryStream.Dispose() }
            }
        }
        finally { $archive.Dispose() }
    }
    finally { $stream.Dispose() }
}

# Entry names and uncompressed sizes of a zip, read back with ZipArchive.
function Read-PackageZip([string]$ZipFile) {
    $list = New-Object System.Collections.Generic.List[object]
    $stream = [System.IO.File]::OpenRead($ZipFile)
    try {
        $archive = New-Object System.IO.Compression.ZipArchive($stream, [System.IO.Compression.ZipArchiveMode]::Read, $false, [System.Text.Encoding]::UTF8)
        try { foreach ($entry in $archive.Entries) { $list.Add([pscustomobject]@{ Name = $entry.FullName; Length = $entry.Length }) } }
        finally { $archive.Dispose() }
    }
    finally { $stream.Dispose() }
    return , $list
}

function Expand-PackageZip([string]$ZipFile, [string]$Destination) {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    $stream = [System.IO.File]::OpenRead($ZipFile)
    try {
        $archive = New-Object System.IO.Compression.ZipArchive($stream, [System.IO.Compression.ZipArchiveMode]::Read, $false, [System.Text.Encoding]::UTF8)
        try {
            foreach ($entry in $archive.Entries) {
                $name = $entry.FullName
                if ($name.EndsWith('/')) { continue }
                if ($name.Contains('\') -or $name.StartsWith('/') -or ($name -split '/') -contains '..') { throw "Unsafe zip entry name: $name" }
                $target = Join-Path $Destination $name.Replace('/', '\')
                $parent = Split-Path -Parent $target
                if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
                $entryStream = $entry.Open()
                try {
                    $output = [System.IO.File]::Create($target)
                    try { $entryStream.CopyTo($output) } finally { $output.Dispose() }
                }
                finally { $entryStream.Dispose() }
            }
        }
        finally { $archive.Dispose() }
    }
    finally { $stream.Dispose() }
}

function Resolve-InputPath([string]$Path, [string]$BaseDirectory) {
    $p = $Path.Trim().Replace('/', '\')
    if ($p -notmatch '^[A-Za-z]:') { $p = Join-Path $BaseDirectory $p }
    return [IO.Path]::GetFullPath($p)
}

# ---------------------------------------------------------------------------
# Flat layout: rewriting of path arguments
# ---------------------------------------------------------------------------

$script:flatKeys = @{}              # path as it can be written (lower case irrelevant) -> flat name
$script:flatLeftoverRx = $null
$rxBraceGroup = [regex]::new('\{([^{}]*/[^{}]*)\}', $rxNone)
$flatEvaluator = [System.Text.RegularExpressions.MatchEvaluator] {
    param($m)
    $changed = $false
    $parts = New-Object System.Collections.Generic.List[string]
    foreach ($item in $m.Groups[1].Value.Split(',')) {
        $key = $item.Trim().Replace('\', '/')
        while ($key.StartsWith('./')) { $key = $key.Substring(2) }
        if ($script:flatKeys.ContainsKey($key)) { $parts.Add($script:flatKeys[$key]); $changed = $true }
        else { $parts.Add($item) }
    }
    if ($changed) { return '{' + ($parts -join ',') + '}' }
    return $m.Value
}

function Convert-FlatCode([string]$Code) {
    $Code = $rxGraphicsPath.Replace($Code, "")
    return $rxBraceGroup.Replace($Code, $flatEvaluator)
}

$stageRelative = @{}                # project path -> path in the stage
$stageToProject = @{}               # path in the stage -> project path
foreach ($file in $script:included) {
    $target = $file.Rel
    if ($Flat) { $target = [IO.Path]::GetFileName($file.Rel) }
    $stageRelative[$file.Rel] = $target
    $stageToProject[$target] = $file.Rel
}
if ($Flat) {
    $directories = New-StringSet @()
    foreach ($file in $script:included) {
        if ($file.Rel -notlike '*/*') { continue }
        $leaf = [IO.Path]::GetFileName($file.Rel)
        $script:flatKeys[$file.Rel] = $leaf
        $noExtension = $file.Rel -replace '\.[^./]+$', ''
        if ($noExtension -and -not $script:flatKeys.ContainsKey($noExtension)) { $script:flatKeys[$noExtension] = [IO.Path]::GetFileNameWithoutExtension($leaf) }
        $directory = $file.Rel.Substring(0, $file.Rel.LastIndexOf('/'))
        while ($directory.Length -gt 0) {
            [void]$directories.Add($directory)
            $cut = $directory.LastIndexOf('/')
            if ($cut -lt 0) { break }
            $directory = $directory.Substring(0, $cut)
        }
    }
    if ($directories.Count -gt 0) {
        $alternatives = ($directories | Sort-Object { $_.Length } -Descending | ForEach-Object { [regex]::Escape($_) }) -join '|'
        $script:flatLeftoverRx = [regex]::new('(?<![A-Za-z0-9_.\-/])(?:' + $alternatives + ')/', $rxIgnoreCase)
    }
}

# Text of a staged .tex file: full-line comments removed (unless -KeepComments), paths flattened (-Flat).
# Returns the new text; end-of-line comments that remain are reported as [comment] notes.
function Convert-TexForStage($File) {
    $model = $texModels[$File.Rel]
    $lines = New-Object System.Collections.Generic.List[string]
    for ($i = 0; $i -lt $model.Raw.Count; $i++) {
        $raw = $model.Raw[$i]
        if ($model.Keep[$i]) { $lines.Add($raw); continue }
        $at = $model.CommentAt[$i]
        $codePart = $raw
        $commentPart = ""
        if ($at -ge 0) { $codePart = $raw.Substring(0, $at); $commentPart = $raw.Substring($at) }
        if (-not $KeepComments -and $at -ge 0 -and $codePart.Trim().Length -eq 0) {
            $magic = ($i -lt 5 -and $raw -match '^\s*%\s*!')
            if (-not $magic) { continue }
        }
        if ($Flat -and $codePart.Length -gt 0) {
            $codePart = Convert-FlatCode $codePart
            if ($null -ne $script:flatLeftoverRx) {
                $left = $script:flatLeftoverRx.Match($codePart)
                if ($left.Success) {
                    Add-ProjectFinding $File.Rel ($i + 1) "flat" "a path into a project folder remains after flattening ('$($left.Value)' in: $(Format-Short $codePart.Trim() 60)); the script cannot rewrite paths built from macros. Use the paths as literal arguments."
                }
            }
        }
        $lines.Add($codePart + $commentPart)
        if (-not $KeepComments -and $at -ge 0) {
            $rest = $commentPart.Substring(1).Trim()
            if (($rest -replace '%', '').Trim().Length -gt 0) {
                Add-ProjectFinding $File.Rel ($i + 1) "comment" "end-of-line comment stays in the package: % $(Format-Short $rest 70)"
            }
        }
    }
    return ($lines -join "`n")
}

# ---------------------------------------------------------------------------
# C. Staging
# ---------------------------------------------------------------------------

$referenceDirectory = Join-Path $workRoot "reference"
Write-Step "Staging $Project into $(Get-DisplayPath $stageDirectory)"
Remove-WorkDirectory $workRoot
New-Item -ItemType Directory -Force -Path $stageDirectory | Out-Null
New-Item -ItemType Directory -Force -Path $referenceDirectory | Out-Null

if ($KeepComments) {
    foreach ($file in $texFiles) {
        $model = $texModels[$file.Rel]
        if ($null -eq $model) { continue }
        for ($i = 0; $i -lt $model.Raw.Count; $i++) {
            if (-not $model.Keep[$i] -and $model.CommentAt[$i] -ge 0 -and $model.Raw[$i].Substring(0, $model.CommentAt[$i]).Trim().Length -eq 0) { $script:run.CommentNotes++ }
        }
    }
}

$failBeforeStaging = Get-FailCount
foreach ($file in $script:included) {
    $target = Join-Path $stageDirectory $stageRelative[$file.Rel].Replace('/', '\')
    $referenceTarget = Join-Path $referenceDirectory $file.Rel.Replace('/', '\')
    foreach ($path in @($target, $referenceTarget)) {
        $parent = Split-Path -Parent $path
        if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
    }
    Copy-Item -LiteralPath $file.Full -Destination $referenceTarget -Force
    $convert = ($file.Rel -like '*.tex') -and ($null -ne $texModels[$file.Rel]) -and ($Flat -or -not $KeepComments)
    $bibStaged = $null
    if ($file.Rel -like '*.bib' -and -not $KeepComments) {
        $bibText = Read-SourceText $file.Full
        if ($null -ne $bibText) {
            $bibResult = Get-BibStagedLines $bibText
            if ($bibResult.Changed) { $bibStaged = $bibResult.Text }
        }
    }
    if ($convert) {
        $text = Convert-TexForStage $file
        [System.IO.File]::WriteAllText($target, $text, $utf8)
        (Get-Item -LiteralPath $target).LastWriteTime = $file.Time
    }
    elseif ($null -ne $bibStaged) {
        # comment lines outside entries and @comment blocks removed (workspace notes, verification status)
        [System.IO.File]::WriteAllText($target, $bibStaged, $utf8)
        (Get-Item -LiteralPath $target).LastWriteTime = $file.Time
    }
    else { Copy-Item -LiteralPath $file.Full -Destination $target -Force }
}
if (Test-NewFail $failBeforeStaging) {
    $script:run.Stopped = "the flat layout cannot be produced safely: no build, no package"
    Complete-Run
}

$beforeFiles = New-StringSet @()
foreach ($rel in (Get-RelativeFiles $stageDirectory)) { [void]$beforeFiles.Add($rel) }
$beforeDirectories = New-StringSet @()
foreach ($directory in @(Get-ChildItem -LiteralPath $stageDirectory -Recurse -Directory -Force)) {
    [void]$beforeDirectories.Add($directory.FullName.Substring($stageDirectory.Length + 1).Replace('\', '/'))
}

# ---------------------------------------------------------------------------
# D. Build in the stage and in an untouched reference copy
# ---------------------------------------------------------------------------

Write-Step "Building the stage (latexmk, installer disabled)"
$stageBuild = Invoke-LatexBuild $stageDirectory $MainFile (Join-Path $workRoot "stage-build.log")
if (-not $stageBuild.Ok) {
    Add-BuildFindings $stageBuild "the staged package"
    $script:run.Stopped = "the staged package does not build: no package written (log: $(Get-DisplayPath (Join-Path $workRoot 'stage-build.log')))"
    Complete-Run
}
Write-Step "Building the reference copy of the untouched project"
$referenceBuild = Invoke-LatexBuild $referenceDirectory $MainFile (Join-Path $workRoot "reference-build.log")
if (-not $referenceBuild.Ok) {
    Add-BuildFindings $referenceBuild "the untouched project (reference copy)"
    $script:run.Stopped = "the untouched project does not build either: fix the project first (log: $(Get-DisplayPath (Join-Path $workRoot 'reference-build.log')))"
    Complete-Run
}

# ---------------------------------------------------------------------------
# E. Verification of the staged PDF
# ---------------------------------------------------------------------------

Write-Step "Verifying the staged PDF"
$failBeforeVerification = Get-FailCount
$stagePdf = $stageBuild.Pdf
$stagePdfDisplay = Get-DisplayPath $stagePdf
$stageText = Get-PdfText $stagePdf (Join-Path $workRoot "stage.txt")
$referenceText = Get-PdfText $referenceBuild.Pdf (Join-Path $workRoot "reference.txt")

$undefinedHits = [regex]::Matches($stageText, '\?\?|\[\?\]')
$shown = 0
foreach ($hit in $undefinedHits) {
    if ($shown -ge 10) { break }
    $page = $stageText.Substring(0, $hit.Index).Split([char]12).Count
    $lineStart = $stageText.LastIndexOf("`n", $hit.Index)
    $lineEnd = $stageText.IndexOf("`n", $hit.Index)
    if ($lineEnd -lt 0) { $lineEnd = $stageText.Length }
    $context = $stageText.Substring($lineStart + 1, $lineEnd - $lineStart - 1)
    Add-Finding $stagePdfDisplay $page "undefined" "'$($hit.Value)' on page ${page}: undefined reference or citation (text: $(Format-Short $context 70))"
    $shown++
}
if ($undefinedHits.Count -gt 10) { Add-Finding $stagePdfDisplay 1 "undefined" "$($undefinedHits.Count - 10) more undefined references or citations" }

foreach ($problem in (Get-FontProblems $stagePdf)) { Add-Finding $stagePdfDisplay 1 "fonts" "$problem; journals reject it" }

$script:run.Pages = Get-PageCount $stagePdf
if ($MaxPages -gt 0 -and $script:run.Pages -gt $MaxPages) {
    Add-Finding $stagePdfDisplay 1 "pages" "$($script:run.Pages) pages, the limit is $MaxPages ($($script:run.Pages - $MaxPages) too many)"
}

$difference = Get-TextDifference $referenceText $stageText
if ($null -ne $difference) {
    Add-Finding $stagePdfDisplay 1 "text-diff" "the text of the staged PDF differs from the reference build of the untouched project ($(Get-DisplayPath $referenceBuild.Pdf)): $difference"
}

# T (d): metadata of the staged PDF (info dictionary, XMP, object and metadata streams; figure info dictionaries
# that pdfTeX copies in)
Invoke-TraceFile $stagePdf ([IO.Path]::GetFileName($stagePdf)) $stagePdfDisplay "<staged PDF>" $false

# [unused]: files of the package that the build did not read (TeX inputs from .fls; BibTeX and biber inputs from
# .fdb_latexmk; .bib and .bst files that the sources name; latexmkrc, which latexmk reads itself)
$readFiles = New-StringSet @()
$flsPath = Join-Path $stageDirectory "$mainBase.fls"
if (Test-Path -LiteralPath $flsPath) {
    foreach ($line in [System.IO.File]::ReadAllLines($flsPath)) {
        if ($line -match '^INPUT\s+(.+)$') { [void]$readFiles.Add((Resolve-InputPath $Matches[1] $stageDirectory)) }
    }
}
$fdbPath = Join-Path $stageDirectory "$mainBase.fdb_latexmk"
if (Test-Path -LiteralPath $fdbPath) {
    foreach ($line in [System.IO.File]::ReadAllLines($fdbPath)) {
        if ($line -match '^\s*"([^"]+)"') { [void]$readFiles.Add((Resolve-InputPath $Matches[1] $stageDirectory)) }
    }
}
if (Test-Path -LiteralPath $flsPath) {
    foreach ($rel in $beforeFiles) {
        $leaf = [IO.Path]::GetFileName($rel)
        if ($readFiles.Contains((Resolve-InputPath $rel $stageDirectory))) { continue }
        if ($staticReferenceTargets.Contains($leaf)) { continue }
        if ($leaf -ieq "latexmkrc") { continue }
        Add-ProjectFinding $stageToProject[$rel] 1 "unused" "not read by the build, but part of the package; it would confuse a submission system. Remove it from the project or keep it out of the package."
    }
}

if (Test-NewFail $failBeforeVerification) {
    $script:run.Stopped = "FAIL findings in the verification (E): no package written"
    Complete-Run
}

# ---------------------------------------------------------------------------
# F. Package
# ---------------------------------------------------------------------------

Write-Step "Packing"
# The PDF waits beside the stage until the staged files have passed the trace scan.
$heldPdf = Join-Path $workRoot "held-$pdfName"
Move-Item -LiteralPath $stagePdf -Destination $heldPdf -Force
foreach ($rel in (Get-RelativeFiles $stageDirectory)) {
    if ($beforeFiles.Contains($rel)) { continue }
    if ($rel -ieq "$mainBase.bbl") { continue }
    Remove-Item -LiteralPath (Join-Path $stageDirectory $rel.Replace('/', '\')) -Force
}
foreach ($directory in @(Get-ChildItem -LiteralPath $stageDirectory -Recurse -Directory -Force | Sort-Object { $_.FullName.Length } -Descending)) {
    $rel = $directory.FullName.Substring($stageDirectory.Length + 1).Replace('\', '/')
    if (-not $beforeDirectories.Contains($rel) -and @(Get-ChildItem -LiteralPath $directory.FullName -Force).Count -eq 0) {
        Remove-Item -LiteralPath $directory.FullName -Force
    }
}

# T (b, c): the staged files exactly as they will be zipped (.bbl included); a project file whose hits were
# reported in (a) is not reported again.
Write-Step "Trace scan of the staged files"
$failBeforeTrace = Get-FailCount
foreach ($rel in @(Get-RelativeFiles $stageDirectory | Sort-Object)) {
    $projectRel = $null
    if ($stageToProject.ContainsKey($rel)) { $projectRel = $stageToProject[$rel] }
    if ($null -ne $projectRel -and $script:traceSkipped.Contains($projectRel)) { continue }
    $traceKey = $(if ($null -ne $projectRel) { $projectRel } else { "<stage>/" + $rel })
    $stagedFull = Join-Path $stageDirectory $rel.Replace('/', '\')
    Invoke-TraceFile $stagedFull $rel (Get-DisplayPath $stagedFull) $traceKey $false
}
if (Test-NewFail $failBeforeTrace) {
    $script:run.Stopped = "[trace] FAIL in the staged files: no package written (stage: $(Get-DisplayPath $stageDirectory))"
    Complete-Run
}

New-Item -ItemType Directory -Force -Path $packageDirectory | Out-Null
Move-Item -LiteralPath $heldPdf -Destination $packagePdfPath -Force
$stageSnapshot = Get-TreeSnapshot $stageDirectory
New-PackageZip $stageDirectory $zipPath
$script:run.ZipEntries = Read-PackageZip $zipPath
$script:run.ZipBuilt = $true
$script:run.PdfBuilt = $true

$zipDisplay = Get-DisplayPath $zipPath

# T (e): the entry names of the written zip
$failBeforeNames = Get-FailCount
[void]$script:traceFiles.Add("<zip>")
foreach ($entry in $script:run.ZipEntries) {
    $projectRel = $null
    if ($stageToProject.ContainsKey($entry.Name)) { $projectRel = $stageToProject[$entry.Name] }
    if ($null -ne $projectRel -and $script:traceSkipped.Contains($projectRel)) { continue }
    $traceKey = $(if ($null -ne $projectRel) { $projectRel } else { "<stage>/" + $entry.Name })
    Register-TraceText $zipDisplay 1 $entry.Name 0 -1 "zip entry name" $traceKey "<file name>" $false $null
}
if (Test-NewFail $failBeforeNames) {
    Remove-Item -LiteralPath $zipPath, $packagePdfPath -Force -ErrorAction SilentlyContinue
    $script:run.ZipBuilt = $false
    $script:run.PdfBuilt = $false
    $script:run.Stopped = "[trace] FAIL in the zip entry names: the zip was removed"
    Complete-Run
}
$badNames = @($script:run.ZipEntries | Where-Object { $_.Name.Contains('\') -or $_.Name.StartsWith('/') })
if ($badNames.Count -gt 0) { Add-Finding $zipDisplay 1 "roundtrip" "zip entry names with backslashes or a leading slash: $($badNames[0].Name)" }
if (-not (@($script:run.ZipEntries | Where-Object { $_.Name -ceq $MainFile }).Count -gt 0)) {
    Add-Finding $zipDisplay 1 "roundtrip" "the main file $MainFile is not at the top level of the zip"
}

# ---------------------------------------------------------------------------
# G. Round trip
# ---------------------------------------------------------------------------

Write-Step "Round trip: extracting the zip and building it"
Expand-PackageZip $zipPath $roundtripDirectory
$extractedSnapshot = Get-TreeSnapshot $roundtripDirectory
foreach ($rel in ($stageSnapshot.Keys | Sort-Object)) {
    if (-not $extractedSnapshot.ContainsKey($rel)) { Add-Finding $zipDisplay 1 "roundtrip" "$rel is in the stage but not in the extracted zip" }
    elseif ($extractedSnapshot[$rel] -ne $stageSnapshot[$rel]) { Add-Finding $zipDisplay 1 "roundtrip" "$rel differs after extraction" }
}
foreach ($rel in ($extractedSnapshot.Keys | Sort-Object)) {
    if (-not $stageSnapshot.ContainsKey($rel)) { Add-Finding $zipDisplay 1 "roundtrip" "$rel is in the extracted zip but not in the stage" }
}
$roundtripBuild = Invoke-LatexBuild $roundtripDirectory $MainFile (Join-Path $workRoot "roundtrip-build.log")
if (-not $roundtripBuild.Ok) {
    Add-BuildFindings $roundtripBuild "the extracted zip"
    foreach ($finding in @($script:findings | Where-Object { $_.Category -eq "build" })) { $finding.Category = "roundtrip" }
}
else {
    $roundtripText = Get-PdfText $roundtripBuild.Pdf (Join-Path $workRoot "roundtrip.txt")
    $difference = Get-TextDifference $stageText $roundtripText
    if ($null -ne $difference) {
        Add-Finding (Get-DisplayPath $roundtripBuild.Pdf) 1 "roundtrip" "the text of the PDF built from the extracted zip differs from the text of the staged PDF: $difference"
    }
}
if (@($script:findings | Where-Object { $_.Category -eq "roundtrip" }).Count -gt 0) {
    # an unproven package must not look valid
    Remove-Item -LiteralPath $zipPath, $packagePdfPath -Force -ErrorAction SilentlyContinue
    $script:run.ZipBuilt = $false
    $script:run.PdfBuilt = $false
    $script:run.Stopped = "the round trip failed: the zip was removed (see $(Get-DisplayPath $workRoot))"
}
Complete-Run
