# *Ez* cliy
A hassle-free framework for creating command line tools

## Install

from PyPi
```
pip3 install ezcliy
```

or from directly from Github
```
pip3 install git+https://github.com/kpostekk/ezcliy.git
```

More details in [docs](https://ezcliy.readthedocs.io/en/latest/)

## Fast example

```python
from ezcliy import Command, Flag  # Import required classes


class SmallTextProcessor(Command):
    # Define excpected parameters
    capitalize = Flag('-c', '--capitalize')
    verbose = Flag('--verbose')

    def invoke(self):  # There put your sweet code
        string = ' '.join(self.values)

        if self.verbose:
            print('Verbose stuff', self.parameters, self.values)

        if self.capitalize:
            string = string.capitalize()

        if not string.endswith('.'):
            string += '.'

        print(string)


if __name__ == '__main__':
    SmallTextProcessor().cli_entry()

```

The exec of that will look like this

```
./somescript.py "this sentence require cap" -c --verbose
```

And output will be

```
Verbose stuff {'capitalize': <Flag -c --capitalize has value True>, 'verbose': <Flag --verbose has value True>} ['this sentence require cap']
This sentence require cap.
```