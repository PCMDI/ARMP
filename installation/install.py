import os
import subprocess


def main():
    # Get the directory of the current script (install.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to install.sh in the same package directory
    install_script_path = os.path.join(current_dir, "install.sh")

    # Run the shell script
    subprocess.run(["bash", install_script_path], check=True)


if __name__ == "__main__":
    main()
