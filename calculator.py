"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
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