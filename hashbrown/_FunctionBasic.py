class Function:
    def __init__(self,f,var,name = 'Function'):
        """
        hasbrown's wrapper class for functions

        Parameters
        ----------
        f (function): core function. must have at least one input (time)

        var (int): number of variables

        name (string): name of function. later used as result variable names
        """
        self.name = name
        self.f = f
        self.var = int(var)
    
    
    def minus(self,name = None):
        """
        returns a (class Function) object that has sign-inverted function from the subject.

        Parameters
        ----------
        name (string): new name for the inverted function. default value keeps the original name

        Notes
        -----
        mainly used internally. not recommended for use in user API
        """
        if name != None:
            Function(lambda *x: -self.f(*x),self.var,name = name)            
        return Function(lambda *x: -self.f(*x),self.var,name = self.name)

def invSign(f): #f is assumed to be a tuple of Function Objects
    """
    hasbrown/_Functionbasic: inverts an iterable of (class Function) objects

    Parameters
    ----------
    f (iterable): an iterable of (class Function) objects

    Notes
    -----
    mainly used internally. not recommended for use in user API
    """
    x = []
    for i in f:
        x.append(i.minus())
    return tuple(x)