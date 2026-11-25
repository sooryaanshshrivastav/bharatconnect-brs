import fitz,io
from PIL import Image
doc=fitz.open("/mnt/user-data/uploads/_Untitled.pdf")
out=[]
for pn,page in enumerate(doc,1):
    for i,img in enumerate(page.get_images(full=True)):
        xref,smask=img[0],img[1]
        pix=fitz.Pixmap(doc,xref)
        if pix.n-pix.alpha>3: pix=fitz.Pixmap(fitz.csRGB,pix)
        im=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        if smask:
            m=Image.open(io.BytesIO(fitz.Pixmap(doc,smask).tobytes("png"))).convert("L").resize(im.size)
            im=im.convert("RGBA"); im.putalpha(m)
        name=f"p{pn:02d}_{i:02d}"
        W=900 if im.width>900 else im.width
        if im.width>W: im=im.resize((W,int(im.height*W/im.width)),Image.LANCZOS)
        if im.mode=="RGBA": im.save(f"img/{name}.png",optimize=True); ext="png"
        else: im.save(f"img/{name}.jpg",quality=72,optimize=True); ext="jpg"
        out.append((name,ext,im.size,xref))
for o in out: 
    if o[0][:3]>="p15": print(o)
