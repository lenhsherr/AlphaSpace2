"""
shared options
"""
alphaspace_folder_prefix = 'as'
cluster_number = 1
use_clustering = False
clustering_method = 'lig_bb_rmsd'


"""
Structure Clustering option'
"""

QUITE = False

"""
DCC options
"""
spread_mode = "AVERAGE"
cluster_method = "lig_bb_rmsd"
residue_list = []



"""
resude plot options
"""
max_cluster_index = 2
total_cluster_number = 3
output_log_filename = 'log.dat'
pocket_detection_residue_indices = range(844, 859)
pocket_plot_residue_indices = range(844, 859)
residue_to_visualize = range(844, 859)
color = ['#F98D67', '#69C1A5', '#8DA1CA']
light_color = ["pink", 'pink', 'pink']
error_bar = False
width = 0.35
y_lim = 190
