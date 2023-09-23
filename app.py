import streamlit as st
from PIL import Image
from main import satelite_image_detection 

# Streamlit UI
# Set the company logo image path







cols = st.columns([1,1])

logo_image_path = "QAIG.jpg"
image1 = Image.open(logo_image_path)
# image1 = image1.resize((300,150))
# Display the company logo
cols[0].image(image1)


# title_style = """
#     <style>
#         /* Change the color to red (you can use any valid CSS color value) */
#         .title {
#             color: red;
#         }
#     </style>
# """

# # Display the title with the custom style
# cols[1].markdown(f'<h1 class="title">OBJECT DETECTION</h1>', unsafe_allow_html=True)

satra_logo_image_path = "satra_logo.jpg"
image2 = Image.open(satra_logo_image_path)
image2 = image2.resize((270,342))
cols[1].image(image2)



st.title("OBJECT DETECTION")
# st.write("Upload a .tif image for display:")

# Upload a .tif image
uploaded_image = st.file_uploader("Choose a image...", type=["tif", "tiff","jpg","png"])

if uploaded_image is not None:
    # Read the uploaded image
    image_type = uploaded_image.type
    if image_type == 'image/tiff':
        tif_image = Image.open(uploaded_image)
        if tif_image.mode != 'RGB':
            tif_image = tif_image.convert('RGB')
        # Convert and save it as a .jpg image
        tif_image.save("input_image.jpg")
        uploaded_image = Image.open("input_image.jpg")
    else:
       uploaded_image.save("input_image.jpg")
        
    # Display the uploaded image
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    if st.button("Detect"):
        rows = 7
        columns = 13
        labels = {0:'building',1:'rail_network',2:'agriculture_land',3:'trees',4:'water_bodies',5:'road_network'}
        confidences = {0:[],1:[],2:[],3:[],4:[],5:[]}
        st.session_state.prediction = True
        if st.session_state.prediction == True:
            satelite_image_detection(rows,columns,"input_image.jpg",labels,confidences)
    
        jpeg_image = Image.open("merged_image.jpg")
        # Save the TIFF image
        jpeg_image.save("output.tif")
        
        logo_image_path = "output.tif"
        pred_image = Image.open(logo_image_path)
        st.image(pred_image, caption="predicted Image", use_column_width=True)

if 'prediction' not in st.session_state:
    st.session_state.prediction = False



