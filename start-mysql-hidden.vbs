' Пуска start-mysql.bat без да отваря черен прозорец.
' Копие от този файл стои в папката Startup, за да се вдига MySQL при влизане в Windows.
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
bat = fso.GetParentFolderName(WScript.ScriptFullName) & "\start-mysql.bat"
sh.Run """" & bat & """", 0, False
