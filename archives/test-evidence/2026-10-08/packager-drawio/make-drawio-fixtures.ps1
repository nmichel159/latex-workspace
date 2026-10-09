# Builds trace fixtures in a copy of a project: PNG tEXt mxfile chunks and an SVG whose only trace term is hidden
# by URL encoding or inside a compressed draw.io page.
param([Parameter(Mandatory = $true)][string]$ProjectDir)
$ErrorActionPreference = 'Stop'
$latin1 = [System.Text.Encoding]::GetEncoding(28591)
$utf8 = New-Object System.Text.UTF8Encoding $false

function Get-Crc32([byte[]]$Data) {
    $poly = [long]3988292384
    $mask = [long]4294967295
    $table = New-Object 'long[]' 256
    for ($n = 0; $n -lt 256; $n++) {
        $c = [long]$n
        for ($k = 0; $k -lt 8; $k++) { if ($c -band 1) { $c = $poly -bxor ($c -shr 1) } else { $c = $c -shr 1 } }
        $table[$n] = $c
    }
    $crc = $mask
    foreach ($b in $Data) { $crc = $table[[int](($crc -bxor [long]$b) -band 255)] -bxor ($crc -shr 8) }
    return [uint32](($crc -bxor $mask) -band $mask)
}

function Get-DrawioPage([string]$Xml) {
    $encoded = [uri]::EscapeDataString($Xml)
    $raw = $utf8.GetBytes($encoded)
    $ms = New-Object System.IO.MemoryStream
    $ds = New-Object System.IO.Compression.DeflateStream($ms, [System.IO.Compression.CompressionMode]::Compress)
    $ds.Write($raw, 0, $raw.Length)
    $ds.Dispose()
    return [Convert]::ToBase64String($ms.ToArray())
}

# Replaces the tEXt chunk 'mxfile' of a PNG with a new value.
function Set-PngMxfile([string]$Path, [string]$Value) {
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $out = New-Object System.IO.MemoryStream
    $out.Write($bytes, 0, 8)
    $pos = 8
    $written = $false
    while ($pos + 12 -le $bytes.Length) {
        $len = ([int]$bytes[$pos] -shl 24) -bor ([int]$bytes[$pos + 1] -shl 16) -bor ([int]$bytes[$pos + 2] -shl 8) -bor [int]$bytes[$pos + 3]
        $type = [System.Text.Encoding]::ASCII.GetString($bytes, $pos + 4, 4)
        $isMx = ($type -eq 'tEXt' -and $latin1.GetString($bytes, $pos + 8, [Math]::Min(7, $len)) -eq "mxfile`0")
        if (-not $isMx) { $out.Write($bytes, $pos, 12 + $len) }
        if ($isMx -or ($type -eq 'IEND' -and -not $written)) {
            if (-not $written) {
                $payload = $latin1.GetBytes("tEXtmxfile`0" + $Value)
                $data = New-Object byte[] ($payload.Length - 4)
                [Array]::Copy($payload, 4, $data, 0, $data.Length)
                $lenBytes = [BitConverter]::GetBytes([uint32]$data.Length); [Array]::Reverse($lenBytes)
                $crcBytes = [BitConverter]::GetBytes((Get-Crc32 $payload)); [Array]::Reverse($crcBytes)
                if ($type -eq 'IEND') {
                    # insert before IEND: rewind the IEND just written
                    $out.SetLength($out.Length - 12)
                }
                $out.Write($lenBytes, 0, 4); $out.Write($payload, 0, $payload.Length); $out.Write($crcBytes, 0, 4)
                if ($type -eq 'IEND') { $out.Write($bytes, $pos, 12 + $len) }
                $written = $true
            }
        }
        $pos += 12 + $len
    }
    [System.IO.File]::WriteAllBytes($Path, $out.ToArray())
}

$img = Join-Path $ProjectDir 'img'
# 1: URL-encoded mxfile, term only in the agent attribute (" Claude-Desktop/1.0" -> "%20Claude-Desktop")
$page1 = Get-DrawioPage '<mxGraphModel><root><mxCell id="0"/></root></mxGraphModel>'
$mx1 = '<mxfile host="app.diagrams.net" agent="Mozilla/5.0 Claude-Desktop/1.0" version="28.1.0"><diagram name="Page-1" id="a">' + $page1 + '</diagram></mxfile>'
Set-PngMxfile (Join-Path $img 'chain-link.png') ([uri]::EscapeDataString($mx1))
# 2: term only inside the compressed page (a hidden label)
$page2 = Get-DrawioPage '<mxGraphModel><root><mxCell id="0"/><mxCell id="2" value="sketch made with Anthropic tools" vertex="1"/></root></mxGraphModel>'
$mx2 = '<mxfile host="app.diagrams.net" agent="Mozilla/5.0" version="28.1.0"><diagram name="Page-1" id="b">' + $page2 + '</diagram></mxfile>'
Set-PngMxfile (Join-Path $img 'chain.png') ([uri]::EscapeDataString($mx2))
# 3: draw.io SVG export: HTML-escaped mxfile in the content attribute, term only inside the compressed page
$page3 = Get-DrawioPage '<mxGraphModel><root><mxCell id="0"/><mxCell id="2" value="ChatGPT draft" vertex="1"/></root></mxGraphModel>'
$mx3 = '<mxfile host="app.diagrams.net"><diagram name="Page-1" id="c">' + $page3 + '</diagram></mxfile>'
$svg = '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" content="' + [System.Net.WebUtility]::HtmlEncode($mx3) + '"><rect width="10" height="10"/></svg>'
[System.IO.File]::WriteAllText((Join-Path $img 'drawio-test.svg'), $svg, $utf8)
"fixtures written"
