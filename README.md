#42-Taskmaster

In this 42 project we were asked to create a basic version of [supervisor](https://github.com/Supervisor/supervisor).
We were restricted to our language of choice's standard library. Except for the config file parsing.

The script reads the tasks parameters from the yaml file, and executes some kind of user prompt to effectively control this tasks.

The only argument needed is a config file.

All info about making your own config file is in exampleconfig.yaml.

To launch the script, you can either use:

```
$/> python3 taskmanager.py config_files/testconfig.yaml
```

or


```
$/> ./taskmanager.py config_files/testconfig.yaml
```

dependencies: yaml