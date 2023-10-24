import os 
import openai
from utils.tools import get_completion, Timer

with Timer():
    print(get_completion("1+1是什么？"))
