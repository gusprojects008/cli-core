## Implementar/adicionar
* Adaptar setup para se basear em projeto que utilizam pyproject.toml

## Explicando a ideia por trás da arquitetura do template de aplicações cli/tui python:
app.py: Módulo auxiliar que permite aplicações definirem configurações do app, a variável de configuração final do app será passada para classe Context, que será responsável por definir variáveis relacionadas ao ambiente e contexto de execução do app, e assim, ela irá também incluir a variável de configuração do app "config" dentro desse Context. Esse context deverá ser acessível por funções/funcionalidades dentro de Operations, para assim, elas poderem acessar variáveis de configuração do app, tanto as padrões como as personalizadas que o app adicionou na variável AppConfig que ele definiu através do dataclass cli_core.app.Config.

app.bootstrap: É a função responsável por receber o AppConfig que a aplicação principal definiu através do dataclass cli_core.app.Config, e então acessar e tentar utilizar as variáveis padrões dela para realizar operações básicas como checar dependencias de módulos ou do sistema que a função make_config do app principal definiu (ou não) para a variável config que ele construi utilizado o dataclass cli_core.app.Config, além disso, ele irá obter e verificar se a variável argparse foi definida em config, se tiver, define logging_config e passa logging_config para setup_logging. Caso contrário apenas faz o setup_logging. No fim, ele irá definir a instancia de Context passando a variável config, e irá passar a variável de context para Operations. E então irá retornar BootstrapResult.

A questão é como irei permitir o usuário utilizar a classe operations como base para definir suas própria operações/funcionalidades. Essa ideia de classe "Operations" é escalável? e se o app quiser fornecer classes como funcionalidades para as aplicações? lembrando que a ideia é que Operations seja utilzado tanto por CLI quanto por TUI.

Não faz mais sentido que a classe Operations de cli_core.app seja algo como por exemplo:
class Operations:
    def __init__(self, context):
        self.ctx = context

        self.profiles_manager = ProfilesManager(self.ctx.config_dir, self.ctx.config_file_path)
        self.wpa_manager = WPAProcessManager()
        self.dhcpcd_manager = DHCPCDProcessManager()

        self.dispatch_table = {
            "start": lambda args: self.start(
                background=args.background,
                sleep_time=args.sleep,
            ),
            "scan": lambda args: self.scan(
                ifname=args.ifname,
                output_filename=args.output,
            ),
            "create-profile": lambda args: self.create_profile(),
            "remove-profile": lambda args: self.profiles_manager.remove_profile(args.ifname),
            "remove-profiles": lambda args: self.profiles_manager.remove_all_profiles(),
            "list-profiles": lambda args: self.profiles_manager.list_profiles(),
            "list-interfaces": lambda args: self.list_interfaces(),
        }

    def dispatch(self):
        args = self.ctx.config.get("argparse").get("args")
        handler = self.dispatch_table.get(args.command)
        if not handler:
            raise ValueError(f"Unknown command: {args.command}")
        return handler(args)
 


Mas fornecendo métodos que permitem fazer algo como o registro de uma callback/funconalidade para operations? se for uma classe, então essa classe pode herdar também a própria instância de Operations ou algo assim caso seja necessário.


Meu problema agora é como 

Operations do app específico irá utiliza BaseOperations de cli_core.
