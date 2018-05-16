import sys  ,os
from cx_Freeze import setup, Executable


os.environ['TCL_LIBRARY'] = "E:\\soft\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "E:\\soft\\Python\\Python36-32\\tcl\\tk8.6"

base = None 
if sys.platform == "win32": 
    base = "Win32GUI" 

setup( 
  name = "MyApp",  
version = "1.0", 
description = "MyApp",
options = {  
                'build_exe':   
                        {
                "include_files":["./temp",'E:\\soft\\Python\\Python36-32\\DLLs\\tcl86t.dll', 'E:\\soft\\Python\\Python36-32\\DLLs\\tk86t.dll'],
               
              "packages": ["idna","PIL","re","time","urllib","requests","os","sys","json","random","pygame","tkinter","threading"]  
                              
                            }  
                  
                } ,
executables = [Executable("./MP3pygame.py",base = "Win32GUI",icon = "./temp/9.ico",targetName='MUSIC.exe')])
