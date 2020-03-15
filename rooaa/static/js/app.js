
// Url to the server
const url = "/api/v1/image";

// Creating XMLHR to handle server requests and responses 
const xhr = new XMLHttpRequest();


// web socket
const socket = io.connect('https://' + document.domain + ':' + location.port + '/predict');
function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }
  
let image_name = uuidv4() + ".jpeg";

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
const messageArea = document.querySelector('#messageArea');
messageArea.style.paddingTop = '25%';

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


    rooaaFile = JSON.stringify({
        "data": data,
        "filename": image_name
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
                socket.emit("prediction", image_name);

            } catch (error) {
                console.log(error.toString());
                setTimeOut(send_photo, 1000);
            }
        } else {
            messageArea.innerHTML = "Server is offline, trying again..."
            setTimeOut(send_photo, 1000);
        }
    } else {
        console.log("Waiting..");
        messageArea.innerHTML = "Waiting for the server...";
    }
}

socket.on('result', function (predictions) {
    const msg = new SpeechSynthesisUtterance(predictions);
    messageArea.innerHTML = msg.text;
    msg.onend = send_photo;
    synth.speak(msg);
});

camera_start();