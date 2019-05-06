#!/usr/bin/env bash
rsync -avz /Users/samcrane/Documents/GitLab/Icarus/business-logic-server -e "ssh -i ../7305Key.pem" ubuntu@api.icarusmap.com:/home/ubuntu/ --exclude *.pyc --exclude venv/ --exclude dump.rdb --exclude secrets.json