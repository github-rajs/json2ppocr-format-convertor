import os
import shutil

#for text detection
ppocr_det_dataset_dir='DATASET/DET/'
det_train=ppocr_det_dataset_dir+'train/'
det_valid=ppocr_det_dataset_dir+'valid/'

#for text recognition
ppocr_rec_dataset_dir='DATASET/REC/'
rec_train=ppocr_rec_dataset_dir+'train/'
rec_valid=ppocr_rec_dataset_dir+'valid/'

#temp directory
#create these folder manually
tmp_imgs_lbls='TEMP/images/'
tmp_crop_imgs_lbls='TEMP/crops/'

#dataset split
dataset_train_split=80
dataset_valid_split=20

ppocr_det = open('TEMP/ppocr_labels_imgs.txt','r')
ppocr_det_lbls = ppocr_det.readlines()

ppocr_rec = open('TEMP/ppocr_labels_crops.txt','r')
ppocr_rec_lbls = ppocr_rec.readlines()

for_train_det=int(len(ppocr_det_lbls)/100*dataset_train_split)
for_valid_det=int(len(ppocr_det_lbls)/100*dataset_valid_split)

for_train_rec=int(len(ppocr_rec_lbls)/100*dataset_train_split)
for_valid_rec=int(len(ppocr_rec_lbls)/100*dataset_valid_split)

print('detection training train images:',for_train_det)
print('detection training validation images:',for_valid_det)
print('recognition training train :',for_train_rec)
print('recognition training valid:',for_valid_rec)

def det_dataset_create():
    with open("TEMP/ppocr_labels_imgs.txt") as file_in:
        counter=0
        for line in file_in:
            img=line.split()[0]
            lbl_data=line.strip('\n').split()[0]
            if counter <= for_train_det:
                if len(lbl_data) != 0:
                    shutil.copy(tmp_imgs_lbls+str(img),det_train+'images/'+img)
                    with open(det_train+'ppocr_train_labels.txt', 'a') as f:
                        f.write(line)
                else:
                    pass
            else:
                if len(lbl_data) != 0:
                    shutil.copy(tmp_imgs_lbls+str(img),det_valid+'images/'+img)
                    with open(det_valid+'ppocr_valid_labels.txt', 'a') as f:
                        f.write(line) 
                else:
                    pass 
            counter+=1
                    
                    

def rec_dataset_create():
    with open("TEMP/ppocr_labels_crops.txt") as file_in:
        counter=0
        for line in file_in:
            img=line.strip('\n').split()[0]
            if counter <= for_train_rec:
                shutil.copy(tmp_crop_imgs_lbls+str(img),rec_train+'images/'+img)
                with open(rec_train+'ppocr_train_labels.txt', 'a') as f:
                    f.write(line)
            else:
                shutil.copy(tmp_crop_imgs_lbls+str(img),rec_valid+'images/'+img)
                with open(rec_valid+'ppocr_valid_labels.txt', 'a') as f:
                    f.write(line)
            counter+=1
            
     
rec_dataset_create()
#det_dataset_create()
