import argparse
import math
import sys

sys.path.append("generators")
sys.path.append("helper_functions")
sys.path.append("fume")
sys.path.append("parsers")

import fume.fuzzing_engine as fe
import fume.markov_model as mm
import fume.run_target as rt
import fume.sync_manager as sm
import globals as g
import helper_functions.parse_config_file as pcf
import helper_functions.print_configuration as pc
import helper_functions.validate_fuzzing_params as vfp


def calculate_X1():
    g.X1 = 1 / g.CONSTRUCTION_INTENSITY


def calculate_X2():
    g.X2 = 1 - g.FUZZING_INTENSITY


def calculate_X3():
    g.X3 = 1 - (2 * math.log(1 + g.FUZZING_INTENSITY, 10))


def main():
    parser = argparse.ArgumentParser(description="FUME: Fuzzing MQTT Brokers")

    parser.add_argument("config_file", nargs="?", help="Path to configuration file")

    parser.add_argument(
        "-o",
        "--output",
        help="Output directory for sync data (Required for parallel mode)",
        default="fume_sync",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-M", "--master", help="Master instance name")
    group.add_argument("-S", "--secondary", help="Secondary instance name")

    args = parser.parse_args()

    # if args.secondary and args.config_file:
    #     print("Error: Secondary instances cannot use a configuration file.")
    #     exit(-1)

    if args.config_file:
        try:
            config_f = open(args.config_file, "r")
            config = config_f.readlines()
            pcf.parse_config_file(config)
            config_f.close()
        except FileNotFoundError:
            print("Could not find the supplied file: %s" % args.config_file)
            exit(-1)

    g.SYNC_DIRECTORY = args.output

    if args.master:
        g.INSTANCE_ID = args.master
        g.IS_MASTER = True
        print(f"[*] Mode: MASTER ({g.INSTANCE_ID})")
    elif args.secondary:
        g.INSTANCE_ID = args.secondary
        g.IS_MASTER = False
        print(f"[*] Mode: SECONDARY ({g.INSTANCE_ID})")
    else:
        g.INSTANCE_ID = "fuzzer01"
        g.IS_MASTER = True
        print(f"[*] Mode: STANDALONE (Defaulting to {g.INSTANCE_ID})")

    g.sync_manager = sm.SyncManager()

    if g.user_supplied_X[0] == 0:
        calculate_X1()
    if g.user_supplied_X[1] == 0:
        calculate_X2()
    if g.user_supplied_X[2] == 0:
        calculate_X3()

    vfp.validate_all()

    pc.print_configuration()

    markov_model = mm.initialize_markov_model()

    rt.run_target()

    fe.run_fuzzing_engine(markov_model)


if __name__ == "__main__":
    main()
