
import argparse
import sys

from p4aspaces.actions import actions
from p4aspaces.actions.launch_shell_or_cmd import process_uname_arg
import p4aspaces.buildenv as buildenv

def print_dockerfile(args):
    argparser = argparse.ArgumentParser(
        description="action \"print-dockerfile\": " +
        str(actions()["print-dockerfile"]["description"]))
    argparser.add_argument("env", help="Name of the environment " +
        "of which to print the combined Dockerfile")
    argparser.add_argument("--map-to-user",
        default="root", nargs=1,\
        help="The unprivileged user which the Dockerfile should use."
        " If none is specified, defaults to unsafe root",
        dest="maptouser")
    args = argparser.parse_args(args)

    # Get user:
    if type(args.maptouser) == list:
        args.maptouser = args.maptouser[0]
    uname_or_uid = process_uname_arg(
        args.maptouser,
        complain_about_root=False
    )

    # Get environment:
    envs = buildenv.get_environments()
    env = None
    for _env in envs:
        if _env.name == args.env:
            env = _env
            break
    if env is None:
        print("p4aspaces: error: " +
            "no such environment found: '" + str(args.env) + "'",
            file=sys.stderr, flush=True)
        sys.exit(1)
    print(env.get_docker_file(add_workspace=True,
        user_id_or_name=uname_or_uid))
    sys.exit(0)
