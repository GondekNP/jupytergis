import subprocess
from pathlib import Path
import argparse

def execute(cmd: str, cwd=None):
    subprocess.run(cmd.split(" "), check=True, cwd=cwd)


def install_dev(target_path: str = None):

    if not target_path:
        target_path = str(Path(__file__).parents[1])
    else:
        target_path = Path(target_path).resolve()

    requirements_build_path = target_path / "requirements-build.txt"
    install_build_deps = f"python -m pip install -r {requirements_build_path}"
    install_js_deps = "jlpm install"
    build_js = "jlpm build"

    python_package_prefix = "python"
    python_packages = [
        "jupytergis_core",
        "jupytergis_lab",
        "jupytergis_qgis",
    ]

    execute(install_build_deps, cwd=target_path)
    execute(install_js_deps, cwd=target_path)
    execute(build_js, cwd=target_path)

    for py_package in python_packages:
        execute(f"pip uninstall {py_package} -y")
        execute("jlpm clean:all", cwd=target_path / "python" / py_package)
        execute(f"pip install -e {python_package_prefix}/{py_package}")

        if py_package == "jupytergis_qgis":
            execute("jupyter server extension enable jupytergis_qgis")

        execute(
            f"jupyter labextension develop {python_package_prefix}/{py_package} --overwrite"
        )

    execute(f"pip install -e {python_package_prefix}/jupytergis")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Install JupyterGIS development environment.")
    parser.add_argument(
        "--target-path",
        type=str,
        default=None,
        help="Path to the JupyterGIS repository root directory.",
    )

    args = parser.parse_args()

    install_dev(target_path=args.target_path)
