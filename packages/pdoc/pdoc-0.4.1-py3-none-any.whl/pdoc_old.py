import sys

def warn_old_python():
    print("Warning: pdoc itself now requires Python 3.7 or above.\n" + 
    	  "You can still document Python 3.5+ code.\n" +
          "Please upgrade your Python installation and reinstall pdoc.")
    sys.exit(1)

if __name__ == "__main__":
    warn_old_python()