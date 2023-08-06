# NagiosCheckHelper

This library helps with the boilerplate nagios check formating/status information when writing a Python check

## NagErrors Object

An object to hold the Errors that have occured.

Generally you can call it with obj.addCritical(error text) or obj.addWarning(error text) to accumulate your errors

Then call obj.printStatus() to print the formatted Errors

Then call obj.doExit() to exit your program with the proper result code.

2cent example:
```
import NagErrors from NagiosCheckHelper
nerr = NagErrors()
nerr.addCritical("This is a Critical Event")
nerr.addWarning("This is a Warning Event")
nerr.printStatus()
nerr.doExit()
```

## NagEval Object

An object with common subroutines to evaluate data and cause error events based on the comparisons.

Be sure to initite it with an NagErrors Object.

### evalEnum
Evaluate a value and see if it matches with an array of values

```
obj.evalEnum("ALL OK", defaultStatus="CRITICAL", okValues=["ALL OK"], unknownValues=["Don't Know"])
```

### evalNumberAsc
Evaluate a number and see if it is above a certain value
```
obj.evalNumberAsc(50, warningAbove=80, criticalAbove=95, numberUnits=" degrees F")
```

### evalNumberDesc
Evaluate a number and see if it is below a certain value
```
obj.evalNumberDesc(50, warningBelow=32, criticalBelow=10, numberUnits=" degrees F")
```

