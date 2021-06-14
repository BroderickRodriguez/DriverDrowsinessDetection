#ear threshold, subject to change
EYE_AR_THRESH = 0.3

#frame threshold for early closing eyes
EYE_AR_CONSEC_FRAMES = 48 # 3s Time threshold of person closing eyes

# normal blink is 400ms(0.4), 0.4 x avg fps
BLINK_THRESH = 6

# frames where your face is not seen,  (>2 seconds) 2*30 or 2*15
# source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3999409/#:~:text=According%20to%20analyses%20of%20data,a%20crash%20or%20near%20crash.
NOFACE_THRESH = 32

# total frames for perclos
TOTAL_WINDOW_FRAMES = 600

# source: https://iopscience.iop.org/article/10.1088/1742-6596/1090/1/012037/pdf
awake = 0
slight_drowsy = 30
drowsy = 60
