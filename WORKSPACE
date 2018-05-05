git_repository(
    name = "io_bazel_rules_python",
    commit = "8b5d0683a7d878b28fffe464779c8a53659fc645",
    remote = "https://github.com/bazelbuild/rules_python",
)

git_repository(
    name = "subpar",
    remote = "https://github.com/google/subpar",
    tag = "1.3.0",
)

load("@io_bazel_rules_python//python:pip.bzl", "pip_import")
load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

pip_import(
    name = "pip_deps",
    requirements = "//:requirements.txt",
)

load("@pip_deps//:requirements.bzl", "pip_install")

pip_install()
