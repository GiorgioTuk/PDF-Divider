[Setup]
AppName=PDF Divider
AppVersion=1.0.0
AppPublisher=Giorgio Tuccinardi
AppPublisherURL=https://github.com/GiorgioTuk/PDF-Divider
DefaultDirName={localappdata}\PDF_Divider
DefaultGroupName=PDF Divider
OutputDir=..\release
OutputBaseFilename=PDF_Divider_Setup_v1.0.0
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\PDF_Divider.exe
SetupIconFile=..\assets\pdf_icon.ico

[Files]
Source: "..\dist\PDF_Divider\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{autodesktop}\PDF Divider"; Filename: "{app}\PDF_Divider.exe"
Name: "{group}\PDF Divider";       Filename: "{app}\PDF_Divider.exe"
Name: "{group}\Disinstalla PDF Divider"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\PDF_Divider.exe"; Description: "Avvia PDF Divider"; Flags: nowait postinstall skipifsilent
