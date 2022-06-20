def A(args, kwargs):
    print(args, kwargs)
    
def K(*args, **kwargs):
    A(args, kwargs)
    
K(1, a=2)