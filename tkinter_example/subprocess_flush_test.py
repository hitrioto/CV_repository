import contextlib
import subprocess
import os

# Unix, Windows and old Macintosh end-of-line
newlines = ["\n", "\r\n", "\r"]


def unbuffered(proc, stream="stdout"):
    stream = getattr(proc, stream)
    with contextlib.closing(stream):
        while True:
            out = []
            last = stream.read(1)
            # Don't loop forever
            if last == "" and proc.poll() is not None:
                break
            while last not in newlines:
                # Don't loop forever
                if last == "" and proc.poll() is not None:
                    break
                out.append(last)
                last = stream.read(1)
            out = "".join(out)
            yield out


def example():
    # pyinstaller --onefile simulation.py
    cmd1 = os.path.join("tkinter_example", "dist", "simulation.exe")
    cmd2 = ["python", os.path.join("tkinter_example", "simulation.py")]

    proc = subprocess.Popen(
        cmd1,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        # Make all end-of-lines '\n'
        universal_newlines=True,
    )
    for line in unbuffered(proc):
        print(line)


example()
