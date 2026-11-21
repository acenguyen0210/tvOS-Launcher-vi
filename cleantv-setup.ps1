# CleanTV & tvOS Launcher Tiếng Việt - Cài đặt tự động qua Wi-Fi
param(
    [Parameter(Mandatory=$true)]
    [string]$TvHost
)

$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  CleanTV & tvOS Launcher Tiếng Việt - Cài Đặt Tự Động" -ForegroundColor Cyan
Write-Host "  Mục tiêu TV/Máy chiếu: $TvHost" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Kiểm tra ADB
$adb = (Get-Command adb -ErrorAction SilentlyContinue)?.Source
if (-not $adb) {
    # Thử tìm adb trong tools của CleanYourTV hoặc Android SDK
    $candidates = @(
        "$PSScriptRoot\..\Cleadtv\tools\adb.exe",
        "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe",
        "C:\Program Files\platform-tools\adb.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) { $adb = $c; break }
    }
}

if (-not $adb) {
    Write-Host "[!] Không tìm thấy công cụ ADB. Đang tải portable ADB..." -ForegroundColor Yellow
    $adbZip = "$env:TEMP\platform-tools.zip"
    $dest = "$env:LOCALAPPDATA\CleanTV\platform-tools"
    Invoke-WebRequest -Uri "https://dl.google.com/android/repository/platform-tools-latest-windows.zip" -OutFile $adbZip
    Expand-Archive -Path $adbZip -DestinationPath (Split-Path $dest) -Force
    Remove-Item $adbZip -Force
    $adb = "$dest\adb.exe"
}

Write-Host "[1/4] Đang kết nối TV qua ADB ($TvHost:5555)..." -ForegroundColor Green
& $adb connect "$TvHost`:5555" | Out-Null
Start-Sleep -Seconds 2

$devices = & $adb devices
if ($devices -notmatch "$TvHost`:5555\s+device") {
    Write-Host "[X] Không thể kết nối ADB với TV tại $TvHost`:5555!" -ForegroundColor Red
    Write-Host "    Vui lòng kiểm tra: TV đã bật 'Gỡ lỗi USB / Gỡ lỗi mạng' và cùng mạng Wi-Fi." -ForegroundColor Yellow
    exit 1
}

$model = (& $adb -s "$TvHost`:5555" shell getprop ro.product.model).Trim()
$brand = (& $adb -s "$TvHost`:5555" shell getprop ro.product.brand).Trim()
$sdk = (& $adb -s "$TvHost`:5555" shell getprop ro.build.version.sdk).Trim()
Write-Host "    ✓ Đã kết nối: $brand $model (Android SDK $sdk)" -ForegroundColor Green

# 2. Dọn rác TV (CleanTV)
Write-Host ""
Write-Host "[2/4] Đang dọn dẹp quảng cáo và ứng dụng rác (CleanTV)..." -ForegroundColor Green

# Danh sách an toàn: chỉ tắt (disable), không gỡ bỏ
$bloatList = @(
    "com.google.android.youtube.tvunplugged",
    "com.google.android.tungsten.setupwraith",
    "com.uv.droid.uota",
    "com.uv.droid.uotaback",
    "com.mobisystems.editor.office_registered",
    "com.newlink.tvtestingtools",
    "com.hikeymasterprovision",
    "com.newlink.isuperred.ijkplayerdemo"
)

$disabledCount = 0
foreach ($pkg in $bloatList) {
    $exists = & $adb -s "$TvHost`:5555" shell pm list packages "$pkg"
    if ($exists -match $pkg) {
        & $adb -s "$TvHost`:5555" shell pm disable-user --user 0 "$pkg" | Out-Null
        Write-Host "    - Đã đóng băng: $pkg" -ForegroundColor DarkGray
        $disabledCount++
    }
}
Write-Host "    ✓ Hoàn tất dọn dẹp: Đã vô hiệu hóa $disabledCount gói rác an toàn." -ForegroundColor Green

# 3. Tải & Cài đặt tvOS Launcher Tiếng Việt
Write-Host ""
Write-Host "[3/4] Cài đặt tvOS Launcher Tiếng Việt..." -ForegroundColor Green
$apkLocal = "$PSScriptRoot\build\tvos-home.apk"
if (-not (Test-Path $apkLocal)) {
    $apkLocal = "C:\Users\Admin\Desktop\tvOS-Launcher-v2.1.5-vi.apk"
}
if (-not (Test-Path $apkLocal)) {
    $apkLocal = "$env:TEMP\tvOS-Launcher-v2.1.5-vi.apk"
    Write-Host "    - Đang tải APK từ GitHub Releases..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri "https://github.com/acenguyen0210/tvOS-Launcher-vi/releases/latest/download/tvOS-Launcher-v2.1.5-vi.apk" -OutFile $apkLocal
}

Write-Host "    - Đang đẩy file APK sang TV và cài đặt..." -ForegroundColor Cyan
& $adb -s "$TvHost`:5555" install -r "$apkLocal" | Out-Null
Write-Host "    ✓ Đã cài đặt tvOS Launcher Tiếng Việt thành công!" -ForegroundColor Green

# 4. Gán Launcher Mặc Định
Write-Host ""
Write-Host "[4/4] Thiết lập tvOS Launcher làm giao diện mặc định..." -ForegroundColor Green
& $adb -s "$TvHost`:5555" shell cmd package set-home-activity "com.techgenius.tvoslauncher/.MainActivity" | Out-Null
& $adb -s "$TvHost`:5555" shell am start -n "com.techgenius.tvoslauncher/.MainActivity" | Out-Null

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  HOÀN TẤT THÀNH CÔNG!" -ForegroundColor Green
Write-Host "  1. Tivi đã được dọn sạch quảng cáo và app rác." -ForegroundColor White
Write-Host "  2. tvOS Launcher Tiếng Việt đã được kích hoạt làm Home mặc định." -ForegroundColor White
Write-Host "================================================================" -ForegroundColor Cyan
