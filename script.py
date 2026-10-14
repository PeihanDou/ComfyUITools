import json
import torch
from urllib import request


# Make Sure Using GPU version of PyTorch
def gpu_check():
	print(f"PyTorch 版本: {torch.__version__}")
	print(f"PyTorch 构建类型: {'CUDA/GPU' if torch.version.cuda else 'CPU'}")
	print(f"CUDA 是否可用: {torch.cuda.is_available()}")
	if torch.cuda.is_available():
		print(f"CUDA 版本: {torch.version.cuda}")
		print(f"GPU: {torch.cuda.get_device_name(0)}")
		return True
	else:
		print("CUDA 不可用")
		return False

# 调用保存的工作流

def get_workflow(s):
	with open(s, "r", encoding="utf-8") as f:
		base_workflow = json.load(f)
		return base_workflow # s should be the JSON file of a workflow

# 默认的工作流json如下
# prompt_text = """
# {
#     "3": {
#         "class_type": "KSampler",
#         "inputs": {
#             "cfg": 8,
#             "denoise": 1,
#             "latent_image": [
#                 "5",
#                 0
#             ],
#             "model": [
#                 "4",
#                 0
#             ],
#             "negative": [
#                 "7",
#                 0
#             ],
#             "positive": [
#                 "6",
#                 0
#             ],
#             "sampler_name": "euler",
#             "scheduler": "normal",
#             "seed": 13579,
#             "steps": 20
#         }
#     },
#     "4": {
#         "class_type": "CheckpointLoaderSimple",
#         "inputs": {
#             "ckpt_name": "v1-5-pruned-emaonly.safetensors"
#         }
#     },
#     "5": {
#         "class_type": "EmptyLatentImage",
#         "inputs": {
#             "batch_size": 1,
#             "height": 512,
#             "width": 512
#         }
#     },
#     "6": {
#         "class_type": "CLIPTextEncode",
#         "inputs": {
#             "clip": [
#                 "4",
#                 1
#             ],
#             "text": "masterpiece best quality girl"
#         }
#     },
#     "7": {
#         "class_type": "CLIPTextEncode",
#         "inputs": {
#             "clip": [
#                 "4",
#                 1
#             ],
#             "text": "bad hands"
#         }
#     },
#     "8": {
#         "class_type": "VAEDecode",
#         "inputs": {
#             "samples": [
#                 "3",
#                 0
#             ],
#             "vae": [
#                 "4",
#                 2
#             ]
#         }
#     },
#     "9": {
#         "class_type": "SaveImage",
#         "inputs": {
#             "filename_prefix": "ComfyUI",
#             "images": [
#                 "8",
#                 0
#             ]
#         }
#     }
# }
# """

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)

save_name = "sdxl_work_api.json" # change the workflow name you want to use
workflow_dir = "./ComfyUI/user/default/workflows/" + save_name
prompt = get_workflow(workflow_dir)

#set the text prompt for our positive CLIPTextEncode
prompt["10"]["text"] = "masterpiece, 1girl, drinking coffee, clean outer line, (artist: modare)"
prompt["11"]["text"] = "waterproof, worst quality, nsfw"
prompt["12"]["inputs"]["seed"] = 5


queue_prompt(prompt)