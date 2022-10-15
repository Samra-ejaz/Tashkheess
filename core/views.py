from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import KidneyStoneDetection, Report, Meeting
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import KidneyImageUploadForm, ReportForm, MeetingForm
from django.contrib.auth import get_user_model
from django.contrib import messages
import io
import cv2
import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
from django.core.files.base import ContentFile
from django.conf import settings
import numpy as np

User = get_user_model()


def index(request):
    return render(request, "index.html")

@login_required
def patient_list(request):
    patients = User.objects.filter(user_type="PT")
    return render(request, "patients/patient_list.html", {"patients": patients})

@login_required
def patient_detail(request, id):
    patient = get_object_or_404(User, id=id)
    return render(request, "patients/patient_detail.html", {"patient": patient})

@login_required
def reports_list(request):
    reports = Report.objects.filter(uploaded_by=request.user)
    return render(request, "reports/reports_list.html", {"reports": reports})

@login_required
def report_detail(request, uuid):
    report = get_object_or_404(Report, uuid=uuid)
    return render(request, "reports/report_detail.html", {"report": report})

@login_required
def meetings(request):
    if request.user.user_type == "PT":
        meetings = Meeting.objects.filter(patient=request.user)
    elif request.user.user_type == "DR":
        meetings = Meeting.objects.filter(doctor=request.user)
    return render(request, "meetings/meetings_list.html", {"meetings": meetings})


class ArrangeMeetingView(FormView, LoginRequiredMixin):
    template_name = "meetings/arrange_meeting.html"
    form_class = MeetingForm
    success_url = "/"

    def form_valid(self, form):
        form.save(user=self.request.user)
        messages.success(self.request, "Meeting Scheduled.")
        return super().form_valid(form)


class ReportFormView(FormView, LoginRequiredMixin):
    template_name = "reports/report_form.html"
    form_class = ReportForm
    success_url = "/reports/"

    def form_valid(self, form):
        form.save(request=self.request)
        return super().form_valid(form)

def detect_kidney_stones(request):
    context = {}
    if request.method == 'POST':
        form = KidneyImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("yes")
            instance = KidneyStoneDetection.objects.create(
                orignal_image=form.cleaned_data["image"],
                uploaded_by=request.user,
            )
            # Load Image with PIL
            # img = cv2.imread("./imgs/STONE- (3140).jpg")
            # image = cv2.cvtColor(instance.image, cv2.COLOR_BGR2RGB)
            # pilImage = Image.fromarray(image)
            pilImage = Image.open(instance.orignal_image)

            # Convert to JPEG Buffer
            buffered = io.BytesIO()
            pilImage.save(buffered, quality=100, format="JPEG")

            # Build multipart form and post request
            m = MultipartEncoder(
                fields={"file": ("imageToUpload", buffered.getvalue(), "image/jpeg")}
            )

            response = requests.post(
                f"https://detect.roboflow.com/{settings.ROBOFLOW_PROJECT_ID}/{settings.ROBOFLOW_MODEL_VERSION}?api_key={settings.ROBOFLOW_PROJECT_API_KEY}",
                data=m,
                headers={"Content-Type": m.content_type},
            )

            print(response)
            print(response.json())
            response_json = response.json()
            predictions = response_json.get("predictions")


            # figure, axes = plt.subplots()
            # axes.imshow(pilImage)
            # img_byte_arr = io.BytesIO()
            # pilImage.save(img_byte_arr, format=pilImage.format)
            # img_byte_arr = img_byte_arr.getvalue()

            arr = np.asarray(bytearray(buffered.getvalue()), dtype=np.uint8)
            bytesImg = cv2.imdecode(arr, -1)
            for prediction in predictions:
                x = prediction["x"]
                y = prediction["y"]
                width = prediction["width"]
                height = prediction["height"]
                class_name = prediction["class"]
                # Draw bounding boxes for object detection prediction
                cv2.rectangle(
                    bytesImg,
                    (int(x - width / 2), int(y + height / 2)),
                    (int(x + width / 2), int(y - height / 2)),
                    (255, 0, 0),
                    10,
                )
                # Get size of text
                text_size = cv2.getTextSize(
                    class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1
                )[0]
                # Draw background rectangle for text
                cv2.rectangle(
                    bytesImg,
                    (int(x - width / 2), int(y - height / 2 + 1)),
                    (
                        int(x - width / 2 + text_size[0] + 1),
                        int(y - height / 2 + int(1.5 * text_size[1])),
                    ),
                    (255, 0, 0),
                    -1,
                )
                # Write text onto image
                cv2.putText(
                    bytesImg,
                    class_name,
                    (int(x - width / 2), int(y - height / 2 + text_size[1])),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (255, 255, 255),
                    thickness=1,
                )

            # final_image = cv2.imwrite("result.jpg", bytesImg)
            ret, buf = cv2.imencode(".jpg", bytesImg)  # cropped_image: cv2 / np array
            content = ContentFile(buf.tobytes())
            instance.processed_image = SimpleUploadedFile(
                instance.orignal_image.name, content.read(), content_type="image/jpeg"
            )
            instance.number_of_stones = len(predictions)
            instance.is_stone_detected = True if len(predictions) > 0 else False
            instance.save()

            context["stone_detection"] = instance
            
            return render(request, 'reports/detect_kidney_stone.html', context)

    else:
        form = KidneyImageUploadForm()

    context['form'] = form

    return render(request, 'reports/detect_kidney_stone.html', context)