#!/usr/bin/env python3

import sys
import argparse
import re

import yaml
import pyotp
import pyperclip
from fuzzywuzzy import process


def cli_parse():
    parser = argparse.ArgumentParser(description='Generate One-time Password')
    parser.add_argument('provider',
                        nargs='?',
                        type=str,
                        help='fuzzy search provider names',
                        metavar='P')
    parser.add_argument('-a',
                        '--account',
                        type=str,
                        help='fuzzy search account names',
                        metavar='A')
    parser.add_argument('-c',
                        '--no-clip',
                        action='store_true',
                        help='if set, do not use clipboard')

    args = parser.parse_args()

    if args.provider is None and args.account is None:
        parser.print_help(sys.stderr)
        parser.error("'P' and/or 'A' required, see usage")

    return args


class Searchable:
    def __init__(self, name):
        self.name = name
        self.alias_set = {self.name}
        self.sanitized_name = self.sanitize_name()
        self.add_alias(self.sanitized_name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '%s %s' % (type(self), self.sanitized_name)

    def add_alias(self, alias):
        self.alias_set.add(alias)

    def sanitize_name(self):
        pattern = re.compile(r'[\W_]+')
        alias = pattern.sub('', self.name).lower()
        return alias

    def fuzzy(self, query):
        matches = process.extract(query, list(self.alias_set))
        match_ratio = max([x[1] for x in matches])
        return (self, match_ratio)


class Provider(Searchable):
    def __init__(self, name):
        super(Provider, self).__init__(name)
        self.accounts = list()

    def __iter__(self):
        return iter(self.accounts)

    def add_account(self, account):
        self.accounts.append(account)


class Account(Searchable):
    def __init__(self, name, provider, token):
        super(Account, self).__init__(name)
        self.provider = provider
        self.__token = token

    def gen_otp(self, no_copy):
        self.otp = pyotp.TOTP(self.__token).now()
        if not no_copy:
            pyperclip.copy(self.otp)

    def __str__(self):
        account_str = (str(self.provider) + '\n'
                       + self.name + '\n'
                       + self.otp)
        return account_str


def fuzzy_match(choices, query):
    best_match = (None, 55)
    for choice in choices:
        match = choice.fuzzy(query)
        if match and match[1] > best_match[1]:
            best_match = match
    return best_match[0]


def load_otp_yaml(yaml_doc):
    providers = list()
    for provider in yaml_doc.keys():
        provider_obj = Provider(provider)
        if 'alias' in yaml_doc[provider]:
            provider_obj.add_alias(yaml_doc[provider]['alias'])
        for account in yaml_doc[provider]['accounts']:
            account, token = list(account.items())[0]
            account_obj = Account(account, provider_obj, token)
            provider_obj.add_account(account_obj)
        providers.append(provider_obj)
    return providers


def main():
    args = cli_parse()
    yaml_doc = yaml.safe_load(sys.stdin.read())

    providers = load_otp_yaml(yaml_doc)
    accounts = [a for p in providers for a in p]

    if args.provider is not None:
        provider_match = fuzzy_match(providers, args.provider)
        if provider_match is None:
            sys.exit("No Match For: " + args.provider)
        accounts = provider_match.accounts

    if args.account is not None:
        account_match = fuzzy_match(accounts, args.account)
        if account_match is None:
            sys.exit("No Match For: " + args.account)
    else:
        account_match = accounts[0]

    account_match.gen_otp(args.no_clip)
    print(str(account_match))


if __name__ == "__main__":
    main()

