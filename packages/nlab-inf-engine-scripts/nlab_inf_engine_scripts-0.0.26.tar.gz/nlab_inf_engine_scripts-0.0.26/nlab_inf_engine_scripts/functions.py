import datetime
import random
import string
import subprocess
import tempfile
from pathlib import Path


def create_temp_dir(parent_dir: Path) -> Path:  # tempfile.TemporaryDirectory:
    """ Create a temp directory, which will be deleted on object destruction. """

    current_time = datetime.datetime.now()

    # temp_dir = tempfile.TemporaryDirectory(
    #     prefix=f"{current_time.year}-{current_time.month}-{current_time.day}_{current_time.hour}-{current_time.minute}_",
    #     dir=parent_dir,
    # )

    randomized_name = "".join(random.choices(string.ascii_letters, k=6))
    temp_dir = (
        parent_dir / f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        f"_{randomized_name}"
    )
    temp_dir.mkdir(parents=True)

    return temp_dir


def symlink(frm: Path, to: Path, force: bool = False):
    """ Create a symlink from one file to another. """

    if force:
        cmd = f"ln -sfT {frm} {to}"
    else:
        cmd = f"ln -s {frm} {to}"

    completed_process = subprocess.run(cmd, shell=True)

    if completed_process.returncode:
        raise Exception(f"Can't create a symlink: {cmd}")

    return to
