PUSHd C:\apps\astToolFactory\astToolFactory\datacenter
FOR /L %%G IN (11,1,15) DO CALL py -3.%%G probeInterpreter.py
SET filename=probeInterpreter.csv
DEL %filename%
COPY *.Z0Z_csv %filename%
DEL *.Z0Z_csv
POPd
