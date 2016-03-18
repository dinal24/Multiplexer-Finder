import MultiplexPrune

# main method to start the program
def main(args):
    setGoal(map(int, list(args[1])))
    init()
    nodes = process()

    for lev in nodes:
        for n in lev:
            print(n.level)
            print(n.name+":"+str(n.parent))
        print ""

if __name__ == "__main__":
    main(sys.argv)      