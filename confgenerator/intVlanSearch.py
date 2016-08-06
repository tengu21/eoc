from ciscoconfparse import CiscoConfParse

device_name = "can1paswoff05"
vlan_new = "61"

vlan_old = "12"
prt_old = "2"
#prt_new = "60"

conf_file = device_name + ".conf"
conf_new = device_name + "_new.conf"

cisco_cfg = CiscoConfParse(conf_file)
data_vlan = cisco_cfg.find_objects_w_child(parentspec=r"^interface", childspec=r"switchport access vlan " + vlan_old)
data_trunk = cisco_cfg.find_objects_w_child(parentspec=r"^interface Port-channel", childspec=r"switchport trunk")
#prt_vlan = cisco_cfg.find_objects_w_child(parentspec=r"^interface", childspec=r"switchport access vlan " + prt_old)

newconf = open(conf_new, 'a')

newconf.write("term mon\n")
newconf.write("conf t\n")
newconf.write(("vlan ") + vlan_new + ("\n"))
#newconf.write(" name v00_wks\n")
newconf.write(" name v00_sec\n")
#newconf.write(("vlan ") + prt_new + ("\n"))
#newconf.write(" name v00_prt\n")

for my_trunk in data_trunk:
 newconf.write(my_trunk.text)
 newconf.write("\n")
 newconf.write((" switchport trunk allow vlan remove ") + vlan_old + ("\n"))
 #newconf.write((" switchport trunk allow vlan add ") + vlan_new + (",") + prt_new + ("\n"))
 newconf.write((" switchport trunk allow vlan add ") + vlan_new + ("\n"))

for my_int in data_vlan:
 newconf.write(my_int.text)
 newconf.write("\n")
 newconf.write(" shut\n")
 newconf.write((" switchport access vlan ") + vlan_new + ("\n"))
 newconf.write((" authentication event server dead action authorize vlan ") + vlan_new + ("\n"))
 newconf.write(" no shut\n")

#for my_prt in prt_vlan:
# newconf.write(my_prt.text)
# newconf.write("\n")
# newconf.write(" shut\n")
# newconf.write((" switchport access vlan ") + prt_new + ("\n"))
# newconf.write((" authentication event server dead action authorize vlan ") + prt_new + ("\n"))
# newconf.write(" no shut\n")

newconf.write("end\n")
newconf.write("wr\n")

newconf.close()