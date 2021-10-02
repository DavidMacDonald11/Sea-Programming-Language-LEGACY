def begin_interfacing(debug):
    print("Sea Programming Language")

    try:
        while True:
            buffer = input("sea > ")

            if buffer == "exit":
                raise Exit()

            print(buffer)
    except (KeyboardInterrupt, EOFError):
        print()
    except Exit:
        pass

class Exit(Exception):
    pass
