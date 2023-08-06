from .toppy import Toppy, ToppyArgs


def main():
    args = ToppyArgs.parse_args()
    Toppy(args).run()

if __name__ == '__main__':
    main()
