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
   v) Apply detection threshold : Pixels above 240 brightness become White rest become black, so overall image inside mask now in form of 0 and 1 only where in single channel image, pixel above the threshold(240) become white(1) and rest become black(0)   
   vi) `cv2.findContours` will find the bright spots, it will detect the white boundaries of white pixels (1). It will return the list of countours each forming boundary around the detected bright spots.  
