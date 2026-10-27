"""Starting point of the program. Run it with: python3 main.py"""

# Import the function that starts the calculator's command-line loop
from app.calculator import run_repl

# This only runs when you start this file directly (not when it is imported)
if __name__ == "__main__":
    run_repl()