import argparse






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some inputs.')
    # parser.add_argument('-f', type=string,
    #                     help='an integer for the accumulator')
    parser.add_argument('--fuzzy', type=int, default=0,
                        help='fuzzy match groups within N milliseconds')

    args = parser.parse_args()
    print(args)
