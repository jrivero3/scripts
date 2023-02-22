<?php
$contador_ip=10;
$randIP = mt_rand(0, 255) . "." . $contador_ip;
$hostname="Smart Things----------d0:52:a8:0067:5e----------Wired";
$hostname_replace=str_replace("----------", ";",$hostname);
$datoshost=explode(";", $hostname_replace);
// echo $datoshost[1];
echo "host" . $datoshost[0] . "{\n";
echo "\t #Asignacion estatica \n";
echo "\t hardware ethernet " . $datoshost[1] . "; #Direccion mac del host \n";
echo "\t fixed-address 192.168." . $randIP . "; #Ip a asignar al host \n";
echo "}";
?>



---------------------------------------------------------
PYTHON


contador_ip=10
hostname="Smart Things----------d0:52:a8:0067:5e----------Wired"
hostname_replace= hostname.replace("----------", ";")
datoshost=hostname_replace.split(";")
""" echo $datoshost[1]"""
print ("host" , datoshost[0] , "{")
print ("\t #Asignacion estatica ")
print ("\t hardware ethernet " , datoshost[1] , "; #Direccion mac del host ")
print ('\t fixed-address 192.168.100.%d' %contador_ip , "; #Ip a asignar al host ")
print ("}")