"""Exposes high level build tasks."""
from pathlib import Path, PurePath
import platform
import shutil
from multiprocessing.dummy import Pool

from halfling.compile import CompileOptions, force_compile, link, is_compile_needed


class _TaskPool:
    def __init__(self, num_processes):
        self.pool = Pool(num_processes)
        self.pending = 0
        self.exc = None

    def _job_callback(self, _):
        # TODO: this is probably not atomic
        self.pending -= 1

    def _job_err_callback(self, exc):
        # TODO: this is almost certainly not atomic
        self.exc = exc

    def submit_job(self, func, args):
        self.pending += 1
        self.pool.apply_async(
            func, args, callback=self._job_callback, error_callback=self._job_err_callback)

    def wait_for_done(self):
        while self.pending:
            # raise exceptions from threads here
            if self.exc:
                self.pool.terminate()
                self.pool.join()
                raise self.exc


def build(config, build_type, num_processes):
    """Builds project.

    Args:
        config (Config): Halfling configuration.
        build_type (str): "debug" or "release"
        num_processes (int): Number of processes to run the build with. If 'None'
            is provided for this argument, will default to os.cpu_count().

    Returns:
        None

    Raises:
        HalfingError: if any build compilation errors occur. Will contain 
        compiler error message.
    """
    print(f"Building {config.project_name}..")
    # create build + obj directory if they don't exist
    obj_dir = Path(config.build_dir, config.obj_dir)
    obj_dir.mkdir(parents=True, exist_ok=True)
    # create compile options
    options = CompileOptions(config, build_type)
    # we need to keep track of a flag indicating linking is required,
    # object file names in the case linking is required, and a file
    # modified times dictionary to save on f.stat() queries
    needs_link = False
    obj_fnames = []
    file_mtimes = {}

    # compile files as needed in a thread pool
    pool = _TaskPool(num_processes)
    for src_fname in config.sources:
        src_fname = Path(src_fname)
        obj_fname = obj_dir / src_fname.with_suffix(".o").name

        if is_compile_needed(src_fname, obj_fname, file_mtimes):
            pool.submit_job(force_compile, (config.compiler,
                                            src_fname, obj_fname, options))
            needs_link = True

        obj_fnames.append(obj_fname)

    pool.wait_for_done()

    # get windows-compatible exe name
    executable_name = Path(config.build_dir, config.project_name)
    if platform.system() == "Windows":
        executable_name = executable_name.with_suffix(".exe")
    # link
    if needs_link or not executable_name.exists():
        link(config.compiler, obj_fnames, executable_name, options)
        print("Build successful.")
    else:
        print("Build up to date.")


def clean(config):
    """Cleans project (removes build dir).

    Args:
        config (Config): Halfling configuration.

    Returns:
        None
    """
    shutil.rmtree(config.build_dir)
    print("Clean successful.")
