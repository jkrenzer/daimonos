import Commands

@Commands.command("test me")
def test(hello, world="world"):
    for h in hello:
        print(h + " - " + world)

if __name__ == "__main__":
    Commands.Shell.interpret("test  me: hello = Dave Mike Seb, world =     earth")
