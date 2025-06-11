from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["aifc", "speech_recognition", "chunk", "audioop"],
    "include_files": ["recursos/"
        
    ],
}

setup(
    name="MeuJogo",
    version="1.0",
    description="Jogo em Pygame com reconhecimento de voz",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="Win32GUI", icon="recursos/icone.ico")]
)