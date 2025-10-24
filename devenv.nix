{ pkgs, config, ... }:
{
  languages.python = {
    enable = true;
    venv.enable = true;
    venv.requirements = "-r ${config.devenv.root}/api/requirements.txt";
  };
}
