import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--coin', '-m', type=str, default='BTC', help='coin type')
@click.option('--size', '-s', type=int, default=10000, help='size of pool')
def create_kp_pool(coin, size):
    click.echo('Create pool of key pairs(%s, %s)' % (coin, size))


@click.command()
@click.option('--coin', '-m', type=str, default='BTC', help='coin type')
@click.option('--size', '-s', type=int, default=10000, help='size of pool')
def extend_kp_pool(coin, size):
    click.echo('Create pool of key pairs(%s, %s)' % (coin, size))


@click.command()
def create_mnemonic():
    click.echo('Create Mnemonic')


if __name__ == '__main__':
    cli.add_command(create_kp_pool)
    cli.add_command(create_mnemonic)
    cli.add_command(extend_kp_pool)
    cli()
