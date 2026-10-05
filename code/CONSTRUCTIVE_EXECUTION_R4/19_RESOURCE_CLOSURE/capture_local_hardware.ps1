$ErrorActionPreference = 'Stop'
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1 Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed
$computer = Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer,Model,TotalPhysicalMemory
$os = Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber,FreePhysicalMemory,TotalVisibleMemorySize
$gpus = @(Get-CimInstance Win32_VideoController | Select-Object Name,AdapterRAM,DriverVersion)
$drives = @(Get-Volume | Where-Object DriveLetter | Select-Object DriveLetter,Size,SizeRemaining,HealthStatus)
$payload = [ordered]@{
    schema_version = '1.0'
    classification = 'MEASURED_LOCAL_HARDWARE_SNAPSHOT'
    captured_at = (Get-Date).ToString('o')
    cpu = $cpu
    computer = $computer
    operating_system = $os
    gpu_inventory = $gpus
    volumes = $drives
    scope = 'local pilot host only; not an authoritative production-target selection'
}
$out = Join-Path $PSScriptRoot 'LOCAL_HARDWARE.json'
$payload | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $out -Encoding utf8
$payload | ConvertTo-Json -Depth 8
