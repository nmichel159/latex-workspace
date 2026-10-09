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
    C. Staging (not with -CheckOnly). The project is copied to tmp/package-<Project>/stage/ without the
       workspace-only material listed under LEFT OUT below. Unless -KeepComments, full-line
       comments of the .tex files are removed (not inside verbatim, Verbatim, lstlisting, minted, comment,
       filecontents, alltt; magic comments "%!" in the first five lines stay) and the remaining end-of-line comments are
       listed as [comment] notes, so a human can read them before the zip is sent. .tex files are written as UTF-8
       without BOM. With -Flat all files move into one directory and the path arguments are rewritten (see -Flat).
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
    F. Package: build products are removed (the .bbl stays: journals and arXiv build without BibTeX) and the zip is
       written with forward slashes in the entry names and no top-level folder:
         outputs/<Project>/package/<Project>-<yyyyMMdd>.zip   (-Flat: <Project>-<yyyyMMdd>-flat.zip)
         outputs/<Project>/package/<Project>-<yyyyMMdd>.pdf
       A second main file beside main.tex (-MainFile exam.tex) adds its name: <Project>-exam-<yyyyMMdd>.zip.
    G. Round trip: the zip is extracted to tmp/package-<Project>/roundtrip/ and built there; [roundtrip] FAIL unless
       the build succeeds, the extracted files equal the stage and the text equals the text of E.
    H. Report: findings as "path:line: [category] message", the files in the zip, page count, paths and links of zip
       and PDF, and the last line "Verdict: PASS" or "Verdict: FAIL (<categories>)".

    LEFT OUT of the package (workspace-only material; every report lists it as "Excluded from the package"):
      README.md, response-to-reviewers.tex and main-marked.tex in the project root; the folders submission/ and
      experiments/ in the project root; *.zip; every file or folder whose name starts with a dot; pdfa.xmpi
      (pdfx scratch file); editor backups (*~, *.bak, *.swp); LaTeX build products (*.aux *.log *.out *.toc
      *.fls *.fdb_latexmk *.synctex.gz *.blg). Everything else goes into the package: .tex, .bib, images, the
      venue's .cls/.bst/.sty, a ready .bbl. The main file may be a wrapper that reads another file (exam.tex
      reads main.tex): the class is found by following \input from the main file.

    Static FAIL findings (A, B) stop the run before staging: a package that is known to be wrong is not built.
    FAIL findings of the verification (E: [undefined], [text-diff]) stop it before the zip is written, and a failed
    round trip deletes the zip and the PDF again ("Stopped:" in the report says why). Stale output of an earlier run
    with the same name is deleted first, so a FAIL never leaves a valid-looking zip.

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
    Do not remove comment lines.

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

$failCategories = New-StringSet @("template-file", "outside", "missing", "case", "flat", "build", "undefined", "pages", "text-diff", "roundtrip", "internal")
$categoryOrder = @("template-file", "template-bst", "layout", "outside", "missing", "case", "filename", "flat", "build",
    "undefined", "fonts", "pages", "text-diff", "unused", "comment", "encoding", "roundtrip", "internal")

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

function Add-Finding([string]$File, [int]$Line, [string]$Category, [string]$Message) {
    $script:findings.Add([pscustomobject]@{
            File     = $File
            Line     = $Line
            Category = $Category
            Fail     = $failCategories.Contains($Category)
            Message  = $Message
        })
}

# Finding in a source file of the project; $Rel is relative to the project folder.
function Add-ProjectFinding([string]$Rel, [int]$Line, [string]$Category, [string]$Message) {
    Add-Finding "projects/$Project/$Rel" $Line $Category $Message
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
    if ($AtRoot -and ($Name -ieq 'README.md' -or $Name -ieq 'response-to-reviewers.tex' -or $Name -ieq 'main-marked.tex')) { return "workspace-only" }
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
    foreach ($finding in $script:findings) {
        if ($counts.ContainsKey($finding.Category)) { $counts[$finding.Category]++ } else { $counts[$finding.Category] = 1 }
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
                $mark = $(if ($failCategories.Contains($category)) { "  FAIL" } else { "" })
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

    $reasons = @()
    foreach ($category in $categoryOrder) { if ($counts.ContainsKey($category) -and $failCategories.Contains($category)) { $reasons += $category } }
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
    Add-Finding "scripts/package-project.ps1" $_.InvocationInfo.ScriptLineNumber "internal" "unexpected error: $($_.Exception.Message)"
    $script:run.Stopped = "internal error: the package must not be sent"
    Complete-Run
}

if ($CheckOnly) { Complete-Run }

# Output of an earlier run with the same name is stale from here on: a FAIL never leaves a valid-looking zip.
foreach ($stale in @($zipPath, $packagePdfPath)) {
    if (Test-Path -LiteralPath $stale) { Remove-Item -LiteralPath $stale -Force }
}
if (@($script:findings | Where-Object { $_.Fail }).Count -gt 0) {
    $script:run.Stopped = "static FAIL findings (A, B): nothing was staged, built or packed"
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
    if ($convert) {
        $text = Convert-TexForStage $file
        [System.IO.File]::WriteAllText($target, $text, $utf8)
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
New-Item -ItemType Directory -Force -Path $packageDirectory | Out-Null
Move-Item -LiteralPath $stagePdf -Destination $packagePdfPath -Force
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
$stageSnapshot = Get-TreeSnapshot $stageDirectory
New-PackageZip $stageDirectory $zipPath
$script:run.ZipEntries = Read-PackageZip $zipPath
$script:run.ZipBuilt = $true
$script:run.PdfBuilt = $true

$zipDisplay = Get-DisplayPath $zipPath
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
