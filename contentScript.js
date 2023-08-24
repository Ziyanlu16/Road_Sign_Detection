// let session;

// // Load the ONNX model
// async function loadModel() {
//     session = new onnx.InferenceSession();
//     await session.loadModel('yolov5/yolov5s.onnx');
// }

// loadModel();

chrome.runtime.onMessage.addListener(async function(request, sender, sendResponse) {
    if(request.message === "start_detection") {
        document.body.style.backgroundColor = "black";
    }
});