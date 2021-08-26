import numpy as np
import pandas as pd

from utils.fns_general import get_kappa, get_params

from model.eqm_fns import RootAnalyser, StabilityMatrix


def get_var_name_for_scan(def_or_custom, cust_choice, NPT_var, PT_var):
    if def_or_custom=="def-NPT":
        return NPT_var
    elif def_or_custom=="def-PT":
        return PT_var
    elif def_or_custom=="def-C":
        if cust_choice=="NPT":
            return NPT_var
        elif cust_choice=="PT":
            return PT_var
        else:
            raise Exception("invalid custom transmission type")
    else:
        raise Exception("invalid default vs custom choice")


def get_ps_var_info(slider_list, var):

    df = pd.DataFrame(slider_list)
    filtered = df[df["var"]==var]

    xmin = list(filtered["min"])[0]
    xmax = list(filtered["max"])[0]
    xlab = list(filtered["axis_label"])[0]
    
    xval = list(filtered["value"])[0]

    if xval>0:
        high = 100*xmax/xval
        low = 100*xmin/xval
    else:
        high = "NA"
        low = "NA"

    out = dict(min=xmin, max=xmax, value=xval, lab=xlab, high=high, low=low)

    return out







class ParScanData:
    def __init__(self, x_info, *all_params) -> None:
        
        self.var = all_params[-1]

        self.pars_use = all_params[:-1]

        self.n_points = 501

        self.x_info = x_info

        traces = self.get_ps_data()

        self.traces = self.ensure_real(traces)



    def get_ps_data(self):

        traces = []

        traces += self.get_traces_dis_free_vec()
        
        traces += self.get_traces_dis_free_no_vec()

        # reorder traces
        traces = [traces[1], traces[3], traces[0], traces[2]]

        traces += self.get_traces_non_0()

        traces += self.get_baseline_trc()
        
        return traces


    def get_traces_dis_free_vec(self):
        dis_free = self.get_dis_free_df_with_vec()
        trcs_v = ZeroIncTraces(dis_free, "present").traces

        return trcs_v
    
    def get_traces_dis_free_no_vec(self):
        dis_free_no_vec = self.get_dis_free_df_no_vec()
        trcs_nv = ZeroIncTraces(dis_free_no_vec, "dies out").traces

        return trcs_nv


    def get_traces_non_0(self):
        df_non_0 = self.get_ps_equilibria_df()
        n0_df_nN = df_non_0[~df_non_0["stab"].isin([None])]
        
        trcs = PositiveIncidenceTraces(n0_df_nN).traces
    
        trcs = ConnectedPosToZeroTraces(trcs).traces

        if len(trcs)==2:
            trcs = ConnectedPosIncTraces(trcs).traces

        return trcs

    
    def get_baseline_trc(self):
        return [dict(x=[self.x_info['value']],
                    y=[0],
                    marker=dict(color="red", size=12),
                    showlegend=True,
                    name="Baseline value",
                    mode="markers")]



    # normal eqms
    def get_ps_equilibria_df(self):
        p = get_params(*self.pars_use)

        xs = []
        host_out = []
        stabs = []
        
        for x in np.linspace(self.x_info["min"], self.x_info["max"], self.n_points):
            p = self.update_params(p, x)

            try:
                hh, stab = self.get_terminal_incidence_and_stab(p)
                host_out += hh
                xs += [x]*len(stab)
                stabs += stab

            except Exception as e:
                print("get_ps_equilibria_df error", e)

                xs += [x]
                host_out += [None]
                stabs += [None]

        out = pd.DataFrame(dict(x=xs,
                                host=host_out,
                                stab=stabs))
        return out


    def get_terminal_incidence_and_stab(self, p):
        df = self.get_eqm_vals(p)
        
        S_list = list(df.S)
        I_list = list(df.I)
        
        host_term_inc = [I_list[ii]/(S_list[ii] + I_list[ii])
                        for ii in range(len(S_list))]

        stability = list(df.is_stable)

        return host_term_inc, stability

    
    def get_eqm_vals(self, p):
        
        rta = RootAnalyser(p)
        
        df = rta.df

        df = df[df['bio_realistic']]

        return df

    # end of normal eqms



    # dis free eqms
    def get_dis_free_df_with_vec(self):
        p = get_params(*self.pars_use)

        xs = []
        zero_inc = []
        stabs = []

        for x in np.linspace(self.x_info["min"], self.x_info["max"], self.n_points):
            p = self.update_params(p, x)
            
            kappa = get_kappa(p)

            dis_free_eqm = [p.N, 0, kappa, 0]
            stab = StabilityMatrix(p, dis_free_eqm).is_stable
            
            xs.append(x)
            zero_inc.append(0)
            stabs.append(stab)

        return pd.DataFrame(dict(x=xs, 
                        host=zero_inc,
                        stab=stabs))
    

    def get_dis_free_df_no_vec(self):
        p = get_params(*self.pars_use)

        xs = []
        zero_inc = []
        stabs = []

        for x in np.linspace(self.x_info["min"], self.x_info["max"], self.n_points):
            p = self.update_params(p, x)
            
            dis_free_eqm = [p.N, 0, 0, 0]
            stab = StabilityMatrix(p, dis_free_eqm).is_stable
            
            xs.append(x)
            zero_inc.append(0)
            stabs.append(stab)

        return pd.DataFrame(dict(x=xs, 
                        host=zero_inc,
                        stab=stabs))



    def update_params(self, p, x):

        # the following variables have side effects:
        # - om_p if PT
        # - eps_m
        # - om_m
        
        # special cases:
        # - zeta/tau - two inputs, pick appropriate one
        # - nu - update nu_m and nu_p

        var_to_update = self.var
        
        if var_to_update=="om":
            # double update
            p.update_eta_om_m_eps_m(x, p.eps_m)
            p.update_om_p(x)
        
        elif var_to_update=="eps":
            # double update
            p.update_eta_om_m_eps_m(p.om_m, x)
            setattr(p, f"eps_p", x)
        
        elif var_to_update=="nu":
            # double update
            setattr(p, "nu_m", x)
            setattr(p, "nu_p", x)
        
        elif var_to_update=="eps_m":
            p.update_eta_om_m_eps_m(p.om_m, x)

        elif var_to_update=="om_m":
            p.update_eta_om_m_eps_m(x, p.eps_m)

        elif var_to_update=="om_p":
            p.update_om_p(x)

        elif "tau" in var_to_update:
            # so if var_to_update is tau, tau-NPT or tau-PT
            setattr(p, "tau", x)
        
        elif "zeta" in var_to_update:
            # so if var_to_update is zeta, zeta-NPT or zeta-PT
            setattr(p, "zeta", x)
        
        else:
            setattr(p, var_to_update, x)

        return p




    def ensure_real(self, data):
        out = []
        for trc in data:            
            trc['x'] = self.get_real_version(list(trc['x']))
            trc['y'] = self.get_real_version(list(trc['y']))
            out.append(trc)

        return out


    @staticmethod
    def get_real_version(list_):
        if any(np.iscomplex(list_)):
            raise Exception(f"List should not be complex {list_}")
        else:
            list_ = np.asarray(list_)
            return list_.real
















class ZeroIncTraces:
    def __init__(self, df, vector_state) -> None:
        self.df = df
        self.vector_state = vector_state
        self.traces = self.get_traces()

    def get_traces(self):
        trcs = []
        for stab in [True, False]:
            trc = self.get_output(stab)
            trcs.append(trc)
        
        return trcs


    def get_output(self, stable):
        df = self.df
        vec_state = self.vector_state

        filt = df[df["stab"].isin([stable])]

        name = "Stable" if stable is True else "Unstable" 
        name = name + f" (vect. {vec_state})"
        
        clr = "rgb(151,251,151)" if stable is not True else "rgb(0,89,0)"
        dsh = "dash" if vec_state=="present" else "dot"

        return dict(x=filt['x'],
                    y=filt['host'], 
                    name=name, 
                    line=dict(color=clr, width=3, dash=dsh),
                    showlegend=True,
                    mode="lines")




class PositiveIncidenceTraces:
    """
    Get traces for those equilibria which have positive incidence.

    Expect there to be up to 4 for any particular x, some stable some unstable.
    """
    def __init__(self, df) -> None:
        self.df = df
        self.traces = self.get_traces()
        


    def get_traces(self):
        df = self.df

        df = df.sort_values(by=["x", "stab", "host"])

        df_s = self.get_df(df, True)
        df_u = self.get_df(df, False)

        df_u_list = self.split_if_gaps(df_u)
        df_s_list = self.split_if_gaps(df_s)

        trcs = []

        for df_un in df_u_list:
            if df_un is not None:
                trcs += self.get_traces_from_df(df_un)

        for df_st in df_s_list:
            if df_st is not None:
                trcs += self.get_traces_from_df(df_st)

        traces = self.modify_showlegends(trcs)

        return traces




    @staticmethod
    def get_df(df_in, stab):
        df_in = df_in[df_in.stab.isin([stab])]

        if not df_in.shape[0]:
            return None

        host_vec = np.array(df_in['host'])
        if any(np.iscomplex(host_vec)):
            return None
        
        df_in['host'] = host_vec.real

        df_in['rank'] = df_in.groupby(by=["stab", "x"]).rank()

        df_in['diffs'] = [0] + [df_in.index[ii+1] - df_in.index[ii] for ii in range(len(df_in.index)-1)]

        return df_in



    @staticmethod
    def split_if_gaps(df_in):
        """
        If there is a gap in the df, split into separate traces.

        Otherwise plotly will join them up even when they shouldn't be.
        """
        
        if df_in is None:
            return [None]

        gap_inds = df_in.loc[df_in.diffs>4].index

        gap_inds = [0] + list(gap_inds) + [max(list(df_in.index))]

        if len(gap_inds)<=1:
            return [df_in]
        
    
        out = []

        for ii in range(len(gap_inds)-1):
            try:
                df_add = df_in.loc[gap_inds[ii]:gap_inds[ii+1], :]
                df_add = df_add.iloc[:-1]

                out.append(df_add)
            except Exception as e:
                print(f"Split dfs at gaps error: {e}")
            
        return out





    def get_traces_from_df(self, df_in):
        out = []

        for ii in df_in['rank'].unique():
            df_use = df_in[df_in['rank']==ii]
            trc = self.get_trace_from_df(df_use)
            
            if trc is not None:
                out.append(trc)

        return out



    @staticmethod
    def modify_showlegends(trcs):
        stab_count=0
        unstab_count=0

        for trc in trcs:
            if trc['name']=="Stable":
                stab_count += 1
                if stab_count>1:
                    trc['showlegend'] = False
            
            if trc['name']=="Unstable":
                unstab_count += 1
                if unstab_count>1:
                    trc['showlegend'] = False
        
        return trcs
    

    @staticmethod
    def get_trace_from_df(df):

        if df.shape[0]:
            stable = list(df['stab'])[0]
            
            name = "Stable" if stable is True else "Unstable"
            clr = "rgb(151,251,151)" if stable is not True else "rgb(0,89,0)"
            
            trc = dict(x=list(df['x']),
                    y=list(df['host']),
                    name=name,
                    showlegend=True,
                    line=dict(color=clr, width=3, dash="solid"),
                    mode="lines",
                    )
            
            return trc
        else: 
            return None









class ConnectedPosIncTraces:
    """
    Connect up the stable and unstable positive incidence traces
    which should be joined.
    """
    def __init__(self, traces) -> None:
        self.traces = self.get_traces_without_gaps(traces)
        
    
    
    def get_traces_without_gaps(self, trcs):
        trcs_m = self.connect_ends(trcs, "max")
        joined_traces = self.connect_ends(trcs_m, "min")
        return joined_traces
        
    
    def connect_ends(self, trcs, min_or_max):
        x_ms = []

        for trc in trcs:
            if min_or_max=="max":
                x_ms.append(max(trc['x']))
            elif min_or_max=="min":
                x_ms.append(min(trc['x']))
        
        x_ms = np.array(x_ms)
        unq_xm = np.unique(x_ms)

        trcs = self.join_at_end(trcs, unq_xm, x_ms, min_or_max)
        return trcs


    def join_at_end(self, trcs, unq_xm, x_m, min_or_max):
        if len(unq_xm)==len(x_m):
            return trcs
        
        for xx in unq_xm:
            ind = np.where(x_m==xx)[0]

            if len(ind)==2:
                # then join them up
                i1 = int(ind[0])
                i2 = int(ind[1])

                x1 = list(trcs[i1]['x'])
                x2 = list(trcs[i2]['x'])

                y1 = list(trcs[i1]['y'])
                y2 = list(trcs[i2]['y'])

                if min(len(x1), len(x2), len(y1), len(y2))<2:
                    continue

                is_close_enough = self.check_close_enough(y1, y2, min_or_max)

                if not is_close_enough:
                    continue

                if min_or_max=="max":
                    yy = 0.5*(y1[-1] + y2[-1])

                    trcs[i1]['x'] = x1 + [xx]
                    trcs[i1]['y'] = y1 + [yy]
                    
                    trcs[i2]['x'] = x2 + [xx]
                    trcs[i2]['y'] = y2 + [yy]

                elif min_or_max=="min":
                    yy = 0.5*(y1[0] + y2[0])
                
                    trcs[i1]['x'] = [xx] + x1
                    trcs[i1]['y'] = [yy] + y1
                    
                    trcs[i2]['x'] = [xx] + x2
                    trcs[i2]['y'] = [yy] + y2
        
        return trcs
        


    def check_close_enough(self, y1, y2, min_or_max):
        thresh = 0.1*max(y1+y2)
        
        if min_or_max=="max":
            y1_near = y1[-2]
            y1_real = y1[-1]

            y2_near = y2[-2]
            y2_real = y2[-1]
        else:
            y1_near = y1[1]
            y1_real = y1[0]

            y2_near = y2[1]
            y2_real = y2[0]


        if abs(y1_real-y2_real)>thresh:
            
            # if far away, see if locally steep in y
            if (abs(y1_near-y1_real)>0.5*thresh
                    or abs(y2_near-y2_real)>0.5*thresh):
                return True
            
            return False

        else:
            return True





class ConnectedPosToZeroTraces:
    """
    Connect positive incidence traces to the zero incidence line.

    Uses linear interpolation to find the x value to connect to.
    """
    def __init__(self, traces) -> None:
        self.traces = self.connect_traces_to_0(traces)
        
    
    def connect_traces_to_0(self, traces):

        for trc in traces:
            xs = list(trc['x'])
            ys = list(trc['y'])

            if len(xs)<3 or len(ys)<3:
                continue

            where_close_enough = self.check_y_vals(ys)

            if where_close_enough is None:
                continue
            elif where_close_enough=="start":
                gdt = (ys[1]-ys[0])/(xs[1]-xs[0])
                c = ys[0] - gdt*xs[0]

                try:
                    xv = -c/gdt
                except:
                    xv = xs[0] - 0.1*(xs[1]-xs[0])
                
                if xv<0:
                    continue
                
                trc['x'] = [xv] + xs
                trc['y'] = [0] + ys
            elif where_close_enough=="end":

                gdt = (ys[-1]-ys[-2])/(xs[-1]-xs[-2])
                c = ys[-1] - gdt*xs[-1]
                
                try:
                    xv = -c/gdt
                except:
                    xv = xs[-1] + 0.1*(xs[-1]-xs[-2])
                
                if xv>1.2*xs[-1]:
                    continue

                trc['x'] = xs + [xv]
                trc['y'] = ys + [0]
        
        return traces



    def check_y_vals(self, ys):
        ymax = max(ys)

        if self.check_close_enough(ys[0], ys[1], ymax):
            return "start"
        
        if self.check_close_enough(ys[-1], ys[-2], ymax):
            return "end"
    
        return None



    def check_close_enough(self, y0, y1, ymax):
        thresh = 0.02*ymax

        if abs(y0)>thresh:
            
            # if far away, see if locally steep in y
            # need distance from y1 to y0 to be similar to
            # 0 and y0
            if abs(y1-y0) > 0.8*abs(y0):
                return True
            
            return False

        else:
            return True


