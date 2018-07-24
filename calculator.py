# WSGI Calculator


def homepage():
    
    return """
    
    <h1>wsgi-calculator</h1>

    <h2>A How-To</h2>

    <p>
    To access, start with http://localhost:8080/ and add the operator and operands to perform a calculation.
    
    For example:
    <a href="http://localhost:8080/multiply/7/8">http://8080/multiply/7/8</a>
    should yield "56"
    
    </br>
    </br>

    Accepted operands:
    <ul>
      <li>add</li>
      <li>subtract</li>
      <li>multiply</li>
      <li>divide</li>
    </ul>

    """

def add(*args):
    """
    Returns a STRING with the sum of the arguments
    """
    num1, num2 = int(args[0]), int(args[1])
    sum = num1 + num2

    return str(sum)

def subtract(*args):
    """
    Returns a string with the difference of the arguments
    """
    num1, num2 = int(args[0]), int(args[1])
    difference = str(num1 - num2)

    return difference

def multiply(*args):
    """
    Returns a string with the product of the arguments
    """
    num1, num2 = int(args[0]), int(args[1])
    product = str(num1 * num2)

    return product

def divide(*args):
    """
    Returns a string with the quotient of the arguments
    """
    num1, num2 = int(args[0]), int(args[1])
    quotient = str(num1 / num2)

    return quotient

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # dictionary that correlates a function to the directory
    func_directory = {
      '': homepage, 
      'add': add,
      'subtract': subtract,
      'multiply': multiply,
      'divide': divide,
      }
  
    # convert the received path to a list. path should look something like 
    # "/multiply/7/8"
    # save the operator (func) and operands (args)
    # should yield something like below
    # func = add
    # args = ['25', '32']

    recd_path = path.split('/')
    func = func_directory.get(recd_path[1])
    args = recd_path[2:]

    return func, args

def application(environ, start_response):
    # invokes start_response
    # gets the path and calls resolve path
    # returns in Byte encoding
    
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        print(path)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # wsgiref simple server creation
    from wsgiref.simple_server import make_server

    srv = make_server('localhost', 8080, application)
    srv.serve_forever()