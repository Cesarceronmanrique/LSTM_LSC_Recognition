const video = document.getElementById('video');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
let mediaRecorder;
let recordedBlobs;

startButton.addEventListener('click', async () => {
    // Configuración de las restricciones de la cámara
    const constraints = {
        video: {
            width: { ideal: 640 }, // Ancho deseado
            height: { ideal: 360 }, // Alto deseado
            frameRate: { ideal: 10 } // Tasa de fotogramas deseada
        },
        audio: true
    };

    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = stream;
    recordedBlobs = [];
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
            console.log(`Data available of size: ${event.data.size}`);
            recordedBlobs.push(event.data);
        }
    };

    mediaRecorder.onstop = () => {
        console.log('MediaRecorder stopped');
        uploadVideov1();
    };

    mediaRecorder.start();
    console.log('MediaRecorder started');
    startButton.disabled = true;
    stopButton.disabled = false;
});

stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    startButton.disabled = false;
    stopButton.disabled = true;
    video.srcObject.getTracks().forEach(track => track.stop());
});

async function uploadVideo() {
    console.log(`Recorded blobs: ${recordedBlobs.length}`);
    if (recordedBlobs.length === 0) {
        console.error('No recorded blobs. Not uploading.');
        return;
    }

    const blob = new Blob(recordedBlobs, { type: 'video/webm' });
    console.log(`Blob size: ${blob.size}`);

    if (blob.size === 0) {
        console.error('Blob is empty. Not uploading.');
        return;
    }

    const fileName = `video_${new Date().toISOString().replace(/[:.-]/g, '')}.webm`;

    const presignedUrlResponse = await fetch('https://vk8qor0b7c.execute-api.us-east-1.amazonaws.com/video', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fileName, fileType: 'video/webm' })
    });

    if (!presignedUrlResponse.ok) {
        console.error('Error obtaining presigned URL:', presignedUrlResponse.statusText);
        return;
    }

    const { presignedUrl } = await presignedUrlResponse.json();
    console.log(`Presigned URL: ${presignedUrl}`);

    try {
        const response = await fetch(presignedUrl, {
            method: 'PUT',
            headers: {
                'Content-Type': 'video/webm'
            },
            body: blob,
        });

        if (response.ok) {
            console.log('Video uploaded successfully');
        } else {
            console.error('Error uploading video:', response.statusText);
            const errorText = await response.text();
            console.error('Response error text:', errorText);
        }
    } catch (error) {
        console.error('Error uploading video:', error);
    }
}

async function uploadVideov1() {
    console.log(`Recorded blobs: ${recordedBlobs.length}`);
    if (recordedBlobs.length === 0) {
        console.error('No recorded blobs. Not uploading.');
        return;
    }

    const blob = new Blob(recordedBlobs, { type: 'video/webm' });
    console.log(`Blob size: ${blob.size}`);

    if (blob.size === 0) {
        console.error('Blob is empty. Not uploading.');
        return;
    }

    const fileName = `video_${new Date().toISOString().replace(/[:.-]/g, '')}.webm`;

    const formData = new FormData();
    formData.append('file', blob, fileName);

    try {
        const response = await fetch('https://vk8qor0b7c.execute-api.us-east-1.amazonaws.com/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            console.error('Error uploading video:', response.statusText);
            return;
        }

        const result = await response.json();
        console.log('Success:', result);

        if (result.redirect_url) {
            // Redirigir a la URL especificada en la respuesta JSON
            window.location.href = result.redirect_url;
        } else {
            console.error("No se encontró la URL de redirección en la respuesta.");
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
