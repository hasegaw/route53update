#!/bin/bash

# FIXME: Update with your own parameters.
export AWS_ACCESS_KEY_ID="TBD"
export AWS_SECRET_ACCESS_KEY="TBD"

cd /home/hasegaw/route53update
/usr/local/bin/python3 ./route53update.py
