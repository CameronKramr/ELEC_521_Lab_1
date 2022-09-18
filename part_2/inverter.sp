.subckt inv in out vdd vss size =1 
Xm1 out in vss vss NMOS_VTG L='len' W='wid_n*size'
Xm0 out in vdd vdd PMOS_VTG L='len' W='wid_p*size'
.ends
