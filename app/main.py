import sys
import os
import subprocess
class MiniShell:
    def __init__(self):
        self.builtin_commands = ["echo", "type", "exit", "pwd", "cd"]
    def run(self):
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            args = input().strip()
            if not args:
                continue
            parts = args.split()
            command = parts[0]
            args = parts[1:]
            # Handle PATH assignments
            if "=" in command:
                var, value = command.split("=", 1)
                if var == "PATH":
                    os.environ[var] = value
                    continue
            if command == "exit" and args == ["0"]:
                exit(0)
            if command == "echo":
                self.echo(args)
                continue
            if command == "type":
                self.type_command(args)
                continue
            if command == "pwd":
                self.pwd_command()
                continue
            if command == "cd":
                self.cd_command(args)
                continue
            if command not in self.builtin_commands:
                self.run_command(command, args)
                continue
            print(f"{command}: command not found")
    def echo(self, args):
        print(" ".join(args))
    def type_command(self, args):
        if not args:
            print("type: missing argument")
            return
        cmd_to_check = args[0]
        if cmd_to_check in self.builtin_commands:
            print(f"{cmd_to_check} is a shell builtin")
        else:
            found = False
            if "PATH" in os.environ:
                for path_dir in os.environ["PATH"].split(":"):
                    if os.path.exists(os.path.join(path_dir, cmd_to_check)):
                        print(os.path.join(path_dir, cmd_to_check))
                        found = True
                        break
            if not found:
                print(f"{cmd_to_check} not found")
    def run_command(self, command, args):
        if "PATH" in os.environ:
            for path_dir in os.environ["PATH"].split(":"):
                full_path = os.path.join(path_dir, command)
                if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                    try:
                        subprocess.run([full_path] + args)
                    except Exception as e:
                        print(f"Error executing command: {e}")
                    return
        print(f"{command}: command not found")
    def pwd_command(self):
        print(os.getcwd())
    def cd_command(self, args):
        if not args:
            print("cd: missing argument")
            return
        try:
            if args[0] == "~":
                os.chdir(os.path.expanduser(args[0]))
            else:
                os.chdir(args[0])
        except FileNotFoundError:
            print(f"cd: {args[0]}: No such file or directory")
        except NotADirectoryError:
            print(f"cd: {args[0]}: Not a directory")
        except PermissionError:
            print(f"cd: {args[0]}: Permission denied")
        except Exception as e:
            print(f"cd: {args[0]}: {e}")
if __name__ == "__main__":
    shell = MiniShell()
    shell.run()