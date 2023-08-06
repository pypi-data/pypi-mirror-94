from collections import defaultdict
import pandas as pd


def get_net_migration_from_od_matrix(od_matrix_file_path, origin_col_name, dest_col_name, count_col_name, adm_name):
    df = pd.read_csv(od_matrix_file_path)

    outflow = defaultdict(int, dict(df.groupby(origin_col_name)[count_col_name].sum()))
    inflow = defaultdict(int, dict(df.groupby(dest_col_name)[count_col_name].sum()))

    admins = set(outflow.keys()).union(set(inflow.keys()))

    net_mvmt = {}

    for admin in admins:
        net_mvmt[admin] = inflow[admin] - outflow[admin]

    result = pd.DataFrame(net_mvmt.items(), columns=[adm_name, 'net_mvmt'])
    result['total'] = result[adm_name].map(outflow)

    return result


def get_avg_dist_per_dest(od_matrix_file_path, dist_matrix_file_path, adm_code_col_name, origin_col_name='origin',
                          destination_col_name='dest', count_col_name='count(1)'):
    od_matrix = pd.read_csv(od_matrix_file_path)
    dist_matrix = pd.read_csv(dist_matrix_file_path, index_col=adm_code_col_name)

    od_matrix['dist'] = od_matrix.apply(
        lambda x: dist_matrix.loc[x[origin_col_name], str(x[destination_col_name]).zfill(3)], axis=1)

    groups = od_matrix.groupby(destination_col_name)
    od_matrix['temp'] = od_matrix['dist'] * od_matrix[count_col_name] / groups[count_col_name].transform('sum')

    return dict(groups['temp'].sum())
