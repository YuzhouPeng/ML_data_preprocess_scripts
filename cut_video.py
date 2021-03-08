import os
os.system("ffmpeg  -i FiberFault.mp4 -vcodec copy -acodec copy -ss 00:00:00 -to 00:13:20 ./cutout1.mp4 -y")