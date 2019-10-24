// To prevent dublication and losing photos
let current_photo_number = 0;
//responding properties
let audio_factor = 1000;
// Url to the server
let url = "/api/v1/image";

// Creating SSU for voice
const msg = new SpeechSynthesisUtterance();

// Set constraints for the video stream
let constraints = {
    video: {
        facingMode: "environment"
    },
    audio: false
};

// Creating video element for camera streaming
const cameraView = document.createElement('video');
// Creating canvas element to store a specific frame -- image -- from the camera
const canvas = document.createElement('canvas');


// Access the device camera and stream to cameraView
function camera_start() {
    cameraView.playsinline = true;
    cameraView.autoplay = true;

    /* Setting up the constraint */
    var facingMode = "environment"; // Can be 'user' or 'environment' to access back or front camera (NEAT!)
    var constraints = {
        audio: false,
        video: {
            facingMode: facingMode
        }
    };

    /* Stream it to video element */
    navigator.mediaDevices.getUserMedia(constraints).then(function success(stream) {
        cameraView.srcObject = stream;
    }).then(function () {
        send_photo();
    });
}

function send_photo() {
    canvas.height = cameraView.videoHeight;
    canvas.width = cameraView.videoWidth;
    // Get current frame of the video into the canvas 
    canvas.getContext("2d").drawImage(cameraView, 0, 0);

    // Getting the source of the image 
    let data = canvas.toDataURL("image/jpeg");

    // Check if the camera is still ON 
    if (data === "data:,") {
        console.log("Turn on Your Camera");
        setTimeout(send_photo, 1000);
        return;
    }


    // Sending a request to the server
    $.post(url, JSON.stringify({
        "data": data,
        "filename": (current_photo_number++).toString() + ".jpeg"
    }), function (err, req, resp) {
        let time_before_next_response;
        // Check if AJAX call has completed.
        msg.text = resp.responseText;
        time_before_next_response = msg.text.trim().split(' ').length;
        window.speechSynthesis.speak(msg);

        setTimeout(send_photo, audio_factor * time_before_next_response);
    })
}

camera_start();