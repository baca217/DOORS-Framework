import sklearn_sims as sk

def comp(command):
    sk.compare_command(command)

def main():
    comp("homie what's the weather like today")

if __name__ == "__main__":
    main()
