import cv2

class Decorators:

    @staticmethod
    def get_grayscale(function):
        def wrapper(self, image):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return function(self, image)
        return wrapper
    
    @staticmethod
    def applyAddaptiveThresholdingMean(function):
        def wrapper(self, image):
            image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,11,2)
            return function(self, image)
        return wrapper

    @staticmethod
    def applyAddaptiveThresholdingGaussian(function):
        def wrapper(self, image):
            image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
            return function(self, image)
        return wrapper

    @staticmethod
    def applyThresholding(function):
        def wrapper(self, image):
            (T, image) = cv2.threshold(image, 170, 255, cv2.THRESH_BINARY_INV)
            return function(self, image)
        return wrapper

    @staticmethod
    def applyThresholdingOtsu(function):
        def wrapper(self, image):
            (T, image) = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            return function(self, image)
        return wrapper
