class thres:
    
    def thres2(gray):
        import cv2 as cv
        
        
        gray = cv.threshold(gray, 0, 255,
        	cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
            
        
        gray = cv.medianBlur(gray, 3)
            
        filex = gray
        
        return filex