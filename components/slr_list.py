

slider_list = [
                # host
                dict(step=10, min=1, max=2000, value=1000, var='N', axis_label='N', name='N: number of plants (in absence of virus)'),
                dict(step=0.001, min=0.001, max=0.05, value=0.01, var='rho', axis_label=u'\u03C1', name=u'\u03C1: natural plant death rate'),
                dict(step=0.001, min=0.001, max=0.2, value=0.01, var='mu', axis_label=u'\u03BC', name=u'\u03BC: roguing rate/disease induced mortality'),
                # vector
                dict(step=0.01, min=0, max=0.6, value=0.12, var='alpha', axis_label=u'\u03B1', name=u'\u03B1: vector death due to flights'),
                
                dict(step=0.01, min=0, max=8, value=4, var='tau-NPT', axis_label=u'\u03C4', name=u'\u03C4: vectors losing infectivity'),
                dict(step=0.01, min=0, max=8, value=0.05, var='tau-PT', axis_label=u'\u03C4', name=u'\u03C4: vectors losing infectivity'),

                dict(step=0.01, min=0.000001, max=0.4, value=0.18, var='sigma', axis_label=u'\u03C3', name=u'\u03C3: per capita vector birth rate (at low density)'),
                
                dict(step=0.1, min=1, max=2400, value=1977.6, var='zeta-NPT', axis_label=u'\u03B6', name=u'\u03B6: vector population density dependent threshold'),
                dict(step=0.1, min=1, max=2400, value=163.2, var='zeta-PT', axis_label=u'\u03B6', name=u'\u03B6: vector population density dependent threshold'),

                dict(step=0.01, min=0.01, max=4, value=2, var='Gamma', axis_label=u'\u0393', name=u'\u0393: average time feeding per settled landing'),
                dict(step=0.01, min=0, max=1, value=0, var='delta', axis_label=u'\u03B4', name=u'\u03B4: increase in death rate as more plants visited per feed'),
                dict(step=0.01, min=0, max=3, value=1, var='beta', axis_label=u'\u03B2', name=u'\u03B2: change in birth rate on infected plants'),
                # pref
                dict(step=0.01, min=0.001, max=4, value=1, var='nu_m', axis_label=u'\u03BD\u208B', name=u'\u03BD\u208B: bias of non-viruliferous vectors to land on infected plants'),
                dict(step=0.01, min=0.001, max=4, value=1, var='nu_p', axis_label=u'\u03BD\u208A', name=u'\u03BD\u208A: bias of viruliferous vectors to land on infected plants'),
                dict(step=0.01, min=0.001, max=1, value=0.5, var='om_m', axis_label=u'\u03C9\u208B', name=u'\u03C9\u208B: probability non-viruliferous vector settles to feed on susceptible plant'),
                dict(step=0.01, min=0.001, max=1, value=0.5, var='om_p', axis_label=u'\u03C9\u208A', name=u'\u03C9\u208A: probability viruliferous vector settles to feed on susceptible plant'),
                dict(step=0.01, min=0.001, max=2, value=1, var='eps_m', axis_label=u'\u03B5\u208B', name=u'\u03B5\u208B: bias of non-viruliferous vector to feed on infected plants'),
                dict(step=0.01, min=0.001, max=2, value=1, var='eps_p', axis_label=u'\u03B5\u208A', name=u'\u03B5\u208A: bias of viruliferous vector to feed on infected plants'),
                #
                dict(step=0.01, min=0.001, max=4, value=1, var='nu', axis_label=u'\u03BD', name=u'\u03BD: bias of vectors to land on infected plants'),
                dict(step=0.01, min=0.001, max=1, value=0.5, var='om', axis_label=u'\u03C9', name=u'\u03C9: probability vector settles to feed on susceptible plant'),
                dict(step=0.01, min=0.001, max=2, value=1, var='eps', axis_label=u'\u03B5', name=u'\u03B5: bias of vectors to feed on infected plants'),
                # init conds
                dict(step=0.01, min=0, max=1, value=0.02, var='host-inc-0', axis_label=u'I\u2080/(S\u2080+I\u2080)', name=u'I\u2080/(S\u2080+I\u2080): initial host incidence'),
                dict(step=0.01, min=0.01, max=1, value=1, var='N-frac', axis_label="IHA", name=u'(S\u2080+I\u2080)/N: initial host amount'),
                dict(step=0.01, min=0, max=1, value=0.02, var='vec-inc-0', axis_label=u'Z\u2080/(X\u2080+Z\u2080)', name=u'Z\u2080/(X\u2080+Z\u2080): initial vector incidence'),
                dict(step=0.01, min=0.01, max=1, value=1, var='kapp-frac', axis_label="IVA", name=u'(X\u2080+Z\u2080)/\u03BA: initial vector amount'),
                ]


SLIDER_IND_MAP = {}
for ii in range(len(slider_list)):    
    SLIDER_IND_MAP[slider_list[ii]['var']] = ii
