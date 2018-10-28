import argparse
from forge import AlphaGenerator

def build_arg_parser():
    parser = argparse.ArgumentParser(prog='survey-forge')
    parser.add_argument('-n', '--num-respondents', type=int, default=20,
                        help='Number of respondents to the survey', metavar='num')
    parser.add_argument('-i', '--num-items', type=int, default=40,
                        help='Number of items in the survey', metavar='num')
    parser.add_argument('-f', '--output-file', type=str, default="output.csv",
                        help='File to write final data set to', metavar='path')

    sub_parsers = parser.add_subparsers()
    alpha_parser = sub_parsers.add_parser('alpha')
    alpha_parser.add_argument('-s', '--scale', type=int, default=5, metavar='num',
                              help='Number of points in the Likert scale for each item')
    alpha_parser.add_argument('-a', '--coeff-alpha', type=float, default=0.80, metavar='float',
                              help='Cronbach\'s alpha for the resulting survey data')
    alpha_parser.add_argument('-t', '--alpha-tol', type=float, default=0.05, metavar='float',
                              help='Tolerance for Cronbach\'s alpha')
    
    return parser

def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    generator = AlphaGenerator(vars(args))
    print(generator)
    generator.generate_data()
    print(generator.calc_coeff_alpha())
    generator.write(vars(args)['output_file'])

if __name__ == '__main__':
    main()
