import os
import cloudinary
import cloudinary.uploader
#from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv

load_dotenv()

cloudinary.config( 
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key = os.getenv('CLOUDINARY_API_KEY'), 
    api_secret = os.getenv('CLOUDINARY_API_SECRET'), 
    secure=True
)

def storeImg(image):
    uploadResult=cloudinary.uploader.upload(image)
    print(uploadResult)
    secureUrl=uploadResult['secure_url']
    imgId=uploadResult['public_id']
    return secureUrl,imgId
    #checking if already an image exist if so need to delete from cloudinary
    #if user_data[6]:
    #    result=cloudinary.uploader.destroy(user_data[len(user_data)-1])
    #    print(result)            

def deleteImg(imageId):
    result=cloudinary.uploader.destroy(imageId)
    print(result)