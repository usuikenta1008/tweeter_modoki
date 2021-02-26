import json

# JSON - JavaScriptObjectNotation

"""
INDEPENDANT on the Language
{
    "name": "Kenta Usui",
    "age": "23",
    "hobbies": [
        "soccer", "swimming"
    ],
    "languages":[
        "Front-End": ["HTML", "CSS", "JAVASCRIPT"]
        "BackEnd": ["python", "C#"]
    ]
}
"""
dictionary = {
    "name": "Kenta Usui",
    "age": "23",
    "hobbies": [
        "soccer", "swimming"
    ],
     "languages":{
        "Front-End": ["HTML", "CSS", "JAVASCRIPT"],
        "BackEnd": ["python", "C#"]
    }
}

list_sample = [1, 2, 3, 4, 5]

json_string = json.dumps(dictionary)
dictionary_converted = json.loads(json_string)

print(type(json_string))