
import sys
import click

class NagErrors(object):
    def __init__(self):
        self.critical = []
        self.warning = []
        self.unknown = []

    def addRecord(self, etype, etext):
        if etype == 'critical':
            self.critical.append(etext)
        elif etype == 'warning':
            self.warning.append(etext)
        else:
            self.unknown.append(etext)

    def addCritical(self, etext):
        self.addRecord('critical', etext)
    
    def addWarning(self, etext):
        self.addRecord('warning', etext)
    
    def addUnknown(self, etext):
        self.addRecord('unknown', etext)

    def formatStatus(self, stype, sarr):
        ret = ""
        if len(sarr) == 1:
            ret += "{} {}\r\n".format(stype, sarr[0])
        else:
            ret += "{}:\r\n".format(stype)
            for l in sarr:
                ret += "    {}\r\n".format(l)
        return(ret)

    def printStatus(self):
        if len(self.unknown) > 0 :
            click.echo(self.formatStatus('UNKNOWN', self.unknown))
        if len(self.critical) > 0 :
            click.echo(self.formatStatus('CRITICAL', self.critical))
        if len(self.warning) > 0 :
            click.echo(self.formatStatus('WARNING', self.warning))
        if len(self.unknown) + len(self.critical) + len(self.warning) == 0 :
            click.echo('OK')
        
    def getExitCode(self):
        if len(self.unknown) > 0 :
            return 3
        if len(self.critical) > 0 :
            return 2
        if len(self.warning) > 0 :
            return 1
        return 0

    def doExit(self):
        sys.exit(self.getExitCode())


class NagEval(object):
    def __init__(self, errObj):
        self.errObj = errObj

    def evalEnum(self, value, defaultStatus="UNKNOWN", okValues=[], warningValues=[], criticalValues=[], unknownValues=[], prefixText="", postfixText= ""):
        if value in unknownValues:
            self.errObj.addUnknown("{}value is {}{}".format(prefixText, value, postfixText))
            return("UNKNOWN")
        if value in criticalValues:
            self.errObj.addCritical("{}value is {}{}".format(prefixText, value, postfixText))
            return("CRITICAL")
        if value in warningValues:
            self.errObj.addWarning("{}value is {}{}".format(prefixText, value, postfixText))
            return("WARNING")
        if value in okValues:
            return("OK")
        if defaultStatus != "OK":
            self.errObj.addRecord(defaultStatus.lower(), "{}value {} not found{}".format(prefixText, value, postfixText))
        return(defaultStatus)

    def evalNumberAsc(self, value, warningAbove=None, criticalAbove=None, prefixText="", postfixText="", numberUnits=""):
        if criticalAbove is not None and value > criticalAbove:
            self.errObj.addCritical("{}{}{} is > {}{}{}".format(prefixText, value, numberUnits, criticalAbove, numberUnits, postfixText))
            return("CRITICAL")
        if warningAbove is not None and value > warningAbove:
            self.errObj.addWarning("{}{}{} is > {}{}{}".format(prefixText, value, numberUnits, warningAbove, numberUnits, postfixText))
            return("WARNING")
        return("OK")
    
    def evalNumberDesc(self, value, warningBelow=None, criticalBelow=None, prefixText="", postfixText= "", numberUnits=""):
        if criticalBelow is not None and value < criticalBelow:
            self.errObj.addCritical("{}{}{} is < {}{}{}".format(prefixText, value, numberUnits, criticalBelow, numberUnits, postfixText))
            return("CRITICAL")
        if warningBelow is not None and value > warningBelow:
            self.errObj.addWarning("{}{}{} is < {}{}{}".format(prefixText, value, numberUnits, warningBelow, numberUnits, postfixText))
            return("WARNING")
        return("OK")
