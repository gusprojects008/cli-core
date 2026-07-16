from cli_core.app import bootstrap
from {{ mypackage }} import app

def main():
    config = app.make_config()
    """ 
    Se for uma aplicação CLI posso definir argparse.args e argparse.parser para o resultado de config:
    parser = parse_args()
    args = parser.parse_args()
    config.argparse.parser = parser
    config.argparse.args = args
    """
    bootstrap_result = bootstrap(config)
    """
    Se for aplicação CLI, é possível fazer:
    bootstrap_result.operations.dispatch()
    """
