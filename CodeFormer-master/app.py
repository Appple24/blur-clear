# Clone CodeFormer and enter the CodeFormer folder
import os

# Clone CodeFormer and enter the CodeFormer folder
#def fun():
#os.system('python inference_codeformer.py -w 0.7 --input_path runtime_inputs/image.png --bg_upsampler realesrgan --face_upsample --bg_upsampler realesrgan')


from flask import *
import uuid

app=Flask(__name__)

UPLOAD_FOLDER = 'runtime_inputs'
OUTPUT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        #check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]  # Generate a unique filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            file.save(file_path)

            #return redirect(url_for('process_and_show', filename=filename))
            file_name=process_and_show(filename)
            file_name=(file_name.split("."))[0]+'.png'
            # Replace 'path_to_image' with the path to your image file
            image_path = 'results\\test_img_0.7\\final_results\\'+file_name
            print(image_path)
            return send_file(image_path, mimetype='image/jpeg')

            # with open('/runtime_inputs/image.png', 'rb') as img_file:
            #     image_content = img_file.read()
            # mime_type = 'image/jpeg'
            # return send_file(image_content, mimetype=mime_type)


#@app.route('/process_and_show/<filename>')
def process_and_show(filename):
    print('python inference_codeformer.py -w 0.7 --input_path runtime_inputs/{} --bg_upsampler realesrgan --face_upsample --bg_upsampler realesrgan'.format(filename))
    
    os.system('python inference_codeformer.py -w 0.7 --input_path runtime_inputs/{} --bg_upsampler realesrgan --face_upsample --bg_upsampler realesrgan'.format(filename))
    return filename

@app.route('/home')
def home():
    return render_template("base.html")

        




if __name__=="__main__":
    app.run(debug='true')