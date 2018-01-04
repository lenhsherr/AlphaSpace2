"""
AS_Vina contains function and classes for scoring probes using vina scoring function.
=====================================================================================


"""

import numpy as np
from scipy import spatial

POLAR_ATOM_TYPE = np.array(['OA', 'OS', 'N', 'NS', 'NA', 'S', 'SA'])

ALI_ATOM = np.array(['C', 'A'])

HP_DICT = dict(
    ALA={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    ARG={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NP", "NP"], "CD": ["NNP", "NNP"],
         "NE": ["P", "NNP"], "CZ": ["NNP", "NNP"], "NH1": ["P", "NNP"], "NH2": ["P", "NNP"], "C": ["NNP", "NNP"],
         "O": ["NPP", "P"]},
    ASN={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NNP", "NNP"], "OD1": ["NNP", "P"],
         "ND2": ["P", "NNP"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    ASP={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NNP", "NNP"], "OD1": ["NNP", "P"],
         "OD2": ["NNP", "P"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    CYS={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NNP", "NNP"], "SG": ["NNP", "P"], "C": ["NNP", "NNP"],
         "O": ["NPP", "P"]},
    GLN={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NP", "NP"], "CD": ["NNP", "NNP"],
         "OE1": ["NNP", "P"], "NE2": ["P", "NNP"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    GLU={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NP", "NP"], "CD": ["NNP", "NNP"],
         "OE1": ["NNP", "P"], "OE2": ["NNP", "P"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    GLY={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    HIS={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NNP", "NNP"], "ND1": ["P", "P"],
         "CD2": ["NNP", "NNP"], "CE1": ["NNP", "NNP"], "NE2": ["P", "P"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    HIE={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NNP", "NNP"], "ND1": ["P", "P"],
         "CD2": ["NNP", "NNP"], "CE1": ["NNP", "NNP"], "NE2": ["P", "P"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    HID={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NNP", "NNP"], "ND1": ["P", "P"],
         "CD2": ["NNP", "NNP"], "CE1": ["NNP", "NNP"], "NE2": ["P", "P"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    HIP={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NNP", "NNP"], "ND1": ["P", "P"],
         "CD2": ["NNP", "NNP"], "CE1": ["NNP", "NNP"], "NE2": ["P", "P"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    ILE={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG1": ["NP", "NP"], "CG2": ["NP", "NP"],
         "CD1": ["NP", "NP"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    LEU={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NP", "NP"], "CD1": ["NP", "NP"],
         "CD2": ["NP", "NP"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    LYS={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NP", "NP"], "CD": ["NP", "NP"],
         "CE": ["NNP", "NNP"], "NZ": ["P", "NNP"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    MET={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NNP", "NNP"], "SD": ["NNP", "P"],
         "CE": ["NNP", "NNP"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    PHE={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NP", "NP"], "CD1": ["NP", "NP"],
         "CD2": ["NP", "NP"], "CE1": ["NP", "NP"], "CE2": ["NP", "NP"], "CZ": ["NP", "NP"], "C": ["NNP", "NNP"],
         "O": ["NPP", "P"]},
    PRO={"N": ["NNP", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NP", "NP"], "CD": ["NNP", "NNP"],
         "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    SER={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NNP", "NNP"], "OG": ["P", "P"], "C": ["NNP", "NNP"],
         "O": ["NPP", "P"]},
    THR={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NNP", "NNP"], "OG1": ["P", "P"], "CG2": ["NNP", "NNP"],
         "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    TRP={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NP", "NP"], "CD1": ["NNP", "NNP"],
         "CD2": ["NP", "NP"], "NE1": ["P", "NNP"], "CE2": ["NNP", "NNP"], "CE3": ["NP", "NP"], "CZ2": ["NP", "NP"],
         "CZ3": ["NP", "NP"], "CH2": ["NP", "NP"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    TYR={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG": ["NP", "NP"], "CD1": ["NP", "NP"],
         "CD2": ["NP", "NP"], "CE1": ["NP", "NP"], "CE2": ["NP", "NP"], "CZ": ["NNP", "NNP"], "OH": ["P", "P"],
         "C": ["NNP", "NNP"], "O": ["NPP", "P"]},
    VAL={"N": ["P", "NNP"], "CA": ["NNP", "NNP"], "CB": ["NP", "NP"], "CG1": ["NP", "NP"], "CG2": ["NP", "NP"],
         "CZ": ["NP", "NP"], "C": ["NNP", "NNP"], "O": ["NPP", "P"]})

ADV_DICT = {'H': [1.0, False], 'HD': [1.0, True], 'HS': [1.0, True], 'C': [2.0, False], 'A': [2.0, False],
            'N': [1.75, False], 'NA': [1.75, True], 'NS': [1.75, True], 'OA': [1.6, True], 'OS': [1.6, True],
            'F': [1.545, False], 'Mg': [0.65, False], 'MG': [0.65, False], 'P': [2.1, False], 'SA': [2.0, True],
            'S': [2.0, False], 'Cl': [2.045, False], 'CL': [2.045, False], 'Ca': [0.99, False], 'CA': [0.99, False],
            'Mn': [0.65, False], 'MN': [0.65, False], 'Fe': [0.65, False], 'FE': [0.65, False], 'Zn': [0.74, False],
            'ZN': [0.74, False], 'Br': [2.165, False], 'BR': [2.165, False], 'I': [2.36, False]}

ADV_PARM = {"gauss_1": -0.035579,
            "gauss_2": -0.005156,
            "repulsion": 0.840245,
            "hydrophobic": -0.035069,
            "Hydrogen": -0.587439}

PROBE_TYPE = ['C', 'Br', 'F', 'Cl', 'I', 'OA', 'SA', 'N', 'P']


def _NP_interp(r):
    """
    #step function for nonpolar interactions.
    :param r: radii
    :type r: float
    :return: stepped
    :rtype: float
    """
    if r < 0.5:
        x = 1.0
    elif r > 1.5:
        x = 0.0
    else:
        x = 1.5 - r
    #        x=np.interp(r, [0.i5,1.5], [1,0])
    return x


def _P_interp(r):  ##step for polar
    if r < -0.7:
        x = 1.0
    elif r >= 0:
        x = 0.0
    else:
        x = -r / 0.7
    return x


def _calc_score(g1, g2, rep, hydrophobe, hbond, vina_weights_dict):
    """

    Sum the score component from Vina scoring function.


    Parameters
    ----------
    g1
    g2
    rep
    hydrophobe
    hbond
    vina_weights_dict

    Returns
    -------

    """
    return g1 * vina_weights_dict['gauss_1'] \
           + g2 * vina_weights_dict['gauss_2'] \
           + rep * vina_weights_dict['repulsion'] \
           + hydrophobe * vina_weights_dict['hydrophobic'] \
           + hbond * vina_weights_dict['Hydrogen']


def _assign_hp(prot_coord, prot_types, hp_type):
    """
    This assigns hydrophobicity type for UNK atoms

    :param prot_coord: protein coordinate shape =  N*3
    :param prot_types: protein atom types shape = N
    :param hp_type: type_to be modified.
    :return: hp_type
    """

    tree = spatial.KDTree(prot_coord)
    for ix in np.where(hp_type == 'UNK')[0]:
        indx = np.array(tree.query_ball_point(prot_coord[ix], 2.0))
        if prot_types[ix] not in POLAR_ATOM_TYPE:
            if np.any(np.in1d(prot_types[indx[indx != ix]], POLAR_ATOM_TYPE)):
                hp_type[ix] = 'NNP'
            else:
                hp_type[ix] = 'NP'
        else:
            hp_type[ix] = 'XXX'
    return hp_type


def _assign_acc(prot_coord, prot_types, hp_type):
    """

    Parameters
    ----------
    prot_coord
    prot_types
    hp_type

    Returns
    -------

    """
    tree = spatial.KDTree(prot_coord)
    for ix in np.where(hp_type == 'UNK')[0]:
        indx = np.array(tree.query_ball_point(prot_coord[ix], 2.0))
        if prot_types[ix] in ['OA', 'OS', 'SA', 'S']:
            hp_type[ix] = 'P'
        else:
            hp_type[ix] = 'XXX'
    return hp_type


def _assign_don(prot_coord, prot_types, hp_type):
    tree = spatial.KDTree(prot_coord)
    for ix in np.where(hp_type == 'UNK')[0]:
        indx = np.array(tree.query_ball_point(prot_coord[ix], 2.0))
        if prot_types[ix] in ['N', 'NS', 'NA']:
            if len(indx[indx != ix]) > 2:
                hp_type[ix] = 'NPP'
            else:
                hp_type[ix] = 'P'
        else:
            hp_type[ix] = 'XXX'
    return hp_type


def pre_process_pdbqt(pdbqt_file, types_dict):
    """

    Parameters
    ----------
    pdbqt_file : str
        path to pdbqt file
    types_dict : dict


    Returns
    -------

    """
    ali_atoms = np.array(['C', 'A'])
    with open(pdbqt_file, 'r') as f:
        templines = f.readlines()
    hp_type = []
    don_type = []
    acc_type = []
    prot_coord = []
    prot_types = []
    for t in templines:
        if t[0:6] in ['ATOM  ', 'HETATM'] and t[-3:].strip() not in ['H', 'HD', 'HS']:
            prot_coord.append([float(t[30:38].strip()), float(t[38:46].strip()), float(t[46:54].strip())])
            prot_types.append(t[76:].strip())
            if t[17:20].strip() in types_dict.keys():
                if t[12:16].strip() in types_dict[t[17:20].strip()].keys():
                    if t[76:].strip() in ali_atoms:
                        hp_type.append(types_dict[t[17:20].strip()][t[12:16].strip()][0])
                        don_type.append('XXX')
                        acc_type.append('XXX')
                    if t[76:].strip() in POLAR_ATOM_TYPE:
                        don_type.append(types_dict[t[17:20].strip()][t[12:16].strip()][0])
                        acc_type.append(types_dict[t[17:20].strip()][t[12:16].strip()][1])
                        hp_type.append('XXX')
                else:
                    hp_type.append('UNK')
                    don_type.append('UNK')
                    acc_type.append('UNK')
            else:
                hp_type.append('UNK')
                don_type.append('UNK')
                acc_type.append('UNK')
    prot_coord = np.array(prot_coord)
    prot_types = np.array(prot_types)
    hp_type = np.array(hp_type)
    acc_type = np.array(acc_type)
    don_type = np.array(don_type)
    if np.any(hp_type == 'UNK'):
        _assign_hp(prot_coord, prot_types, hp_type)
        _assign_don(prot_coord, prot_types, don_type)
        _assign_acc(prot_coord, prot_types, acc_type)
    return prot_coord, prot_types, hp_type, acc_type, don_type


def get_probe_score(prot_coord, prot_types, hp_type, don_type, acc_type, probe_coords):
    """

    Example
    -------

    get_probe_score(*pre_process_pdbqt(),probe_coords)


    Parameters
    ----------
    prot_coord : np.ndarray
        shape = (n,3)
    prot_types : np.ndarray
        shape = (n,3)
    hp_type : np.ndarray
        shape = (n,3)
    don_type : np.ndarray
        shape = (n,3)
    acc_type : np.ndarray
        shape = (n,3)
    probe_coords : np.ndarray
        shape = (n,3)

    Returns
    -------
    prb_dict : dict
        probe score dictionary.



    """
    dist = spatial.distance.cdist(probe_coords, prot_coord)
    prb_dict = {i: [] for i in PROBE_TYPE}

    for px in range(len(probe_coords)):
        dist_bool = dist[px] <= 8.0
        temp_dist = dist[px][dist_bool]

        temp_type = prot_types[dist_bool]
        NP_type = (hp_type[dist_bool] == 'NP')
        Pdon_type = (don_type[dist_bool] == 'P')
        Pacc_type = (acc_type[dist_bool] == 'P')
        dist_radii = np.array([ADV_DICT[ty][0] for ty in temp_type])

        for prb in ['C', 'Br', 'F', 'Cl', 'I', 'OA', 'SA', 'N', 'P']:
            probe_dist = ADV_DICT[prb][0]
            proc_dist = temp_dist - dist_radii - probe_dist
            g1 = np.sum(np.exp(-(proc_dist / 0.5) ** 2))
            g2 = np.sum(np.exp(-((proc_dist - 3.0) / 2.0) ** 2))
            rep = np.sum([dd ** 2 if dd < 0.0 else 0.0 for dd in proc_dist])
            if prb in ['C', 'Br', 'Cl', 'F', 'I']:
                h1 = np.sum([_NP_interp(dd) for dd in proc_dist[NP_type]])
                h2 = 0.0
            elif prb in ['OA', 'SA']:
                h1 = 0.0
                h2 = np.sum([_P_interp(dd) for dd in proc_dist[Pdon_type]])
            elif prb in ['N', 'P']:
                h1 = 0.0
                h2 = np.sum([_P_interp(dd) for dd in proc_dist[Pacc_type]])
            prb_dict[prb].append([_calc_score(g1, g2, rep, h1, h2, vina_weights_dict=ADV_PARM), g1, g2, rep, h1, h2])
    return prb_dict


if __name__ == '__main__':
    import sys
    import numpy as np

    probe_coords = np.random.rand(10, 3)

    prot_coord, prot_types, hp_type, acc_type, don_type = pre_process_pdbqt(sys.argv[1], HP_DICT)

    prb_dict = get_probe_score(prot_coord, prot_types, hp_type, acc_type, don_type, probe_coords=probe_coords)

    print(prb_dict)