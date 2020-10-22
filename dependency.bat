@echo off
SETLOCAL EnableDelayedExpansion


set module=callbacks
set outfile=%module%.dot
call pydeps %module%  --cluster --exclude dash* networkx* pandas* matplotlib* numpy* flask*  --max-cluster-size=1000 --max-bacon 3 --reverse  --noshow  --show-dot  1> doxygen\%outfile%
set module=layouts
set outfile=%module%.dot
call pydeps %module%  --cluster --exclude dash* networkx* pandas* matplotlib* numpy* flask* --max-cluster-size=1000 --max-bacon 3 --reverse  --noshow  --show-dot  1> doxygen\%outfile%
set module=utils
set outfile=%module%.dot
call pydeps %module%  --cluster --exclude dash* networkx* pandas* matplotlib* numpy* flask* --max-cluster-size=1000 --max-bacon 3 --reverse  --noshow  --show-dot  1> doxygen\%outfile%
set module=settings
set outfile=%module%.dot
call pydeps %module%  --cluster --exclude dash* networkx* pandas* matplotlib* numpy* flask* --max-cluster-size=1000 --max-bacon 3 --reverse  --noshow  --show-dot  1> doxygen\%outfile%

call pydeps run.py  --cluster   --max-cluster-size=0 --max-bacon 4 --reverse --noshow --show-dot 1> doxygen\run.dot
rem call pydeps controller.py  --cluster   --max-cluster-size=0 --max-bacon 3 --reverse --noshow --show-dot 1> doxygen\controller.dot
