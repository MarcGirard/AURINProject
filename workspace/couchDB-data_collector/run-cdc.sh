#!/bin/bash

# University of Melbourne
# COMP90024 - Team52
# Name of contributors and student id:
# * Edward Formainir: 1073708
# * Niloy Sarkar: 991245
# * Marc Girard: 1155873
# * Runqi Zhu: 793024

. ./openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=~/.ssh/id_rsa wordpress.yaml