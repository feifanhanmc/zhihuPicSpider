# -*- coding: utf-8 -*-
import requests

class Facepp:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.detect_req_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    
    def has_female(self, image_url):
        return_attributes = 'gender,age'
        faces_list = self.detect_by_image_url(image_url, return_attributes)
        if not faces_list:
            return False
        else:
            for face in faces_list:
                try:
                    if face['attributes']['gender']['value'] == 'Female':
                        return True
                except:
                    pass
            else:
                return False
            
    def detect_by_image_url(self, image_url, return_attributes = None):
        data = {'api_key' : self.api_key,
                'api_secret' : self.api_secret,
                'image_url' : image_url,
                'return_attributes' : return_attributes
        }
        faces_list = []
        try:
            r = requests.post(self.detect_req_url, data = data)
            faces_list = r.json()['faces']
        except:
            pass
        return faces_list
    
if __name__ == "__main__":
    p = Facepp('FR2qXQzfPwSzjZNC1KSdQBiJD8h_sVIx','0M7jG1b4nxdp6eBH8nnirkcefUWD91C-')
    image_url = 'https://pic2.zhimg.com/v2-cee25f70eadb4b477d74a7017f220b61_b.jpg'    #女
#     image_url = 'https://pic1.zhimg.com/27a1a0c48a799f60b655d8949879949c_b.png'    #狗
#     image_url = 'https://pic4.zhimg.com/v2-8709766148ac3bada3e96c2771a17feb_b.jpg'    #男
    print p.has_female(image_url)


