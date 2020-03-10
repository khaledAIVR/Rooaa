// To prevent dublication and losing photos
let current_photo_number = 0;

// Url to the server
let url = "/api/v1/image";


// Creating XMLHR to handle server requests and responses 
const xhr = new XMLHttpRequest();


// Creating SS to convert server responses to voice messages
const synth = window.speechSynthesis;

// Set constraints for the video stream
let constraints = {
    video: {
        facingMode: 'environment'
    },
    audio: false
};

// Creating video element for camera streaming
const cameraView = document.createElement('video');
// Creating canvas element to store a specific frame -- image -- from the camera
const canvas = document.createElement('canvas');
// Creating Error Area div, anyerror will show up to the user in this div
const messageArea = document.createElement('div');
messageArea.style.paddingTop = '25%';
document.body.appendChild(messageArea);

cameraView.autoplay = true;
cameraView.playsinline = true;

// Access the device camera and stream to cameraView
function camera_start() {
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function (stream) {
            track = stream.getTracks()[0];
            cameraView.srcObject = stream;
        }).then(function () {
            send_photo();
        })
        .catch(function (error) {
            cameraErr = 'In order to this app to work:</br>' +
                '- You need a device with a camera</br>' +
                '- Allow us to use your camera</br>' +
                'Please note: All photos sent to the server are automatically deleted';
            console.error(error, cameraErr);
            messageArea.innerHTML = cameraErr;
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
        console.log("Turning on Your Camera");
        messageArea.innerHTML = "Turning on Your Camera";
        setTimeout(send_photo, 1000);
        return;
    }

    let rooaaFile = JSON.stringify({
        "data": data,
        "filename": (current_photo_number++).toString() + ".jpeg"
    });


    // Sending a request to the server
    xhr.open("POST", url);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(rooaaFile);
    xhr.onreadystatechange = handle_server_response;
}

function handle_server_response() {
    // Check if AJAX call has completed.
    if (xhr.readyState === 4) {
        // Completed not necessary meaning everything went okay :D 
        if (xhr.status == 200) {
            try {

                status_url = JSON.parse(xhr.responseText)['location']
                update_progress(status_url)

            } catch (error) {
                console.log(error.toString());
                send_photo();
            }
        } else {
            messageArea.innerHTML = "Server is offline, trying again..."
            send_photo();
        }
    } else {
        console.log("Waiting..");
        messageArea.innerHTML = "Waiting for the server...";
    }
}

function update_progress(status_url) {
    $.getJSON(status_url, function (data) {
        if (data['state'] != 'PENDING' && data['state'] != 'PREDICTING') {
            if ('result' in data) {
                const msg = new SpeechSynthesisUtterance(data["result"]);
                messageArea.innerHTML = msg.text;
                msg.onend = send_photo;
                synth.speak(msg);
            } else {
                console.log("Something unexpected happened..")
                setTimeOut(send_photo, 1000)
            }
        } else {
            messageArea.innerHTML = `${data["status"]}`
            // rerun in 2 seconds
            setTimeout(function () {
                update_progress(status_url);
            }, 1000);
        }
    });
}

camera_start();