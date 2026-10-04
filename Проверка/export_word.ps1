$rpzPath = 'C:\Users\User\Documents\Индивидуальное задание\Отчёты\РПЗ_Последовательная_коррекция.docx'
$rpzPdf = 'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы\Проверка\Рендер\report_final.pdf'
$rpzWord = New-Object -ComObject Word.Application
$rpzWord.Visible = $false
$rpzWord.DisplayAlerts = 0
try {
 Write-Output 'opening'; $rpzDoc = $rpzWord.Documents.Open($rpzPath,$false,$false); Write-Output 'opened'
 $null = $rpzDoc.Fields.Update()
 foreach($rpzToc in $rpzDoc.TablesOfContents) { $rpzToc.Update() }
 $rpzDoc.Repaginate()
 $rpzDoc.Save(); Write-Output ('saved pages=' + $rpzDoc.ComputeStatistics(2))
 $rpzDoc.ExportAsFixedFormat($rpzPdf,17,$false,1,0,1,1,0,$true,$false,0,$false,$false,$false)
 Write-Output ('pages=' + $rpzDoc.ComputeStatistics(2))
 $rpzDoc.Close(0)
} finally { $rpzWord.Quit() }
