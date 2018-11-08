import argparse
from forge import AlphaGenerator, AnovaGenerator, RegressionGenerator

def build_arg_parser():
    parser = argparse.ArgumentParser(prog='survey-forge')
    parser.add_argument('-n', '--num-respondents', type=int, default=20,
                        help='Number of respondents to the survey', metavar='num')
    parser.add_argument('-f', '--output-file', type=str, default="output.csv",
                        help='File to write final data set to', metavar='path')

    sub_parsers = parser.add_subparsers()
    anova_parser = sub_parsers.add_parser('anova')
    anova_parser.add_argument('-g', '--num-groups', type=int, default=5, metavar='num',
                              help='Number of groups')
    anova_parser.add_argument('-f', '--f-stat', type=float, default=1.5, metavar='float',
                              help='The F-statistic of the resulting data')
    anova_parser.add_argument('-s', '--scale', type=int, default=20, metavar='num',
                              help='Scale for the group means')
    anova_parser.set_defaults(func=run_anova)

    alpha_parser = sub_parsers.add_parser('alpha')
    alpha_parser.add_argument('-i', '--num-items', type=int, default=40, metavar='num',
                              help='Number of items in the survey')
    alpha_parser.add_argument('-s', '--scale', type=int, default=5, metavar='num',
                              help='Number of points in the Likert scale for each item')
    alpha_parser.add_argument('-a', '--coeff-alpha', type=float, default=0.80, metavar='float',
                              help='Cronbach\'s alpha for the resulting survey data')
    alpha_parser.add_argument('-t', '--alpha-tol', type=float, default=0.05, metavar='float',
                              help='Tolerance for Cronbach\'s alpha')
    alpha_parser.set_defaults(func=run_alpha)

    reg_parser = sub_parsers.add_parser('regression')
    reg_parser.add_argument('-s', '--scales', type=int, nargs='+', metavar='num', required=True,
                            help='Scale for each predictor feature [0, num]. The number of features will be infered from this list')
    reg_parser.add_argument('-t', '--target-scale', type=int, default=1, metavar='num',
                            help='Scale for the target column')
    reg_parser.add_argument('-b', '--norm-betas', type=float, nargs='+', metavar='float', required=True,
                            help='Normalized regression weights, must be same length as --scales')
    reg_parser.add_argument('-d', '--betas-tol', type=float, nargs='+', metavar='float', required=True,
                            help='Tolerance for the regression weights, must be same length as --scales')
    reg_parser.set_defaults(func=run_regression)
    
    return parser

def run_anova(args):
    print(args)
    generator = AnovaGenerator(vars(args))
    print(generator)
    generator.generate_data()

def run_alpha(args):
    generator = AlphaGenerator(vars(args))
    print(generator)
    generator.generate_data()
    print(generator.calc_coeff_alpha())
    generator.write()

def run_regression(args):
    generator = RegressionGenerator(vars(args))
    print(generator)
    generator.generate_data()
    generator.write()

def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    if 'func' in vars(args):
        args.func(args)
    else:
        print("Subcommand not specified, use -h for help")

if __name__ == '__main__':
    main()

