import solcx


def compile_file(f):
    return solcx.compile_files([f], output_values=["abi", "bin-runtime", "bin"])
