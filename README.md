# COMP90024: City Analytics on the Cloud - Team52 - AURINProject

Name of contributors and student id:
* Edward Formainir: 1073708
* Niloy Sarkar: 991245
* Marc Girard: 1155873
* Runqi Zhu: 793024

Supervised by Prof. Richard Sinnott, Professor Applied Science & Director, E-Research at the University of Melbourne

## Requirements

* Ansible 2.9.x (https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
* Docker 19.03.x (https://docs.docker.com/install/)
* Docker-Compose 1.25.x (https://docs.docker.com/compose/install)
* About 2GB of RAM available for this deployment
* Node 12.10.x (https://nodejs.org/en/blog/release/v12.11.0/)
* NPM 6.10.x (Installed along Node.js)
* Grunt CLI 1.2.x (https://gruntjs.com/installing-grunt)
* jq 1.5.x (https://stedolan.github.io/jq/download/)
* a Linux-based shell (tested it with Ubuntu, scripts are provided to have it run on MacOS, which has some know limitations when it comes to MacOS https://docs.docker.com/docker-for-mac/networking/)

## System setup

* To launch ansible scripts

```shell script
cd workspace/nectar/
./run-nectar.sh
cd workspace/couchDB-data_collector/
./run-cdc.sh
```

* To run the webapp and visualize the data:

```shell script
cd workspace/steam/
export dbname='aussteamids'
grunt couch-compile
grunt couch-push
```

(The ansible playbooks and the python scripts wont begin without a password which can be found in the report).

## Source data from AURIN and data collectors
All the data can be available via https://drive.google.com/drive/folders/1EWHV1Bvgk1D3V4YqxtmwuWQGdjufm-ER?usp=sharing.
