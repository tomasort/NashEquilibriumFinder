#!/usr/bin/env python3
"""
Example script to demonstrate running tests with pytest
"""

import os
import subprocess
import sys

def run_tests():
    """Run the pytest tests"""
    print("Running Nash Equilibrium Finder tests...")
    
    # Change to the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Run pytest
    try:
        subprocess.run(["pytest", "-v"], check=True)
        print("\nTests completed successfully!")
    except subprocess.CalledProcessError:
        print("\nSome tests failed. Check the output above for details.")
        sys.exit(1)
    except FileNotFoundError:
        print("\nError: pytest not found. Please install it with 'pip install pytest'")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
