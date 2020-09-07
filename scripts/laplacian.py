from surf.functions import  FUNCS
from surf.curvatures import CURVS
from surf.testing_igl import get_laplacian
import argparse
from surf.areas import AREA_TYPES

def main():
    """
    Wrapper for the `get_laplacian` function.
    """
    # argument handling
    parser = argparse.ArgumentParser(
        description="This script evaluates a given function "
                    + "on the vertices of a given surface then "
                    + "evaluates the laplacian of this. The "
                    + "results are then saved as a func.gii"
    )
    parser.add_argument(
        "surface",
        help="The surface on which to evaluate and save."
    )
    parser.add_argument(
        "-s",
        "--speed",
        help="Speed at which the function varies. Default is 1.0.",
        default=1.0,
        type=float
    )
    parser.add_argument(
        "u_name",
        help="Savename for the function evaluation's .func.gii"
    )
    parser.add_argument(
        "Lu_name",
        help="Savename for the result of the Laplacian's application "
            +"to the function, u."
    )
    parser.add_argument(
        "-m",
        "--mass_matrix",
        help="Type of mass matrix to use for the Laplacian computation. "
            +f"Choose from one of {list(AREA_TYPES.keys())}. Default is "
            +"Voronoi. "
            +"Implementation of mayer area is lightly adapted from "
            +"Tom Kirk's Toblerone module.",
        default="voronoi",
        type=str
    )
    parser.add_argument(
        "--glu_name",
        help="Savename for the result using the Graph Laplacian.",
        default=None
    )
    parser.add_argument(
        "-f",
        "--function",
        help="The function to evaluate on the given surface." 
            +"This should be one of:"
            +f"{list(FUNCS.keys())}",
        default="sumsincos",
        type=str
    )
    parser.add_argument(
        "-a",
        "--analytic",
        help="Compare against analytic curvature and save results "
            +"with the basename provided via this argument. This "
            +f"is available for {list(CURVS.keys())}. By default "
            "this is not required.",
        default=None
    )

    # parse arguments
    args = parser.parse_args()
    surface_name = args.surface
    s = args.speed
    u_name = args.u_name
    lbo_u_name = args.Lu_name
    gl_u_name = args.glu_name
    function = args.function
    mass_type = args.mass_matrix
    an_name = args.analytic

    # do work
    get_laplacian(surface_name, function, u_name, lbo_u_name, s, mass_type, gl_u_name, an_name)