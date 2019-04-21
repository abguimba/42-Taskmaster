# 42-Taskmaster

In this 42 project we were asked to create a basic version of [supervisor](https://github.com/Supervisor/supervisor).
We were restricted to our language of choice's standard library. Except for the config file parsing.

The script reads the tasks parameters from the yaml file, and executes some kind of user prompt to effectively manage these tasks.

The only argument needed is a config file.
All info about making your own config file is in exampleconfig.yaml.

Partners in this project -> [@toshuomj](https://github.com/toshuomj)

<img src="/images/Taskmaster01.gif" alt="Taskmaster01" width="700"/>

To launch the script, you first need to do a simple `make` and then either:

``` zsh
$/> python3 taskmaster.py config_files/<yourconfig>.yaml
```

or

``` zsh
$/> ./taskmaster.py config_files/<yourconfig>.yaml
```

dependencies: yaml
