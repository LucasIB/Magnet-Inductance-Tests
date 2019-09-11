# Magnet-Inductance-Tests
Describe the behavior of the inductance of the magnet under test as a function of the current steps applied to the coils.


#### Model: FC-001 - Correction function: FC1
@author: lucas.balthazar
> - **Magnet under test:** Fast Corrector - FC-001 - CV & CH Coil;
>
> - **Power Supply:** CAENels FAST-PS 1020;
> - **Goal:** Measure the possible inductance variation as a function of the applied current.
> - **Procedure:** The input current in the coils is varied in continuous steps from 0.1 A amplitude to a maximum nominal setting according to magnetic field requirements. With the oscilloscope, we measure the variation of current and voltage in the coils,
calculate the resistance through the relation between voltage and current over time, it is possible to determine the time constant of the RL circuit and this way, calculate the inductance of the coil.
    
More graphics in `plotly.com` in [plot.ly/~LucasIB](http://chart-studio.plot.ly/organize/LucasIB:home#/)
