# The Fuck [![Version][version-badge]][version-link] [![Build Status][workflow-badge]][workflow-link] [![Coverage][coverage-badge]][coverage-link] [![MIT License][license-badge]](LICENSE.md)

*The Fuck* 是一个神奇的应用，灵感来自 [@liamosaur](https://twitter.com/liamosaur/) 的
[推文](https://twitter.com/liamosaur/status/506975850596536320)，
它可以自动纠正你之前输入的错误命令。

*The Fuck* 运行太慢？[试试实验性的即时模式！](#experimental-instant-mode)

[![示例动图][examples-link]][examples-link]

更多示例：

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ fuck
sudo apt-get install vim [enter/↑/↓/ctrl+c]
[sudo] password for nvbn:
Reading package lists... Done
...
```

```bash
➜ git push
fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master


➜ fuck
git push --set-upstream origin master [enter/↑/↓/ctrl+c]
Counting objects: 9, done.
...
```

```bash
➜ puthon
No command 'puthon' found, did you mean:
 Command 'python' from package 'python-minimal' (main)
 Command 'python' from package 'python3' (main)
zsh: command not found: puthon

➜ fuck
python [enter/↑/↓/ctrl+c]
Python 3.4.2 (default, Oct  8 2014, 13:08:17)
...
```

```bash
➜ git brnch
git: 'brnch' is not a git command. See 'git --help'.

Did you mean this?
    branch

➜ fuck
git branch [enter/↑/↓/ctrl+c]
* master
```

```bash
➜ lein rpl
'rpl' is not a task. See 'lein help'.

Did you mean this?
         repl

➜ fuck
lein repl [enter/↑/↓/ctrl+c]
nREPL server started on port 54848 on host 127.0.0.1 - nrepl://127.0.0.1:54848
REPL-y 0.3.1
...
```

如果你不介意直接运行修正后的命令，可以在[设置](#settings)中禁用 `require_confirmation` 选项：

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ fuck
sudo apt-get install vim
[sudo] password for nvbn:
Reading package lists... Done
...
```

## 目录

1. [系统要求](#requirements)
2. [安装](#installation)
3. [更新](#updating)
4. [工作原理](#how-it-works)
5. [创建自己的规则](#creating-your-own-rules)
6. [设置](#settings)
7. [第三方规则包](#third-party-packages-with-rules)
8. [实验性即时模式](#experimental-instant-mode)
9. [开发](#developing)
10. [许可证](#license-mit)

## 系统要求

- python (3.5+)
- pip
- python-dev

##### [返回目录](#contents)

## 安装

在 macOS 或 Linux 上，你可以通过 [Homebrew][homebrew] 安装 *The Fuck*：

```bash
brew install thefuck
```

在 Windows 上，你可以使用以下方式安装和配置 *The Fuck*：

1. 使用 pip 安装：
```bash
pip install thefuck
```

2. 配置 Git Bash：
   - 打开 Git Bash
   - 编辑 `~/.bashrc` 文件（如果不存在则创建）：
   ```bash
   notepad ~/.bashrc
   ```
   - 添加以下内容：
   ```bash
   eval $(thefuck --alias)
   # 或者使用其他别名，比如：
   # eval $(thefuck --alias FUCK)
   ```
   - 保存文件并重新加载配置：
   ```bash
   source ~/.bashrc
   ```

3. 配置 PowerShell：
   - 以管理员身份打开 PowerShell
   - 创建或编辑 PowerShell 配置文件：
   ```powershell
   if (!(Test-Path -Path $PROFILE)) {
       New-Item -ItemType File -Path $PROFILE -Force
   }
   notepad $PROFILE
   ```
   - 添加以下内容：
   ```powershell
   $env:PYTHONIOENCODING = "utf-8"
   Invoke-Expression (thefuck --alias)
   # 或者使用其他别名，比如：
   # Invoke-Expression (thefuck --alias FUCK)
   ```
   - 保存文件并重新加载配置：
   ```powershell
   . $PROFILE
   ```

在 Ubuntu / Mint 上，使用以下命令安装 *The Fuck*：
```bash
sudo apt update
sudo apt install python3-dev python3-pip python3-setuptools
pip3 install thefuck --user
```

在 FreeBSD 上，使用以下命令安装 *The Fuck*：
```bash
pkg install thefuck
```

在 ChromeOS 上，使用 [chromebrew](https://github.com/skycocker/chromebrew) 安装 *The Fuck*：
```bash
crew install thefuck
```

在基于 Arch 的系统上，使用以下命令安装 *The Fuck*：
```
sudo pacman -S thefuck
```

在其他系统上，使用 `pip` 安装 *The Fuck*：

```bash
pip install thefuck
```

[或者，你也可以使用操作系统包管理器（OS X、Ubuntu、Arch）。](https://github.com/nvbn/thefuck/wiki/Installation)

<a href='#manual-installation' name='manual-installation'>#</a>
建议将以下命令添加到你的 `.bash_profile`、`.bashrc`、`.zshrc` 或其他启动脚本中：

```bash
eval $(thefuck --alias)
# 你可以使用任何你想要的别名，比如周一用：
eval $(thefuck --alias FUCK)
```

[或者在你的 shell 配置文件中（Bash、Zsh、Fish、Powershell、tcsh）。](https://github.com/nvbn/thefuck/wiki/Shell-aliases)

更改只会在新的 shell 会话中生效。要使更改立即生效，运行 `source ~/.bashrc`（或你的 shell 配置文件，如 `.zshrc`）。

要运行修正后的命令而不需要确认，使用 `--yeah` 选项（或简写 `-y`，或者特别沮丧时用 `--hard`）：

```bash
fuck --yeah
```

要递归修复命令直到成功，使用 `-r` 选项：

```bash
fuck -r
```

##### [返回目录](#contents)

## 更新

```bash
pip3 install thefuck --upgrade
```

**注意：别名功能在 *The Fuck* v1.34 版本中有所改变**

## 卸载

要卸载 *The Fuck*，请反向执行安装过程：
- 从你的 Bash、Zsh、Fish、Powershell、tcsh 等 shell 配置中删除或注释掉 *thefuck* 别名行
- 使用你的包管理器（brew、pip3、pkg、crew、pip）卸载二进制文件

## 工作原理

*The Fuck* 尝试将之前的命令与规则进行匹配。如果找到匹配项，则使用匹配的规则创建新命令并执行。默认启用以下规则：

* `adb_unknown_command` &ndash; 修复拼写错误的命令，如 `adb logcta`；
* `ag_literal` &ndash; 在建议时添加 `-Q` 到 `ag`；
* `aws_cli` &ndash; 修复拼写错误的命令，如 `aws dynamdb scan`；
* `az_cli` &ndash; 修复拼写错误的命令，如 `az providers`；
* `cargo` &ndash; 运行 `cargo build` 而不是 `cargo`；
* `cargo_no_command` &ndash; 修复错误的命令，如 `cargo buid`；
* `cat_dir` &ndash; 当你尝试 `cat` 一个目录时，用 `ls` 替换 `cat`；
* `cd_correction` &ndash; 拼写检查和修正失败的 cd 命令；
* `cd_cs` &ndash; 将 `cs` 改为 `cd`；
* `cd_mkdir` &ndash; 在 cd 进入之前创建目录；
* `cd_parent` &ndash; 将 `cd..` 改为 `cd ..`；
* `chmod_x` &ndash; 添加执行权限；
* `choco_install` &ndash; 为 chocolatey 包添加常见后缀；
* `composer_not_command` &ndash; 修复 composer 命令名称；
* `conda_mistype` &ndash; 修复 conda 命令；
* `cp_create_destination` &ndash; 当你尝试 `cp` 或 `mv` 到不存在的目录时创建新目录；
* `cp_omitting_directory` &ndash; 当你 `cp` 目录时添加 `-a`；
* `cpp11` &ndash; 为 `g++` 或 `clang++` 添加缺失的 `-std=c++11`；
* `dirty_untar` &ndash; 修复在当前目录解压的 `tar x` 命令；
* `dirty_unzip` &ndash; 修复在当前目录解压的 `unzip` 命令；
* `django_south_ghost` &ndash; 为失败的 django south 迁移添加 `--delete-ghost-migrations`；
* `django_south_merge` &ndash; 为不一致的 django south 迁移添加 `--merge`；
* `docker_login` &ndash; 执行 `docker login` 并重复之前的命令；
* `docker_not_command` &ndash; 修复错误的 docker 命令，如 `docker tags`；
* `docker_image_being_used_by_container` &dash; 在删除镜像之前删除使用该镜像的容器；
* `dry` &ndash; 修复重复的命令，如 `git git push`；
* `fab_command_not_found` &ndash; 修复拼写错误的 fabric 命令；
* `fix_alt_space` &ndash; 将 Alt+Space 替换为 Space 字符；
* `fix_file` &ndash; 在 `$EDITOR` 中打开有错误的文件；
* `gem_unknown_command` &ndash; 修复错误的 `gem` 命令；
* `git_add` &ndash; 修复 *"pathspec 'foo' did not match any file(s) known to git."*；
* `git_add_force` &ndash; 当路径被 .gitignore 时，为 `git add <pathspec>...` 添加 `--force`；
* `git_bisect_usage` &ndash; 在二分查找时修复 `git bisect strt`、`git bisect goood`、`git bisect rset` 等；
* `git_branch_delete` &ndash; 将 `git branch -d` 改为 `git branch -D`；
* `git_branch_delete_checked_out` &ndash; 当尝试删除已检出的分支时，将 `git branch -d` 改为 `git checkout master && git branch -D`；
* `git_branch_exists` &ndash; 当创建已存在的分支时，提供 `git branch -d foo`、`git branch -D foo` 或 `git checkout foo`；
* `git_branch_list` &ndash; 捕获 `git branch list` 而不是 `git branch` 并删除创建的分支；
* `git_branch_0flag` &ndash; 修复 `git branch 0v` 和 `git branch 0r` 等命令，删除创建的分支；
* `git_checkout` &ndash; 修复分支名称或创建新分支；
* `git_clone_git_clone` &ndash; 将 `git clone git clone ...` 替换为 `git clone ...`
* `git_clone_missing` &ndash; 为看起来像 git 仓库的 URL 添加 `git clone`；
* `git_commit_add` &ndash; 如果之前的提交因为没有任何内容被暂存而失败，提供 `git commit -a ...` 或 `git commit -p ...`；
* `git_commit_amend` &ndash; 在之前的提交后提供 `git commit --amend`；
* `git_commit_reset` &ndash; 在之前的提交后提供 `git reset HEAD~`；
* `git_diff_no_index` &ndash; 为未跟踪文件的 `git diff` 添加 `--no-index`；
* `git_diff_staged` &ndash; 为输出意外的 `git diff` 添加 `--staged`；
* `git_fix_stash` &ndash; 修复 `git stash` 命令（拼写错误的子命令和缺失的 `save`）；
* `git_flag_after_filename` &ndash; 修复 `fatal: bad flag '...' after filename`
* `git_help_aliased` &ndash; 修复 `git help <alias>` 命令，将 <alias> 替换为别名命令；
* `git_hook_bypass` &ndash; 在 `git am`、`git commit` 或 `git push` 命令之前添加 `--no-verify` 标志；
* `git_lfs_mistype` &ndash; 修复拼写错误的 `git lfs <command>` 命令；
* `git_main_master` &ndash; 修复 `main` 和 `master` 之间的错误分支名称
* `git_merge` &ndash; 为分支名称添加远程；
* `git_merge_unrelated` &ndash; 在需要时添加 `--allow-unrelated-histories`；
* `git_not_command` &ndash; 修复错误的 git 命令，如 `git brnch`；
* `git_pull` &ndash; 在执行之前的 `git pull` 之前设置上游；
* `git_pull_clone` &ndash; 当仓库不存在时克隆而不是拉取；
* `git_pull_uncommitted_changes` &ndash; 在拉取之前暂存更改并在之后弹出；
* `git_push` &ndash; 为之前失败的 `git push` 添加 `--set-upstream origin $branch`；
* `git_push_different_branch_names` &ndash; 当本地分支名称与远程分支名称不匹配时修复推送；
* `git_push_pull` &ndash; 当 `push` 被拒绝时运行 `git pull`；
* `git_push_without_commits` &ndash; 如果你忘记并只 `git add .`，在设置新项目时创建初始提交；
* `git_rebase_no_changes` &ndash; 当没有更改时运行 `git rebase --skip` 而不是 `git rebase --continue`；
* `git_remote_delete` &ndash; 将 `git remote delete remote_name` 替换为 `git remote remove remote_name`；
* `git_rm_local_modifications` &ndash; 当你尝试 `rm` 一个本地修改的文件时添加 `-f` 或 `--cached`；
* `git_rm_recursive` &ndash; 当你尝试 `rm` 一个目录时添加 `-r`；
* `git_rm_staged` &ndash; 当你尝试 `rm` 一个有暂存更改的文件时添加 `-f` 或 `--cached`；
* `git_rebase_merge_dir` &ndash; 当正在进行 rebase 时提供 `git rebase (--continue | --abort | --skip)` 或删除 `.git/rebase-merge` 目录；
* `git_remote_seturl_add` &ndash; 当 `git remote set_url` 在不存在的远程上时运行 `git remote add`；
* `git_stash` &ndash; 在 rebase 或切换分支之前暂存你的本地修改；
* `git_stash_pop` &ndash; 在弹出暂存之前添加你的本地修改，然后重置；
* `git_tag_force` &ndash; 当标签已存在时为 `git tag <tagname>` 添加 `--force`；
* `git_two_dashes` &ndash; 为 `git commit -amend` 或 `git rebase -continue` 等命令添加缺失的破折号；
* `go_run` &ndash; 在编译/运行 Go 程序时添加 `.go` 扩展名；
* `go_unknown_command` &ndash; 修复错误的 `go` 命令，例如 `go bulid`；
* `gradle_no_task` &ndash; 修复未找到或模糊的 `gradle` 任务；
* `gradle_wrapper` &ndash; 将 `gradle` 替换为 `./gradlew`；
* `grep_arguments_order` &ndash; 修复 `grep` 参数顺序，如 `grep -lir . test`；
* `grep_recursive` &ndash; 当你尝试 `grep` 目录时添加 `-r`；
* `grunt_task_not_found` &ndash; 修复拼写错误的 `grunt` 命令；
* `gulp_not_task` &ndash; 修复拼写错误的 `gulp` 任务；
* `has_exists_script` &ndash; 当脚本/二进制文件存在时添加 `./`；
* `heroku_multiple_apps` &ndash; 为 `heroku pg` 等 `heroku` 命令添加 `--app <app>`；
* `heroku_not_command` &ndash; 修复错误的 `heroku` 命令，如 `heroku log`；
* `history` &ndash; 尝试用历史记录中最相似的命令替换命令；
* `hostscli` &ndash; 尝试修复 `hostscli` 用法；
* `ifconfig_device_not_found` &ndash; 修复错误的设备名称，如将 `wlan0` 改为 `wlp2s0`；
* `java` &ndash; 在运行 Java 程序时删除 `.java` 扩展名；
* `javac` &ndash; 在编译 Java 文件时添加缺失的 `.java`；
* `lein_not_task` &ndash; 修复错误的 `lein` 任务，如 `lein rpl`；
* `long_form_help` &ndash; 当不支持短形式版本时将 `-h` 改为 `--help`；
* `ln_no_hard_link` &ndash; 捕获目录上的硬链接创建，建议使用符号链接；
* `ln_s_order` &ndash; 修复 `ln -s` 参数顺序；
* `ls_all` &ndash; 当输出为空时为 `ls` 添加 `-A`；
* `ls_lah` &ndash; 为 `ls` 添加 `-lah`；
* `man` &ndash; 更改手册部分；
* `man_no_space` &ndash; 修复没有空格的 man 命令，例如 `mandiff`；
* `mercurial` &ndash; 修复错误的 `hg` 命令；
* `missing_space_before_subcommand` &ndash; 修复缺少空格的命令，如 `npminstall`；
* `mkdir_p` &ndash; 当你尝试创建没有父目录的目录时添加 `-p`；
* `mvn_no_command` &ndash; 为 `mvn` 添加 `clean package`；
* `mvn_unknown_lifecycle_phase` &ndash; 修复 `mvn` 的拼写错误生命周期阶段；
* `npm_missing_script` &ndash; 修复 `npm run-script <script>` 中的 `npm` 自定义脚本名称；
* `npm_run_script` &ndash; 为自定义 `npm` 脚本添加缺失的 `run-script`；
* `npm_wrong_command` &ndash; 修复错误的 npm 命令，如 `npm urgrade`；
* `no_command` &ndash; 修复错误的控制台命令，例如 `vom/vim`；
* `no_such_file` &ndash; 使用 `mv` 和 `cp` 命令创建缺失的目录；
* `omnienv_no_such_command` &ndash; 修复 `goenv`、`nodenv`、`pyenv` 和 `rbenv` 的错误命令（例如：`pyenv isntall` 或 `goenv list`）；
* `open` &ndash; 为传递给 `open` 的地址添加 `http://` 前缀，或创建新文件/目录并传递给 `open`；
* `pip_install` &ndash; 通过添加 `--user` 或在必要时添加 `sudo` 前缀来修复 `pip install` 命令的权限问题；
* `pip_unknown_command` &ndash; 修复错误的 `pip` 命令，例如 `pip instatl/pip install`；
* `php_s` &ndash; 在尝试运行本地 php 服务器时将 `-s` 替换为 `-S`；
* `port_already_in_use` &ndash; 终止绑定端口的进程；
* `prove_recursively` &ndash; 在调用目录时添加 `-r`；
* `python_command` &ndash; 当你尝试运行不可执行/没有 `./` 的 python 脚本时添加 `python` 前缀；
* `python_execute` &ndash; 在执行 Python 文件时添加缺失的 `.py`；
* `python_module_error` &ndash; 通过尝试 `pip install` 该模块来修复 ModuleNotFoundError；
* `quotation_marks` &ndash; 修复包含参数时 `'` 和 `"` 的不均匀使用；
* `path_from_history` &ndash; 用历史记录中相似的绝对路径替换未找到的路径；
* `rails_migrations_pending` &ndash; 运行待处理的迁移；
* `react_native_command_unrecognized` &ndash; 修复未识别的 `react-native` 命令；
* `remove_shell_prompt_literal` &ndash; 删除前导 shell 提示符 `$`，常见于从文档复制命令时；
* `remove_trailing_cedilla` &ndash; 删除尾随的 cedillas `ç`，这是欧洲键盘布局的常见拼写错误；
* `rm_dir` &ndash; 当你尝试删除目录时添加 `-rf`；
* `scm_correction` &ndash; 修正错误的 scm，如将 `hg log` 改为 `git log`；
* `sed_unterminated_s` &ndash; 为 `sed` 的 `s` 命令添加缺失的 '/'；
* `sl_ls` &ndash; 将 `sl` 改为 `ls`；
* `ssh_known_hosts` &ndash; 在警告时从 `known_hosts` 中删除主机；
* `sudo` &ndash; 如果之前的命令因权限问题失败，则添加 `sudo` 前缀；
* `sudo_command_from_user_path` &ndash; 使用 `sudo` 运行用户 `$PATH` 中的命令；
* `switch_lang` &ndash; 将命令从本地布局切换到英文；
* `systemctl` &ndash; 正确排序令人困惑的 `systemctl` 参数；
* `terraform_init.py` &ndash; 在 plan 或 apply 之前运行 `terraform init`；
* `terraform_no_command.py` &ndash; 修复未识别的 `terraform` 命令；
* `test.py` &ndash; 运行 `pytest` 而不是 `test.py`；
* `touch` &ndash; 在 "touching" 之前创建缺失的目录；
* `tsuru_login` &ndash; 如果未认证或会话过期，运行 `tsuru login`；
* `tsuru_not_command` &ndash; 修复错误的 `tsuru` 命令，如 `tsuru shell`；
* `tmux` &ndash; 修复 `tmux` 命令；
* `unknown_command` &ndash; 修复 hadoop hdfs 风格的 "unknown command"，例如在 `hdfs dfs ls` 上为命令添加缺失的 '-'；
* `unsudo` &ndash; 如果进程拒绝在超级用户权限下运行，则从之前的命令中删除 `sudo`。
* `vagrant_up` &ndash; 启动 vagrant 实例；
* `whois` &ndash; 修复 `whois` 命令；
* `workon_doesnt_exists` &ndash; 修复 `virtualenvwrapper` 环境名称或建议创建新的。
* `wrong_hyphen_before_subcommand` &ndash; 删除位置不当的连字符（`apt-install` -> `apt install`，`git-log` -> `git log` 等）
* `yarn_alias` &ndash; 修复别名的 `yarn` 命令，如 `yarn ls`；
* `yarn_command_not_found` &ndash; 修复拼写错误的 `yarn` 命令；
* `yarn_command_replaced` &ndash; 修复替换的 `yarn` 命令；
* `yarn_help` &ndash; 使打开 `yarn` 文档更容易；

##### [返回目录](#contents)

以下规则仅在特定平台上默认启用：

* `apt_get` &ndash; 如果应用未安装，则从 apt 安装（需要 `python-commandnotfound` / `python3-commandnotfound`）；
* `apt_get_search` &ndash; 将使用 `apt-get` 搜索改为使用 `apt-cache` 搜索；
* `apt_invalid_operation` &ndash; 修复无效的 `apt` 和 `apt-get` 调用，如 `apt-get isntall vim`；
* `apt_list_upgradable` &ndash; 在 `apt update` 后帮助你运行 `apt list --upgradable`；
* `apt_upgrade` &ndash; 在 `apt list --upgradable` 后帮助你运行 `apt upgrade`；
* `brew_cask_dependency` &ndash; 安装 cask 依赖；
* `brew_install` &ndash; 修复 `brew install` 的公式名称；
* `brew_reinstall` &ndash; 将 `brew install <formula>` 改为 `brew reinstall <formula>`；
* `brew_link` &ndash; 如果链接失败，添加 `--overwrite --dry-run`；
* `brew_uninstall` &ndash; 如果安装了多个版本，为 `brew uninstall` 添加 `--force`；
* `brew_unknown_command` &ndash; 修复错误的 brew 命令，例如 `brew docto/brew doctor`；
* `brew_update_formula` &ndash; 将 `brew update <formula>` 改为 `brew upgrade <formula>`；
* `dnf_no_such_command` &ndash; 修复拼写错误的 DNF 命令；
* `nixos_cmd_not_found` &ndash; 在 NixOS 上安装应用；
* `pacman` &ndash; 如果应用未安装，则使用 `pacman` 安装（如果可用，则使用 `yay`、`pikaur` 或 `yaourt`）；
* `pacman_invalid_option` &ndash; 将小写的 `pacman` 选项替换为大写。
* `pacman_not_found` &ndash; 使用 `pacman`、`yay`、`pikaur` 或 `yaourt` 修复包名。
* `yum_invalid_operation` &ndash; 修复无效的 `yum` 调用，如 `yum isntall vim`；

以下命令与 *The Fuck* 捆绑在一起，但默认不启用：

* `git_push_force` &ndash; 为 `git push` 添加 `--force-with-lease`（可能与 `git_push_pull` 冲突）；
* `rm_root` &ndash; 为 `rm -rf /` 命令添加 `--no-preserve-root`。

##### [返回目录](#contents)

## 创建自己的规则

要添加自己的规则，在 `~/.config/thefuck/rules` 中创建一个名为 `your-rule-name.py` 的文件。规则文件必须包含两个函数：

```python
match(command: Command) -> bool
get_new_command(command: Command) -> str | list[str]
```

此外，规则可以包含可选函数：

```python
side_effect(old_command: Command, fixed_command: str) -> None
```
规则还可以包含可选的变量 `enabled_by_default`、`requires_output` 和 `priority`。

`Command` 有三个属性：`script`、`output` 和 `script_parts`。
你的规则不应该改变 `Command`。

**规则 API 在 3.0 中改变：** 要访问规则的设置，使用
 `from thefuck.conf import settings` 导入

`settings` 是一个特殊的对象，由 `~/.config/thefuck/settings.py` 和
环境变量中的值组装而成（[详见下文](#settings)）。

一个简单的运行脚本时使用 `sudo` 的规则示例：

```python
def match(command):
    return ('permission denied' in command.output.lower()
            or 'EACCES' in command.output)


def get_new_command(command):
    return 'sudo {}'.format(command.script)

# 可选：
enabled_by_default = True

def side_effect(command, fixed_command):
    subprocess.call('chmod 777 .', shell=True)

priority = 1000  # 越低越优先，默认为 1000

requires_output = True
```

[更多规则示例](https://github.com/nvbn/thefuck/tree/master/thefuck/rules)，
[规则实用函数](https://github.com/nvbn/thefuck/tree/master/thefuck/utils.py)，
[应用/操作系统特定助手](https://github.com/nvbn/thefuck/tree/master/thefuck/specific/)。

##### [返回目录](#contents)

## 设置

几个 *The Fuck* 参数可以在文件 `$XDG_CONFIG_HOME/thefuck/settings.py` 中更改
（`$XDG_CONFIG_HOME` 默认为 `~/.config`）：

* `rules` &ndash; 启用的规则列表，默认为 `thefuck.const.DEFAULT_RULES`；
* `exclude_rules` &ndash; 禁用的规则列表，默认为 `[]`；
* `require_confirmation` &ndash; 在运行新命令之前需要确认，默认为 `True`；
* `wait_command` &ndash; 获取上一个命令输出的最大时间（秒）；
* `no_colors` &ndash; 禁用彩色输出；
* `priority` &ndash; 规则优先级的字典，优先级较低的规则将优先匹配；
* `debug` &ndash; 启用调试输出，默认为 `False`；
* `history_limit` &ndash; 要扫描的历史命令数量的数值，如 `2000`；
* `alter_history` &ndash; 将修正后的命令推送到历史记录，默认为 `True`；
* `wait_slow_command` &ndash; 如果命令在 `slow_commands` 列表中，获取上一个命令输出的最大时间（秒）；
* `slow_commands` &ndash; 慢命令列表；
* `num_close_matches` &ndash; 建议的最大接近匹配数，默认为 `3`。
* `excluded_search_path_prefixes` &ndash; 搜索命令时要忽略的路径前缀，默认为 `[]`。

`settings.py` 的示例：

```python
rules = ['sudo', 'no_command']
exclude_rules = ['git_push']
require_confirmation = True
wait_command = 10
no_colors = False
priority = {'sudo': 100, 'no_command': 9999}
debug = False
history_limit = 9999
wait_slow_command = 20
slow_commands = ['react-native', 'gradle']
num_close_matches = 5
```

或通过环境变量：

* `THEFUCK_RULES` &ndash; 启用的规则列表，如 `DEFAULT_RULES:rm_root` 或 `sudo:no_command`；
* `THEFUCK_EXCLUDE_RULES` &ndash; 禁用的规则列表，如 `git_pull:git_push`；
* `THEFUCK_REQUIRE_CONFIRMATION` &ndash; 在运行新命令之前需要确认，`true/false`；
* `THEFUCK_WAIT_COMMAND` &ndash; 获取上一个命令输出的最大时间（秒）；
* `THEFUCK_NO_COLORS` &ndash; 禁用彩色输出，`true/false`；
* `THEFUCK_PRIORITY` &ndash; 规则的优先级，如 `no_command=9999:apt_get=100`，
优先级较低的规则将优先匹配；
* `THEFUCK_DEBUG` &ndash; 启用调试输出，`true/false`；
* `THEFUCK_HISTORY_LIMIT` &ndash; 要扫描的历史命令数量，如 `2000`；
* `THEFUCK_ALTER_HISTORY` &ndash; 将修正后的命令推送到历史记录 `true/false`；
* `THEFUCK_WAIT_SLOW_COMMAND` &ndash; 如果命令在 `slow_commands` 列表中，获取上一个命令输出的最大时间（秒）；
* `THEFUCK_SLOW_COMMANDS` &ndash; 慢命令列表，如 `lein:gradle`；
* `THEFUCK_NUM_CLOSE_MATCHES` &ndash; 建议的最大接近匹配数，如 `5`。
* `THEFUCK_EXCLUDED_SEARCH_PATH_PREFIXES` &ndash; 搜索命令时要忽略的路径前缀，默认为 `[]`。

例如：

```bash
export THEFUCK_RULES='sudo:no_command'
export THEFUCK_EXCLUDE_RULES='git_pull:git_push'
export THEFUCK_REQUIRE_CONFIRMATION='true'
export THEFUCK_WAIT_COMMAND=10
export THEFUCK_NO_COLORS='false'
export THEFUCK_PRIORITY='no_command=9999:apt_get=100'
export THEFUCK_HISTORY_LIMIT='2000'
export THEFUCK_NUM_CLOSE_MATCHES='5'
```

##### [返回目录](#contents)

## 第三方规则包

如果你想制作一组非公开的规则，但仍想与他人分享，创建一个名为 `thefuck_contrib_*` 的包，结构如下：

```
thefuck_contrib_foo
  thefuck_contrib_foo
    rules
      __init__.py
      *third-party rules*
    __init__.py
    *third-party-utils*
  setup.py
```

*The Fuck* 将找到位于 `rules` 模块中的规则。

##### [返回目录](#contents)

## 实验性即时模式

*The Fuck* 的默认行为需要时间重新运行之前的命令。
在即时模式下，*The Fuck* 通过使用 [script](https://en.wikipedia.org/wiki/Script_(Unix)) 记录输出来节省时间，
然后读取日志。

[![即时模式动图][instant-mode-gif-link]][instant-mode-gif-link]

目前，即时模式仅支持使用 bash 或 zsh 的 Python 3。zsh 的自动更正功能也需要禁用，以便 thefuck 正常工作。

要启用即时模式，在 `.bashrc`、`.bash_profile` 或 `.zshrc` 中的别名初始化中添加 `--enable-experimental-instant-mode`。

例如：

```bash
eval $(thefuck --alias --enable-experimental-instant-mode)
```

##### [返回目录](#contents)

## 开发

参见 [CONTRIBUTING.md](CONTRIBUTING.md)

## MIT 许可证
项目许可证可以在[这里](LICENSE.md)找到。


[version-badge]:   https://img.shields.io/pypi/v/thefuck.svg?label=version
[version-link]:    https://pypi.python.org/pypi/thefuck/
[workflow-badge]:  https://github.com/nvbn/thefuck/workflows/Tests/badge.svg
[workflow-link]:   https://github.com/nvbn/thefuck/actions?query=workflow%3ATests
[coverage-badge]:  https://img.shields.io/coveralls/nvbn/thefuck.svg
[coverage-link]:   https://coveralls.io/github/nvbn/thefuck
[license-badge]:   https://img.shields.io/badge/license-MIT-007EC7.svg
[examples-link]:   https://raw.githubusercontent.com/nvbn/thefuck/master/example.gif
[instant-mode-gif-link]:   https://raw.githubusercontent.com/nvbn/thefuck/master/example_instant_mode.gif
[homebrew]:        https://brew.sh/

##### [返回目录](#contents) 