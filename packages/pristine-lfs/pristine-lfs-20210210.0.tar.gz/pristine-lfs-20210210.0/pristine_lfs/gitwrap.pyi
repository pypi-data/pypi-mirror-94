# Extremely simplified type stubs for the Git wrapper.
# Extend as needed.
#
# Copyright (C) 2021 Collabora Ltd
# Andrej Shadura <andrew.shadura@collabora.co.uk>

from sh.contrib import git as sh_git


class Git(sh_git):
    lfs: sh_git.lfs


git: Git
