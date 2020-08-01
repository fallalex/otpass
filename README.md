# otpass

This script accepts a TOTP token file over stdin, from a tool like
[Pass](https://www.passwordstore.org/). Using a combination of aliases
and fuzzy search to find the one-time password to generate then place in
the clipboard.

With longer provider names having an alias is helpful `aws` =\> `Amazon
Web Services`. Most providers will only have one account with TOTP,
making an alias for accounts less valuable. Rather than completion this
script uses fuzzy search for providers and account descriptions. The
combination of fuzzy search and aliases is more powerful in many ways
and less distracting when compared to completion.

There are tools that fill this role like
[pass-otp](https://github.com/tadfisher/pass-otp). I hope this
alternative's helps others, as it has me.

Here are some examples:

    $ otpass go
    Google
    abc@gmail.com
    439013

    $ otpass go -a 1
    Google
    123@gmail.com
    946887

    $ otpass -a ro ams
    Amazon Web Services
    root
    200685

    $ otpass am
    Amazon
    abc@gmail.com
    916049

The structure of the YAML file follows the example below, `alias` is
optional the rest are required. The YAML file should be encrypted, how
is up to the user.

    Amazon:
      accounts:
        - abc@gmail.com: EJCO324TR4KCPSGR
    Amazon Web Services:
      alias: aws
      accounts:
        - myuser: GZBTHCYO5DWMHVMI
        - root: EQF5MDZFBUTFM4AD
    GitHub:
      accounts:
        - example@email.com: V7VU5M336VMW7ZQX
        - abc@gmail.com: X5IPLL76KTEKP24J
    Google:
      accounts:
        - abc@gmail.com: G654U2GGSO3T4RSI
        - 123@gmail.com: KILLKXQT3W56M66L

Below is an example of piping the YAML token file to the script and
making an alias to the command for ease of use. This would be added to
`.bash_profile` or `.zshrc`.

    alias otpass="pass otp.yaml | otpass.py"

    usage: otpass.py [-h] [-c] [-a ACCOUNT] [Q]

    positional arguments:
      Q                     fuzzy search provider names

    optional arguments:
      -h, --help            show this help message and exit
      -c, --no-clip         do not put result into clipboard
      -a ACCOUNT, --account ACCOUNT
                            fuzzy search account names

## Dependencies

  - [yaml](https://pyyaml.org/)
  - [pyotp](https://github.com/pyauth/pyotp)
  - [pyperclip](https://github.com/asweigart/pyperclip)
  - [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)

## Install

All the external requirements are easy to install with pip, for other
methods refer to their docs.

    pip install yaml
    pip install pyotp
    pip install pyperclip
    pip install fuzzywuzzy[speedup]

  - ideas for expansion
      - save fuzzy match results to speed up subsequent runs
  - Continuous Integration
      - Travis CI
      - Jenkins
  - [PyPI](https://pypi.org/)
      - [tutorial](https://packaging.python.org/tutorials/packaging-projects/)
  - Github
      - README
      - first commit
      - banners for coverage and builds
  - testing
      - [tox](https://github.com/tox-dev/tox)
      - [pyflakes](https://github.com/PyCQA/pyflakes)
      - [pydocstyle](https://github.com/PyCQA/pydocstyle)
      - [pycodestyle](https://github.com/PyCQA/pycodestyle)
      - [pytest](https://github.com/pytest-dev/pytest/)
      - [hypothesis](https://github.com/HypothesisWorks/hypothesis)
      - [radon](https://github.com/rubik/radon)
  - documentation
      - [sphinx](https://github.com/sphinx-doc/sphinx/)
