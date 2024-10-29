from flask import Flask, request, jsonify,render_template
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration       
cloudinary.config( 
    cloud_name = "dq67ufqzg", 
    api_key = "613482934461827", 
    api_secret = "V-UqeYavan7egZA1aN8CSyvlLjo", # V-UqeYavan7egZA1aN8CSyvlLjo
    secure=True
)

app = Flask(__name__)

@app.route('/')
def home():
    print('Im inside home page')
    return render_template('cloudDemo.html')
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Upload the image to Cloudinary
        upload_result = cloudinary.uploader.upload(file)
        # Get the URL of the uploaded image
        image_url = upload_result#['secure_url']
        print(image_url)
        # Optionally store the image URL in your database here
        return jsonify({"message": "Image uploaded successfully", "image_url": image_url['secure_url']}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
'''
const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://your-flask-backend-url/upload', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    if (response.ok) {
      console.log('Image uploaded successfully:', result.image_url);
    } else {
      console.error('Error uploading image:', result.error);
    }
  } catch (error) {
    console.error('Error:', error);
  }
};

// Assume you have an input element to select the file
document.getElementById('file-input').addEventListener('change', (event) => {
  const file = event.target.files[0];
  uploadImage(file);
});

'''


'''
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Read the raw binary data from request.data
        file_data = request.data

        if not file_data:
            return jsonify({"error": "No file data received"}), 400

        # You can create an in-memory file object from the raw data
        file = io.BytesIO(file_data)

        # Upload the image to Cloudinary
        upload_result = cloudinary.uploader.upload(file)

        # Get the URL of the uploaded image
        image_url = upload_result['secure_url']

        return jsonify({"message": "Image uploaded successfully", "image_url": image_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

'''