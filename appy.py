##
# Function to connect the variable 'app' to the Dash framework.\n
# this variable is used for annotating the call-back functions in other part of the application, \n

# this file must exist on the toplevel
# otherwise content in the assets folder cannot be served with default flask settings
import dash

# DISABLE the next line when creating Sphinx documentation
app = dash.Dash(__name__,)

# ENABLE this following code section when creating Sphinx documentation
# inspired by https://github.com/plotly/dash/issues/696

# class app:
#     def callback(*argument):
#         def decorator(function):
#             def wrapper(*args, **kwargs):
#                 result = function(*args, **kwargs)
#                 return result
#             return wrapper
#         return decorator
