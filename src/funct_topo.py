#
# funct_plot.py
#

# import packages
from base_external_packages import *


def create_dictionary_key_mapping(dictionary):
    """
    """

    ini_keys = list(dictionary[0].keys())
    new_keys = [key.replace(" ", "_") for key in ini_keys]
    lower_new_keys = [key.lower() for key in new_keys]
    door_type_parametername_map = dict(zip(ini_keys, lower_new_keys))
    return door_type_parametername_map


def map_dictionary_keys(dictionary, mapping):
    """
    """

    ini_keys = list(dictionary[0].keys())
    new_keys = [mapping[key] for key in ini_keys]

    for row in dictionary:
        # for each type
        for ini_key, new_key in zip(ini_keys, new_keys):
            row[new_key] = row.pop(ini_key)
    return dictionary


def read_dictionary_to_classobjects(dictionary, class_name='X'):
    """
    """

    objects = []
    for row in dictionary:
        # for each type
        row_in_string = json.dumps(row)
        object = json.loads(
            row_in_string,
            object_hook=lambda d: namedtuple(class_name, d.keys())(*d.values()))
        objects.append(object)

    return objects


def convert_revitdict_to_clsobjs(dict, class_name='X', string_mapping=True):
    """
    """

    if string_mapping:
        parametername_map = create_dictionary_key_mapping(dict)
        dictionary_mapped = map_dictionary_keys(dict, parametername_map)
    else:
        dictionary_mapped = dict
    class_objects = read_dictionary_to_classobjects(
        dictionary_mapped, class_name=class_name)

    return class_objects


def convert_clsobjs_into_df(cls_objs):
    """
    """

    # Get the class attributes.
    attributes = dir(cls_objs[0])

    # Clean unrelevant attributes.
    attributes = [att for att in attributes if not att.startswith('_')]
    attributes = [att for att in attributes if att !=
                  'index' and att != 'count']

    # Convert to pandasDataFrame.
    df = pd.DataFrame([[getattr(obj, att) for att in attributes]
                      for obj in cls_objs], columns=attributes)

    return df


def build_instance_df(
        cls_objs_instance, instance_type=[], final_index_name='ifcguid'):
    """
    final_index_name: id / ifcguid.
    """

    df_instances = convert_clsobjs_into_df(cls_objs_instance)

    if final_index_name:
        df = df_instances.set_index(final_index_name)
    else:
        df = df_instances

    # if one single classification.
    if instance_type:
        df['classification'] = instance_type

    # if there's a list of classification by default.
    else:
        df['classification'] = df.apply(
            lambda x: x['name'].rsplit('_', 1)[0], axis=1)
        df['classification'] = df.apply(
            lambda x: 'Space_' + x['classification'], axis=1)
    return df


def flatten(list):
    return [item for sublist in list for item in sublist]


def split_guids(guids, separator=',', remove_repeat=False):

    guid_multilist = copy.deepcopy(guids)
    for ii in range(len(guid_multilist)):
        if separator in guid_multilist[ii]:
            guid_multilist[ii] = guid_multilist[ii].split(separator)
        elif guid_multilist[ii]:
            guid_multilist[ii] = [guid_multilist[ii]]
        else:
            continue
    
    if remove_repeat:
        guid_multilist = [list(set(l)) for l in guid_multilist]
        
    return guid_multilist


def build_guid_edges(
        lst_host, lst_targets, set_sort=True):
    
    all_edges = []
    if len(lst_host) != len(lst_targets):
        return all_edges
    else:
        for host, targets in zip(lst_host, lst_targets):
            edges_per_host = []
            actual_targets = [tt for tt in targets if (tt != host[0] and tt)]
            edges_per_host = [[host[0], target] for target in actual_targets]
            all_edges.append(edges_per_host)

    all_edges = flatten(all_edges)
    if set_sort:
        all_edges = [sorted(x, key=lambda x:x[0]) for x in all_edges]
    all_edges = [list(i) for i in set(map(tuple, all_edges))]
    return all_edges


def build_networkx_graph(
        all_df_edges, all_dict_attrs=[]):

    G_all = []
    for df in all_df_edges:
        G = nx.Graph()
        G = nx.from_pandas_edgelist(df, 'host', 'target')
        G_all.append(G)

    G_all = nx.compose_all(G_all)

    if all_dict_attrs:
        for dict_attrs in all_dict_attrs:
            nx.set_node_attributes(G_all, dict_attrs)

    return G_all


def get_tempo_data(
        lst, k_track, k):
    """
    get the temporary data at k_track
    """

    k_lst = []
    if isinstance(lst, list):
        if len(lst) == k:
            if len(lst) > 1:
                k_lst = lst[k_track]
            elif len(lst) == 1:
                k_lst = lst[0]
        else:
            print('the input data doest fit the assigned link level.')
    else:
        k_lst = lst
    return k_lst


def plot_networkx_per_rule(
        path,
        G,
        nodesize_map,
        nodecolor_map,
        rule='',
        pos_layout_scale= 0.75):
    """
    plot the networkx graph with specified maps for node size and node color.
    """

    fig = plt.figure(figsize=(30, 18))
    ax = plt.axes((0.05, 0.05, 0.90, 0.90))
    G_nodes = G.nodes()
    G_nodes_sizes = [nodesize_map[G.nodes[n]['classification']]
                     for n in G_nodes]
    G_nodes_colors = [nodecolor_map[G.nodes[n]['classification']]
                      for n in G_nodes]

    nx.draw_networkx(
        G,
        pos=nx.kamada_kawai_layout(G, scale=pos_layout_scale),
        # pos = nx.spiral_layout(G, scale=pos_layout_scale),
        arrows=True,
        with_labels=False,
        node_size=G_nodes_sizes,
        node_shape="o",
        node_color=G_nodes_colors,
        linewidths=0.1,
        width=2,
        alpha=0.80,
        edge_color='black')
    ax.title.set_position([.5, 0.975])

    for kk in list(nodecolor_map.keys()):
        plt.scatter([], [], c=nodecolor_map[kk], label=kk)

    plt.legend(fontsize="xx-large", ncol=4, loc=(0.35,0.05))
    plt.savefig(path + '\\res_G_' + str(rule) + '.png', dpi=200)


def createDictGlobalParametersPerRule(rules, df_gps):
    """
    """

    dictGPperRule = dict()
    for rule in rules:
        lst_gps_per_rule = [
            gp for gp in df_gps[rule].tolist() if str(gp) != 'nan']
        dictGPperRule[rule] = lst_gps_per_rule

    return dictGPperRule
