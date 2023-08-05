import sys
from os.path import expanduser, basename
import argparse
from configparser import ConfigParser
from ldap3.core.exceptions import LDAPOperationsErrorResult

from .utils import (n2sn_list_group_users_as_table,
                    n2sn_list_user_search_as_table)
from .ldap import ADObjects

from . import __version__

sys.tracebacklimit = 0

config_files = ['/etc/n2sn_tools.conf',
                expanduser('~/.config/n2sn_tools.conf')]


def base_argparser(description, default_inst=True):
    parser = argparse.ArgumentParser(
        prog=basename(sys.argv[0]),
        description=description
    )

    parser.add_argument('--version', action='version',
                        version=('%(prog)s v' + __version__))

    if default_inst:
        parser.add_argument(
            '-i', '--instrument', '--beamline', dest='instrument',
            action='store', help='Name of N2SN instrument',
            default=None
        )

    return parser


def read_config(parser, instrument=None, no_inst=False):
    config = ConfigParser()

    config.read(config_files)

    if 'common' not in config:
        print(parser.error(
            "Section 'common' missing from config file."))

    if no_inst is False:
        if instrument is None:
            if 'default_instrument' not in config['common']:
                print(parser.error(
                    "'default_instrument' not defined in config file. "
                    "Please specify on command line"))

            instrument = config['common']['default_instrument']

        if instrument not in config:
            print(parser.error("instrument '{}' is not "
                                "defined in the config file.".format(instrument)))

        return config['common'], config[instrument]

    else:
        return config['common'], None


def n2sn_list(desc, message, group_name):
    parser = base_argparser(
        'List current enabled users for an instrument', True
    )

    args = parser.parse_args()

    common_config, config = read_config(parser, args.instrument)

    print("\n{} for instrument {}\n"
          .format(message, config['name'].upper()))

    print(n2sn_list_group_users_as_table(
          common_config['server'],
          common_config['group_search'].strip('"'),
          common_config['user_search'].strip('"'),
          config[group_name]))


def n2sn_list_users():
    n2sn_list(
        'List current enabled users for an instrument',
        'Current users enabled',
        'user_group'
    )


def n2sn_list_staff():
    n2sn_list(
        'List current beamline staff for an instrument',
        'Current instrument staff',
        'staff_group'
    )


def n2sn_change_user(operation):
    parser = base_argparser('Add or remove user to/from instrument users list')

    user_group = parser.add_mutually_exclusive_group()
    user_group.add_argument(
        '-u', '--username', dest='username', action='store',
        help='Username of user',
    )
    user_group.add_argument(
        '-n', '--life-number', dest='life_number', action='store',
        help='Life number of guest number of user',
    )

    args = parser.parse_args()

    if (args.username is None) and (args.life_number is None):
        print(parser.error("You must specify the user by either"
                           " username or life/guest number"))

    common_config, inst_config = read_config(parser, args.instrument)

    with ADObjects(common_config['server'],
                   common_config['group_search'].strip('"'),
                   common_config['user_search'].strip('"')) as ad:

        # Get the beamlie group
        group = ad.get_group_by_samaccountname(inst_config['user_group'])
        if len(group) != 1:
            raise RuntimeError("Unable to find correct group for users")

        if args.username is not None:
            user = ad.get_user_by_samaccountname(args.username)
            if len(user) == 0:
                raise RuntimeError("Unable to find user {}, please check."
                                   .format(args.username))
            if len(user) != 1:
                raise RuntimeError("Username {} is not unique. Please check."
                                   .format(args.username))

        if args.life_number is not None:
            user = ad.get_user_by_id(args.life_number)
            if len(user) == 0:
                raise RuntimeError("Unable to find user with life/guest"
                                   " number {}, please check."
                                   .format(args.life_number))
            if len(user) != 1:
                raise RuntimeError("Life/Guest number {} is not unique."
                                   " Please check."
                                   .format(args.life_number))

        group = group[0]
        user = user[0]

        if operation == "add":
            try:
                ad.add_user_to_group_by_dn(group['distinguishedName'],
                                           user['distinguishedName'])
            except LDAPOperationsErrorResult:
                raise RuntimeError("Error adding user to group, "
                                   "check you have the correct "
                                   "permission.") from None

            print("\nSucsesfully added user \"{}\" to list of users"
                  " for instrument {}\n"
                  .format(user['displayName'], inst_config['name'].upper()))

        if operation == "remove":
            try:
                ad.remove_user_from_group_by_dn(group['distinguishedName'],
                                                user['distinguishedName'])
            except LDAPOperationsErrorResult:
                raise RuntimeError("Error removing user from group, "
                                   "check you have the correct "
                                   "permission.") from None

            print("\nSucsesfully removed user \"{}\" from list of users"
                  " for instrument {}\n"
                  .format(user['displayName'], inst_config['name'].upper()))


def n2sn_add_user():
    n2sn_change_user('add')


def n2sn_remove_user():
    n2sn_change_user('remove')


def n2sn_search_user():

    parser = base_argparser(
        'Add user to instrument users list',
        False
    )

    parser.add_argument(
        '--surname', dest='surname', action='store',
        help='Username of user',
    )

    parser.add_argument(
        '--givenname', dest='givenname', action='store',
        help='Given name (forename) of user',
    )

    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument(
        '--guest', dest='type', action='store_const',
        const='LT',
        help='Limit to accounts that are NSLS-II guests'
    )
    type_group.add_argument(
        '--staff', dest='type', action='store_const',
        const='PS',
        help='Limit to accounts that are NSLS-II staff'
    )
    type_group.add_argument(
        '--cfn', dest='type', action='store_const',
        const='NC',
        help='Limit to accounts that are CFN staff'
    )
    type_group.add_argument(
        '--cfn-user', dest='type', action='store_const',
        const='XX',
        help='Limit to accounts that are CFN users'
    )

    args = parser.parse_args()

    common_config, inst_config = read_config(parser, no_inst=True)

    if (args.surname is None) and (args.givenname is None) and (args.type is None):
        # Thats a lot of users!
        print(parser.error("You must limit the search!"
                           " Do you really want ALL users?"))

    table = n2sn_list_user_search_as_table(
        common_config['server'],
        common_config['group_search'].strip('"'),
        common_config['user_search'].strip('"'),
        args.surname, args.givenname, args.type
    )

    print(table)
