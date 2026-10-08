#!/bin/bash
# usage: sync.sh <variant>   -- fresh copy of the template into <variant>/src (out/ is removed too), then variant patch
V=$1
B=/c/Users/norom/Documents/latex/tmp/thesis-build/$V
rm -rf "$B/src" "$B/out"
mkdir -p "$B/src"
cp -r /c/Users/norom/Documents/latex/templates/thesis-modular/. "$B/src/"
if [ -f "/c/Users/norom/Documents/latex/tmp/thesis-build/patch-$V.sh" ]; then bash "/c/Users/norom/Documents/latex/tmp/thesis-build/patch-$V.sh" "$B/src"; fi
echo synced $V
