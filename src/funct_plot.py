#
# funct_plot.py
#

# import packages
from base_external_packages import *
from funct_data import map_label_y

# define plot functions

def boxplot_sample_variation(dirs_fig, sa_samples_df):
    """
    Plot means and standard deviations for ensitivity indices

    """

    fig = plt.figure(figsize=(12, 8))  # unit of inch
    ax = plt.axes((0.1, 0.15, 0.85, 0.8))  # in range (0,1)
    boxplot = sa_samples_df.boxplot(grid=False)
    
    ax.set_yscale('log')
    ax.tick_params(
        axis='y',
        reset=True,
        which='major',
        # direction='in',
        # length=5,
        # width=2,
        # color='black',
        # pad=5,
        grid_alpha=0,
        labelrotation=0,
        labelsize=10,
        labelcolor='black',
        )
    ax.set_ylabel("Parameter values (meter)", color="black", fontsize=16)
    
    ax.tick_params(
        axis='x',
        which='major',
        direction='out',
        length=5,
        width=2,
        color='black',
        pad=5,
        grid_alpha=0.2,
        grid_linewidth=0.5,
        grid_color='grey',
        labelsize=10,
        labelcolor='black',
        labelrotation=15)
    ax.set_xlabel("Parameters", color="black", fontsize=16)
    
    ax.grid(True)

    plt.savefig(dirs_fig+'/SA_sample_variations.png', dpi=200)


# new
def plot_parallel_parameters(dirs_fig, samples_df):
    """
    Plot parallel coordinates.

    """

    tm_identity = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    plot_name = r'\Parallel_parameters_' + tm_identity

    tempo_samples_df = copy.deepcopy(samples_df)
    clmns = tempo_samples_df.columns
    
    # label the initial design

    fig = px.parallel_coordinates(
        tempo_samples_df,
        color='type',
        dimensions=clmns,
        color_continuous_scale=px.colors.diverging.RdYlGn,
        width=1500,
        height=600)

    plotly.offline.plot(fig, filename=dirs_fig + plot_name + '.html')


# new
def extract_singleorder_indices(Si_df, filter_name, relevant_number):
    """
    extract_singleorder_indices.

    """

    CONF_COLUMN = "_conf"
    conf_cols = Si_df.columns.str.contains(CONF_COLUMN)
    tempo_confs = Si_df.loc[:, conf_cols]
    tempo_confs.columns = [c.replace(CONF_COLUMN, "") for c in tempo_confs.columns]
    tempo_sensi = Si_df.loc[:, ~conf_cols]
    
    confs = tempo_confs.replace(np.nan, 0.) # Replace NaN Values with Zero
    sensi = tempo_sensi.replace(np.nan, 0.) # Replace NaN Values with Zero
    
    # if the order is already given.
    sensi_sort = sensi.sort_values(by=[filter_name],ascending=False) # Sort by Descending values of the column[filter_name]
    relevant_number = min(len(sensi_sort.index), relevant_number) # in case the row numbers are smaller than the given number
    filter_idx = sensi_sort.index.values[:relevant_number]

    sensi_filtered = sensi_sort.loc[filter_idx,:]     # Filter the sensi dataframe to fixed index amount (=relevant_number)
    confs_flitered = confs.loc[filter_idx,:]          # Filter the confs dataframe to fixed index amount within the correct order
    
    return sensi_filtered, confs_flitered

# new
def sobol_plot_sa_S1ST(
    dirs_fig,
    rl,
    first_df,
    total_df,
    relevant_number=4):
    """
    to check with:
    
    """

    fig_title = "First and total order indices to rule {} \n (The {} most relevant parameters)".format(rl,relevant_number)

    # The first- and total-order indices are sorted according to ST values.
    sensi_t, confs_t = extract_singleorder_indices(total_df,'ST',relevant_number)
    sensi_f, confs_f = extract_singleorder_indices(first_df,'S1',relevant_number)
    sensi_f = sensi_f.reindex(sensi_t.index.tolist())
    confs_f = confs_f.reindex(sensi_t.index.tolist())

    # .reindex(['11-', 'Just 12', 'Some College', 'Bachelor+'])

    fig = plt.figure(figsize=(8,5))  # unit of inch
    ax = plt.axes((0.10, 0.10, 0.80, 0.80))  # in range (0,1)
    
    # S_1 errorbar
    s1_est = plt.errorbar(
        x=sensi_f.index, 
        y=sensi_f['S1'],
        yerr=confs_f['S1'], 
        capsize=3,
        marker='+', 
        color='navy', 
        markersize=4,
        linewidth=0.1, 
        linestyle='dashed')
    # s1_val, s1_capsline, s1_c = s1_est
    # [s1_capsl.set_linestyle('dashed') for s1_capsl in s1_est[1]]

    # S_1 errorbar region
    s1_err = plt.fill_between(
        sensi_f.index,
        sensi_f['S1'] - confs_f['S1'],
        sensi_f['S1'] + confs_f['S1'],
        color='blue', alpha=0.05, label='S_1 error')
    
    # S_T errorbar
    st_est = plt.errorbar(
        x=sensi_t.index, 
        y=sensi_t['ST'],
        yerr=confs_t['ST'], 
        capsize=3,
        marker='x', 
        color='maroon', 
        markersize=4, 
        linewidth=0.1, 
        linestyle='dotted')
    # st_val, st_capsline, st_c = st_est
    # [st_capsl.set_marker('1') for st_capsl in st_est[1]]

    # S_T errorbar region
    st_err = plt.fill_between(
        sensi_t.index,
        sensi_t['ST'] - confs_t['ST'],
        sensi_t['ST'] + confs_t['ST'],
        color='red', alpha=0.05, label='S_T error')

    # to change legend together with the linestyle of error-caps
    plt.legend((s1_est, s1_err, st_est, st_err),("S1","S1 error","ST","ST error")) 

    # x axis
    ax.tick_params(
        axis='x',
        which='major', direction='out', color='grey',
        grid_alpha=0.33,
        pad=3, labelsize=8, labelcolor='black', labelrotation=0
        )
    ax.set_xlabel("Parameters", color="black", fontsize=10)

    # y axis
    ax.set_yticks(np.arange(0-0.25, 2, 0.25))
    ax.tick_params(
        axis='y',
        which='major', direction='out', color='grey',
        grid_alpha=0.0,
        pad=3, length=5, width=2,
        labelsize=8, labelcolor='black', labelrotation=0
        )
    ax.set_ylabel("Sensitivity Indices", color="black", fontsize=10)
    
    # title
    ax.set_title(fig_title, size=12)
    ax.title.set_position([.5, 0.965])
    
    # grid
    ax.grid(True)

    # save
    plt.savefig(dirs_fig + '/SA_{}_sobol_S1ST_indices.png'.format(rl), dpi=200)

# new
def sobol_plot_sa_S2(
    dirs_fig,
    rl,
    second):
    """
    Plot second sensitivity indices.

    """

    def convert2Matrix(second):
        param_names = []
        for m in range(second.shape[0]):
            for n in range(second.shape[1]):
                if second.index[m][n] not in param_names:
                    param_names.append(second.index[m][n])
                else:
                    continue

        matrix = np.zeros((len(param_names), len(param_names)), float)
        for k in range(second['S2'].shape[0]):
            j = param_names.index(second['S2'].index[k][0])
            i = param_names.index(second['S2'].index[k][1])
            matrix[j][i] = second['S2'].iloc[k]
        return param_names, matrix

    param_names, matrix = convert2Matrix(second)

    fig = plt.figure(figsize=(10, 10))  # unit of inch
    ax1 = plt.axes((0.1, 0.1, 0.8, 0.8))  # in range (0,1)

    pos = ax1.imshow(matrix, interpolation='none', cmap='BuPu')

    ax1.set_xticks(np.arange(len(param_names)), param_names)
    ax1.set_yticks(np.arange(len(param_names)), param_names)
    ax1.tick_params(axis='x', which='major', direction='out', length=5, width=2, color='maroon',
                    pad=10, labelsize=10, labelcolor='navy', labelrotation=15)
    ax1.tick_params(axis='y', which='major', direction='out', length=5, width=2, color='maroon',
                    pad=10, labelsize=10, labelcolor='navy', labelrotation=15)
    ax1.set_title(r'Second-order sensitivity indices for rule: '+rl, size=16)
    fig.colorbar(pos, location='right', shrink=0.8)

    for (i, j), z in np.ndenumerate(matrix):
        if z != 0:
            ax1.text(j, i, '{:0.3f}'.format(z), ha='center', va='center')

    plt.savefig(dirs_fig + '/SA_{}_sobol_S2_indices.png'.format(rl), dpi=200)

# new
def _sort_Si(Si, key, sortby='mu_star'):
    return np.array([Si[key][x] for x in np.argsort(Si[sortby])])

def morris_horizontal_bar_plot(
    ax,
    Si,
    plotmu,
    bcolor='navy',
    bheight=0.5,
    lwidth=0.25,
    y_loc=0,
    alpah=0.75,
    opts=None,
    unit=''):

    '''Updates a matplotlib axes instance with a horizontal bar plot
    of mu_star, with error bars representing mu_star_conf.
    '''
    sortby = plotmu
    assert sortby in ['mu_star', 'mu_star_conf', 'sigma', 'mu']

    if opts is None:
        opts = {}

    # Sort all the plotted elements by mu_star (or optionally another metric)
    names_sorted = _sort_Si(Si, 'names', sortby)

    mu_sorted = _sort_Si(Si, 'mu', sortby)
    sigma_sorted = _sort_Si(Si, 'sigma', sortby)

    mu_star_sorted = _sort_Si(Si, 'mu_star', sortby)
    mu_star_conf_sorted = _sort_Si(Si, 'mu_star_conf', sortby)

    if plotmu == 'mu_star':
        mean, varian = mu_star_sorted, mu_star_conf_sorted
    elif plotmu == 'mu':
        mean, varian = mu_sorted, sigma_sorted

    # Plot horizontal barchart
    y_pos = np.arange(len(mu_star_sorted))
    plot_names = names_sorted

    out = ax.barh(y_pos + y_loc,
                  mean,
                  xerr=varian,
                  color=bcolor,
                  height=bheight,
                  linewidth=lwidth,
                  alpha=alpah,
                  align='center',
                  ecolor='black',
                  edgecolor='black',
                  **opts)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(plot_names)
    ax.tick_params(axis='y', which='major', labelsize=16)
    ax.tick_params(axis='x', which='major', labelsize=16)
    ax.set_xlabel(r'$\mu$' + unit, fontsize=18)

    ax.set_ylim(min(y_pos)-1, max(y_pos)+1)

    return out


def morris_covariance_plot(
    ax,
    Si,
    plotmu,
    annotate_size=14,
    opts=None,
    unit=''):

    '''
    Plots mu*/mu against sigma or the 95% confidence interval

    '''

    mu_type = '\mu^{\star}' if plotmu =='mu_star' else '\mu'

    if opts is None:
        opts = {}

    if Si['sigma'] is not None:

        # sigma is not present if using morris groups
        y = Si['sigma']
        out = ax.scatter(Si[plotmu], y, c='navy', marker=u'o',
                         **opts)
        
        for i, txt in enumerate(Si['names']):
            ax.annotate(
                txt,
                (Si[plotmu][i], y[i]),
                xytext=(Si[plotmu][i]*0.85, y[i]*0.85),
                fontsize=annotate_size)

        ax.set_ylabel(r'$\sigma$', fontsize=16)

        ax.set_xlim(-1.0,1.0)
        ax.set_ylim(0.0,)

        x_axis_bounds = np.array(ax.get_xlim())

        line1_p, = ax.plot(x_axis_bounds, x_axis_bounds, 'k-', c='maroon')
        line1_n, = ax.plot(x_axis_bounds, -x_axis_bounds, 'k-', c='maroon')
        line2_p, = ax.plot(x_axis_bounds, 0.5 * x_axis_bounds, 'k--', c='maroon')
        line2_n, = ax.plot(x_axis_bounds, -0.5 * x_axis_bounds, 'k--', c='maroon')
        line3_p, = ax.plot(x_axis_bounds, 0.1 * x_axis_bounds, 'k-.', c='maroon')
        line3_n, = ax.plot(x_axis_bounds, -0.1 * x_axis_bounds, 'k-.', c='maroon')

        ax.legend((line1_p, line2_p, line3_p), (r'$\sigma / {} = \pm 1.0$'.format(mu_type),
                                          r'$\sigma / {} = \pm 0.5$'.format(mu_type),
                                          r'$\sigma / {} = \pm 0.1$'.format(mu_type)),
                  loc='lower right')

    else:
        y = Si['mu_star_conf']
        out = ax.scatter(Si['mu_star'], y, c=u'k', marker=u'o',
                         **opts)
        ax.set_ylabel(r'$95\% CI$')
    
    ax.set_xlabel(r'${}$ '.format(mu_type) + unit, fontsize=16)
    ax.set_ylim(0-(0.01 * np.array(ax.get_ylim()[1])),)

    return out


def morris_sa_plot(
    dirs_fig,
    rl,
    Si,
    beta=1,
    input_sample=[],
    problem=[],
    ):

    # see API: https://salib.readthedocs.io/en/latest/_modules/SALib/plotting/morris.html
    
    # horizontal_bar_plot: https://jsbin.com/pucadowa/8/edit?html,js,output # plot_morris.horizontal_bar_plot(ax, Si)
    fig = plt.figure(figsize=(16,8))  # unit of inch
    ax = plt.axes((0.15, 0.10, 0.80, 0.80))  # in range (0,1)
    morris_horizontal_bar_plot(ax, Si, plotmu='mu')
    plt.savefig(dirs_fig + '/SA_mu_{}_morris_Si_indices_horbar_beta_{}.png'.format(rl, str(beta)), dpi=200)

    # covariance_plot(ax, Si, opts=None, unit=''): 
    
    # covariance_plot: http://a.web.umkc.edu/andersonbri/Variance.html
    fig = plt.figure(figsize=(16,8))  # unit of inch
    ax = plt.axes((0.15, 0.10, 0.80, 0.80))  # in range (0,1)
    morris_covariance_plot(ax, Si, plotmu='mu')
    plt.savefig(dirs_fig + '/SA_mu_{}_morris_Si_indices_convar_beta_{}.png'.format(rl, str(beta)), dpi=200)

    # sample_histograms:
    # fig = plt.figure(figsize=(8,5))  # unit of inch
    # ax = plt.axes((0.10, 0.10, 0.80, 0.80))  # in range (0,1)
    # plot_morris.sample_histograms(
    #     fig, input_sample, problem, opts=None)
    # plt.savefig(dirs_fig + '/SA_{}_{}_morris_Si_indices_histo.png'.format(tgt, rl), dpi=200)




def plot_pca_matrix(
    dirs_fig, rulename, pca_data_X_Y, pca_labels,
    diag_visi=False, set_result_label_type='validity'):     
    """
    plot the pca matrix of samples via px.scatter_matrix

    """

    dim = len(pca_labels.keys())
    plot_name = '/PCA_matrix_' + \
        rulename + '_n_pca_' + str(dim)
    colr_valid, colr_invalid = "blue", "darkred"
    symb_initial,symb_adjusted = 'square', 'circle-open'

    fig = px.scatter_matrix(
        pca_data_X_Y,
        labels=pca_labels,
        dimensions=list(pca_labels.values()),

        color=pca_data_X_Y[rulename],
        color_discrete_map={
            map_label_y(+0.1,set_result_label_type): colr_valid,
            map_label_y(-0.1,set_result_label_type): colr_invalid,
        },
        symbol=pca_data_X_Y['type'],
        symbol_map={
            "initial": symb_initial,
            "adjusted": symb_adjusted,
        },
        opacity=0.5,
        template="plotly_white",
        width=dim*250 - 100,
        height=dim*150
    )

    fig.update_layout(
        title={
            'text': "PCA matrix, on rule: {}".format(rulename),
            'y': 0.985,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig.update_traces(diagonal_visible=diag_visi, marker={'size': 3})
    
    plotly.offline.plot(fig, filename=dirs_fig + plot_name + '.html')


def plot_loadings_in_pca_2d_plus_region(
    dirs_fig, rulename, pcs_4_2d,
    components, tempo_loadings,
    pca_data_X_Y_with_regions, pca_labels,
    initial_design,
    feasible_regions=[],
    tol_loadings=1.0e-5,
    set_result_label_type='validity'):
    """
    plot the loadings with two pcas (choose one couple of components)
    along with the most reliable feasible regions detected.
    
    """
    
    pca_nr1, pca_nr2  = pcs_4_2d
    x_nr, y_nr = pca_nr1-1, pca_nr2-1
    tempo_feature_names = initial_design.parameters
    loadings, feature_names = [], []

    # remove the unrelated parameters' loadings
    for one_lds, name in zip(tempo_loadings, tempo_feature_names):
        if all(abs(ld) >= tol_loadings for ld in one_lds):
            loadings.append(one_lds)
            feature_names.append(name)
    loadings = np.array(loadings)

    # plot settings
    plot_name = '/PCA_loadings_in_pca_2d_' + \
        rulename + '_' + str(pca_nr1) + '_' + str(pca_nr2)
    colr_valid, colr_invalid = "blue", "darkred"
    symb_initial,symb_adjusted = 'square', 'circle-open'

    # plot scatters
    fig = px.scatter(
        components, x=x_nr, y=y_nr,
        color=pca_data_X_Y_with_regions[rulename],
        color_discrete_map={
            map_label_y(+0.1,set_result_label_type): colr_valid,
            map_label_y(-0.1,set_result_label_type): colr_invalid,
            },
        symbol=pca_data_X_Y_with_regions['type'],
        symbol_map={
            "initial": symb_initial,
            "adjusted": symb_adjusted,
            },
        opacity=0.5,
        template="plotly_white",
        width=1200,
        height=800)

    # plot loadings of the parameters 
    for i, feature in enumerate(feature_names):
        fig.add_shape(
            type='line',
            x0=0, y0=0,
            x1=loadings[i, x_nr],
            y1=loadings[i, y_nr]
        )
        fig.add_annotation(
            x=loadings[i, x_nr],
            y=loadings[i, y_nr],
            ax=0, ay=0,
            xanchor="center",
            yanchor="bottom",
            text=feature,
        )
    
    # plot the xx most reliable regions 
    if feasible_regions:
        
        fesi_regions = feasible_regions[rulename]
        for ii in range(len(fesi_regions)):

            df_fesi = pca_data_X_Y_with_regions.loc[pca_data_X_Y_with_regions[rulename+'_cluster'] == fesi_regions[ii]]
            x_fesi, y_fesi = df_fesi[pca_labels[str(x_nr)]], df_fesi[pca_labels[str(y_nr)]]

            # plot the ConvexHull
            convex_points = np.array(list(zip(x_fesi.values.tolist(), y_fesi.values.tolist())))
            convex_hull = ConvexHull(convex_points)
            convex_points_x, convex_points_y = convex_points[convex_hull.vertices,0], convex_points[convex_hull.vertices,1]
            convex_points_x = np.concatenate([convex_points_x,[convex_points[convex_hull.vertices[0],0]]])
            convex_points_y = np.concatenate([convex_points_y,[convex_points[convex_hull.vertices[0],1]]])
            
            fig.add_trace(go.Scatter(
                x=convex_points_x,
                y=convex_points_y,
                name=f'Preliminary feasible region {(ii+1)}',
                fill='toself',
                hoveron='points',
                fillcolor = colr_valid,
                line_color=colr_valid,
                opacity=0.15,))

    # update the plot settings.
    fig.update_traces(marker={'size': 5})  
    fig.update_layout(
        title={
            'text': "Solution space and feasible regions digitalized in PCs, on rule: {}".format(rulename),
            'y': 0.925,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title=pca_labels[str(x_nr)],
        yaxis_title=pca_labels[str(y_nr)])
    
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99))

    plotly.offline.plot(fig, filename=dirs_fig + plot_name + '.html')


def plot_loadings_in_pca_3d(
    dirs_fig, rulename, pcs_4_3d,
    components, tempo_loadings, pca_data_X_Y, pca_labels, 
    initial_design, tol_loadings=1.0e-12,
    set_result_label_type='validity'):
    """
    plot scatter based on the first 3 components px

    """

    pca_nr1, pca_nr2, pca_nr3 = pcs_4_3d
    x_nr, y_nr, z_nr = pca_nr1-1, pca_nr2-1, pca_nr3-1
    tempo_feature_names = initial_design.parameters
    loadings, feature_names = [], []

    # remove the unrelated features
    for one_lds, name in zip(tempo_loadings, tempo_feature_names):
        if all(abs(ld) >= tol_loadings for ld in one_lds):
            loadings.append(one_lds)
            feature_names.append(name)
    loadings = np.array(loadings)

    plot_name = '/PCA_loadings_in_pca_3d_' + \
        rulename + '_' + str(pca_nr1) + '_' + str(pca_nr2) + '_' + str(pca_nr3) 

    fig = px.scatter_3d(
        components, x=x_nr, y=y_nr, z=z_nr,

        color=pca_data_X_Y[rulename],
        color_discrete_map={
            map_label_y(+0.1,set_result_label_type): "blue",
            map_label_y(-0.1,set_result_label_type): "darkred",
        },
        symbol=pca_data_X_Y['type'],
        symbol_map={
            "initial": 'square',
            "adjusted": 'circle-open',
            },
        opacity=0.5,
        labels={
            str(x_nr): pca_labels[str(x_nr)],
            str(y_nr): pca_labels[str(y_nr)],
            str(z_nr): pca_labels[str(z_nr)]},
        template="plotly_white",
        width=800,
        height=800)

    fig.update_traces(marker={'size': 5})  
    fig.update_layout(
        title={
            'text': "PCA with loadings in 3D, on rule: {}".format(rulename),
            'y': 0.90,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
            )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.85,
        xanchor="right",
        x=0.95))
    
    plotly.offline.plot(fig, filename=dirs_fig + plot_name + '.html')


def plot_real_parameters_3d(
    dirs_fig, rulename,
    pca_data_X_Y_with_regions,
    plot_parameters,
    feasible_regions,
    set_result_label_type='validity',):
    """
    plot scatter based on the first 3 components px

    """

    [x_nr, y_nr, z_nr] = plot_parameters
    plot_name = '/Solution_space_in_3d_' + rulename + '-'.join(plot_parameters)

    fig = px.scatter_3d(
        pca_data_X_Y_with_regions, x=x_nr, y=y_nr, z=z_nr,

        color=pca_data_X_Y_with_regions[rulename],
        color_discrete_map={
            map_label_y(+0.1,set_result_label_type): "blue",
            map_label_y(-0.1,set_result_label_type): "darkred",
        },
        symbol=pca_data_X_Y_with_regions['type'],
        symbol_map={
            "initial": 'square',
            "adjusted": 'circle-open',
            },
        opacity=0.5,
        labels={
            str(x_nr): x_nr,
            str(y_nr): y_nr,
            str(z_nr): z_nr},
        template="plotly_white",
        width=800,
        height=800)

    fig.update_traces(marker={'size': 5})
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.85,
        xanchor="right",
        x=0.95))
    
    plotly.offline.plot(fig, filename=dirs_fig + plot_name + '.html')