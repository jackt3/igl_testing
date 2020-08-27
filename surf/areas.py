import multiprocessing as mp
import numpy as np
import functools
from scipy import sparse
import igl

AREA_TYPES = {
    'voronoi': igl.MASSMATRIX_TYPE_VORONOI,
    'barycentric': igl.MASSMATRIX_TYPE_VORONOI,
    'mayer': 'mayer'
}

def _distributeObjects(objs, ngroups):
    """Distribute a set of objects into n groups.
    For preparing chunks before multiprocessing.pool.map
    
    Returns a set of ranges, each of which are index numbers for 
    the original set of objs 
    """

    chunkSize = np.floor(len(objs) / ngroups).astype(np.int32)
    chunks = [] 

    for n in range(ngroups):
        if n != ngroups - 1: 
            chunks.append(range(n * chunkSize, (n+1) * chunkSize))
        else:
            chunks.append(range(n * chunkSize, len(objs)))

    assert sum(map(len, chunks)) == len(objs), \
        "Distribute objects error: not all objects distributed"        

    return chunks

def __meyer_worker(points, tris, edges, edge_lengths, worklist):
    """
    Woker function for _meyer_areas()
    Args: 
        points: Px3 array
        tris: Tx3 array of triangle indices into points 
        edges: Tx3x3 array of triangle edges 
        edge_lengths: Tx3 array of edge lengths 
        worklist: iterable object, point indices to process (indexing
            into the tris array)
    Returns: 
        PxT sparse CSR matrix, where element I,J is the area of triangle J
            belonging to vertx I 
    """

    # We pre-compute all triangle edges, in the following order:
    # e1-0, then e2-0, then e2-1. But we don't necessarily process
    # the edge lengths in this order, so we need to keep track of them
    EDGE_INDEXING = [{1,0}, {2,0}, {2,1}]
    FULL_SET = set(range(3))
    vtx_tri_areas = sparse.dok_matrix((points.shape[0], tris.shape[0]))

    # Iterate through each triangle containing each point 
    for pidx in worklist:
        tris_touched = (tris == pidx)

        for tidx in np.flatnonzero(tris_touched.any(1)):
            # We need to work out at which index within the triangle
            # this point sits: could be {0,1,2}, call it the cent_pidx
            # Edge pairs e1 and e2 are defined as including cent_pidx (order
            # irrelevant), then e3 is the remaining edge pair
            cent_pidx = np.flatnonzero(tris_touched[tidx,:]).tolist()
            e3 = FULL_SET.difference(cent_pidx)
            other_idx = list(e3)
            e1 = set(cent_pidx + [other_idx[0]])
            e2 = set(cent_pidx + [other_idx[1]])

            # Match the edge pairs to the order in which edges were calculated 
            # earlier 
            e1_idx, e2_idx, e3_idx = [ np.flatnonzero(
                [ e == ei for ei in EDGE_INDEXING ]
                ) for e in [e1, e2, e3] ] 

            # And finally load the edges in the correct order 
            L12 = edge_lengths[tidx,e3_idx]
            L01 = edge_lengths[tidx,e1_idx]
            L02 = edge_lengths[tidx,e2_idx]

            # Angles 
            alpha = (np.arccos((np.square(L01) + np.square(L02) - np.square(L12)) 
                        / (2*L01*L02)))
            beta  = (np.arccos((np.square(L01) + np.square(L12) - np.square(L02)) 
                        / (2*L01*L12)))
            gamma = (np.arccos((np.square(L02) + np.square(L12) - np.square(L01))
                        / (2*L02*L12)))
            angles = np.array([alpha, beta, gamma])

            # Area if not obtuse
            if not np.any((angles > np.pi/2)): # Voronoi
                a = ((np.square(L01)/np.tan(gamma)) + (np.square(L02)/np.tan(beta))) / 8
            else: 
                # If obtuse, heuristic approach
                area_t = 0.5 * np.linalg.norm(np.cross(edges[tidx,0,:], edges[tidx,1,:]))
                if alpha > np.pi/2:
                    a = area_t / 2
                else:
                    a = area_t / 4

            vtx_tri_areas[pidx,tidx] = a 

    return vtx_tri_areas.tocsr()

def _vtx_tri_weights(points, tris, cores=mp.cpu_count()):
    """
    Form a matrix of size (n_vertices x n_tris) where element (I,J) corresponds
    to the area of triangle J belonging to vertex I. 
    Areas are calculated according to the definition of A_mixed in "Discrete 
    Differential-Geometry Operators for Triangulated 2-Manifolds", M. Meyer, 
    M. Desbrun, P. Schroder, A.H. Barr.
    
    This code has been copied with limited adaptation from Tom Kirk's 
    implementation in Toblerone. This will soon be unnessecary when we discover 
    the conflict between igl and toblerone.

    Args: 
        surf: Surface object 
        cores: number of CPU cores to use, default max 
    Returns: 
        sparse CSR matrix, size (n_points, n_tris) where element I,J is the 
            area of triangle J belonging to vertx I 
    """

    edges = np.stack([points[tris[:,1],:] - points[tris[:,0],:],
                      points[tris[:,2],:] - points[tris[:,0],:],
                      points[tris[:,2],:] - points[tris[:,1],:]], axis=1)
    edge_lengths = np.linalg.norm(edges, axis=2)
    worker_func = functools.partial(__meyer_worker, points, tris, 
                                    edges, edge_lengths)

    if cores > 1: 
        worker_lists = _distributeObjects(range(points.shape[0]), cores)
        with mp.Pool(cores) as p: 
            results = p.map(worker_func, worker_lists)

        # Flatten results back down 
        vtx_tri_weights = results[0]
        for r in results[1:]:
            vtx_tri_weights += r 

    else: 
        vtx_tri_weights = worker_func(range(points.shape[0]))

    assert (vtx_tri_weights.data > 0).all(), 'Zero areas returned'
    return vtx_tri_weights 

def mayer_area(v, f):
    a = _vtx_tri_weights(v, f)
    a = sparse.diags(np.squeeze(np.asarray(a.sum(axis=1))))
    return a

def get_mass_matrix(v, f, area_type):
    if (area_type == 'voronoi') or (area_type == 'barycentric'):
        return igl.massmatrix(v, f, AREA_TYPES[area_type])
    elif area_type == 'mayer':
        return mayer_area(v, f)
    else:
        raise ValueError("Please choose one of the supported mass"
                        +f" matrix types:{list(AREA_TYPES.keys())}")