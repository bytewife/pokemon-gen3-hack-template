#!/bin/bash

git submodule foreach "git fetch && git reset --hard origin/main"
