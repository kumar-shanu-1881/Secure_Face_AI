const video = document.querySelector("#webcam");
const canvas = document.querySelector("#canvas");
const statusMsg = document.querySelector("#statusMessage");
let detectionStopped = false;
let latestBlob = null;
let faceDetected = false;

// Start Webcam
navigator.mediaDevices.getUserMedia({
    video: true
})
.then(stream => {
    video.srcObject = stream;
    // setInterval(detectFace, 150); // Call detectFace every 150ms
    video.onloadedmetadata = () => {
        detectFace(); // Start the loop manually once
    };
})
.catch(err => {
    alert("Access to Camera Denied.");
    console.log(err);
});

//sending frames to the server for face detection
async function detectFace(){
    if(detectionStopped)
        return;

    if(video.videoWidth===0) return;
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video,0,0,canvas.width,canvas.height);

    canvas.toBlob(async (blob) => {

        latestBlob = blob;
        const formData = new FormData();
        formData.append("frame", blob);
        
        try {
            
            const response = await fetch("/detect", {
                method: "POST",
                body: formData,
            });
            
            const data = await response.json();

            faceDetected = data.face

            if (data.success) {
                faceDetected = data.face;
                statusMsg.style.color = "lightgreen";
                statusMsg.innerHTML = "✅ " + data.message;
                
            } else{
                faceDetected = false;
                
                statusMsg.style.color = "red";

                statusMsg.innerHTML = "❌ " + data.message;

            }

            } catch (err) {

            console.log(err);

        }
        finally {
            // CRITICAL: Schedule the next frame ONLY after this one finishes (or fails)
            // This prevents network queue flooding
            setTimeout(detectFace, 350);
        }

    }, "image/jpeg");

}
