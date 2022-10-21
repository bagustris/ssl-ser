Notes:  
1. convert_label.sh is used to generate CMU_MOSEI_Labels.csv
2. Install necessary additional packages. In Ubuntu,
   $ sudo apt install ffmpeg libavcodec-extra
3. segment_audio.py is used by segment_audio.sh to segment audio. 
   Run this bash file after changing the location of your CMU-MOSE Audio.
   $ ./segment_audio.sh
   You may need to change the permission (`chmod +x')
