import os
import io
import platform
from base64 import encodebytes

from flask import Flask, request
from flask_restful import Resource, Api, abort

from PIL import Image


IS_PI = False

if platform.uname().machine == "armv6l":
    from protodriver import leddriver
    IS_PI = True


app = Flask(__name__)
api = Api(app)
UPLOAD_DIRECTORY = "api_uploaded_files"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def find_file(filename):
    if "/" in filename:
        abort(400)
    if not os.path.exists(os.path.join(UPLOAD_DIRECTORY, filename)):
        abort(404)


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


class Ping(Resource):
    def get(self):
        return {"data": "Pong"}


class UploadImage(Resource):
    def post(self, filename):
        if "/" in filename:
            abort(400)

        if os.path.exists(os.path.join(UPLOAD_DIRECTORY, filename)):
            abort(409)

        with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
            fp.write(request.data)

        return "File Created", 201


class UpdateImage(Resource):
    def put(self, filename):

        find_file(filename)
        with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
            fp.write(request.data)

        return "File Created", 200


class DeleteImage(Resource):
    def delete(self, filename):

        find_file(filename)
        os.remove(os.path.join(UPLOAD_DIRECTORY, filename))


class GetImage(Resource):
    def get(self, filename):

        find_file(filename)
        return get_response_image(os.path.join(UPLOAD_DIRECTORY, filename))


class GetAllImages(Resource):
    def get(self):
        files = [f for f in os.listdir(UPLOAD_DIRECTORY) if os.path.isfile(os.path.join(UPLOAD_DIRECTORY, f))]
        response = []
        for file in files:
            response.append((file, get_response_image(os.path.join(UPLOAD_DIRECTORY, file))))

        return {"data": response}


if IS_PI:

    class DisplayImage(Resource):
        def get(self, filename):
            find_file(filename)
            leddriver.display_image(os.path.join(UPLOAD_DIRECTORY, filename))
            return "Image displayed", 200

    class ClearDisplay(Resource):
        def get(self):
            leddriver.clear_display()
            return "Display Cleared", 200


api.add_resource(Ping, "/ping")
api.add_resource(UploadImage, "/uploadimage/<filename>")
api.add_resource(UpdateImage, "/updateimage/<filename>")
api.add_resource(DeleteImage, "/deleteimage/<filename>")
api.add_resource(GetImage, "/getimage/<filename>")
api.add_resource(GetAllImages, "/getallimages")

if IS_PI:
    api.add_resource(DisplayImage, "/displayimage/<filename>")
    api.add_resource(ClearDisplay, "/cleardisplay")


def run(**kwargs):
    app.run(**kwargs)


if __name__ == "__main__":
    print("Starting Api...")
    run(debug=True, port=5000)
