from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from mysite.camera import VideoCamera, gen
from django.http import StreamingHttpResponse


class Home(TemplateView):
    template_name = 'home.html'



# for video input and detection
# the whole thing, video
# is returned as a streaming http response, or bytes
def video_stream(request):
    vid = StreamingHttpResponse(gen(VideoCamera(), False), 
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid


def video_input(request):
    return render(request, 'camera.html')