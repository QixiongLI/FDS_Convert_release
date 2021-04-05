@setlocal enableextensions
@cd /d "%~dp0"
@prompt $G
@set Framework4Dir=C:\Windows\Microsoft.NET\Framework\v4.0.30319
%Framework4Dir%\regasm .\MDT.ParameterInterface.dll /codebase /tlb:MDT.ParameterInterface.tlb

pause