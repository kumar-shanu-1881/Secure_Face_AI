const video = document.querySelector("#webcam");
const canvas = document.querySelector("#canvas");
const form = document.querySelector("#registerForm");
const statusMsg = document.querySelector("#statusMessage");
const registerBtn = document.querySelector("#registerBtn");
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
    if(video.videoWidth===0) return;
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video,0,0,canvas.width,canvas.height);

    canvas.toBlob(async (blob) => {

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
                registerBtn.disabled = false;
                statusMsg.style.color = "lightgreen";
                statusMsg.innerHTML = "✅ " + data.message;
                
            } else{
                faceDetected = false;
                registerBtn.disabled = true;
                
                statusMsg.style.color = "red";

                statusMsg.innerHTML = "❌ " + data.message;

            }

            } catch (err) {

            console.log(err);

        }
        finally {
            // CRITICAL: Schedule the next frame ONLY after this one finishes (or fails)
            // This prevents network queue flooding
            setTimeout(detectFace, 150);
        }

    }, "image/jpeg");

}


// Register
form.addEventListener("submit", async function(e){

    e.preventDefault();

    statusMsg.style.color = "#75b3ff";
    statusMsg.innerHTML = "Processing...";

     if(!faceDetected){

        statusMsg.style.color="red";

        statusMsg.innerHTML="Face validation failed.";

        return;
    }
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video,0,0,canvas.width,canvas.height);


    canvas.toBlob(async (blob) =>{
        const formData = new FormData();
        formData.append("full_name", document.querySelector("#fullName").value);
        formData.append("email", document.querySelector("#email").value);
        formData.append("password", document.querySelector("#password").value);
        
        // Append the blob and give it a fake filename ("face.jpg")
        formData.append("image", blob, "face.jpg");


    try{

        const response = await fetch("/api/register",{

            method:"POST",

            body:formData

        });

        const data = await response.json();

        if(response.ok){

            statusMsg.style.color="lightgreen";

            statusMsg.innerHTML="✔ "+data.message;

            form.reset();

        }

        else{

            statusMsg.style.color="red";

            statusMsg.innerHTML="✖ "+data.message;

        }

    }

    catch(error){

        statusMsg.style.color="red";

        statusMsg.innerHTML="Network Error.";

    }
},"image/jpeg",0.99);

});