# 🚀 COMPLETE STEP-BY-STEP SETUP GUIDE
## Deepfake Detection Web Application

---

## 📋 WHAT YOU NEED

✅ Your trained model file: `deepfake_detector.h5` (just downloaded from Colab)  
✅ Python 3.8 or higher installed on your computer  
✅ The project files (downloaded from Claude)  
✅ Basic command line knowledge  

---

## 🗂️ PART 1: ORGANIZE YOUR FILES

### Step 1: Create Project Folder

1. Create a new folder on your Desktop called `deepfake-detector`
2. Put it somewhere easy to find (e.g., `C:\Users\YourName\Desktop\deepfake-detector`)

### Step 2: Move Downloaded Files

Move ALL these files into your `deepfake-detector` folder:

```
deepfake-detector/
├── app.py                          ← Flask backend
├── deepfake_detector.h5            ← Your trained model (from Colab)
├── requirements.txt                ← Python dependencies
├── templates/
│   └── index.html                  ← Frontend webpage
├── README.md                       ← Documentation
├── QUICKSTART.md                   ← Quick guide
└── .gitignore                      ← Git ignore file
```

**Important:** Make sure `deepfake_detector.h5` is in the SAME folder as `app.py`

---

## 💻 PART 2: INSTALL PYTHON (If not installed)

### Windows:

1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.10
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Click "Install Now"

### Mac:

1. Open Terminal
2. Install Homebrew (if not installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python@3.11
   ```

### Verify Installation:

Open Terminal (Mac) or Command Prompt (Windows) and type:
```bash
python --version
```
You should see something like: `Python 3.11.x` or `Python 3.10.x`

---

## 🔧 PART 3: SETUP ENVIRONMENT

### Step 1: Open Terminal/Command Prompt in Your Project Folder

**Windows:**
1. Open File Explorer
2. Navigate to your `deepfake-detector` folder
3. Type `cmd` in the address bar and press Enter
4. Command Prompt opens in that folder

**Mac/Linux:**
1. Open Terminal
2. Navigate to folder:
   ```bash
   cd Desktop/deepfake-detector
   ```

### Step 2: Create Virtual Environment (Recommended)

**Why?** Keeps project dependencies separate from your system Python.

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear before your command prompt.

### Step 3: Install Required Packages

Copy and paste this command:

```bash
pip install flask flask-cors tensorflow opencv-python numpy werkzeug
```

**OR** use the requirements file:

```bash
pip install -r requirements.txt
```

This will take 2-5 minutes. You'll see lots of text scrolling - that's normal!

Wait until you see "Successfully installed..." messages.

---

## ▶️ PART 4: RUN THE APPLICATION

### Step 1: Start Flask Server

Make sure you're in the `deepfake-detector` folder with virtual environment activated.

Type this command:

```bash
python app.py
```

### Step 2: Look for Success Messages

You should see:

```
Loading model...
Model loaded successfully!
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server...
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
Press CTRL+C to quit
```

✅ **If you see this - YOU'RE READY!**

❌ **If you see errors, skip to TROUBLESHOOTING section below**

### Step 3: Open in Browser

1. Open your web browser (Chrome, Firefox, Edge, Safari)
2. Type this URL in the address bar:
   ```
   http://localhost:5000
   ```
   OR
   ```
   http://127.0.0.1:5000
   ```

3. Press Enter

You should see your Deepfake Detector webpage! 🎉

---

## 🎯 PART 5: TEST YOUR APPLICATION

### Step 1: Prepare Test Images

Find some images to test:
- Download sample deepfake images from the internet
- Use your own photos
- Use images from the dataset you trained on

### Step 2: Upload and Analyze

1. **Click** the upload area OR **drag and drop** an image
2. Click the **"Analyze Image"** button
3. Wait 1-3 seconds for processing
4. See your results!

### Step 3: Interpret Results

- **Green box = REAL image**
- **Red box = FAKE image**
- **Confidence bar** shows how certain the model is
- **Percentages** show Real vs Fake probability

### Step 4: Test Multiple Images

Click "Analyze Another Image" to test more images.

Try both real and fake images to see how well your model performs!

---

## 📸 PART 6: DOCUMENTATION FOR YOUR PROJECT

### Screenshots to Take:

1. **Terminal showing Flask running**
   - Shows "Model loaded successfully"
   - Shows the server URL

2. **Homepage of your web app**
   - The upload interface

3. **Upload in progress**
   - Image preview before analysis

4. **Results for REAL image**
   - Green result box with confidence

5. **Results for FAKE image**
   - Red result box with confidence

6. **Your project folder structure**
   - File explorer showing all files

### For Your Report/Presentation:

Include these sections:

1. **Introduction**
   - What is deepfake detection?
   - Why is it important?

2. **Methodology**
   - Dataset used (Kaggle deepfake dataset)
   - Model architecture (CNN)
   - Training process

3. **Implementation**
   - Technologies used (Flask, TensorFlow, JavaScript)
   - System architecture diagram
   - Screenshots of web interface

4. **Results**
   - Model accuracy (from training)
   - Sample predictions (screenshots)
   - Confusion matrix

5. **Conclusion**
   - What you learned
   - Limitations
   - Future improvements

---

## 🛑 TROUBLESHOOTING

### Error: "Model not found" or "No such file"

**Solution:**
1. Make sure `deepfake_detector.h5` is in the same folder as `app.py`
2. Check the filename is EXACTLY `deepfake_detector.h5` (not .keras)
3. If your model is .keras format, edit `app.py` line 19:
   ```python
   model = tf.keras.models.load_model('deepfake_detector.keras')
   ```

### Error: "Port 5000 already in use"

**Solution:**
1. Stop any other programs using port 5000
2. OR change port in `app.py` (last line):
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```
3. Then visit `http://localhost:5001`

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
1. Make sure virtual environment is activated (see `(venv)` in terminal)
2. Install requirements again:
   ```bash
   pip install -r requirements.txt
   ```

### Error: "No module named 'tensorflow'"

**Solution:**
```bash
pip install tensorflow
```

### Error: Upload button doesn't work

**Solution:**
1. Check if `templates` folder exists
2. Check if `index.html` is inside `templates` folder
3. Folder structure should be:
   ```
   deepfake-detector/
   ├── app.py
   └── templates/
       └── index.html
   ```

### Error: Images not uploading

**Solution:**
1. Check file size (must be under 16MB)
2. Check file format (only PNG, JPG, JPEG)
3. Try a different image

### Application loads but predictions are wrong

**Solution:**
1. This is normal! Model accuracy is typically 80-90%
2. Try testing with more diverse images
3. Model performs better on images similar to training data

### Everything crashes when uploading

**Solution:**
1. Image might be too large - try resizing it first
2. Check terminal for specific error message
3. Restart Flask server: `Ctrl+C` then `python app.py` again

---

## 🎓 PART 7: NEXT STEPS

### For Your College Project:

1. ✅ **Document everything** - Take screenshots at each step
2. ✅ **Test thoroughly** - Try 10-20 different images
3. ✅ **Note accuracy** - Track how many predictions are correct
4. ✅ **Create presentation** - Use screenshots in slides
5. ✅ **Upload to GitHub** - Version control your project

### Optional Improvements:

1. **Deploy online** - Use Render, Heroku, or Railway
2. **Add video support** - Analyze videos frame-by-frame
3. **Improve UI** - Add more features, animations
4. **Better model** - Try transfer learning with ResNet or EfficientNet
5. **Add database** - Store analysis history
6. **User accounts** - Add login functionality

---

## 💡 QUICK COMMANDS REFERENCE

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Deactivate virtual environment
deactivate

# Check Python version
python --version

# Check installed packages
pip list
```

---

## 📞 NEED HELP?

Common places to find solutions:
1. Check error message in terminal carefully
2. Google the specific error message
3. Check Flask documentation: https://flask.palletsprojects.com/
4. Check TensorFlow documentation: https://www.tensorflow.org/
5. Ask your professor or classmates

---

## ✅ SUCCESS CHECKLIST

Before submitting your project, verify:

- [ ] All files are organized correctly
- [ ] Virtual environment is created
- [ ] All dependencies are installed
- [ ] Model file is in correct location
- [ ] Flask server starts without errors
- [ ] Web page loads at localhost:5000
- [ ] Image upload works
- [ ] Predictions are displayed
- [ ] Tested with multiple images
- [ ] Screenshots taken for documentation
- [ ] Code is commented
- [ ] README is complete
- [ ] Project is on GitHub (optional)

---

## 🎉 YOU'RE DONE!

Congratulations! You now have a fully functional deepfake detection web application.

Good luck with your project presentation! 🚀

---

**Last updated:** January 2026
**For:** College Deepfake Detection Project
