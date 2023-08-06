import os
import json
import re
import click
import yaml


from .ethz_iam import ETH_IAM_conn
from .verbose import VERBOSE


class Service():
    def __init__(self, conn, data):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])


def _load_configuration(paths, filename='.ethz_iam_webservice'):
    if paths is None:
        paths = [os.path.expanduser("~")]

    # look in all config file paths
    # for configuration files and load them
    admin_accounts = []
    for path in paths:
        abs_filename = os.path.join(path, filename)
        if os.path.isfile(abs_filename):
            with open(abs_filename, 'r') as stream:
                try:
                    config = yaml.safe_load(stream)
                    for admin_account in config['admin_accounts']:
                        admin_accounts.append(admin_account)
                except yaml.YAMLError as e:

                    print(e)
                    return None

    return admin_accounts


def login(admin_username=None, admin_password=None, hostname="https://iam.passwort.ethz.ch"):
    hostname = hostname
    endpoint_base = "/iam-ws-legacy"

    config_path = os.path.join(
        os.path.expanduser("~"),
        '.ethz_iam'
    )
    if os.path.exists(config_path):
        import configparser
        raise Exception("not yet implemented")

    if admin_username is None:
        admin_username = input(
            "Enter the admin username: ")

    if admin_password is None:
        import getpass
        admin_password = getpass.getpass(
            "Enter the password for admin user {}".format(admin_username))

    return ETH_IAM_conn(admin_username, admin_password, hostname, endpoint_base)


def get_username_password(ctx):

    if ctx.obj['username'] is None:
        ctx.obj['username'] = os.environ.get('IAM_USERNAME', '') \
            or click.prompt(
            text='Username',
            default=os.environ.get('USER', ''),
            show_default=True,
        )

    if ctx.obj['password'] is None:
        ctx.obj['password'] = os.environ.get('IAM_PASSWORD', '') \
            or click.prompt(text='Password', hide_input=True)


@click.command()
@click.argument('person')
@click.option('-i', '--info',
              is_flag=True,
              default=True,
              help='all information about the person',
              )
@click.pass_context
def person(ctx, person, info):
    get_username_password(ctx)

    e = login(ctx.obj['username'], ctx.obj['password'], ctx.obj['hostname'])
    person = e.get_person(person)

    print(json.dumps(person.data, indent=4, sort_keys=True))


@click.command()
@click.argument('user')
@click.option('-d', '--delete',
              is_flag=True,
              help='delete this user'
              )
@click.option('-i', '--info',
              is_flag=True,
              help='all information about the user',
              )
@click.option('-g', '--grant-service',
              multiple=True,
              help='grant a service to this user, e.g. AD, LDAPS, VPN. Use this option for every service you want to grant'
              )
@click.option('-r', '--revoke-service',
              multiple=True,
              help='revoke a service from this user, e.g. AD, LDAPS, VPN. Use this option for every service you want to revoke'
              )
@click.option('--set-password',
              is_flag=True,
              help='set the password for that user. Use -s to specify for which service(s)',
              )
@ click.option('-s', '--service',
               multiple=True,
               help='specify the service you want to set the password for',
               )
@click.option('-sp', '--service-password',
              help='set a password for the given service. Use the --service option to specify the service.',
              )
@ click.pass_context
def user(ctx, user, delete, info, grant_service=None, revoke_service=None, set_password=None, service_password=None, service=None):
    get_username_password(ctx)
    e = login(ctx.obj['username'], ctx.obj['password'], ctx.obj['hostname'])
    user = e.get_user(user)

    if delete:
        click.confirm(
            'Do you really want to delete this user?', abort=True)
        user.delete()

    elif grant_service:
        for service_name in grant_service:
            user.grant_service(service_name)

    elif revoke_service:
        for service_name in revoke_service:
            user.revoke_service(service_name)

    elif service_password or set_password:
        if not service_password:
            service_password = click.prompt(
                text='Service Password', hide_input=True
            )
        if service:
            for s in service:
                try:
                    user.set_password(
                        password=service_password,
                        service_name=s
                    )
                    print(f"successfully set password for service {s}")
                except ValueError as err:
                    print(err)
        elif 'services' in user.data:
            for service in user.data['services']:
                try:
                    user.set_password(
                        password=service_password,
                        service_name=service['name']
                    )
                    print("successfully set password for service {}".format(
                        service['name']))
                except ValueError as err:
                    print(err)
    else:
        print(json.dumps(user.data, indent=4, sort_keys=True))


@ click.command()
@ click.argument('group')
@ click.option('-d', '--delete',
               is_flag=True,
               help='delete this group'
               )
@ click.option('-m', '--members',
               is_flag=True,
               help='show members of the group',
               )
@ click.option('-i', '--info',
               is_flag=True,
               default=True,
               help='all information about the group',
               )
@ click.option('-a', '--add',
               help='username to add to group. Can be used multiple times: -a us1 -a us2',
               multiple=True
               )
@ click.option('-r', '--remove',
               help='username to remove from group. Can be used multiple times: -r us1 -r us2',
               multiple=True
               )
@ click.pass_context
def group(ctx, group, delete, members, info, add=None, remove=None):
    """group modifications.
    """
    if add is None:
        add = ()
    if remove is None:
        remove = ()

    get_username_password(ctx)

    e = login(ctx.obj['username'], ctx.obj['password'],ctx.obj['hostname'])
    group = e.get_group(group)

    if add:
        group.add_members(*add)
    if remove:
        group.del_members(*remove)

    if add or remove or members:
        print(json.dumps(group.members))
        return

    if delete:
        click.confirm(
            'Do you really want to delete this group?', abort=True)
        group.delete()
        return

    print(json.dumps(group.data, indent=4, sort_keys=True))



# default=os.environ.get('NEO4J_HOSTNAME')
# @click.option('--password', prompt=True, hide_input=True,
#    help='password of your ETHZ IAM admin account')
@ click.group()
@ click.option('-u', '--username',
               help='username of your ETHZ IAM admin account (if not provided, it will be prompted)')
@ click.option('--password',
               help='password of your ETHZ IAM admin account (if not provided, it will be prompted)')
@ click.option('-h', '--host',
               default="iam.passwort.ethz.ch",
               help="default: iam.passwort.ethz.ch"
               )
@ click.pass_context
def cli(ctx, host, username, password=None):
    """ETHZ IAM command-line tool.
    """
    ctx.ensure_object(dict)
    if not host.startswith('https://'):
        host = 'https://' + str(host)
    ctx.obj['hostname'] = host
    ctx.obj['username'] = username
    ctx.obj['password'] = password


cli.add_command(group)
cli.add_command(user)
cli.add_command(person)

if __name__ == '__main__':
    cli()
