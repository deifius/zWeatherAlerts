#!/bin/bash

pip3 list --outdated| cut -d ' ' -f1|xargs -n1 sudo pip3 install -U
