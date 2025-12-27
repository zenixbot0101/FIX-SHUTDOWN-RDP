$installers = @(
    @{Name="VC Redist x64"; Url="https://download.microsoft.com/download/9/3/f/93fcf1e7-e6a4-478b-96e7-d4b285925b00/vc_redist.x64.exe"; File="vc_redist.x64.exe"; Args="/install /quiet /norestart"; CheckRegistry="HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64"},
    @{Name="Steam Client"; Url="https://cdn.fastly.steamstatic.com/client/installer/SteamSetup.exe"; File="SteamSetup.exe"; Args="/S"; CheckFile="$env:ProgramFiles(x86)\Steam\Steam.exe"},
    @{Name="Apollo"; Url="https://github.com/ClassicOldSong/Apollo/releases/download/v0.4.7-alpha.1/Apollo-0.4.7-alpha.1.exe"; File="Apollo-0.4.7-alpha.1.exe"; Args="/S"; CheckFile="$env:ProgramFiles\Apollo\Apollo.exe"},
    @{Name="XNA Framework 4.0"; Url="https://download.microsoft.com/download/a/c/2/ac2c903b-e6e8-42c2-9fd7-bebac362a930/xnafx40_redist.msi"; File="xnafx40_redist.msi"; Args="/qn /norestart"; Type="msi"; CheckRegistry="HKLM:\SOFTWARE\Microsoft\XNA\Framework\v4.0"},
    @{Name=".NET Framework 4.0"; Url="https://download.microsoft.com/download/1/b/e/1be39e79-7e39-46a3-96ff-047f95396215/dotNetFx40_Full_setup.exe"; File="dotNetFx40_Full_setup.exe"; Args="/quiet /norestart"; CheckRegistry="HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full"},
    @{Name="WinRAR"; Url="https://www.rarlab.com/rar/winrar-x64-602.exe"; File="winrar-x64-602.exe"; Args="/S"; CheckFile="$env:ProgramFiles\WinRAR\WinRAR.exe"}
)

$logFile = "$PSScriptRoot\auto_setup_log.txt"
$dxUrl = "https://download.microsoft.com/download/8/4/a/84a35bf1-dafe-4ae8-82af-ad2ae20b6b14/directx_Jun2010_redist.exe"
$dxExe = "$PSScriptRoot\directx_Jun2010_redist.exe"
$dxExtractFolder = "$PSScriptRoot\DirectX"
$nvDriver = "C:\nvidia-tesla-573.76.exe"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$timestamp] $Message"
    Write-Host $line
    Add-Content -Path $logFile -Value $line
}

function Download-File {
    param([string]$Url, [string]$Destination)
    if (-Not (Test-Path $Destination)) {
        Write-Log "Downloading $Destination ..."
        Invoke-WebRequest -Uri $Url -OutFile $Destination
    } else {
        Write-Log "$Destination already exists, skipping download."
    }
}

function Install-File {
    param([hashtable]$inst)
    
    $skip = $false
    if ($inst.CheckFile -and (Test-Path $inst.CheckFile)) { $skip = $true; Write-Log "$($inst.Name) is already installed (found file), skipping..." }
    if ($inst.CheckRegistry -and -not $skip) { if (Test-Path $inst.CheckRegistry) { $skip = $true; Write-Log "$($inst.Name) is already installed (registry), skipping..." } }

    if (-not $skip) {
        $type = $inst.Type; if (-not $type) { $type="exe" }
        Write-Log "Installing $($inst.Name) ..."
        if ($type -eq "msi") { Start-Process msiexec.exe -ArgumentList "/i `"$($inst.File)`" $($inst.Args)" -Wait -PassThru | Out-Null }
        else { Start-Process $inst.File -ArgumentList $inst.Args -Wait -PassThru | Out-Null }
        Write-Log "$($inst.Name) installation finished."
    }
}

function Install-DirectX {
    if (-not (Test-Path $dxExe)) { Invoke-WebRequest -Uri $dxUrl -OutFile $dxExe; Write-Log "Downloading DirectX..." }
    else { Write-Log "DirectX installer already exists, skipping download." }

    if (-not (Test-Path $dxExtractFolder)) { New-Item -ItemType Directory -Path $dxExtractFolder | Out-Null; Start-Process -FilePath $dxExe -ArgumentList "/Q /T:$dxExtractFolder" -Wait; Write-Log "Extracting DirectX..." }
    else { Write-Log "DirectX already extracted, skipping extraction." }

    $dxSetup = Join-Path $dxExtractFolder "DXSETUP.exe"
    if (Test-Path $dxSetup) { Start-Process -FilePath $dxSetup -ArgumentList "/silent" -Wait; Write-Log "DirectX installation finished." }
    else { Write-Log "DXSETUP.exe not found! Extraction may have failed." }
}

function Install-NVIDIA {
    if (Test-Path $nvDriver) { Start-Process -FilePath $nvDriver -ArgumentList "-s" -Wait; Write-Log "NVIDIA driver installation finished." }
    else { Write-Log "NVIDIA driver file not found at $nvDriver, skipping." }
}

$host.UI.RawUI.ForegroundColor = "Green"
Write-Host "==============================================="
Write-Host "          AUTO SETUP ALL TOOLS (FULL)         "
Write-Host "==============================================="
Write-Host ""

foreach ($inst in $installers) { Download-File -Url $inst.Url -Destination $inst.File; Install-File -inst $inst; Write-Host "---------------------------------------------------" }

Install-DirectX
Write-Host "---------------------------------------------------"

Install-NVIDIA
Write-Host "---------------------------------------------------"

Write-Host ""
Write-Log "All setup steps completed. System will restart in 10 seconds..."
Start-Sleep -Seconds 10
shutdown.exe /r /t 0 /c "Restarting after auto setup"
