import os
import asyncio
import requests
import numpy as np
import json
from PIL import Image
import base64
from io import BytesIO
import re
import math

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

endpoint = 'https://7rq1vzhvxj.execute-api.us-west-1.amazonaws.com/Prod/infer/'
# Endpoint override for development
devmode = False
if 'BoosteURL' in os.environ:
    print("Dev Mode")
    devmode = True
    if os.environ['BoosteURL'] == 'local':
        endpoint = 'http://localhost:8080/2015-03-31/functions/function/invocations'
    else:
        endpoint = os.environ['BoosteURL']
    print("Hitting endpoint:", endpoint)


async def async_api_caller(api_key, prompt, image):
    global endpoint
    url = endpoint
    # print(url)

    # defaults
    is_path = False
    is_url = False

    if re.match(url_regex, image) is not None:
        is_url = True
        image_send = image

    if os.path.exists(image):
        is_path = True

        if image[-3:] == "jpg" or image[-4:] == "jpeg":
            image_pil = Image.open(image)
            image_file = BytesIO()
            image_pil.save(image_file, format="JPEG")
            image_bytes = image_file.getvalue()  # im_bytes: image in binary format.
            image_send = base64.b64encode(image_bytes).decode('utf-8')
        elif image[-3:] == "png":
            image_pil = Image.open(image)
            image_file = BytesIO()
            image_pil.save(image_file, format="PNG")
            image_bytes = image_file.getvalue()  # im_bytes: image in binary format.
            image_send = base64.b64encode(image_bytes).decode('utf-8')
        else:
            print("Warning, image failed: {}\nImage must be .jpg or .png.\n".format(image))
            return None

    if is_path == False and is_url == False:
        print("Warning: image failed: {}\nImage must be valid a URL or a path to local image file\n\texample:  https://google.com\n\texample:  ./my-image.jpg\n\texample:  /home/user/my-image.png\n".format(image))
        return None

    # sequence = []
    payload = {
        "apiKey" : api_key,
        "prompt" : prompt,
        "image" : image_send,
        "isUrl" : is_url
    }

    response = requests.post(url, json=payload)
    try:
        if devmode: # then it returns as full json blob
            out = response.json()
            code = out['statusCode']
            body = json.loads(out['body'])
        else:
            # then api gateway converts status code in blob to status code, and body in json to json
            code = response.status_code
            body = response.json()

    except Exception as e:
        print("Warning, server failed to process one request:\n\tprompt:  {}\n\timage:  {}\n".format(prompt, image))
        return None
        
    if code == 200:
        return body
    else:
        raise Exception("Server returned error code {}\n{}".format(code,body))



def api_caller(api_key, prompt, image):
    global endpoint
    url = endpoint
    # print(url)

    # defaults
    is_path = False
    is_url = False

    if re.match(url_regex, image) is not None:
        is_url = True
        image_send = image

    if os.path.exists(image):
        is_path = True

        if image[-3:] == "jpg" or image[-4:] == "jpeg":
            image_pil = Image.open(image)
            image_file = BytesIO()
            image_pil.save(image_file, format="JPEG")
            image_bytes = image_file.getvalue()  # im_bytes: image in binary format.
            image_send = base64.b64encode(image_bytes).decode('utf-8')
        elif image[-3:] == "png":
            image_pil = Image.open(image)
            image_file = BytesIO()
            image_pil.save(image_file, format="PNG")
            image_bytes = image_file.getvalue()  # im_bytes: image in binary format.
            image_send = base64.b64encode(image_bytes).decode('utf-8')
        else:
            print("Warning, image failed: {}\nImage must be .jpg or .png.\n".format(image))
            return None

    if is_path == False and is_url == False:
        print("Warning: image failed: {}\nImage must be valid a URL or a path to local image file\n\texample:  https://google.com\n\texample:  ./my-image.jpg\n\texample:  /home/user/my-image.png\n".format(image))
        return None

    # sequence = []
    payload = {
        "apiKey" : api_key,
        "prompt" : prompt,
        "image" : image_send,
        "isUrl" : is_url
    }

    response = requests.post(url, json=payload)
    try:
        if devmode: # then it returns as full json blob
            out = response.json()
            code = out['statusCode']
            body = json.loads(out['body'])
        else:
            # then api gateway converts status code in blob to status code, and body in json to json
            code = response.status_code
            body = response.json()

    except Exception as e:
        print("Warning, server failed to process one request:\n\tprompt:  {}\n\timage:  {}\n".format(prompt, image))
        return None
        
    if code == 200:
        return body
    else:
        raise Exception("Server returned error code {}\n{}".format(code,body))


def softmax_caller(similarities, api_key):
    global endpoint
    url = endpoint

    # sequence = []
    payload = {
        "similarities" : similarities,
        "softmax" : True,
        "apiKey" : api_key
    }

    response = requests.post(url, json=payload)

    try:
        if devmode: # then it returns as full json blob
            out = response.json()
            code = out['statusCode']
            body = json.loads(out['body'])
        else:
            # then api gateway converts status code in blob to status code, and body in json to json
            code = response.status_code
            body = response.json()

    except Exception as e:
        print("Warning, server failed to run the probability step.")
        return None
        
    if code == 200:
        return body
    else:
        raise Exception("Server returned error code {}\n{}".format(code,body))


# # correct solution:
# def softmax(x):
#     """Compute softmax values for each sets of scores in x."""
#     e_x = np.exp(x - np.max(x))
    # return e_x / e_x.sum(axis=0) # only difference

def clip_main(api_key, prompts, images, pretty_print):
    if type(prompts) != type([]):
        raise Exception("Error: prompts not of type: list")
    
    if type(images) != type([]):
        raise Exception("Error: images not of type: list")

    if prompts == []:
        raise Exception("Error: prompts cannot be length: 0")
    else:
        for item in prompts:
            if type(item) != type(""):
                raise Exception("Error: all prompts must be type: string")

    if images == []:
        raise Exception("Error: images cannot be length: 0")
    else:
        for item in images:
            if type(item) != type(""):
                raise Exception("Error: all images must be type: string")


    outs = {}
    out_logits = np.zeros((len(prompts), len(images)))
    for i, prompt in enumerate(prompts):
        outs[prompt] = {}
        for j, image in enumerate(images):
            out = api_caller(api_key, prompt, image)
            outs[prompt][image] = out
            if out != None:
                out_logits[i,j] = out['similarity']

    out_probs = softmax_caller(out_logits.tolist(), api_key)
    if out_probs != None:
        for i, prompt in enumerate(prompts):
            for j, image in enumerate(images):
                if outs[prompt][image] != None:
                    outs[prompt][image]["probabilityRelativeToPrompts"] = out_probs["relativeToPrompts"][i][j]
                    outs[prompt][image]["probabilityRelativeToImages"] = out_probs["relativeToImages"][i][j]
    
    if pretty_print:
        pretty_print_output(prompts, images, outs)

    return outs

async def async_clip_main(api_key, prompts, images, pretty_print):

    if type(prompts) != type([]):
        raise Exception("Error: prompts not of type: list")
    
    if type(images) != type([]):
        raise Exception("Error: images not of type: list")

    if prompts == []:
        raise Exception("Error: prompts cannot be length: 0")
    else:
        for item in prompts:
            if type(item) != type(""):
                raise Exception("Error: all prompts must be type: string")

    if images == []:
        raise Exception("Error: images cannot be length: 0")
    else:
        for item in images:
            if type(item) != type(""):
                raise Exception("Error: all images must be type: string")


    tasks = {}
    for prompt in prompts:
        tasks[prompt] = {}
        for image in images:
            tasks[prompt][image] = asyncio.create_task(async_api_caller(api_key, prompt, image))

    outs = {}
    out_logits = np.zeros((len(prompts), len(images)))
    for i, prompt in enumerate(prompts):
        outs[prompt] = {}
        for j, image in enumerate(images):
            out = await tasks[prompt][image]
            outs[prompt][image] = out
            if out != None:
                out_logits[i,j] = out['similarity']
    # print(out_logits.tolist())

    out_probs = softmax_caller(out_logits.tolist(), api_key)
    if out_probs != None:
        for i, prompt in enumerate(prompts):
            for j, image in enumerate(images):
                if outs[prompt][image] != None:
                    outs[prompt][image]["probabilityRelativeToPrompts"] = out_probs["relativeToPrompts"][i][j]
                    outs[prompt][image]["probabilityRelativeToImages"] = out_probs["relativeToImages"][i][j]
    
    if pretty_print:
        pretty_print_output(prompts, images, outs)

    return outs

def pretty_print_output(prompts, images, outs):

    print("\n---------\nSimilarity scores\n---------\n")
    for prompt in prompts:
        for image in images:
            if outs[prompt][image] != None:
                print("\n\tPrompt:\t\t", prompt, "\n\tImage URL:\t", image, "\n\tSimilarity:\t", outs[prompt][image]["similarity"])
    print("\n")

    print("\n---------\nPrompt probabilities for each image:\n---------\n")
    for image in images:
        print("\tImage:", image)
        for prompt in prompts:
            if outs[prompt][image] != None:
                print("\n\t\tPrompt:", prompt, "\n\t\tProb:", outs[prompt][image]["probabilityRelativeToPrompts"])
            else:
                print("\n\t\tPrompt:", prompt, "\n\t\tFailed")
        print()
    print("\n")

    print("\n---------\nImage probabilities for each prompt:\n---------\n")
    for prompt in prompts:
        print("\tPrompt:", prompt)
        for image in images:
            if outs[prompt][image] != None:
                print("\n\t\tImage:", image, "\n\t\tProb:", outs[prompt][image]["probabilityRelativeToImages"])
            else:
                print("\n\t\tImage:", image, "\n\t\tFailed")
        print()
    print("\n")

def clip_image_main(images):
    return dict_out

def clip_text_main(prompts):
    return dict_out