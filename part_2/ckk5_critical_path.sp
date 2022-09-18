*PDK Library
.LIB "./../sky130_model/sky130.spice" tt

*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*
* Hspice Options. Copied from the provided sample file

.option method=gear accurate=1 runlvl=6 gmin=1e-21 gmindc=1e-21
.option absmos=1e-12 relmos=1e-4 relv=1e-4 relvdc=1e-4
.option ingold=2 $ ingold=0: Engineering Format, ingold=2: E-Format
.option measdgt=7 numdgt=7 mcbrief=1 nopage nomod
.option post

*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*
* Parameters, Power Supplies

.PARAM
+	vdd = 1.8
*Mosfet sizing information
+	len = 150n
+	wid_p = 900n
+	wid_n = 360n
*Capacitance information
+	C_unit = 1f
+	C_output = 50f
*Stage scale information
+	size_stage_1 = 2
+	size_stage_2 = 3
+	size_stage_3 = 4

*Simulation sweep parameter
.INCLUDE ./sweep_params.sp

*Definition of the unit inverter
.INCLUDE ./inverter.sp

*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*
*CIRCUITS

*Input inverter
Xinput in In_0 vdd vss inv

*Input amplifier inverters
XIn_0 In_0 In_1 vdd vss inv size ='size_stage_1'	

XIn_1 In_1 In_2 vdd vss inv size ='size_stage_2'

XIn_2 In_2 output vdd vss inv size ='size_stage_3'

*Put these in an external file to reduce clutter in this one.
.INCLUDE ./output_load.sp

*Output loading capacitor
Coutput output vss C_output

*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*
* Initial Conditions

.IC
+	V(in)=0
*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*
*Controls

v1 vss 0 DC = 0
v0 vdd 0 DC='vdd'
v2 in 0 PWL 0 0 200p 0 220p 1.8 1.22n 1.8 1.24n 0

*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*
*ANalysis

.TEMP 25.0
.TRAN 1e-12 2e-9
+SWEEP DATA=sweep_params

.PROBE TRAN
+	V(output)
+	V(in)

.OP
.measure TRAN delay TRIG V(in) VAL=0.9 RISE=1 TARG V(output) VAL=0.9 FALL=1

