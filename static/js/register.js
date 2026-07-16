const video = document.querySelector("#webcam");
const canvas = document.querySelector("#canvas");
const form = document.querySelector("#registerForm");
const statusMsg = document.querySelector("#statusMessage");
const registerBtn = document.querySelector("#registerBtn");
const bxrit=document.querySelector(".box-left");
let faceDetected = false;
let detectionStopped = false;
let capturedImageURL = null;
let latestBlob = null;

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
                registerBtn.disabled = false;
                statusMsg.style.color = "lightgreen";
                statusMsg.innerHTML = "✅ " + data.message;
                
            } else{
                faceDetected = false;

                registerBtn.disabled = true;
                registerBtn.style.color="00072D"
                
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


// Register
form.addEventListener("submit", async function(e){
    
    e.preventDefault();
    detectionStopped = true;

    statusMsg.style.color = "#75b3ff";
    statusMsg.innerHTML = "Processing...";

     if(!faceDetected){

        statusMsg.style.color="red";

        statusMsg.innerHTML="Face validation failed.";

        return;
    }

        if(!latestBlob){
        statusMsg.innerHTML = "No image captured.";
        return;
        }
        
        const formData = new FormData();
        formData.append("full_name", document.querySelector("#fullName").value);
        formData.append("email", document.querySelector("#email").value);
        formData.append("password", document.querySelector("#password").value);
        
        // Append the blob and give it a fake filename ("face.jpg")
        formData.append("image", latestBlob, "face.jpg");
        
        capturedImageURL = URL.createObjectURL(latestBlob);


    try{

        const response = await fetch("/api/register",{

            method:"POST",

            body:formData

        });

        const data = await response.json();

        if(response.ok){
             // Stop detection loop

            // Stop webcam
            const stream = video.srcObject;
            if(stream){
                stream.getTracks().forEach(track => track.stop());
            }

            // Hide webcam
            video.style.display = "none";
            bxrit.innerHTML=`<div class="profile-section"style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; height: 100%;">

            <h2 class="success-heading" style="color: lightgreen; margin-bottom: 15px; font-size: 1.8rem;">
                        🎉 Face Registered
                    </h2>
                <img src="${capturedImageURL}" class="profile-image">
            </div>`;
            // Hide registration form
            form.innerHTML = `
        <div class="success-card">

            

            <div class="user-section">

                <h2>🎉 Registration Successful</h2>

                <div class="user-info">
                    <p><span>User ID</span>${data.user_id}</p>
                    <p><span>Name</span>${document.querySelector("#fullName").value}</p>
                    <p><span>Email</span>${document.querySelector("#email").value}</p>
                </div>

                <button id="gotoLogin">
                    Go to Login
                </button>

            </div>

        </div>
        `;

        document.querySelector("#gotoLogin").addEventListener("click", () => {
            window.location.href = "/login";
        });
        statusMsg.innerHTML = "";
        }

        else{
            
            detectFace();
            
            statusMsg.style.color="red";
            
            statusMsg.innerHTML="✖ "+data.message;
            
            if(data.message === "Email already exists."){
                
                setTimeout(() => {
                    detectionStopped = false;
                    statusMsg.innerHTML = "";
                }, 4000);
    }

        }

    }

    catch(error){
         detectionStopped = false;
        detectFace();
        statusMsg.style.color="red";

        statusMsg.innerHTML="Network Error.";

    }

});