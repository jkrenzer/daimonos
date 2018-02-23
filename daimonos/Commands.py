# -*- coding: utf-8 -*-
import re

class Shell:
    commands = {}
        
    class Exception(Exception):
        def __init__(self, message, expression=""):
            self.expression = expression
            self.message = message

    def __init__(self, client):
        self.client = client

    def interpret(self, input):
        input = re.sub("\s\s+", " ", input) #Get rid of multi-spaces
        delimeted = input.split(':')
        args = []
        kargs = {}
        if len(delimeted) > 0:
            command = delimeted[0].strip()
        else: 
            raise self.Exception("You have to enter a command. Say 'help' if you want to learn more.")
        if len(delimeted) > 1:
            arguments = delimeted[1].strip().split(',')
            for arg in arguments:
                argSplit = arg.split('=')
                if len(argSplit) == 1:
                    if len(argSplit[0].split()) == 1:
                        args.append(argSplit[0])
                    elif len(argSplit[0].split()) > 1:
                        args.append(argSplit[0].split())
                elif len(argSplit) > 1:
                    if len(argSplit[1].split()) == 1:
                        kargs.update({ argSplit[0].strip(): argSplit[1].strip()})
                    elif len(argSplit[1].split()) > 1:
                        kargs.update({ argSplit[0].strip(): argSplit[1].strip().split()})
                else:
                    raise self.Exception("Argument '%s' is of invalid structure." % arg)
        commandDict = self.commands.get(command, None)
        if commandDict is not None:
            func = commandDict.get('function', None)
            if func is not None:
                if commandDict.get('exposeClient', False):
                    return func(*args,_client=self.client,**kargs)
                else:
                    return func(*args,**kargs)
            else:
                raise self.Exception("Function for command %s is not set! This is most propably a bug." % command)
        else:
            raise self.Exception("Command %s is unknown! Consult 'help' to see a list of available commands." % command)
            
        

def command(name: str, exposeClient=False):
    def decorator(func):
        Shell.commands.update({re.sub("\s\s+", " ", name): {
            'function': func,
            'exposeClient': exposeClient
            #TODO ACLs
            }})
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator 
