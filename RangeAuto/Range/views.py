import _thread as th
import os
import tensorflow as tf
import time
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import warnings
import threading
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .decorators import *
import numpy as np
import cv2
from PIL import Image
import io
import uuid
from datetime import date
# Create your views here.


# detect_fn = None
# category_index = None

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Enable GPU dynamic memory allocation
# gpus = tf.config.experimental.list_physical_devices('GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu, True)

# PROVIDE PATH TO IMAGE DIRECTORY
# IMAGE_PATHS = r'M:\\tf\\Tensorflow\\training_demo\\images\\train\\2.jpg'

# PROVIDE PATH TO MODEL DIRECTORY
# PATH_TO_MODEL_DIR = r'M:\idp_detection\my_model'
PATH_TO_MODEL_DIR = r'.\model'
# PROVIDE PATH TO LABEL MAP
# PATH_TO_LABELS = r'M:\idp_detection\my_model\saved_model\label_map.pbtxt'
PATH_TO_LABELS = r'.\model\saved_model\label_map.pbtxt'
# PROVIDE THE MINIMUM CONFIDENCE THRESHOLD
MIN_CONF_THRESH = float(0.60)

# LOAD THE MODEL

PATH_TO_SAVED_MODEL = PATH_TO_MODEL_DIR + "\saved_model"

print('Loading model...', end='')
start_time = time.time()

# LOAD SAVED MODEL AND BUILD DETECTION FUNCTION
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

end_time = time.time()
elapsed_time = end_time - start_time
print('Done! Took {} seconds'.format(elapsed_time))

# LOAD LABEL MAP DATA FOR PLOTTING

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                    use_display_name=True)

warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings


def load(name):
    IMAGE_PATHS = os.path.join(
        'static', 'image', '{}.jpg'.format(name))

    # def load_image_into_numpy_array(path):
    #     return np.array(Image.open(path))

    # print('Running inference for {}... '.format(IMAGE_PATHS), end='')
    image = cv2.imread(IMAGE_PATHS)
    # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image_expanded = np.expand_dims(image_rgb, axis=0)

    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    # input_tensor = np.expand_dims(image_np, 0)
    detections = detect_fn(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(detections.pop('num_detections'))

    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(
        np.int64)

    image_with_detections = image.copy()

    # SET MIN_SCORE_THRESH BASED ON YOU MINIMUM THRESHOLD FOR DETECTIONS
    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_with_detections,
        detections['detection_boxes'],
        detections['detection_classes'],
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=200,
        min_score_thresh=0.15)
    # agnostic_mode=False)
    image_with_detections = cv2.cvtColor(
        image_with_detections, cv2.COLOR_RGB2BGR)
    print('Done')
    any = detections['detection_scores']
    total = 0
    for i in any:
        if i > .15:
            total = total+1
    # DISPLAYS OUTPUT IMAGE
    image_with_detections = cv2.cvtColor(
        image_with_detections, cv2.COLOR_BGR2RGB)
    IMAGE_PATHS_DETECT = os.path.join(
        'static', 'image', '{}.detected.jpg'.format(name))
    cv2.imwrite(IMAGE_PATHS_DETECT,
                image_with_detections)
    return total


@unauthenticated_user
def home(request):
    # th.start_new_thread(load, ())
    return render(request, 'home.html')


@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == 'Unit-User':
                    return redirect('inputfirer')
                elif group == 'Range-Admin':
                    return redirect('adddetail')
            else:
                return redirect('invalid')
        else:
            messages.info(request, "User with this credentials doesn't exist.")
    return render(request, 'login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def aboutus(request):
    return render(request, 'aboutus.html')


@login_required(login_url='login')
@allowed_user(allowed_role=['Unit-User'])
def showmember(request):
    firer = Firer.objects.all()
    context = {'firer': firer}
    return render(request, 'showmember.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['Unit-User'])
def inputfirer(request):
    form = FirerForm()
    if request.method == 'POST':
        form = FirerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "New Firer Created.")
        else:
            messages.warning(
                request, "Wrong Credentials. Firer already exists with this credentials.")
    context = {'form': form}
    return render(request, 'inputfirer.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['Unit-User'])
def firingresult(request):
    firer = None
    if request.method == 'POST':
        number = request.POST['number']
        try:
            firer = Firer.objects.get(number=number)
            return redirect('result', pk=firer.id)
        except:
            messages.warning(
                request, "Person with this number doesnot exits. May be you have typed something wrong.")
    context = {}
    return render(request, 'firingresult.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['Unit-User'])
def result(request, pk):
    firer = Firer.objects.get(id=pk)
    result = Result.objects.filter(firer=firer)
    context = {'firer': firer, 'result': result}
    return render(request, 'result.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['Range-Admin'])
def adddetail(request):
    form = DetailForm()
    if request.method == 'POST':
        form = DetailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "New Detail Created.")
    context = {'form': form}
    return render(request, 'adddetail.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['Range-Admin'])
def compile(request):
    form = FireForm()
    if request.method == 'POST':
        form = FireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tgtimg')
    context = {'form': form}
    return render(request, 'compile.html', context)


def invalid(request):
    context = {}
    return render(request, 'invalid.html', context)


# image capture


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(
            'rtsp://IDP_A_B:1234asdf_@192.168.68.158:554/stream1')
        # self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        image1 = cv2.resize(image, (960, 540))
        name = str(uuid.uuid1())
        imgname = os.path.join(
            'static', 'image', '{}.jpg'.format(name))
        # cv2.imwrite(
        #     'static\\image\\try.jpg', image1)
        cv2.imwrite(imgname, image1)
        self.video.release()
        return name

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    frame = camera.get_frame()
    yield(b'--frame\r\n'
          b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    camera.__del__()


@login_required(login_url='login')
@allowed_user(allowed_role=['Range-Admin'])
@gzip.gzip_page
def tgtimg(request):
    try:
        cam = VideoCamera()
        name = cam.get_frame()
        detected_hits = load(name)
        fire = Fire.objects.last()
        f_id = fire.id
        if fire.new_target == False:
            f_id = f_id - 1
            last = Fire.objects.get(id=f_id).detected_hits
            hits = detected_hits - last
            if hits < 0:
                hits = 0
        else:
            hits = detected_hits
        imgname = os.path.join('{}.jpg'.format(name))
        IMAGE_PATHS_DETECT = os.path.join(
            '{}.detected.jpg'.format(name))
        fire.hits = hits
        fire.detected_hits = detected_hits
        fire.fired = imgname
        fire.detected = IMAGE_PATHS_DETECT
        fire.save()
        r = Result(firer=fire.detail.target_1, fire=fire)
        r.save()
        context = {'fire': fire}
        return render(request, 'tgtimg.html', context)
    except:
        pass


# Update
@login_required(login_url='login')
@allowed_user(allowed_role=['Unit-User'])
def updatefirer(request, pk):
    firer = Firer.objects.get(id=pk)
    form = FirerForm(instance=firer)
    if request.method == 'POST':
        form = FirerForm(request.POST, instance=firer)
        if form.is_valid():
            form.save()
            messages.info(request, "Firer Updated.")
        else:
            messages.warning(
                request, "Wrong Credentials. Firer already exists with this credentials.")
    context = {'form': form}
    return render(request, 'inputfirer.html', context)
# def detect(request):
#     hits = load()
#     context = {'hits': hits}
#     return render(request, 'test2.html', context)
# delete


@login_required(login_url='login')
@allowed_user(allowed_role=['Unit-User'])
def deletefirer(request, pk):
    firer = Firer.objects.get(id=pk)
    if request.method == 'POST':
        firer.delete()
        return redirect('showmember')
    context = {'firer': firer}
    return render(request, 'deletefirer.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['Range-Admin'])
def showdetail(request):
    today = date.today()
    try:
        detail = Detail.objects.filter(date=today)
    except:
        detail = None
    context = {'detail': detail}
    return render(request, 'showdetail.html', context)


# Update
@login_required(login_url='login')
@allowed_user(allowed_role=['Range-Admin'])
def updatedetail(request, pk):
    detail = Detail.objects.get(id=pk)
    form = DetailForm(instance=detail)
    if request.method == 'POST':
        form = DetailForm(request.POST, instance=detail)
        if form.is_valid():
            form.save()
            # messages.info(request, "Detail Updated.")
            return redirect('showdetail')
    context = {'form': form}
    return render(request, 'adddetail.html', context)
# def detect(request):
#     hits = load()
#     context = {'hits': hits}
#     return render(request, 'test2.html', context)
# delete


@login_required(login_url='login')
@allowed_user(allowed_role=['Range-Admin'])
def deletedetail(request, pk):
    detail = Detail.objects.get(id=pk)
    if request.method == 'POST':
        detail.delete()
        return redirect('showdetail')
    context = {'detail': detail}
    return render(request, 'deletedetail.html', context)
