import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import logging

# Import utility modules
from utils.image_processor import process_image
from utils.story_generator import generate_story
from utils.audio_generator import generate_audio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-storylens')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['AUDIO_FOLDER'] = os.path.join('static', 'audio')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create necessary directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['photo']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = str(uuid.uuid4()) + os.path.splitext(secure_filename(file.filename))[1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Process the image
            processed_image = process_image(file_path)
            
            # Generate story from the image
            story_type = request.form.get('story_type', 'story')  # 'story' or 'poem'
            story = generate_story(processed_image, story_type)
            
            # Generate audio narration
            voice_type = request.form.get('voice_type', 'default')
            audio_filename = filename.split('.')[0] + '.wav'
            audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
            generate_audio(story, audio_path, voice_type)
            
            # Prepare data for the story page
            story_data = {
                'image_path': os.path.join('uploads', filename),
                'story': story,
                'audio_path': os.path.join('audio', audio_filename)
            }
            
            return render_template('story.html', story=story_data)
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            flash(f"Error processing your image: {str(e)}")
            return redirect(url_for('index'))
    
    flash('File type not allowed. Please upload a JPG, JPEG or PNG image.')
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 16MB.')
    return redirect(url_for('index'))

@app.errorhandler(500)
def server_error(e):
    flash('An error occurred on our end. Please try again later.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)