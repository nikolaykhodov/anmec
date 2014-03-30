#!/bin/bash
cd /home/anmec2/http
source ./.env/bin/activate
fab update:groups
