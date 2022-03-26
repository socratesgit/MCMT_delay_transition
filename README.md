# MCMT_delay_transition

This tool allows to produce automatically the delay transition for a MCMT model.
If you want to use this tools you have to provide in the _sample.json_ file
a description of your model, which includes, for each process, 
a list of the states and their time invariants, whether or not a process is parameterized, 
the clock variable and other other variables.
Once you run the command _python delay.py_ you'll obtain in a file called _transitions.txt_
the delay transitions of your model.
