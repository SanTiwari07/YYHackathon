# Export the deck with desktop PowerPoint: PDF (real text, embedded fonts) + one 1920x1080 PNG per slide.
param(
  [string]$Pptx = (Join-Path $PSScriptRoot "..\..\AgroStruxure_YuvaYodha_2026_Final.pptx"),
  [string]$PdfOut = (Join-Path $PSScriptRoot "..\..\AgroStruxure_YuvaYodha_2026_Final.pdf"),
  [string]$PngDir = (Join-Path $PSScriptRoot "..\qa")
)
$Pptx = (Resolve-Path $Pptx).Path
New-Item -ItemType Directory -Force $PngDir | Out-Null
$PngDir = (Resolve-Path $PngDir).Path
$PdfOut = [System.IO.Path]::GetFullPath($PdfOut)
$app = New-Object -ComObject PowerPoint.Application
try {
  $pres = $app.Presentations.Open($Pptx, $true, $false, $false)   # ReadOnly, Untitled:false, WithWindow:false
  $pres.SaveAs($PdfOut, 32)                                        # ppSaveAsPDF
  $i = 1
  foreach ($sl in $pres.Slides) {
    $sl.Export((Join-Path $PngDir ("slide_{0:D2}.png" -f $i)), "PNG", 1920, 1080)
    $i++
  }
  $pres.Close()
  Write-Output "Exported $($i-1) slides -> $PdfOut and $PngDir"
} finally {
  $app.Quit()
}
