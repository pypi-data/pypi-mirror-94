""" Core module with CLI """
import click
from pprint import pprint
from ldap3 import Server, Connection, ALL, NTLM

@click.group()
def main():
    """
    PCTap is a cli tool for getting computers from LDAP servers.
    It's a cli wrapper around the ldap3 module.
    https://ldap3.readthedocs.io/en/latest/index.html

    Format: pctap command server search-string username password

    Example: pctap get-pc-list group.com \\
            'OU=Ansible,OU=Servers,OU=Location,DC=Group,DC=com' \\
            'CR\ansible_svc' 'password'
    """

@main.command()
@click.option("--helptext", is_flag=True, help="Print extra help")
def more_help(helptext):
    """ Carious help options for usage information """
    result = "Use --help to view usage"
    if helptext:
        result = print_more_help()
    print(result)


@main.command("get-pc-list", short_help="Get a list of computers")
@click.argument("server")
@click.argument("search-string")
@click.argument("username")
@click.argument("password")
def get_pc_list(server, search_string, username, password):
    """ Uses the ldap3 module to get list of computers from OU """
    lsrv = Server(server, port=636, use_ssl=True)
    conn = Connection(lsrv, user=username, password=password, authentication=NTLM)
    conn.bind()
    conn.search(search_string, '(&(objectclass=computer))')
    data = conn.entries
    pc_list = []
    for entry in data:
        dn_entry = entry.entry_dn.split(",")
        pc = dn_entry[0][3:]
        pc_list.append(pc)
    pprint(pc_list)
    return pc_list


def print_more_help():
    """ Prints help message """
    help_text = """
    This is more help TODO

    """
    return help_text


if __name__ == "__main__":
    main()
