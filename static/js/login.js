const video = document.querySelector("#webcam");
const canvas = document.querySelector("#canvas");
const form = document.querySelector("#loginForm");
const statusMsg = document.querySelector("#statusMessage");
const loginBtn = document.querySelector("#loginBtn");
let faceDetected = false;


// Start Webcam
navigator.mediaDevices.getUserMedia({
    video: true
})
.then(stream => {
    video.srcObject = stream;
    setInterval(detectFace, 150); // Call detectFace every 150ms
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
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video,0,0,canvas.width,canvas.height);

    const imageBase64 = canvas.toDataURL("image/jpeg");

    const payload = {

        email:document.querySelector("#email").value,
        password:document.querySelector("#password").value,
        image:imageBase64
    };

    try{

        const response = await fetch("/api/login",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify(payload)

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

});