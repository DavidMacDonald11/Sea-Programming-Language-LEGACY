from modules.scope import indent
from modules.scope import scopes
from .error import TranspilerError

def transpile(filename):
    new_filename = filename.replace("src", "bin", 1)
    new_filename = new_filename.replace(".hea", ".h")
    new_filename = new_filename.replace(".sea", ".c")

    with open(filename) as seafile, open(new_filename, "w") as cfile:
        i = -2
        scope = 0
        scopes_end = []
        lines_in_scope = {0 : 0}

        try:
            for i, line in enumerate(seafile):
                if line.isspace():
                    continue

                new_scope = indent.get_from_line(line)

                if new_scope > scope:
                    message = f"Current scope is {scope} indents deep not {new_scope}."
                    raise scopes.IncorrectScopeError(message)

                if scope == new_scope:
                    lines_in_scope[scope] += 1
                elif new_scope < scope:
                    scopes_end = scopes.end_scope(scopes_end, new_scope, cfile)

                    if lines_in_scope[scope] < 1:
                        raise scopes.EmptyScopeError("Scope cannot be empty. Consider pass.")

                    scope = new_scope

                line = line.strip()

                if line[-1] == ":":
                    scope += 1
                    lines_in_scope[scope] = 0

                    scopes_end += scopes.match_and_transpile(line[:-1], scope, cfile)
                    continue

            scopes.end_scope(scopes_end, 0, cfile)
        except TranspilerError as e:
            print(f"Line #{i + 1}: {e.message}")
