const video = document.querySelector("#webcam");
const canvas = document.querySelector("#canvas");
const form = document.querySelector("#loginForm");
const statusMsg = document.querySelector("#statusmessage");
const loginBtn = document.querySelector("#loginBtn");
let faceDetected = false;
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
    if(video.videoWidth===0) return;
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video,0,0,canvas.width,canvas.height);

    canvas.toBlob(async (blob) => {

        latestBlob=blob;
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
                loginBtn.disabled = false;
                statusMsg.style.color = "lightgreen";
                statusMsg.innerHTML = "✅ " + data.message;
                
            } else{
                faceDetected = false;
                loginBtn.disabled = true;

                statusMsg.style.color = "red";

                statusMsg.innerHTML = "❌ " + data.message;

            }

            } catch (err) {

            console.log(err);

        }finally{
             // CRITICAL: Schedule the next frame ONLY after this one finishes (or fails)
            // This prevents network queue flooding
            setTimeout(detectFace, 350);
        }

    }, "image/jpeg");

}


// login
form.addEventListener("submit", async function(e){

    e.preventDefault();

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
        formData.append("userid", document.querySelector("#userid").value);
        formData.append("email", document.querySelector("#email").value);
        formData.append("password", document.querySelector("#password").value);
        
        // Append the blob and give it a fake filename ("face.jpg")
        formData.append("image", latestBlob, "face.jpg");
        
        capturedImageURL = URL.createObjectURL(latestBlob);

    try{

        const response = await fetch("/api/login",{

            method:"POST",

            body:formData
        });

        const data = await response.json();


        if(response.ok){
            statusMsg.style.color="lightgreen";

            statusMsg.innerHTML="✔ "+data.message;
            
           setTimeout(() => {
                window.location.href = "/";
                    }, 1000);
            form.reset();
        statusMsg.innerHTML = "";

        }

        else{
            if (data.message === "Face not matched.") {
        alert("❌ Face not matched.\nPlease look at the camera and try again.");
    }

    else if (data.message === "Invalid User ID.") {
        alert("❌ Invalid User ID.");
    }

    else if (data.message === "Email does not exist.") {
        alert("❌ Email not found.\nPlease register first.");
    }

    else if (data.message === "Wrong password.") {
        alert("❌ Incorrect password.");
    }

    else {
        alert(data.message);
    }

    statusMsg.style.color = "red";
    statusMsg.innerHTML = "✖ " + data.message;
}

        }


    catch(error){
         console.error("Login Error:", error);

    statusMsg.style.color = "red";
    statusMsg.innerHTML = "Network Error";

    }

});