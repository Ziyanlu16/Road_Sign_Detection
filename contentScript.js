// 导入所需的onnx.js库（可能需要在manifest.json中设置相应的content_security_policy）
import * as onnx from 'onnxjs';

let model = new onnx.InferenceSession();
let isModelLoaded = false;

// 初始化：加载模型
async function loadModel() {
  await model.loadModel('yolov5/yolov5s.onnx');
  isModelLoaded = true;
}

// 如果模型尚未加载，立即加载
if (!isModelLoaded) {
  loadModel();
}

// 使用模型进行推断
async function infer(imageData) {
  const inputTensor = new onnx.Tensor(new Float32Array(imageData.data.buffer), 'float32', [1, 3, imageData.height, imageData.width]);
  const outputMap = await model.run([inputTensor]);

  // 根据YOLOv5的输出格式处理结果，提取边界框和类别
  const outputData = outputMap.values().next().value.data;
  // 解析输出数据（根据YOLO的输出格式，你可能需要一些额外的处理）
  const boxes = []; // 示例数组，你需要填充这些信息

  return boxes;
}

chrome.runtime.onMessage.addListener(async function(request, sender, sendResponse) {
  if (request.message === "start_detection") {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    const images = document.querySelectorAll('img');  // 获取页面上的所有图像元素

    for (let img of images) {
      // 确保图像来自Google Maps街景
      if (img.src.includes('googleapis.com')) {
        canvas.width = img.width;
        canvas.height = img.height;
        context.drawImage(img, 0, 0, img.width, img.height);
        const imageData = context.getImageData(0, 0, img.width, img.height);

        const boxes = await infer(imageData);

        // 在图像上绘制边界框
        boxes.forEach(box => {
          context.strokeStyle = 'red'; // 选择一个颜色
          context.lineWidth = 2; // 设置线宽
          context.strokeRect(box.x, box.y, box.width, box.height);
          // 如果有其他信息（例如类别、置信度），也可以绘制在图像上
        });

        img.src = canvas.toDataURL('image/png');
      }
    }
  }
});
