[Setup]
AppName=AutoCodeAtive
AppVersion=1.0
DefaultDirName={pf}\AutoCodeAtive
DefaultGroupName=AutoCodeAtive
OutputBaseFilename=AutoCodeAtive_Installer
Compression=lzma
SolidCompression=yes
DisableDirPage=no

[Files]
Source: "src\dist\antepausa.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AutoCodeAtive"; Filename: "{app}\antepausa.exe"
Name: "{group}\Desinstalar AutoCodeAtive"; Filename: "{uninstallexe}"
Name: "{userdesktop}\AutoCodeAtive"; Filename: "{app}\antepausa.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Opções adicionais:"
