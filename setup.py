from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["comtypes"],
    "includes": ["comtypes.stream"],
    "include_files": [
        ("source", "source"),
        ("src", "src"),
        ("C:/Users/Fabio/Documents/comparePDF/lib/site-packages/comtypes/stream.py", "lib/comtypes/stream.py")

    ]
}

setup(
    name="comparePDF",
    version="1.1.2",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")]
)
