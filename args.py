import argparse

# Validate flag arguments expected to be booleans
def flag_bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def flag_int(v):
    try:
        int(v)
        return int(v)
    except ValueError:
        raise argparse.ArgumentTypeError('Integer value expected')

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-rt", "--tests", type=flag_bool, help="Exclusively run test methods")
    parser.add_argument("-st", "--specify_test", type=flag_int, help="Specify test to run")
    parser.add_argument("-ns", "--slack", type=flag_bool, help="Notify Slack")
    parser.add_argument("-np", "--phone", type=flag_bool, help="Notify Phone(s)")
    return parser.parse_args()
