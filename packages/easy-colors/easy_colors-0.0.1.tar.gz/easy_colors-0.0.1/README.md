# Easy Colors

This package allows you to print colored text in the console using ANSI escape codes.

# Installation

Install on Linux/MacOS:
`python3 -m pip install easy_colors`

Install on Windows:
`python -m pip install easy_colors`

# Usage
```python
from easy_colors import Colors

print(f'{Colors.INFO}This is an example{Colors.END}')

print(f'{Colors.DANGER}This is another example{Colors.END}')

```

Note: Make sure to end all colored strings with `Colors.END`