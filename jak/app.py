"""Jak is a CLI tool for encrypting files."""

import click
from .crypto_services import encrypt_file, decrypt_file, generate_256bit_key
from .version import __version_full__


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True)
def main(version):
    """(c) Dispel LLC (GPLv3)

    Jak helps you encrypt/decrypt files.

    All passwords must be exactly 32 characters so that jak can generate
    a strong enough encryption (AES256).

    Jaks intended use is for files in git repos that developers do
    not want to enter their permanent git history. But nothing prevents
    jak from being used with arbitrary files on a case by case basis.
    """

    if version:
        click.echo(__version_full__)

    # TODO if possible show help text if they just type "$> jak"


@main.command(help='jak encrypt <file> --password <pass>')
@click.argument('filename')
@click.option('-p', '--password', required=True, default=None)
def encrypt(filename, password):
    """Encrypts a file"""
    try:
        encrypt_file(key=password, filename=filename)
    except FileNotFoundError:
        click.echo('Sorry I can\'t find the file: {}'.format(filename))
    else:
        click.echo('{} - is now encrypted.'.format(filename))


@main.command(help='jak decrypt <file> --password <pass>')
@click.argument('filename')
@click.option('-p', '--password', required=True, default=None)
def decrypt(password, filename):
    """Decrypts a file"""
    try:
        decrypt_file(key=password, filename=filename)
    except FileNotFoundError:
        click.echo('Sorry I can\'t find the file: {}'.format(filename))
    else:
        click.echo('{} - is now decrypted.'.format(filename))


@main.command(help='Generate a secure password')
def genpass():
    """"""
    password = generate_256bit_key().decode()
    output = '''Here is your shiny new password. It is 32 characters (bytes) and will work just fine with AES256.


{password}

Remember to keep this password secret and save it. Without it you will NOT be able
to decrypt any file(s) you encrypt using it.
    '''.format(password=password)
    click.echo(output)

#
# TODO FUTURE
#

# @main.command()
# def protect():
#     """"""
#     click.echo("TODO")
#
#
# @main.command()
# def abandon():
#     """"""
#     click.echo("TODO")


# @main.command()
# def encrypt_all():
#     """Encrypt all protected files"""
#     click.echo("TODO")
#
#
# @main.command()
# def decrypt_all():
#     """Decrypt all protected files"""
#     click.echo("TODO")
#
#
# @main.command()
# def stomp():
#     """alias for encrypt-all"""
#     encrypt_all()
#
#
# @main.command()
# def shave():
#     """alias for decrypt-all"""
#     decrypt_all()
#
#
# @main.command()
# def unprotect():
#     """alias for abandon"""
#     click.echo("TODO")
