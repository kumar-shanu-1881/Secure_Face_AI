const video = document.querySelector("#webcam");
const canvas = document.querySelector("#canvas");
const form = document.querySelector("#registerForm");
const statusMsg = document.querySelector("#statusMessage");

// Start Webcam
navigator.mediaDevices.getUserMedia({
    video: true
})
.then(stream => {
    video.srcObject = stream;
})
.catch(err => {
    alert("Access to Camera Denied.");
    console.log(err);
});

// Register
form.addEventListener("submit", async function(e){

    e.preventDefault();

    statusMsg.style.color = "#75b3ff";
    statusMsg.innerHTML = "Processing...";

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video,0,0,canvas.width,canvas.height);

    const imageBase64 = canvas.toDataURL("image/jpeg");

    const payload = {

        full_name:document.querySelector("#fullName").value,
        email:document.querySelector("#email").value,
        password:document.querySelector("#password").value,
        image:imageBase64
    };

    try{

        const response = await fetch("/api/register",{

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