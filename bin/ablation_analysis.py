import argparse
import configparser
import pathlib

import magpie


# ================================================================================
# Main function
# ================================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Magpie patch ablation analysis')
    parser.add_argument('--scenario', type=pathlib.Path, required=True)
    parser.add_argument('--patch', type=str, required=True)
    parser.add_argument('--seed', type=int)
    args = parser.parse_args()

    # read config file
    config = configparser.ConfigParser()
    config.read_dict(magpie.bin.default_config)
    config.read(args.scenario)
    magpie.bin.pre_setup(config)

    # recreate patch
    if args.patch.endswith('.patch'):
        with open(args.patch) as f:
            args.patch = f.read().strip()
    patch = magpie.bin.patch_from_string(args.patch)

    # setup
    config['search']['algorithm'] = 'AblationAnalysis'
    magpie.bin.setup(config)
    protocol = magpie.bin.protocol_from_string(config['search']['protocol'])()
    protocol.search = magpie.bin.algo_from_string(config['search']['algorithm'])()
    protocol.search.debug_patch = patch
    protocol.program = magpie.bin.program_from_string(config['software']['program'])(config)
    protocol.setup(config)

    # run experiments
    protocol.run()
