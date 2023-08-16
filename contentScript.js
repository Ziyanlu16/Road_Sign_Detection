let session;

// Load the ONNX model
async function loadModel() {
    session = new onnx.InferenceSession();
    await session.loadModel('yolov5/yolov5s.onnx');
}

loadModel();

chrome.runtime.onMessage.addListener(async function(request, sender, sendResponse) {
    if(request.message === "start_detection") {
        // Capture the image from Google Maps Street View.
        let imageTensor = captureImage();
        
        // Run the ONNX.js model for detection
        let outputMap = await session.run([imageTensor]);
        
        // Process the output
        let detections = processOutput(outputMap);
        
        // Overlay the results on the Google Maps image
        overlayResults(detections);
    }
});

function captureImage(){

}

function processOutput(){

}

function overlayResults(){

}