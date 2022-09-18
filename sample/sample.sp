*PDK Library
.LIB "./../sky130_model/sky130.spice" tt

**************************************************************************************
* Hspice Options
* Accuracy Control

.option	method=gear accurate=1 runlvl=6 gmin=1e-21 gmindc=1e-21 
.option absmos=1e-12 relmos=1e-4 relv=1e-4 relvdc=1e-4
.option	ingold=2 $ ingold=0: Engineering Format, ingold=2: E-Format
.option measdgt=7 numdgt=7 mcbrief=1 nopage nomod 
.option post

*=======================================================================================
* PARAMETERS, POWER SUPPLIES

.PARAM
+      vdd = 1.8
+      len = 150n
+      wid_p = 900n
+      wid_n = 360n
+      size  = 1

*Simulation parameter sweeps
.INCLUDE ./sample.param

*=======================================================================================
* CIRCUITS

.subckt inv in out vdd vss scale=1
Xm1 out in vss vss NMOS_VTG L='len' W='wid_n*scale'
Xm0 out in vdd vdd PMOS_VTG L='len' W='wid_p*scale'
.ends

Xinv in out vdd vss inv scale = size
c1 out vss 1f

*=======================================================================================
* Initial Conditions

.IC
+    V(in)=0
*=======================================================================================
*Controls

v1 vss 0 DC=0
v0 vdd 0 DC='vdd'
v2 in 0 PWL 0 0 200p 0 220p 1.8 1.22n 1.8 1.24n 0

*=======================================================================================
*Analysis

.TEMP 25.0
.TRAN 1e-12 2e-9 
+SWEEP DATA=params

.PROBE TRAN
+    V(out)
+    V(in)

.OP
.measure TRAN delay TRIG V(in) VAL=0.9 RISE=1 TARG V(out) VAL=0.9 FALL=1
*=======================================================================================
* Use Alter command to simulate other cases
* I find the Alter commands to be cumbersome to use.
* They also make a bunch of files that I don't find useful
*.alter
*.PARAM len='300n'

*.alter
*.PARAM wid_n='720n'

*.alter
*.PARAM wid_p='1800n'

.END

