
evpy is a pyhton library used to predict efficiency in electric power trains given high level component specifications. It can be used to predict motor performance, a motors torque/speed/efficeiency contour, motor size given aspect ratio and torque, losses in an ESC given motor performance, ESC size, a batteryâ€™s voltage given time under a load, and battery mass given duration and specific energy.

Documentation:
evpy Functions
evpy.batt_pred(I_load, t_hr, Q_Ah, R_int, n_ser=1, n_prll=1, pkrt=1.2)
predict voltage at a given time under a given load

predict the entire pack’s instantaneous terminal voltage under load uses empirical state-of-charge curve fit obtained from Chen and Mora https://doi.org/10.1109/TEC.2006.874229

INPUTS:

I_loadfloat, Amps
the current draw at the battery terminals

tfloat, hours
the instant in time

Q_Ahfloat, Amp*hr
the rated capacity of the battery unit

R_intfloat, Ohms
the internal resistance of the battery unit in the tens of mili-Ohms range

n_serint, non-dim (optional)
the number of battery units in series

n_prllint, non-dim (optional)
the number of battery units in parallel

pkrtfloat, non-dim (optional)
the Peukert constant of the battery

OUTPUTS:

V_termfloat, Volts
the output voltage of the battery

dodfloat, non-dim
the depth of discharge of the battery (percent depleted)

socfloat, non-dim
the state of charge of the battery (percent remaining)

SPECIAL NOTES:

1.— The applied current (I_load) and the time (t) can be vectors (ndarrays) to calculate the entire discharge curve of the battery. However, BOTH inputs must be vectors of the same length!

2.— Ensure that the inputs have the correct units! Hobby batteries are rated in mili-Amp*hr This code requires you to enter the capacity in Amp*hr

3.— Battery terminology is imprecise. A “pack” and “module” may mean different things to different people.

For example, the Thunder Power TP7700-6SR70 is a 7.7 Ah (Amp*hr) unit which consists of 6 cells in series. To model this battery unit, input 7.7 for Q_Ah and set n_ser = 6 If you had 4 of these units wired in series, set n_ser = 4*6 If you had 4 of these units wired in parallel, set n_prll = 4

4.— Normally, you should not deplete a lithium-ion battery below 3.5 V In extreme circumstances, you can delpete a li-ion battery down to 3.3 V NEVER deplete a battery below 3 V

evpy.batt_size(t_hr, e, rho=2037.0)
predict battery mass, size for a given duration, specific energy

INPUTS:

tfloat, hours
time duration of mission or mission phase

efloat, Wh/kg
specific energy (energy/mass) of mission or mission phase

rhofloat, kg/m^3 (optional)
the mass density (mass/volume) of a lipo battery

OUTPUTS:

mfloat, kg
mass of required battery pack

Ufloat, m^3
volume of required battery pack

SPECIAL NOTES:

mass density (mass/volume) of typical lipo is ~2000 kg/m^3 or 2 g/cm^3

reasonable usable energy densities:
200 Wh/kg for an extremely well-optimized low-current application 170 Wh/kg for a low-current (fixed-wing) application 140 Wh/kg for a high-current (VTOL) application

evpy.esc_pred(Im, Pm, V, d, f_pwm=8000.0, Ron=0.01, Ton=1e-06)
predict ESC losses given specs and motor performance

INPUTS:

Imndarray (float), Amps
the current pulled by the motor

Pmndarray (float), Watts
the power pulled by the motor

Vfloat, Volts
the input (DC) voltage to the ESC

dfloat, non-dim
the non-dimensional throttle setting (duty ratio)

f_pwmfloat, Hertz
the switching frequency of the ESC, about 8-32 kHz

Ronfloat, Ohms
the R_ds_ON measure of the MOSFETs in the ESC, about 5-20 mOhms

Tonfloat, s (seconds)
the transition period of the MOSFETs, about 1 microsecond

OUTPUTS:

I_dcndarray (float), Amps
the current draw of the ESC

P_dcndarray (float), Watts
the power draw of the ESC

nndarray (float), non-dim
the efficiency of the ESC

evpy.esc_size(P_req, sf=2.0)
predict esc size, mass given cont. power

predict the esc volume and mass using a purely empirical fit empirical data collected from 3 KDE, Castle, and HobbyWing data nearly uniform trends among all three datasets

P = 36.203m where [P] = Watts, [m] = grams P = 52.280U where [P] = Watts, [U] = cm^3

INPUTS:

P_reqfloat, Watts
the required continuous power output of the ESC

sffloat, non-dim (optional)
a safety factor for the prediction hobby rule of thumb is 2.0

OUTPUTS:

mfloat, kg
the mass of the ESC

Ufloat, m^3
the volume of the ESC

evpy.motor_contour(N_rated, T_rated, kt, R, I0, num_pts=100)
roughly predict the motor’s torque/speed/efficiency contour

predicts motor efficiency within the motor’s rated operating window uses 3 high-level component parameters (Rm, kt, I0) applicable to sensorless, six-step commutation brushless DC motors DOES NOT factor in harmonics!

Note: kt = kv with SI units

INPUTS:

N_ratedfloat, rev/min
rated motor speed

T_ratedfloat, N.m
rated motor torque

ktfloat, Newton-meter per Amp
torque constant of motor

Rmfloat, Ohms
motor resistance (phase to phase)

I0float, Amps
no-load current of motor

num_ptsint, non-dim
number of data points along each axis

OUTPUTS:

N2D ndarray (float), rev/min
a 2D array of the motor’s speed up to N_rated

T2D ndarray (float), Newton-meter
a 2D array of the motor’s torque up to T_rated

n2D ndarray (float), non-dim
a 2D array of the motor’s non-dimensional motor efficiency grid is over the entire torque/speed window

evpy.motor_pred(w, V, d, kt, Rm, I0)
predict motor performance for given specs

predict torque, power, current, and efficiency over a range of speed uses 3 high-level component parameters (Rm, kt, I0) and throttle applicable to sensorless, six-step commutation brushless DC motors

Note: kt = kv with SI units

INPUTS:

wndarray (float), rads/sec
range of motor speed

Vfloat, Volts
voltage of the DC bus

dfloat, non-dim
non-dimensional throttle setting (duty ratio)

Rmfloat, Ohms
motor resistance (phase to phase)

ktfloat, Newton-meter per Amp
torque constant of motor

I0float, Amps
no-load current of motor

OUTPUTS:

Tndarray (float), Newton-meter
output torque of motor

P_outndarray (float), Watts
output power (mechanical)

Indarray (float), Amps
input current to motor

P_inndarray (float), Watts
input power (AC)

nndarray (float), non-dim
non-dimensional motor efficiency

evpy.motor_size(T, x, shear=5500.0)
Size a motor for a given torque, aspect ratio

Predict mass, diameter, length, figure of merit for given torque, D/L Default shear stress is for sub-500 gram BLDC motors

INPUTS:

Tfloat, N.m
continuous torque required of motor

xfloat, non-dim
stator aspect ratio (D/L)

shearfloat, Pa (N/m^2) - OPTIONAL
shear stress used to size the initial volume default value of 5.5 kPa is a conservative est.

OUTPUTS:

m_totfloat, kg
total mass of the motor

U_totfloat, m^3
total volume of the motor

Dofloat, m
outer motor diameter

Lofloat, m
outer motor length

kmfloat, N.m/sqrt(Ohms)
figure of merit (motor constant) of the motor