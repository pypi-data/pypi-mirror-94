#!/usr/bin/env bash

# Bundles a local CMSSW checkout into a tar archive that is suitable for
# unpacking on a machine with cvmfs.

# Arguments:
# 1. The path to the CMSSW checkout, i.e., the value of the CMSSW_BASE variable.
# 2. The path where the bundle should be stored, should be absolute and end with .tgz.
# 3. A regex for excluding files or directories in src, should start with (e.g.) ^src/. Optional.

action() {
    local cmssw_base="$1"
    if [ -z "$cmssw_base" ]; then
        2>&1 echo "please provide the path to the CMSSW checkout to bundle"
        return "1"
    fi

    if [ ! -d "$cmssw_base" ]; then
        2>&1 echo "the provided path '$cmssw_base' is not a directory or does not exist"
        return "2"
    fi

    local dst_path="$2"
    if [ -z "$dst_path" ]; then
        2>&1 echo "please provide the path where the bundle should be stored"
        return "3"
    fi

    # choose a default value the the exclusion regex that really should not match any path in src
    local exclude="${3:-???}"

    (
        cd "$cmssw_base" && \
        find src -maxdepth 3 -type d \
            | grep -e "^src/.*/.*/\(interface\|data\|python\)" \
            | grep -v -e "$exclude" \
            | tar -czf "$dst_path" --dereference lib biglib bin cfipython --exclude="*.pyc" --files-from -
    )
    local ret="$?"

    return "$ret"
}
action "$@"
