apt-get update
apt-get install -y bind9-host

head_node_ip=$(host $MASTER_ADDR | grep -oP 'has address \K[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -n 1)
echo $head_node_ip
