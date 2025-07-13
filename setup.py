from cx_Freeze import setup, Executable

build_exe_options = {
    "include_files": [
        ("source", "source")
    ]
}

setup(
    name="comparePDF",
    version="1.1.0",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")]
)
