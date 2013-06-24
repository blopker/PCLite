#!/usr/bin/env bash
PKG="PCLite"
DIR="/home/ninj0x/.config/sublime-text-3/Packages"
# zip -r $PKG *
rm -fr "$DIR"/$PKG
sleep 2
cp -r ../$PKG "$DIR"
