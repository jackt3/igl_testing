from surf.functions import  FUNCS
from surf.testing_igl import get_laplacian
import argparse

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
        "u_name",
        help="Savename for the function evaluation's .func.gii"
    )
    parser.add_argument(
        "Lu_name",
        help="Savename for the result of the Laplacian's application "
            +"to the function, u."
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

    # parse arguments
    args = parser.parse_args()
    surface_name = args.surface
    u_name = args.u_name
    lbo_u_name = args.Lu_name
    gl_u_name = args.glu_name
    function = args.function

    # do work
    get_laplacian(surface_name, function, u_name, lbo_u_name, gl_u_name)