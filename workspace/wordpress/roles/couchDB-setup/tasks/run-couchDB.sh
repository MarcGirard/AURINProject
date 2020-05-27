# Activate the proxy by editing the environment file
# Add these lines to the bottom of the environment file
sudo cat "HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/
HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/
http_proxy=http://wwwproxy.unimelb.edu.au:8000/
https_proxy=http://wwwproxy.unimelb.edu.au:8000/
no_proxy=localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.unimelb.edu.au,.cloud.unimelb.edu.au" > /etc/environment

# Activating Docker Daemon proxy by creating the service directory and the proxy config file
sudo mkdir /etc/systemd/system/docker.service.d
# Add these lines to the proxy config file file
sudo echo "[Service]
Environment="HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/"
Environment="HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/"
Environment="NO_PROXY=localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.unimelb.edu.au,.cloud.unimelb.edu.au"" > /etc/systemd/system/docker.service.d

# Restart the Docker Daemon and Docker service
sudo systemctl daemon-reload && sudo systemctl restart docker

# Mounting the attached volumes
sudo mkfs -t ext4 /dev/vdb
sudo mkdir /data
sudo mount /dev/vdb /data

#Add this line to the bottom of fstab
sudo cat "/dev/vdb /data auto defaults 0 0" > /etc/fstab

# Installation and usage of a CouchDB cluster

# The following instructions details how to setup a cluster of CouchDB databases on
# Docker containers hosted on seperate virtual machines, acting as independent nodes.
## Prerequirements
## Cluster setup
 
# Set node IP addresses, electing the first as "master node"
# and admin credentials (make sure you have no other Docker containers running):
# Node IP's are based on virtual machine IP's
export declare -a nodes=(172.26.134.6 172.26.133.171 172.26.133.101 172.26.133.114)

# Declare the first as the master node (simply for forming the cluster, it's not special)
export masternode=`echo ${nodes} | cut -f1 -d' '`

# Obtain the IP address of the current VM 
export node=`echo $(hostname -I) | cut -f1 -d' '`

export declare -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export size=${#nodes[@]}
export lastnode=${nodes[${size}-1]}
export user=admin
export pass=team52
export VERSION='3.0.0'
export cookie='a192aeb9904e6590849337933b000c99'
export uuid='a192aeb9904e6590849337933b001159'

sudo docker pull ibmcom/couchdb3:${VERSION}

# Create Docker container (stops and removes the current ones if existing):
if [ ! -z $(sudo docker ps --all --filter "name=couchdb${node}" --quiet) ] 
   then
        sudo docker stop $(sudo docker ps --all --filter "name=couchdb${node}" --quiet) 
        sudo docker rm $(sudo docker ps --all --filter "name=couchdb${node}" --quiet)
fi 

sudo docker create -p 4369:4369 -p 5984:5984 -p 9100-9200:9100-9200\
  --name couchdb${node}\
  --env COUCHDB_USER=${user}\
  --env COUCHDB_PASSWORD=${pass}\
  --env COUCHDB_SECRET=${cookie}\
  --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${node}\""\
  ibmcom/couchdb3:${VERSION}

# Start the containers (and wait a bit while they boot):

export cont=`echo $(sudo docker ps -aq)`
sudo docker start ${cont}


# Set up the CouchDB cluster:
# Use if statements so we only add the other nodes to the cluster, not the master node
if [[ " ${othernodes[@]} " =~ " ${node} " ]]; then
    echo "Adding current node to the cluster..."
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json"\
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
             \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"5984\",\
             \"remote_node\": \"${node}\", \"node_count\": \"$(echo ${nodes[@]} | wc -w)\",\
             \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
fi

if [[ " ${othernodes[@]} " =~ " ${node} " ]]; then
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup"\
      --header "Content-Type: application/json"\
      --data "{\"action\": \"add_node\", \"host\":\"${node}\",\
             \"port\": \"5984\", \"username\": \"${user}\", \"password\":\"${pass}\"}"
fi

# Finalize cluster setup after adding the last node to cluster
if [ ${node} == ${lastnode} ]; then
# This empty request is to avoid an error message when finishing the cluster setup 
    curl -XGET "http://${user}:${pass}@${masternode}:5984/"

    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup"\
        --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"
fi
```

# Check wether the cluster configuration is correct:
for node in "${nodes[@]}"; do  curl -X GET "http://${user}:${pass}@${node}:5984/_membership"; done

