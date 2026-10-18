param(
    [int]$BatchSize = 250,
    [switch]$Push
)

$ErrorActionPreference = "Stop"

if ($BatchSize -lt 1) {
    throw "BatchSize must be at least 1."
}

if (-not (Test-Path -LiteralPath ".git")) {
    throw "Run this script from the repository root."
}

git status --short
$files = @(git ls-files --others --exclude-standard -- "assets/images")
if ($files.Count -eq 0) {
    Write-Output "No uncommitted image files found."
    exit 0
}

for ($start = 0; $start -lt $files.Count; $start += $BatchSize) {
    $end = [Math]::Min($start + $BatchSize - 1, $files.Count - 1)
    $batch = $files[$start..$end]
    $pathspecFile = Join-Path $env:TEMP "snake-id-pathspec-$PID.txt"
    [System.IO.File]::WriteAllLines(
        $pathspecFile,
        $batch,
        [System.Text.UTF8Encoding]::new($false)
    )

    git add --pathspec-from-file=$pathspecFile
    Remove-Item -LiteralPath $pathspecFile -Force
    git commit -m "Add dataset image batch $([int]($start / $BatchSize) + 1)"

    if ($Push) {
        git push origin main
    }
}

git add assets/dataset_metadata.json
if (git diff --cached --quiet) {
    Write-Output "Dataset metadata is already committed."
} else {
    git commit -m "Update snake dataset metadata"
    if ($Push) {
        git push origin main
    }
}
