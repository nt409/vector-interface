






## Nik comments

<!-- 1 - done -->
2 - done... but not very convincingly
3 - depends on case - which one was unconvincing?
<!-- 4 - done -->
5 - not easily
<!-- 6 - done -->

<!-- 1/ on the parameter scan, could you make the %age of the baseline that is the top and bottom of the x-axis. -->

2/ make the graphs not have gaps

3/ check stability of I = 0 eqm; shouldn’t there be dark green on lhs of axis for the graph from 2/?

5/ For the parameter scan, when it is calculating, could a progress bar be added?

<!-- 6/ At various places the maths symbols are given poorly typeset names, e.g. equilibrium box at bottom of Model tab; eps_m as graph label for parameter scan -->




## error handling
# Parameter restrictions

Must be greater than 0:
    N
    rho
    mu
    sigma
    zeta
    Gamma
    nu_i
    omega_i
    eps_i

Can equal 0:
    alpha
    delta
    beta
    tau

Also need:
    omega_i * eps_i >= 1
    tau and alpha both 0 (I think, get ODE solver error o.w.)

Somewhere it says that nu_- and nu_+ can differ in the PT case. Does this mean they can't differ in the NPT case?

Do you have sensible upper bounds for:
    rho
    zeta
    N
    tau
    alpha







## mobile figs

hidden/shown via CSS
mobile: no ylabel, y axis non scrollable, y in plotly fig title




## style

mob kitchen style?

grey out PS slider of one chosen? or make invisible?

