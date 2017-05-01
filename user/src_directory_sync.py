import os
import subprocess

SRC_DIRECTORY = os.path.join(
  os.path.expanduser("~"),
  "src",
)

ORIGIN_URI_TEMPLATE = "git@eyl.io:jon/{}"
GITHUB_URI_TEMPLATE = "git@github.com:eyolfson/{}"
ECGIT_URI_TEMPLATE = "git@ecgit.uwaterloo.ca:jeyolfso/{}"

PUBLIC_REPOSITORIES = [
  "hello-vulkan",
  "eyl-nes-emulator",
  "eyl-software-development",
  "matasano-challenge",
  "site-eyl-blog",
]

PRIVATE_REPOSITORIES = [
  "eudyptula-challenge",
]

UWATERLOO_REPOSITORIES = [
  "clang-immutability-check",
  "llvm-immutability-analysis",
  "phd-thesis",
]

EXTERNAL_REPOSITORIES = [
  ("clang",
   "http://llvm.org/git/clang.git",
   []),
  ("clang-tools-extra",
   "http://llvm.org/git/clang-tools-extra.git",
   []),
  ("cores",
   "https://github.com/PaulStoffregen/cores.git",
   []),
  ("linux",
   "git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
   [("next",
     "git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git")]),
  ("llvm",
   "http://llvm.org/git/llvm.git",
   []),
]

def clone(git_directory, uri):
  if not os.path.exists(git_directory):
    directory = os.path.dirname(git_directory)
    subprocess.run(["git", "clone", uri],
                   check=True,
                   cwd=directory)

def check_remote(git_directory, name, uri):
  p = subprocess.run(["git", "remote", "get-url", name],
                     cwd=git_directory,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True)
  if p.returncode == 0:
    current_uri = p.stdout.strip()
    if current_uri != uri:
      subprocess.run(["git", "remote", "set-url", name, uri],
                     check=True,
                     cwd=git_directory)
      print("\033[36mRemote '{}' changed\033[m".format(name))
  else:
    subprocess.run(["git", "remote", "add", name, uri],
                   check=True,
                   cwd=git_directory)
    print("\033[36mRemote '{}' added\033[m".format(name))

print("\033[1;34mPrivate Repositories\033[m")
for repo_name in PRIVATE_REPOSITORIES:
  print("\033[1;36mRepository '{}'\033[m".format(repo_name))
  git_directory = os.path.join(SRC_DIRECTORY, "private", repo_name)
  origin_uri = ORIGIN_URI_TEMPLATE.format(repo_name)
  clone(git_directory, origin_uri)
  check_remote(git_directory, "origin", origin_uri)

print("\033[1;34mPublic Repositories\033[m")
for repo_name in PUBLIC_REPOSITORIES:
  print("\033[1;36mRepository '{}'\033[m".format(repo_name))
  git_directory = os.path.join(SRC_DIRECTORY, "public", repo_name)
  origin_uri = ORIGIN_URI_TEMPLATE.format(repo_name)
  github_uri = GITHUB_URI_TEMPLATE.format(repo_name)
  clone(git_directory, origin_uri)
  check_remote(git_directory, "origin", origin_uri)
  check_remote(git_directory, "github", github_uri)

print("\033[1;34mUWaterloo Repositories\033[m")
for repo_name in UWATERLOO_REPOSITORIES:
  print("\033[1;36mRepository '{}'\033[m".format(repo_name))
  git_directory = os.path.join(SRC_DIRECTORY, "uwaterloo", repo_name)
  origin_uri = ORIGIN_URI_TEMPLATE.format(repo_name)
  ecgit_uri = ECGIT_URI_TEMPLATE.format(repo_name)
  clone(git_directory, origin_uri)
  check_remote(git_directory, "origin", origin_uri)
  check_remote(git_directory, "ecgit", ecgit_uri)

print("\033[1;34mExternal Repositories\033[m")
for entry in EXTERNAL_REPOSITORIES:
  repo_name, upstream_uri, external_remotes = entry
  print("\033[1;36mRepository '{}'\033[m".format(repo_name))
  git_directory = os.path.join(SRC_DIRECTORY, "external", repo_name)
  origin_uri = ORIGIN_URI_TEMPLATE.format(repo_name)
  clone(git_directory, origin_uri)
  check_remote(git_directory, "origin", origin_uri)
  check_remote(git_directory, "upstream", upstream_uri)
  for remote_name, remote_uri in external_remotes:
    check_remote(git_directory, remote_name, remote_uri)
