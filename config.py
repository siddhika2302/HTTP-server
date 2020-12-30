#configuration file for HTTP Server
import os

'''identify the current working directory'''
ROOT = os.getcwd()

'''Maximum clients the server can handle at a time'''
MAX_REQUESTS = 3

'''a list to record the current clients of the server'''
thread_list = []

'''Cookie handling'''
COOKIE1 = "Set-Cookie : Id = "
COOKIE2 = "Max-Age = 3000"

#dictionary to convert extensions into content types
file_extension = {'.html':'text/html',
                  '.txt':'text/plain',
                   '': 'text/plain',
                   '.js': 'application/javascript',
                   '.css': 'text/css',
                   '.py' : 'application/python-code',
                   '.java' : 'application/java',
                   '.cpp' : 'application/cpp',
                   '.c' : 'application/c'
                 }

'''Authentication for DELETE'''
USERNAME = 'abcd' 
PASSWORD = 'xyz'


