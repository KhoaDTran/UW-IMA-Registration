# UW IMA Registration
Using selenium in python, script acquires any user desired IMA appointment that is currently offered, either avaliable or unavaliable, script will search for desired appointment slot until acquired or current time has passed. User can either search for appointments in the future or the present day. 

INSTRUCTIONS:
1. Install selenium in terminal using pip
    Run pip install selenium
2. Download chrome or desired browser webDriver. Please make sure the version of Chrome or your browser matches 
the version of the webDriver that you downloaded. 
    Link to Chrome webDriver: https://chromedriver.chromium.org/downloads
3. Replace the path to Chrome webdriver in registerIMA.py on line 186 in the main method.
    Line 186 current: driver = webdriver.Chrome("C:/Users/tynou/googledriver/chromedriver.exe"), 
        Replace the lines in the quote with the path that you have your webDriver downloaded at.
4. Run the script and follow the instructions given!
