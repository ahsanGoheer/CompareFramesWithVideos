import pandas as pd
import xml.etree.ElementTree as ET
import sys
import os
from tqdm import tqdm

#csv_path=r"C:\Users\ahsan\Pictures\FIX FRAMES BY AHSAN GOHEER\Corrected_Frames.csv"

#path of the csv file containing the old and new names..
csv_path=sys.argv[1]
# Path of the folder in which the images and the xml files are located..
img_xml_folder_path = sys.argv[2]
csv_file = pd.read_csv(csv_path)
old_names = csv_file.iloc[:,1].tolist()
new_names=csv_file.iloc[:,2].tolist()
pbar = tqdm(total=len(old_names))
for name in old_names:
 try:
    pbar.update(1)
    index = old_names.index(name)
    new_name = new_names[index]
    new_name_path = os.path.join(img_xml_folder_path,new_name)   
    old_name_path = os.path.join(img_xml_folder_path,name)
    old_xml_path = os.path.join(img_xml_folder_path,name).replace(".jpg",".xml")  
    new_xml_path = os.path.join(img_xml_folder_path,new_name).replace(".jpg",".xml")
    xml_file = ET.parse(os.path.join(img_xml_folder_path,name).replace('.jpg','.xml'))
    root = xml_file.getroot()
    Frame_meta = root.find('FrameMetaData')
    Frame_meta.find('FrameNo').text=new_name.replace(".jpg","")
    xml_file.write(os.path.join(img_xml_folder_path,name).replace('.jpg','.xml'),encoding="UTF-8",xml_declaration=True)
    os.rename(old_name_path,new_name_path)
    os.rename(old_xml_path,new_xml_path)
 except:
    continue
pbar.close()