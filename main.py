import argparse
from forge.generator import Generator

def build_arg_parser():
    parser = argparse.ArgumentParser(prog='survey-forge')
    parser.add_argument('-n', '--num-respondents', type=int, default=20,
                        help='Number of respondents to the survey', metavar='num')
    parser.add_argument('-i', '--num-items', type=int, default=40,
                        help='Number of items in the survey', metavar='num')
    parser.add_argument('-s', '--scale', type=int, default=5,
                        help='Number of points in the Likert scale for each item', metavar='num')
    parser.add_argument('-a', '--coeff-alpha', type=float, default=0.80,
                        help='Cronbach\'s alpha for the resulting survey data', metavar='float')
    
    return parser

def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    generator = Generator(vars(args))
    print(generator)
    print(generator.generate_random_data().head())
    print(generator.calc_coeff_alpha())

if __name__ == '__main__':
    main()
