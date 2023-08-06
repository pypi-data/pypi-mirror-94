# halfling
Small C/++ build system written in Python; supports gcc and clang.

## Installation
```shell
$ pip3 install halfling
```

## Introduction
For some strange reason I felt the urge to create my own build system. This is not intended to be feature rich, free of bugs, or particularly fast. On my machine, builds with halfling are marginally slower than builds with make. Halfling supports incremental builds based on file modified times.

The biggest advantage to halfling is ease of use. Builds are configured with a `halfling.toml` file in the root folder of the project. Most configuration options have reasonable defaults, which means the minimal config file looks like this:

```toml
# This will be the name of the output executable
project_name = "hello_world"

compiler = "clang++"
sources = ["main.cpp"]
```

Your project can then be built by navigating to the same folder with your `halfling.toml` file and running:
```console
$ halfling build
```

To view all of the CLI arguments & options, use `halfling -h`:
```console
$ halfling -h
usage: halfling [-h] [-t {debug,release}] [-j JOBS] {build,clean}

positional arguments:
  {build,clean}         task to be run by halfling

optional arguments:
  -h, --help            show this help message and exit
  -t {debug,release}, --type {debug,release}
                        controls build type; defaults to release
  -j JOBS, --jobs JOBS  controls max processes to run build with; defaults to os.cpu_count()
```

As you can see, halfling can either build your project in debug or release mode, or clean your project (remove the build directory and it's contents). You can also specify the maximum number of processes to run your build with.

A complete TOML with all options specified looks like this:

```toml
# This will be the name of the output executable
project_name = "shotgun"

compiler = "clang++"
sources = [
  "src/main.cpp",
  "src/add.cpp",
  "src/sub.cpp",
]

###### Everything below this line is optional #######

defines = [
  "DEFINED_IN_TOML",
  "ALSO_DEFINED_IN_TOML",
]
include_paths = ["lib/mul/inc"]

libraries = ["mul"]
library_paths = ["lib/mul"]

common_flags = ["-Wall"]
debug_flags = ["-O0"] # defaults to ["-0g", "-g"]
release_flags = ["-O1"] # defualts to ["-02"]

# Specify a different build dir and obj dir -- just to be a contrarian
build_dir = "hbuild" # defaults to build
obj_dir = "hobj" # defaults to obj; this will resolve to {build_dir}/{obj_dir}
```

Example projects can be found in the `examples/` directory.

If you want to do more than what is provided by the CLI, halfling can also be used as a package in your own python scripts. Check the source files in the `halfling/` directory; reasonable docstrings (at least for a lazy person) can be found there.
