# import ultralytics
# from ultralytics import YOLO
import os
import shutil
import cv2
import numpy as np
import openpyxl

def detect_object(image_path,confidences):
        # image_path = 'image1x2.jpg'
        
        # Initialize the YOLO model
        model_path = 'last.pt'
        # model = YOLO(model_path)

        # # Perform the prediction
        # results = model.predict(
        #     source="splitted_data/"+image_path,
        #     conf=0.25,
        #     save=True,
        #     project="results",
        #     name="p1"
        # )

        # Display the output image
        # # print(results[0])
        # result_object = results[0]
        result_object = {}
        conf = compute_confidence(result_object,confidences)

        # Specify the source file path (the image you want to move)
        source_file = 'results/p1/'+image_path

        # Specify the destination folder path
        destination_folder = 'predicted'

        # Use shutil.move to move the file to the destination folder
        try:
            shutil.move(source_file, os.path.join(destination_folder, os.path.basename(source_file)))
            # print(f"Moved '{source_file}' to '{destination_folder}'.")
        except FileNotFoundError:
            print(f"The file '{source_file}' does not exist.")
        except shutil.Error as e:
            print(f"Error moving the file: {e}")


        # Specify the path of the folder you want to delete
        folder_path = 'results/p1'

        # Optionally, check if the folder exists before deleting it
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        else:
            print(f"The folder '{folder_path}' does not exist.")
        return conf


def compute_confidence(result,confidences):
    for i in result.boxes:
        confidences[int(i.cls[0])].append(float(i.conf[0]))
    return confidences


def split_image(rows,columns,parts,path):
  # Load the image
  image = cv2.imread(path)
  # Get the height and width of the image
  height, width , _= image.shape
  # Calculate the dimensions for splitting into rows and columns
  split_height = height // rows
  split_width = width // columns
  #spliting the images
  h1 = 0
  image_count = 0
  for i in range(rows):
    w1 = 0
    h2 = h1+split_height
    w2 = w1+split_width
    for j in range(columns):
      if i==(rows-1):
        h2 = height
      if j==(columns-1):
        w2 = width
      # print(h1,h2,w1,w2)
      part = image[h1:h2,w1:w2]
      cv2.imwrite("splitted_data/"+parts[image_count], part)
      image_count += 1
      w1 += split_width
      w2 += split_width
    h1 += split_height
  return 


def merge_image(rows,columns,parts):
  #create 2d array to held the sizes of individual images
  predicted_path = "predicted\\"
  sizes = []
  image_count = 0
  for i in range(rows):
    l = []
    for j in range(columns):
      part = cv2.imread(predicted_path+parts[image_count])
      l.append(part.shape[:2])
      image_count += 1
    sizes.append(l)
  
  #finding the final image co-ordinates
  h1 = 0
  w1 = 0
  #finding the final image height
  for i in range(rows):
    h1 += sizes[i][0][0]
  #finding the final image width
  for i in range(columns):
    w1 += sizes[0][i][1]
  # Create an empty canvas for the merged image
  merged_image = np.zeros((h1, w1, 3), dtype=np.uint8)
  
  # Place the split images onto the canvas in the correct positions
  h = 0
  w = 0
  image = 0
  for i in range(rows):
    w = 0
    for j in range(columns):
      merged_image[h:h+sizes[i][j][0],w:w+sizes[i][j][1]] = cv2.imread(predicted_path+parts[image])
      image+=1
      w += sizes[i][j][1]
    h += sizes[i][j][0]
  # Save the merged image
  cv2.imwrite('merged_image.jpg', merged_image)
  return


def satelite_image_detection(rows,columns,path,labels,confidences):
    # rows = 7
    # columns = 13
    folder_path = 'results/p1'
        # Optionally, check if the folder exists before deleting it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        
    n = rows*columns
    parts = []
    for i in range(n):
        parts.append("part"+str(i+1)+".jpg")
    # path = 'download.jpeg'

    #splitting the image into parts
    split_image(rows,columns,parts,path)
    
    #detecting the objects
    for i in parts:
        confidences = detect_object(i,confidences)

    #merging the image parts
    merge_image(rows,columns,parts)
    
    clean_folder("predicted")
    clean_folder("splitted_data")
    save_to_Excel(confidences,labels)
    return


def save_to_Excel(confidences,labels):
    final_conf = {}
    for i in confidences.keys():
        if(len(confidences[i])>0):
            final_conf[labels[i]]=round((sum(confidences[i])/len(confidences[i])), 4)
    workbook = openpyxl.load_workbook('my_data.xlsx')

    # Select a specific sheet in the workbook (change 'Sheet1' to your sheet name)
    sheet = workbook['Sheet1']
    
    num_rows = sheet.max_row
    

    data = []
    for i in final_conf.keys():
        num_rows += 1
        data.append(["ID"+str(num_rows),i,final_conf[i]])
    
    for row in data:
        sheet.append(row)

    # Save the workbook to a file
    workbook.save('my_data.xlsx')

    # Close the workbook
    workbook.close()
    
    return


def clean_folder(folder_path):
    # Iterate over the files and subfolders in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Check if the item is a file (not a subfolder)
        if os.path.isfile(file_path):
            os.remove(file_path) 
    return

# rows = 7
# columns = 13
# image_path = 'input_image.jpg'
# # labels = {0:'building',1:'rail_network',2:'agriculture_land',3:'trees',4:'water_bodies',5:'road_network'}
# # confidences = {0:[],1:[],2:[],3:[],4:[],5:[]}
# ls = {0:'building',1:'rail_network',2:'agriculture_land',3:'trees',4:'water_bodies',5:'road_network'}
# cs = {0:[],1:[],2:[],3:[],4:[],5:[]}
# satelite_image_detection(rows,columns,image_path,ls,cs)
