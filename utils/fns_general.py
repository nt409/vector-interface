from model.pars import DefaultParams, CustomParams


def get_kappa(p):
    mult = (p.alpha/p.sigma)
    inner_bracket = (1/p.om_m) - 1
    bracket = 1 + p.delta * inner_bracket
    out = p.zeta * (1 - mult * bracket)
    return out



def get_params(*params):
    default_or_custom = params[0]

    if default_or_custom=="def-NPT":
        return DefaultParams("NPT")

    elif default_or_custom=="def-PT":
        return DefaultParams("PT")

    elif default_or_custom=="def-C":
        trans_type = params[1]
        other_pars = params[2:]
        return CustomParams(trans_type, *other_pars)

    else:
        raise Exception("invalid transmission type entered")
