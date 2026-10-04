$srv=New-Object -ComObject mmain.MVTU_Server
$srv.SetMainFormVisible(0)
$pidSIT=[long]0
$srv.OpenProject('C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы\Схемы\01_ЛАЧХ.xprt',[ref]$pidSIT)
$srv.WaitForAllLoading()
Write-Output $pidSIT
$srv.ProjectStart($pidSIT)
$tSIT=[double]0
$srv.GetProjectTime($pidSIT,[ref]$tSIT)
Write-Output $tSIT
