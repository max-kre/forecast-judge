import random

def main():
    adjectives = [
        "amazing",
        "fabulous",
        "eye-opening",
        "devastating",
        "thrilling",
        "exuberant",
        "flamboyant",
        "gimmicked",
        "fancified",
        "grandiose",
        "tectonic"
    ]

    nouns = [
        "Equilibrium",
        "Blasphemy",
        "Bumblebee",
        "Kaleidoscope",
        "Plebeian",
        "Zigzag",
        "Alligator",
        "Sparkplug",

    ]

    adj = random.randint(0, len(adjectives)-1)
    noun = random.randint(0, len(nouns)-1)

    return "The {} {} project".format(adjectives[adj], nouns[noun])

if __name__ == "__main__":
    print(main())

