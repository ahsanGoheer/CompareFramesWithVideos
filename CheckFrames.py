import cv2
import sys
import glob
import os
import csv
from skimage.measure import compare_nrmse
from tqdm import tqdm
from decimal import *
import time

video_path = sys.argv[1]
frames_path = sys.argv[2]
image_file = glob.glob(os.path.join(frames_path,"*.jpg"))
name_of_vid = os.path.basename(video_path).replace(".mp4","")
csv_file = open(name_of_vid+".csv","w")
fieldNames = ["Path","Old Names","New Names","Time"]
name_dict={}
writer = csv.DictWriter(csv_file,fieldnames=fieldNames,dialect='excel')
writer.writeheader()
pbar  = tqdm(total=len(image_file))
checked_frames=[]
start = time.
for image in image_file:
    frame_num = 0
    cap = cv2.VideoCapture(video_path)
    no_of_frames= cap.get(cv2.CAP_PROP_FRAME_COUNT)
    pbar2=tqdm(total=no_of_frames)

    #print("{} has frames {}".format(os.path.basename(video_path),no_of_frames))
    pbar.update(1)            
    fps = cap.get(cv2.CAP_PROP_FPS)
    #print("{} has FPS : {}".format(os.path.basename(video_path),fps))
    time_of_video = (no_of_frames//fps)//60
    #print("Video Duration  : {}".format(time_of_video))
    if cap.isOpened == False:
        print("There's a problem getting the video!")    
    else:
        frame_Img = cv2.imread(image,0)
        width_FI = int(frame_Img.shape[1] *0.9)
        height_FI=int(frame_Img.shape[0]*0.9)
        dims_FI=(width_FI,height_FI)
        frame_Img = cv2.resize(frame_Img,dims_FI,interpolation=cv2.INTER_AREA)
        old_name = os.path.basename(image)
        #print("Processing FRAME : {}".format(old_name))
        name_dict["Path"]=image
        name_dict["Old Names"]=old_name
        while cap.isOpened():
            playing,frame_video = cap.read()
            width_FV = int(frame_video.shape[1] *0.9)
            height_FV=int(frame_video.shape[0]*0.9)
            dims_FV=(width_FV,height_FV)
            frame_video = cv2.resize(frame_video,dims_FV,interpolation=cv2.INTER_AREA)
            frame_video = cv2.cvtColor(frame_video, cv2.COLOR_BGR2GRAY)
            
            
            #print(frame_num)
            if  playing == True:
                #print("MSE : {}".format(compare_nrmse(frame_Img,frame_video)))
                #print(str(np.mean(frame_Img))+" "+str(np.mean(frame_video)))
                #if compare_ssim(frame_Img,frame_video,multichannel=True)<1 and compare_ssim(frame_Img,frame_video,multichannel=True)>0.998:
                if compare_nrmse(frame_Img,frame_video)<0.05:                 
                    required_frame= frame_num
                    new_name = os.path.basename(video_path).replace(".mp4","_{}.jpg".format(frame_num))
                    #print("CORRECT NAME : {}".format(new_name))
                    name_dict["New Names"]=new_name
                    time_of_frame=(Decimal(frame_num)//Decimal(fps))//Decimal(60)//Decimal(60)
                    #print("Time of Frame : {}".format(time_of_frame))
                    name_dict["Time"] = Decimal(time_of_frame)
                    work=writer.writerow(name_dict)
                    checked_frames.append(frame_num)
                    frame_num+=1
                    pbar2.update(1)
                    break
                else:
                    #Print(compare_ssim(frame_Img,frame_video,multichannel=True))    
                    frame_num+=1   
                    pbar2.update(1)
                    continue
            else:
                break
            
        cap.release()
        pbar2.close()
pbar.close()

csv_file.close()

