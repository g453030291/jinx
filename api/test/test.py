from PIL import Image
from controlnet_aux.processor import Processor

hed_processor = Processor('softedge_hed')

def make_elements(name):
    img = Image.open(name)
    if img.mode == 'RGBA':
        r, g, b, a = img.split()
        img = img.convert('RGB')
        hed_img = hed_processor(img, to_pil=True).resize(img.size).convert('RGB')
        hed_img.putalpha(a)
    else:
        img = img.convert('RGB')
        hed_img = hed_processor(img, to_pil=True).resize(img.size).convert('RGB')
    hed_img.save('/Users/gemushen/test-file/make_elements/result1.png')

if __name__ == '__main__':
    make_elements('/Users/gemushen/test-file/make_elements/Gb3zWbHaMAArlzJ.jpeg')
