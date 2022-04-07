set runningdir=%~dp0
:rerun
%runningdir%\wordle_solver < %runningdir%\wordle_input.txt
pause
goto rerun
