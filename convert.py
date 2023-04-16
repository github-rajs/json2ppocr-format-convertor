import os
import json

folder='eg/'

all_files=os.listdir(folder)

for file in all_files:
    ppocr_format=[]
    with open(folder+file) as f:
        data = json.load(f)
    all_cords=[]
    all_text=[]
    filename = os.path.basename(data['task']['data']['ocr']) 
    for i in data['result']:
        origin_width=i['original_width']
        origin_height=i['original_height']
        
        if 'text' in i['value'].keys()  :
            cords=i['value']['points']
            cords = [[int(num) for num in sublist] for sublist in cords]
            for k in range(len(cords)):
                cords[k][0] = int(cords[k][0]/100.0 * origin_width)
                cords[k][1] = int(cords[k][1]/100.0 * origin_height)
                
            text=i['value']['text']
            
            xx='"transcription":'
            xx1='"{}"'.format(text[0])
            xc='"points":'
            xc1=cords
            xv='"difficult":'
            xv1="false"
            par='{'
            par1='}'
            
            format_tmp="{}{}{},{}{},{}{}{}".format(par,xx,xx1,xc,xc1,xv,xv1,par1)
            #print(format_tmp)
            ppocr_format.append(format_tmp)
            print("{}   {}".format(filename,ppocr_format))
