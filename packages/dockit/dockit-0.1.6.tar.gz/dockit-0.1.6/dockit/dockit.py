"""
Ron's lazy CLI set
"""
import argparse
import os
import subprocess
import sys

class Dyer:

    _RESETALL = '\x1b[0m'
    _STYLE = '\x1b[{style}'

    class Style:
        NORMAL = 0
        BOLD = 1
        DARK = 2
        ITALIC = 3
        UNDERSCORE = 4
        BLINK_SLOW = 5
        BLINK_FAST = 6
        REVERSE = 7
        HIDE = 8
        STRIKE_THROUGH = 9

    class Color:
        BLACK = 0
        RED = 1
        GREEN = 2
        YELLOW = 3
        BLUE = 4
        PURPLE = 5
        CYAN = 6
        GRAY = 7

    @classmethod
    def _validate(cls, fg, bg):
        if fg is None and bg is None:
            raise ValueError('fg and bg either one of them is required.')
        if fg not in cls.Color.__dict__.values():
            raise ValueError('fg color code is out of range.')
        if bg not in cls.Color.__dict__.values():
            raise ValueError('bg color code is out of range.')

    @classmethod
    def dye(cls, fg=None, bg=None, style=None):
        cls._validate(fg=fg, bg=bg)
        style_tag = f'\x1b[{cls.Style.NORMAL};' if style is None else f'\x1b[{style};'
        fg_tag = f'30' if fg is None else f'3{fg}'
        bg_tag = '' if bg is None else f';4{bg}'
        return f'{style_tag}{fg_tag}{bg_tag}m'

    @classmethod
    def reset(cls):
        return cls._RESETALL


class Dockit:
    """
    Fuzzy the current location or appoint specific project name to
        - git
            + pull repository and all submodules

        - docker
            + launch the same prefix service with current project
            + close the same prefix service with current project
            + execute the container with the same as project

    usage: dockit.py [-h] [-a] [-p] [-l] [-c] [-u] [-d] [-e] [-s] [project]

    positional arguments:
      project               appoint specific project name

    optional arguments:
      -h, --help            show this help message and exit
      -a, --docker-attach-container
                            to keep attaching mode after docker-compose upped
      -p, --git-pull        pull git repository and all sub repositories
      -l, --docker-launch-service
                            parse project prefix and launch ${PREFIX}_service
      -c, --docker-close-service
                            parse project prefix and close ${PREFIX}_service
      -u, --docker-up-container
                            docker-compose up -d container with the same name as project
      -d, --docker-down-container
                            docker-compose down container with the same name as project
      -e, --docker-exec-container
                            docker exec -it container bash
      -s, --docker-show-containers
                            show docker processes

    You can change your service source path by setup environment variable
    export DOCKIT_ROOT='~/Documents/'
    """

    _RESET = Dyer.reset()
    _FG_RED = Dyer.dye(fg=Dyer.Color.RED)
    _BG_RED = Dyer.dye(bg=Dyer.Color.RED)

    _FG_BLUE = Dyer.dye(fg=Dyer.Color.BLUE)
    _BG_BLUE = Dyer.dye(bg=Dyer.Color.BLUE)

    _FG_CYAN = Dyer.dye(fg=Dyer.Color.CYAN)
    _BG_CYAN = Dyer.dye(bg=Dyer.Color.CYAN)

    _FG_GRAY = Dyer.dye(fg=Dyer.Color.GRAY)
    _BG_GRAY = Dyer.dye(bg=Dyer.Color.GRAY)

    _FG_GREEN = Dyer.dye(fg=Dyer.Color.GREEN)
    _BG_GREEN = Dyer.dye(bg=Dyer.Color.GREEN)

    _FG_YELLOW = Dyer.dye(fg=Dyer.Color.YELLOW)
    _BG_YELLOW = Dyer.dye(bg=Dyer.Color.YELLOW)

    _BLUE_ON_YELLOW = Dyer.dye(fg=Dyer.Color.BLUE, bg=Dyer.Color.YELLOW)
    _GRAY_ON_CYAN = Dyer.dye(fg=Dyer.Color.GRAY, bg=Dyer.Color.CYAN)
    _GRAY_ON_RED = Dyer.dye(fg=Dyer.Color.GRAY, bg=Dyer.Color.RED)
    _YELLOW_ON_RED = Dyer.dye(fg=Dyer.Color.YELLOW, bg=Dyer.Color.RED)
    _YELLOW_ON_BLUE = Dyer.dye(fg=Dyer.Color.YELLOW, bg=Dyer.Color.BLUE)

    _ROOT = os.environ.get('DOCKIT_ROOT', '~')

    _PROJECT_PATH = str()
    _PROJECT_NAME = str()
    _SERVICE_NAME = str()

    try:
        _TERMINAL_SIZE_WIDTH = os.get_terminal_size().columns
    except:
        _TERMINAL_SIZE_WIDTH = 90

    @classmethod
    def _help(cls):
        print(cls.__doc__)
        sys.exit()

    @classmethod
    def _get_args(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'project',
            help='appoint specific project name',
            type=str,
            nargs='?',
        )
        parser.add_argument(
            '-a', '--docker-attach-container',
            action='store_true',
            help='to keep attaching mode after docker-compose upped',
        )
        parser.add_argument(
            '-p', '--git-pull',
            action='store_true',
            help='pull git repository and all sub repositories',
        )
        parser.add_argument(
            '-l', '--docker-launch-service',
            action='store_true',
            help='parse project prefix and launch ${PREFIX}_service',
        )
        parser.add_argument(
            '-c', '--docker-close-service',
            action='store_true',
            help='parse project prefix and close ${PREFIX}_service',
        )
        parser.add_argument(
            '-u', '--docker-up-container',
            action='store_true',
            help='docker-compose up -d container with the same name as project',
        )
        parser.add_argument(
            '-d', '--docker-down-container',
            action='store_true',
            help='docker-compose down container with the same name as project',
        )
        parser.add_argument(
            '-e', '--docker-exec-container',
            action='store_true',
            help='docker exec -it container bash',
        )
        parser.add_argument(
            '-s', '--docker-show-containers',
            action='store_true',
            help='show docker processes',
        )
        return parser.parse_args()

    @staticmethod
    def _get_project_path():
        return subprocess.getoutput('git rev-parse --show-toplevel')

    @classmethod
    def _get_project_name(cls):
        return os.path.basename(cls._PROJECT_PATH) if cls._PROJECT_PATH else None

    @classmethod
    def _get_service_name(cls):
        if not cls._PROJECT_NAME:
            return None
        prefix = cls._PROJECT_NAME.split('_', 1)[0]
        return f'{prefix}_service'

    @staticmethod
    def _get_submodules(project_path):
        stdout = subprocess.getoutput(f'grep path \'{project_path}/.gitmodules\' | sed \'s/.*= //\'')
        return {f'{project_path}/{submodule}' for submodule in stdout.split('\n')}

    @classmethod
    def _pull_command(cls, path):
        repo = path.split('/')[-1]
        info = subprocess.getoutput(f'git -C {path} pull')
        if info in ['Already up to date.', '已經是最新的']:
            return f'{cls._FG_YELLOW} {repo:<30} {cls._FG_GREEN}✔︎ {cls._BG_GRAY}  {info}  {cls._RESET}'
        return f'{cls._FG_YELLOW} {repo} {cls._RESET}\n{info}'

    @classmethod
    def _git_pull(cls, args):
        """
        grep path '{project_path}/.gitmodules' | sed 's/.*= //' | xargs -I@ git -C {project_path}/@ pull
        """
        project_path = cls._PROJECT_PATH
        if args.project:
            pathname = os.path.join(f'{cls._ROOT}', f'{cls._PROJECT_NAME}')
            project_path = os.path.expanduser(pathname)
        info = cls._pull_command(path=project_path)
        print(f'{cls._BG_BLUE} {"REPOSITORY":10}  {cls._RESET} {info}')
        submodule_pathname = os.path.join(f'{project_path}', '.gitmodules')
        if not os.path.isfile(submodule_pathname):
            sys.exit()
        for submodule in cls._get_submodules(project_path):
            info = cls._pull_command(path=submodule)
            print(f'{cls._BG_CYAN}  {"SUBMODULE":10}  {cls._RESET} {info}')

    @classmethod
    def _get_compose_pathname(cls, project_name):
        pathname = os.path.join(f'{cls._ROOT}', f'{project_name}/docker-compose.yml')
        return os.path.expanduser(pathname)

    @classmethod
    def _show_launch_service_info(cls, service):
        print (
            f'{cls._FG_BLUE} {cls._BG_BLUE} LAUNCH {cls._YELLOW_ON_BLUE} {cls._RESET}'
            f'{cls._BG_YELLOW} {service} {cls._FG_YELLOW}{cls._RESET}'
        )

    @classmethod
    def _launch_docker_service(cls):
        service = cls._SERVICE_NAME
        if not service:
            raise Exception('service name not found')
        compose_pathname = cls._get_compose_pathname(project_name=service)
        command = f'docker-compose -f "{compose_pathname}" up -d'
        cls._show_launch_service_info(service=service)
        os.system(command)

    @classmethod
    def _show_close_service_info(cls, service):
        print (
            f'{cls._FG_YELLOW}{cls._BG_YELLOW} {service} {cls._YELLOW_ON_RED} {cls._RESET}'
            f'{cls._BG_RED} CLOSE {cls._FG_RED}  {cls._RESET}'
        )

    @classmethod
    def _close_docker_service(cls):
        service= cls._SERVICE_NAME
        if not service:
            raise Exception('service name not found')
        compose_pathname = cls._get_compose_pathname(project_name=service)
        command = f'docker-compose -f "{compose_pathname}" down'
        cls._show_close_service_info(service=service)
        os.system(command)

    @classmethod
    def _show_exec_info(cls, container):
        os.system('clear')
        print (
            f'{"  CONTAINER ":^{cls._TERMINAL_SIZE_WIDTH}}\n'
            f'{cls._FG_BLUE} {cls._BG_BLUE} EXEC {cls._BLUE_ON_YELLOW} {cls._RESET}'
            f'{cls._BG_YELLOW}   {container} {cls._FG_YELLOW}  {cls._RESET}'
        )

    @classmethod
    def _exec_container(cls):
        container = cls._PROJECT_NAME
        if not container:
            raise Exception('cannot parse project name')
        if not subprocess.getoutput(f'docker ps -q -f name={container}'):
            raise Exception(f'{cls._PROJECT_NAME} is not exist')
        cls._show_exec_info(container=container)
        os.system(f'docker exec -it {container} bash -l')

    @classmethod
    def _show_up_info(cls, container):
        print (
            f'{cls._FG_GRAY}{cls._BG_GRAY}   {container} {cls._GRAY_ON_CYAN}  {cls._RESET}'
            f'{cls._BG_CYAN}{"UP":^10}{cls._FG_CYAN} {cls._RESET}'
        )

    @classmethod
    def _up_container(cls, args):
        if not cls._PROJECT_NAME:
            raise Exception('cannot parse project name')
        cls._show_up_info(container=cls._PROJECT_NAME)
        if args.project:
            compose_pathname = cls._get_compose_pathname(project_name=cls._PROJECT_NAME)
            command = f'docker-compose -f "{compose_pathname}" up'
        else:
            command = f'docker-compose up'
        if args.docker_attach_container:
            os.system(command)
        os.system(f'{command} -d')

    @classmethod
    def _show_down_info(cls, container):
        print (
            f'{cls._FG_GRAY}{cls._BG_GRAY}   {container} {cls._GRAY_ON_RED}  {cls._RESET}'
            f'{cls._BG_RED}{"DOWN":^10}{cls._FG_RED} {cls._RESET}'
        )

    @classmethod
    def _down_container(cls, args):
        if not cls._PROJECT_NAME:
            raise Exception('cannot parse project name')
        cls._show_down_info(container=cls._PROJECT_NAME)
        if args.project:
            compose_pathname = cls._get_compose_pathname(project_name=cls._PROJECT_NAME)
            command = f'docker-compose -f "{compose_pathname}" down'
        else:
            command = f'docker-compose down'
        os.system(command)

    @classmethod
    def _show_containers(cls):
        os.system(r'docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Image}}"')

    @classmethod
    def cli(cls):
        if len(sys.argv) == 1:
            cls._help()
        args = cls._get_args()
        cls._PROJECT_PATH = cls._get_project_path()
        cls._PROJECT_NAME = args.project or cls._get_project_name()
        cls._SERVICE_NAME = cls._get_service_name()

        """ GIT """
        if args.git_pull:
            cls._git_pull(args)

        """ CONTAINER """
        if args.docker_launch_service:
            cls._launch_docker_service()
        if args.docker_up_container:
            cls._up_container(args=args)
        if args.docker_exec_container:
            cls._exec_container()
        if args.docker_down_container:
            cls._down_container(args=args)
        if args.docker_close_service:
            cls._close_docker_service()
        if args.docker_show_containers:
            cls._show_containers()


if __name__ == '__main__':
    Dockit.cli()
