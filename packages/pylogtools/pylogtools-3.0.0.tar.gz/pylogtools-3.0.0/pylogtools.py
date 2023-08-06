"""
All methods in this package wrap around print, forwarding all arguments, sometimes suppressing all output
"""
import os
import contextlib

BULLET = "\u2022"
RIGHT_ARROW = "\u27f6"

def error(*args, **kwargs):
    print("\033[1;31mError\033[0m: ", end="")
    print(*args, **kwargs)

def note(*args, **kwargs):
    print("[\033[1;33mNOTE\033[0m] ", end="")
    print(*args, **kwargs)

def ok(*args, **kwargs):
    print(*args, **kwargs, end="")
    print(" [\033[1;32mOK\033[0m]")

def x(*args, **kwargs):
    print(*args, **kwargs, end="")
    print(" [\033[1;31mX\033[0m]")

def info(*args, **kwargs):
    print(f" \033[1;36m{RIGHT_ARROW}\033[0m ", end="")
    print(*args, **kwargs)

def bullet(*args, **kwargs):
    print(f"\t{BULLET} ", end="")
    print(*args, **kwargs)

def load(msg: str, func, *args, **kwargs):
    """
    Display message provided, silently execute function and report once done
    """
    info(f"{msg}...", end="", flush=True)
    rv = suppress(func, *args, **kwargs)
    print("\033[1;36mdone\033[0m!")

    return rv

def suppress(foo, *args, **kwargs):
    with open(os.devnull, "w") as devnull:
        with contextlib.redirect_stdout(devnull):
            with contextlib.redirect_stderr(devnull):
                rv = foo(*args, **kwargs)
    return rv

def abort(status: int, *args, **kwargs):
    error(*args, **kwargs)
    exit(status)

if __name__ == "__main__":
    import time

    response_time_in_seconds = 2
    mock_response = {"id": 5, "name": "Hello pylogtools"}
    mock_api_call = lambda seconds: time.sleep(seconds) or mock_response

    response = load(
        f"Imagine fetching data from an API with a response time equal to {response_time_in_seconds} seconds returning {mock_response}", 
        mock_api_call, response_time_in_seconds)

    print()
    note("That was easy")
    bullet("Print arg1", f"Return value obtained: {response}", sep="____separator____")