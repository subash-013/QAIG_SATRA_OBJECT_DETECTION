import streamlit as st
from PIL import Image
from main import satelite_image_detection 

# Streamlit UI
# Set the company logo image path
cols = st.columns([1, 2])
logo_image_path = "logo.jpeg"
image1 = Image.open(logo_image_path)
image1 = image1.resize((200,150))
# Display the company logo
cols[0].image(image1)


title_style = """
    <style>
        /* Change the color to red (you can use any valid CSS color value) */
        .title {
            color: red;
        }
    </style>
"""

# Display the title with the custom style
cols[1].markdown(f'<h1 class="title">QUANTUM AI GLOBAL</h1>', unsafe_allow_html=True)





st.title("Satelitie Image Detection")
# st.write("Upload a .tif image for display:")

# Upload a .tif image
uploaded_image = st.file_uploader("Choose a image...", type=["tif", "tiff","jpg","png"])

if uploaded_image is not None:
    # Read the uploaded image
    image_type = uploaded_image.type
    if image_type == 'image/tiff':
        tif_image = Image.open(uploaded_image)
        if tif_image.mode == 'P':
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
        st.session_state.prediction = True
        if st.session_state.prediction == True:
            satelite_image_detection(rows,columns,"input_image.jpg")
    
        jpeg_image = Image.open("merged_image.jpg")
        # Save the TIFF image
        jpeg_image.save("output.tif")
        
        logo_image_path = "output.tif"
        pred_image = Image.open(logo_image_path)
        st.image(pred_image, caption="predicted Image", use_column_width=True)

if 'prediction' not in st.session_state:
    st.session_state.prediction = False



