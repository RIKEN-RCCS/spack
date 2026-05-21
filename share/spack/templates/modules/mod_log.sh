#!/bin/bash

if [ -n "$PJM_JOBID" ]; then
    modname="$1"

    logdir="/vol0004/data/applog"
    day="$(date '+%Y%m%d')"
    fname="${PJM_JOBID}_${PJM_SUBJOBID:-0}"
    outfile="$logdir/$day/$fname/mod_$fname.csv"

    # Expected format:
    # package/version-compiler-compiler_version-hash
    #
    # Examples:
    # lammps/20240829.2-fj-4.12.0-2lpnpl4
    # py-pkgconfig/1.5.5-none-none-bpvgl67

    pkg="${modname%%/*}"
    rest="${modname#*/}"

    hash="${rest##*-}"
    rest="${rest%-*}"

    compiler_version="${rest##*-}"
    rest="${rest%-*}"

    compiler="${rest##*-}"
    version="${rest%-*}"

    # Convert "none" to empty fields
    [ "$compiler" = "none" ] && compiler=""
    [ "$compiler_version" = "none" ] && compiler_version=""

    mkdir -p -m 777 "$logdir/$day/$fname" || exit 0

    # if [ ! -f "$outfile" ]; then
    #     echo "package,version,compiler,compiler_version,hash" > "$outfile"
    # fi

    echo "${pkg},${version},${compiler},${compiler_version},${hash}" >> "$outfile"

    chmod 644 "$outfile" 2>/dev/null || true
fi
