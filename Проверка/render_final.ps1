$rpzPath = 'C:\Users\User\Documents\Индивидуальное задание\Отчёты\РПЗ_Последовательная_коррекция.docx'
$rpzDir = 'C:\Users\User\Documents\Индивидуальное задание\Рабочие файлы\Проверка\Рендер'
$rpzWord = New-Object -ComObject Word.Application
$rpzWord.Visible=$false
$rpzWord.DisplayAlerts=0
$rpzWord.Options.UpdateFieldsAtPrint=$false
$rpzWord.Options.UpdateLinksAtPrint=$false
$rpzWord.Options.PrintBackground=$false
$rpzWord.Options.BackgroundSave=$false
try {
 $rpzDoc=$rpzWord.Documents.Open($rpzPath,$false,$false)
 $null=$rpzDoc.Fields.Update()
 foreach($rpzToc in $rpzDoc.TablesOfContents){$rpzToc.Update()}
 $rpzDoc.Repaginate()
 $rpzDoc.Save()
 Write-Output ('saved pages='+$rpzDoc.ComputeStatistics(2))
 Write-Output 'opened'
 $rpzDoc.ExportAsFixedFormat(($rpzDir+'\page1_release.pdf'),17,$false,0,3,1,1,0,$false,$false,0,$false,$false,$false)
 Write-Output 'page1 exported'
 $rpzDoc.ExportAsFixedFormat(($rpzDir+'\release_verified.pdf'),17,$false,0,0,1,33,0,$false,$false,0,$false,$false,$false)
 Write-Output 'full exported'
 $rpzDoc.Close(0)
} finally {$rpzWord.Quit()}
