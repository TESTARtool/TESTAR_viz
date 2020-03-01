# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
"""
##############
# this file must be placed in the parent folder
# otherwise files in the assets folder cannot be served with default flask settings
##############
import dash
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# DISABLE the next line when creating Sphinx documentation
app = dash.Dash(__name__,)

# ENABLE this section when creating Sphinx documentation
#inspired by https://github.com/plotly/dash/issues/696
# class app:
#     def callback(*argument):
#         def decorator(function):
#             def wrapper(*args, **kwargs):
#                 result = function(*args, **kwargs)
#                 return result
#             return wrapper
#         return decorator