# Define log file
$logFile = "C:\Users\Public\download_log.txt"

# Logging function
function Log {
    param ([string]$message)
    $message | Out-File -FilePath $logFile -Append
    Write-Output $message
}

# Log the start of the script
Log "Starting download script..."

# Downloading the image directly
Log "Downloading image..."

# Variables
$server = "https://raw.githubusercontent.com/Gallogeta/MCS/main"
$filename = "tenor.gif"
$destinationPath = "C:\Users\Public\$filename"

# Download file using Invoke-WebRequest
try {
    Invoke-WebRequest -Uri "$server/$filename" -OutFile $destinationPath -UseBasicParsing
    Log "Download completed!"
} catch {
    Log "Download failed. $_"
    exit
}

# Check if download was successful
if (-Not (Test-Path -Path $destinationPath)) {
    Log "File not found after download."
    exit
}

# Set variables
$source = $destinationPath
$destination = "C:\Users\Public"

# Loop to copy the file 5 times
for ($i = 1; $i -le 5; $i++) {
    $copyPath = "$destination\tenor_copy$i.gif"
    Copy-Item -Path $source -Destination $copyPath
    Log "Copied to $copyPath"
}

# Open all copied files using Start-Process
for ($i = 1; $i -le 5; $i++) {
    $filePath = "$destination\tenor_copy$i.gif"
    Start-Process -FilePath $filePath
    Log "Opened $filePath"
}

# Log script completion and close PowerShell
Log "Script completed. PowerShell will now close."

# Close PowerShell
Stop-Process -Id $PID
