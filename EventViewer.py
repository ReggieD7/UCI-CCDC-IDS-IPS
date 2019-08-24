p = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe', 
                    'Get-EventLog -logname Security -Newest 5'], 
                      stdin=subprocess.PIPE)
