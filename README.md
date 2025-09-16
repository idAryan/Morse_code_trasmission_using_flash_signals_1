# Morse Based Communication 
A morse Code communication based app.
## Approach 1 : Classical OpenCV 
OpenCV is popular computer vision library. It could be used in Image Processing.
Lets understand how open cv works here

1) Import necessary libraries  
   `cv2(to process frames), numpy(need for faster image operation), time(time duration for enc-dec)`
     
2) Create Morse Dictionary  
   `{'.-': 'A', '-...': 'B'}`
     
3) Function for `create_circular_mask` to detect only in mask region
     
4) Function for `detect_light_in_circle` to detect light only in circular region  
   i) Frame Input : The input image is in RGB format (3 channel image)  
   ii) Gray Scale Conversion : So adjust color variance. The image become 1 channel and only have range of (0-255)  
   iii) apply Circular mask to detect in circular region only rest become 0(black)    
   iv) apply Gaussian Blur to smoothen the image : As What is Blur ? It is the weighted average of pixels around them. Close neighbor have more weight then others.  
   v) Apply brightness threshold : Pixels above 240 brightness become White rest become black, so overall image inside mask now in form of 0 and 1 only where in single channel image, pixel above the threshold(240) become white(1) and rest become black(0)   
   vi) `cv2.findContours` will find the bright spots, it will detect the white boundaries of white pixels (1). It will return the list of countours each forming boundary around the detected bright spots.  
5) There could be multiple contour detections, so it could provide multiple lists. So need to apply area thresholding also (previosly appled brightness threshold), so create a areathreshold function. If area is large enough in comparision to threshold treat it as a flash, otherwise not a flash. 
   ```
   for contour in countours:  
      if cv2.contourArea(countour)>areathreshold:  
         return True,contour  
   return contour
   ```
6) Declare Timing parameters  
   `DIT_MAX_DUR`=0.3 (.,_ are considered as DIT (.))  
   `LETTER_GAP`=0.7 (.--..., in english it is AB and there should be some letter gap duration, to differentiate that the new letter is begin from certain point)  
   `WORD_GAP`=1.4 (To find where the new words starts .-.--...-... in english it is AA BB, so the space between AA and BB is represented by the given duration)  
   The - is determined if Duration of Flash is more then `DIT_MAX_DUR` bit less than `LETTER_GAP`.  
7) Declare function `decode_morse_code_to_english`, it will map ....  
8) Write videocapture code, 0 means default camera, if you have another camera linked to PC/device then you could change it.
   ```
   cap=cv2.VideoCapture(0)
   if not cap.isOpened():
      print("Cannot access webcam")
      return
   ```
9) Declare the empty variables for morse code `current_morse` and decoded text `decoded text`
   Set the last flash status as `off` `last_light_state=False`
   To measure the timings set two variables to track, `light_start_time=0` and `last_light_end_time=0`.
   

### Challenges & Possible solutions in approach 1  
1) Brightness threshold could change according to environment : Since brightness is not constant, it varies place to place, if outside brightness is large enough and satisfies the threshold value, then it will assume it as bright enough as convert the pixels to white (1) in single channel image. Now since it is large enough then it will also satisfies the area threshold due to will `areathreshold` function will return `true`. Thus it will easily fail in outside environment.
   #### Solution: 
   Rather then using a constant brightness threshold use `adaptive brightness thresholding` as it will adjust the threshold value according to the environment. Thus will minimize the false white pixels so areathreshold  will not satisfy thus flashlight will not be detected.
     
2) Hardcoded areathreshold : The area of a flash varies with distance, if flash is far enough then area will be less so there would be less white pixels so areathresholding fails here.
   #### Solution:
   Test the expected flashlight area to various distances and add a expected flashlight distance option in it.
   

## Dataset & References
https://www.kaggle.com/datasets/itsaryanar/smartphone-flashlight-image-mask-dataset-sfimd
