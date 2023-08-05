from PIL import Image
import cv2 
from .config import ServerConfig
from .utils import cv2ToBytes, pilToBytes, printError
from .structs import FaceDetectionResponse, FaceRecognitionResponse, FaceListResponse
from .viz import drawResponse, saveResponse
import requests
import os
import validators
import numpy
import time
import uuid

class Face(object):
    def __init__(self,config: ServerConfig):
        self.config = config
        
    def __detect_face(self,image_data: bytes, min_confidence: float):
        response = requests.post(self.config.server_url+"v1/vision/face",
        files={"image": image_data},
        data={"api_key": self.config.api_key,"min_confidence":min_confidence}
        )

        return response

    def __recognize_face(self,image_data: bytes, min_confidence: float):
        response = requests.post(self.config.server_url+"v1/vision/face/recognize",
        files={"image": image_data},
        data={"api_key": self.config.api_key,"min_confidence":min_confidence}
        )

        return response

    #allow folder input, with exts param specifying comma separated exts
    def detectFace(self, image,format="jpg",min_confidence=0.4,output=None,callback=None, output_font=cv2.FONT_HERSHEY_SIMPLEX,output_font_color=(0,146,224)):
        if isinstance(image,str):
            if os.path.isfile(image):
                image_data = open(image,"rb").read()
            elif validators.url(image):
                image_data = requests.get(image).content
            else:
                raise Exception("file {} does not exist".format(image))
        elif isinstance(image,numpy.ndarray):
            image_data = cv2ToBytes(image,format=format)
        elif isinstance(image,Image.Image):
            image_data = pilToBytes(image,format=format)
        elif isinstance(image,bytes):
            image_data = image
        else:
            raise Exception("Unsupported input type: {}".format(type(image)))

        response = self.__detect_face(image_data, min_confidence)

        if response.status_code == 200:
            data = FaceDetectionResponse(response.json())
            if callback is not None:
                callback(image_data,data)
            if output is not None:
                saveResponse(image_data,data,output,output_font,output_font_color)

            return data
        elif response.status_code == 403:
            raise Exception("The scene endpoint is not enabled on the DeepStack server")
        elif response.status_code == 400:
            raise Exception("Invalid image")
        elif response.status_code == 500:
            raise Exception("An error occured on the DeepStack server")
        else:
            raise Exception("Unknown error : {} occured".format(response.status_code))

     #allow folder input, with exts param specifying comma separated exts
    def recognizeFace(self, image,format="jpg",min_confidence=0.7,output=None,callback=None, output_font=cv2.FONT_HERSHEY_SIMPLEX,output_font_color=(0,146,224)):
        if isinstance(image,str):
            if os.path.isfile(image):
                image_data = open(image,"rb").read()
            elif validators.url(image):
                image_data = requests.get(image).content
            else:
                raise Exception("file {} does not exist".format(image))
        elif isinstance(image,numpy.ndarray):
            image_data = cv2ToBytes(image,format=format)
        elif isinstance(image,Image.Image):
            image_data = pilToBytes(image,format=format)
        elif isinstance(image,bytes):
            image_data = image
        else:
            raise Exception("Unsupported input type: {}".format(type(image)))

        response = self.__recognize_face(image_data, min_confidence)

        if response.status_code == 200:
            print(response.json())
            data = FaceRecognitionResponse(response.json())
            if callback is not None:
                callback(image_data,data)
            if output is not None:
                saveResponse(image_data,data,output,output_font,output_font_color)

            return data
        elif response.status_code == 403:
            raise Exception("The scene endpoint is not enabled on the DeepStack server")
        elif response.status_code == 400:
            raise Exception("Invalid image")
        elif response.status_code == 500:
            raise Exception("An error occured on the DeepStack server")
        else:
            raise Exception("Unknown error : {} occured".format(response.status_code))

    def detectFaceVideo(self,video,min_confidence=0.4,output=None,codec=cv2.VideoWriter_fourcc(*'mp4v'),fps=24,display=False,callback=None, continue_on_error=False,output_font=cv2.FONT_HERSHEY_SIMPLEX,output_font_color=(0,146,224)):
        detections = {}
        video_input = cv2.VideoCapture(video)
        width  = video_input.get(3) 
        height = video_input.get(4)
        if output is not None:
            if isinstance(output,cv2.VideoWriter):
                out = output 
            else:   
                out = cv2.VideoWriter(output,codec,fps,((int(width), int(height))))
        
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        if int(major_ver)  < 3 :
            fps = video_input.get(cv2.cv.CV_CAP_PROP_FPS)
        else :
            fps = video_input.get(cv2.CAP_PROP_FPS)

        is_file = os.path.isfile(video)
        frame_count = 0

        while video_input.isOpened():
            valid, frame = video_input.read()
            if valid:
                frame_count = frame_count + 1
                frame_data = cv2ToBytes(frame)
                response = self.__detect_face(frame_data, min_confidence)
                data = None
                if response.status_code == 200:
                    data = FaceDetectionResponse(response.json())
                    detections[frame_count-1] = data
                    if callback is not None:
                        if is_file:
                            callback(frame_count/fps,frame_data,data)
                        else:
                            callback(time.time(),frame_data,data)
                   
                    if output is not None:
                        frame = drawResponse(frame,data,output_font,output_font_color)
                        
                elif response.status_code == 403:
                    if continue_on_error:
                        printError("The scene endpoint is not enabled on the DeepStack server")
                    else:
                        raise Exception("The scene endpoint is not enabled on the DeepStack server")
                elif response.status_code == 400:
                    if continue_on_error:
                        printError("Invalid image")
                    else:
                        raise Exception("Invalid image")
                elif response.status_code == 500:
                    if continue_on_error:
                        printError("An error occured on the DeepStack server")
                    else:
                        raise Exception("An error occured on the DeepStack server")
                else:
                    if continue_on_error:
                        printError("Unknown error : {} occured".format(response.status_code))
                    else:
                        raise Exception("Unknown error : {} occured".format(response.status_code))
                detections[frame_count-1] = data
                out.write(frame)

                if display:
                    cv2.imshow('Image Viewer', frame)
        
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        video_input.release()
        out.release()

        return detections

    def recognizeFaceVideo(self,video,min_confidence=0.7,output=None,codec=cv2.VideoWriter_fourcc(*'mp4v'),fps=24,display=False,callback=None, continue_on_error=False,output_font=cv2.FONT_HERSHEY_SIMPLEX,output_font_color=(0,146,224)):
        detections = {}
        video_input = cv2.VideoCapture(video)
        width  = video_input.get(3) 
        height = video_input.get(4)
        if output is not None:
            if isinstance(output,cv2.VideoWriter):
                out = output 
            else:   
                out = cv2.VideoWriter(output,codec,fps,((int(width), int(height))))
        
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        if int(major_ver)  < 3 :
            fps = video_input.get(cv2.cv.CV_CAP_PROP_FPS)
        else :
            fps = video_input.get(cv2.CAP_PROP_FPS)

        is_file = os.path.isfile(video)
        frame_count = 0

        while video_input.isOpened():
            valid, frame = video_input.read()
            if valid:
                frame_count = frame_count + 1
                frame_data = cv2ToBytes(frame)
                response = self.__recognize_face(frame_data, min_confidence)
                data = None
                if response.status_code == 200:
                    data = FaceRecognitionResponse(response.json())
                    detections[frame_count-1] = data
                    if callback is not None:
                        if is_file:
                            callback(frame_count/fps,frame_data,data)
                        else:
                            callback(time.time(),frame_data,data)
                   
                    if output is not None:
                        frame = drawResponse(frame,data,output_font,output_font_color)
                        
                elif response.status_code == 403:
                    if continue_on_error:
                        printError("The scene endpoint is not enabled on the DeepStack server")
                    else:
                        raise Exception("The scene endpoint is not enabled on the DeepStack server")
                elif response.status_code == 400:
                    if continue_on_error:
                        printError("Invalid image")
                    else:
                        raise Exception("Invalid image")
                elif response.status_code == 500:
                    if continue_on_error:
                        printError("An error occured on the DeepStack server")
                    else:
                        raise Exception("An error occured on the DeepStack server")
                else:
                    if continue_on_error:
                        printError("Unknown error : {} occured".format(response.status_code))
                    else:
                        raise Exception("Unknown error : {} occured".format(response.status_code))
                detections[frame_count-1] = data
                out.write(frame)

                if display:
                    cv2.imshow('Image Viewer', frame)
        
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        video_input.release()
        out.release()

        return detections

    def registerFace(self, images,userid,format="jpg"):
        files = {}
        for image in images:
            if isinstance(image,str):
                if os.path.isfile(image):
                    image_data = open(image,"rb").read()
                elif validators.url(image):
                    image_data = requests.get(image).content
                else:
                    raise Exception("file {} does not exist".format(image))
            elif isinstance(image,numpy.ndarray):
                image_data = cv2ToBytes(image,format=format)
            elif isinstance(image,Image.Image):
                image_data = pilToBytes(image,format=format)
            elif isinstance(image,bytes):
                image_data = image
            else:
                raise Exception("Unsupported input type: {}".format(type(image)))

            files["image"+str(uuid.uuid4())] = image_data

        response = requests.post(self.config.server_url+"v1/vision/face/register",
        files=files,
        data={"api_key": self.config.api_key,"userid":userid})

        if response.status_code == 200:
            return True
            
        elif response.status_code == 403:
            raise Exception("The scene endpoint is not enabled on the DeepStack server")
        elif response.status_code == 400:
            raise Exception("Invalid image")
        elif response.status_code == 500:
            raise Exception("An error occured on the DeepStack server")
        else:
            raise Exception("Unknown error : {} occured".format(response.status_code))

    def listFaces(self):
       
        response = requests.post(self.config.server_url+"v1/vision/face/list",
        data={"api_key": self.config.api_key})

        if response.status_code == 200:
            data = FaceListResponse(response.json())
            return data
            
        elif response.status_code == 403:
            raise Exception("The scene endpoint is not enabled on the DeepStack server")
        elif response.status_code == 400:
            raise Exception("Invalid image")
        elif response.status_code == 500:
            raise Exception("An error occured on the DeepStack server")
        else:
            raise Exception("Unknown error : {} occured".format(response.status_code))

    def deleteFace(self, userid):
        response = requests.post(self.config.server_url+"v1/vision/face/delete",
        data={"api_key": self.config.api_key,"userid":userid})

        if response.status_code == 200:
            return True
            
        elif response.status_code == 403:
            raise Exception("The scene endpoint is not enabled on the DeepStack server")
        elif response.status_code == 400:
            raise Exception("Invalid image")
        elif response.status_code == 500:
            raise Exception("An error occured on the DeepStack server")
        else:
            raise Exception("Unknown error : {} occured".format(response.status_code))
                




        




        

