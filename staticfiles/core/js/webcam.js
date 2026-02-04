// Webcam handling functions
let stream = null;
let videoElement = null;

function startWebcam() {
    videoElement = document.getElementById('webcam');
    const startButton = document.getElementById('startWebcam');
    const captureButton = document.getElementById('captureImage');
    const previewImage = document.getElementById('previewImage');
    const imageInput = document.getElementById('profile_image');
    const retakeButton = document.getElementById('retakeImage');
    
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(mediaStream) {
            stream = mediaStream;
            videoElement.srcObject = stream;
            videoElement.style.display = 'block';
            previewImage.style.display = 'none';
            startButton.style.display = 'none';
            captureButton.style.display = 'block';
            retakeButton.style.display = 'none';
        })
        .catch(function(err) {
            console.error("Error accessing webcam:", err);
            alert("Error accessing webcam. Please ensure you have granted camera permissions.");
        });
}

function stopWebcam() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    if (videoElement) {
        videoElement.srcObject = null;
    }
}

function captureImage() {
    const canvas = document.createElement('canvas');
    const video = document.getElementById('webcam');
    const previewImage = document.getElementById('previewImage');
    const captureButton = document.getElementById('captureImage');
    const retakeButton = document.getElementById('retakeImage');
    const imageInput = document.getElementById('profile_image_data');

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw current video frame to canvas
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to base64 image data
    const imageData = canvas.toDataURL('image/jpeg');
    
    // Show preview and update hidden input
    previewImage.src = imageData;
    previewImage.style.display = 'block';
    video.style.display = 'none';
    imageInput.value = imageData;
    
    // Show/hide appropriate buttons
    captureButton.style.display = 'none';
    retakeButton.style.display = 'block';
    
    // Stop the webcam stream
    stopWebcam();
}

function retakeImage() {
    const video = document.getElementById('webcam');
    const previewImage = document.getElementById('previewImage');
    const captureButton = document.getElementById('captureImage');
    const retakeButton = document.getElementById('retakeImage');
    const imageInput = document.getElementById('profile_image_data');
    
    // Clear previous capture
    imageInput.value = '';
    previewImage.src = '';
    previewImage.style.display = 'none';
    
    // Restart webcam
    startWebcam();
    
    // Show/hide appropriate buttons
    captureButton.style.display = 'block';
    retakeButton.style.display = 'none';
}