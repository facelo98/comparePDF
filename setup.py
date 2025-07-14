from cx_Freeze import setup, Executable

build_exe_options = {
    "excludes": ["test"],
    "include_files": [
        ("src", "src"),
        ("C:/Users/Fabio/Documents/comparePDF/lib/site-packages/comtypes/stream.py", "lib/comtypes/stream.py")
    ]
}

setup(
    name="comparePDF",
    version="1.2.0",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py",
                 target_name="comparePDF.exe")]
)
