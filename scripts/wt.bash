#!/bin/bash
#
# Kevin Murphy
# 10/3/19
# wt bash completion function.
# https://github.com/keggsmurph21/wt
#
# Source this file in your .bashrc or .bash_profile to use it.
# NOTE: either set __PATH_TO_WT manually or run scripts/install

__PATH_TO_WT="/home/kevinmurphy/src/keggsmurph21/wt/scripts/.."

wt() {
    pushd $__PATH_TO_WT >/dev/null
    dest=$(python3 -m wt $@)
    if [ $? -eq 0 ]; then
        cd "$dest"
    else
        popd >/dev/null
    fi
}

__wt_complete() {
    # adapted from https://www.endpoint.com/blog/2016/06/03/adding-bash-completion-to-python-script
    local curr prev cmds wts opts
    COMPREPLY=()
    curr="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    cmds="list use add"
    worktrees="$(git worktree list --porcelain 2>/dev/null \
        | awk 'NR % 4 == 3' \
        | sed -E 's,.*refs/heads/,,')"

    case "$prev" in
        wt)     opts="$cmds" ;;
        use)    opts="$worktrees" ;;
        add)    opts="" ;;
        list)   opts="" ;;
        *)      opts="" ;;
    esac

    COMPREPLY=( $(compgen -W "$opts" -- $curr) )
}

complete -F __wt_complete wt

