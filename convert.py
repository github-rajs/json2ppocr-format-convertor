import os
import json
import cv2
import numpy as np 
from PIL import Image
from PIL import ImageDraw
import random
import shutil

mini_json_file_dir='output/'
images_annotated_dir='images/'

#for text detection
ppocr_det_dataset_dir='DATASET/DET/'
det_train=ppocr_det_dataset_dir+'train/'
det_valid=ppocr_det_dataset_dir+'valid/'

#for text recognition
ppocr_rec_dataset_dir='DATASET/REC/'
rec_train=ppocr_rec_dataset_dir+'train/'
rec_valid=ppocr_rec_dataset_dir+'train/'+'valid/'

#temp directory
#create these folder manually
tmp_imgs_lbls='TEMP/images/'
tmp_crop_imgs_lbls='TEMP/crops/'

#dataset split
dataset_train_split=80
dataset_valid_split=20

def processor(poly_cords,image,text):
    num = random.randint(1000, 9999)
    file_without_ext=str(image.split('.')[0])
    name_to_save_img=file_without_ext+'_'+str(num)+'.jpg'
    final_txt_op='{}   {}'.format(name_to_save_img,text[0])
    img = Image.open('images/'+image)
    x1,y1=poly_cords[0][0],poly_cords[0][1]
    x2,y2=poly_cords[1][0],poly_cords[1][1]
    x3,y3=poly_cords[2][0],poly_cords[2][1]
    x4,y4=poly_cords[3][0],poly_cords[3][1]
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)], outline=1, fill=1)
    cropped_img = img.crop(mask.getbbox())
    if os.path.exists(images_annotated_dir+image):
        cropped_img.save(tmp_crop_imgs_lbls+name_to_save_img) 
        with open('TEMP/ppocr_labels_crops.txt', 'a') as f:
            f.write(final_txt_op+'\n')
    else:
        print("image file not exist: {}".format(images_annotated_dir+image))
   

def main():
    all_json_files=os.listdir(mini_json_file_dir)
    for json_file in all_json_files:
        with open(mini_json_file_dir+json_file) as f:
            json_data = json.load(f)
            
        ppocr_format=[]
        filename = os.path.basename(json_data['task']['data']['ocr'])
        for i in json_data['result']:
            origin_width,origin_height=i['original_width'],i['original_height']
            if 'text' in i['value'].keys():
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
                ppocr_format.append(format_tmp)
                processor(cords,filename,text)
                
        final_op="{}   {}".format(filename,ppocr_format)
        if os.path.exists(images_annotated_dir+filename) and len(final_op) != 0:
            shutil.copy(images_annotated_dir+filename,tmp_imgs_lbls+filename)
            with open('TEMP/ppocr_labels_imgs.txt', 'a') as f:
                f.write(final_op+'\n')
        else:
            print('imge file not exist : {}'.format(images_annotated_dir+filename))

                      
            
            

main()
