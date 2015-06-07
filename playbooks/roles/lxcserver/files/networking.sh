#!/bin/bash

# ------------------------------------------------------
# Cambia la configuracion de las interfaces de red, para
# convertirlas en un agregado
# ------------------------------------------------------

# Parametros de configuracion

IPADDRESS=192.168.1.210
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNSSERVER1=192.168.1.200
DNSSERVER2=192.168.1.1

# Script - a partir de aqui no hace falta tocar.

cat > /etc/network/interfaces <<EOF
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# The loopback network interface
auto lo
iface lo inet loopback

# The primary and secondary network interfaces
auto eth0
iface eth0 inet manual
  bond-master bond0
  bond-primary eth0

auto eth1
iface eth1 inet manual
  bond-master bond0

# The bonding interface
auto bond0
iface bond0 inet manual
  bond-mode active-backup
  bond-miimon 100
  bond-slaves eth0 eth1

# the bridge interface
auto br0
iface br0 inet static
  bridge_ports bond0
  address $IPADDRESS
  netmask $NETMASK
  gateway $GATEWAY
  dns-nameservers $DNSSERVER1 $DNSSERVER2
  
EOF
