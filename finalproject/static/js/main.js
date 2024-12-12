// 전역 변수 선언
let currentImage = null;
let drawing = false;
let startX, startY;
let bboxes = {};
let canvas, ctx;
let uploadedImages = [];
let lossChart = null;

// EventSource 연결 설정
const eventSource = new EventSource('/stream');

eventSource.onmessage = function (event) {
    const data = JSON.parse(event.data);
    if (!data.heartbeat) {
        updateTrainingUI(data);
    }
};

eventSource.onerror = function (error) {
    console.error("EventSource failed:", error);
    eventSource.close();
};

// Training UI 업데이트 함수
function updateTrainingUI(data) {
    if (data.currentEpoch !== undefined) {
        const progress = (data.currentEpoch / data.totalEpochs) * 100;
        document.getElementById('progressFill').style.width = `${progress}%`;
        document.getElementById('currentEpoch').textContent = `${data.currentEpoch}/${data.totalEpochs}`;
        document.getElementById('gpuMemory').textContent = data.gpu_memory;

        document.getElementById('boxLoss').textContent = data.box_loss.toFixed(4);
        document.getElementById('clsLoss').textContent = data.cls_loss.toFixed(4);
        document.getElementById('dflLoss').textContent = data.dfl_loss.toFixed(4);

        updateLossChart(data);
    }

    if (data.finalMetrics) {
        const metricsBody = document.getElementById('metricsBody');
        metricsBody.innerHTML = '';
        Object.entries(data.finalMetrics).forEach(([key, value]) => {
            metricsBody.innerHTML += `
                <tr>
                    <td>${key}</td>
                    <td>${value.toFixed(4)}</td>
                </tr>
            `;
        });
    }

    if (data.modelSummary) {
        document.getElementById('modelSummary').textContent = `모델 요약:
            레이어 수: ${data.modelSummary.layers}
            파라미터 수: ${data.modelSummary.parameters.toLocaleString()}
            그래디언트: ${data.modelSummary.gradients}
            GFLOPs: ${data.modelSummary.gflops.toFixed(2)}`;

        document.getElementById('finalModelSummary').textContent =
            JSON.stringify(data.modelSummary, null, 2);
    }

    if (data.training_complete) {
        if (data.training_path) {
            setTimeout(() => {
                document.getElementById('loadingOverlay').style.display = 'none';
                document.getElementById('startTraining').disabled = false;
                showTrainingResults(data);
            }, 1000);
        }
    }
}

// 차트 관련 함수들
function initLossChart() {
    const ctx = document.getElementById('lossChart').getContext('2d');
    lossChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Box Loss',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }, {
                label: 'Class Loss',
                data: [],
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }, {
                label: 'DFL Loss',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function updateLossChart(data) {
    if (!lossChart) {
        initLossChart();
    }

    if (data.currentEpoch <= 50) {
        lossChart.data.labels.push(data.currentEpoch);
        lossChart.data.datasets[0].data.push(data.box_loss);
        lossChart.data.datasets[1].data.push(data.cls_loss);
        lossChart.data.datasets[2].data.push(data.dfl_loss);
        lossChart.update();
    }
}

// 이미지 업로드 처리
document.getElementById('uploadForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const imageFiles = e.target.elements.images.files;

    for (let file of imageFiles) {
        try {
            const individualFormData = new FormData();
            individualFormData.append('image', file);

            const response = await fetch('/upload', {
                method: 'POST',
                body: individualFormData
            });

            const data = await response.json();
            if (data.error) {
                alert(`Error processing ${file.name}: ${data.error}`);
                continue;
            }

            uploadedImages.push({
                name: file.name,
                originalPath: data.original_image,
                resultPath: data.result_image,
                jsonPath: data.json_file
            });

            bboxes[file.name] = [];
            updateImagesList();
        } catch (error) {
            console.error(`Error processing ${file.name}:`, error);
            alert(`Error processing ${file.name}`);
        }
    }
};

// 객체 감지 처리
document.getElementById('detectObjects').onclick = async function() {
    if (!currentImage) {
        alert('이미지를 먼저 선택해주세요');
        return;
    }

    const selectedModel = document.getElementById('modelSelect').value;
    
    try {
        const response = await fetch('/detect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'image_name': currentImage,
                'model_type': selectedModel
            })
        });

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        // 감지된 객체로 이미지 업데이트
        const resultImg = document.querySelector('#detectedImage img');
        resultImg.src = `${data.result_image}?t=${new Date().getTime()}`; // 캐시 방지
        
        // 바운딩 박스 업데이트
        bboxes[currentImage] = data.detections.map(det => ({
            x: det.bbox[0],
            y: det.bbox[1],
            width: det.bbox[2],
            height: det.bbox[3],
            class: det.class
        }));
        
        updateBBoxList();
        drawAllBBoxes();
        
    } catch (error) {
        console.error('Detection error:', error);
        alert(`감지 실패: ${error.message}`);
    }
};

// 모델 목록 업데이트
async function updateModelList() {
    try {
        const response = await fetch('/get_models');
        const models = await response.json();
        
        const modelSelect = document.getElementById('modelSelect');
        modelSelect.innerHTML = '<option value="default">기본 모델 (YOLOv5)</option>';
        
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = `학습된 모델: ${model}`;
            modelSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error updating model list:', error);
    }
}

// 학습 관련 함수들
function showTrainingResults(data) {
    const modal = document.getElementById('trainingResultsModal');
    const resultsPlot = document.getElementById('resultsPlot');

    if (data.training_path) {
        resultsPlot.src = `/training_results/results.png`;
    }

    modal.style.display = 'block';
}

function closeTrainingResults() {
    document.getElementById('trainingResultsModal').style.display = 'none';
}

// 학습 시작 처리
document.getElementById('startTraining').onclick = async function () {
    if (!currentImage) {
        alert('이미지를 업로드하고 라벨링을 먼저 해주세요');
        return;
    }

    const button = this;
    const loadingOverlay = document.getElementById('loadingOverlay');

    try {
        button.disabled = true;
        loadingOverlay.style.display = 'flex';

        if (lossChart) {
            lossChart.destroy();
            lossChart = null;
        }

        // 메트릭스 초기화
        document.getElementById('metricsBody').innerHTML = `
            <tr>
                <td>Box Loss</td>
                <td id="boxLoss">0.0000</td>
            </tr>
            <tr>
                <td>Class Loss</td>
                <td id="clsLoss">0.0000</td>
            </tr>
            <tr>
                <td>DFL Loss</td>
                <td id="dflLoss">0.0000</td>
            </tr>
        `;

        const selectedAugmentations = Array.from(
            document.querySelectorAll('input[name="augmentation"]:checked')
        ).map(cb => cb.value);

        const response = await fetch('/train', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'image_name': currentImage,
                'augmentations': selectedAugmentations
            })
        });

        const result = await response.json();

        if (result.error) {
            throw new Error(result.error);
        }
    } catch (error) {
        console.error('Training error:', error);
        alert(`Training failed: ${error.message}`);
        loadingOverlay.style.display = 'none';
        button.disabled = false;
    }
};

// 이미지 및 바운딩 박스 관련 함수들
function updateImagesList() {
    const listDiv = document.getElementById('imagesList');
    listDiv.innerHTML = '<h2>업로드된 이미지:</h2>';

    uploadedImages.forEach((img, index) => {
        const imgContainer = document.createElement('div');
        imgContainer.className = 'image-container';
        imgContainer.innerHTML = `
            <div>
                <span>${img.name}</span>
                <button onclick="showImage(${index})">보기/편집</button>
                <span class="delete-btn" onclick="deleteImage(${index})">×</span>
            </div>
        `;
        listDiv.appendChild(imgContainer);
    });
}

function showImage(index) {
    const img = uploadedImages[index];
    currentImage = img.name;

    document.getElementById('results').innerHTML = `
        <div id="originalImage" class="image-preview">
            <img src="${img.originalPath}">
            <h3>원본 이미지</h3>
        </div>
        <div id="detectedImage" class="image-preview">
            <div class="canvas-container">
                <img src="${img.resultPath}">
                <h3>감지된 객체</h3>
            </div>
        </div>
    `;

    const resultImg = document.querySelector('#detectedImage img');
    resultImg.onload = () => {
        if (canvas) {
            canvas.remove();
        }
        initCanvas(resultImg);
        if (bboxes[currentImage]) {
            drawAllBBoxes();
        }
    };
}

// 캔버스 관련 함수들
function initCanvas(imgElement) {
    const container = document.querySelector('.canvas-container');
    canvas = document.createElement('canvas');
    canvas.id = 'labelCanvas';
    canvas.width = imgElement.width;
    canvas.height = imgElement.height;
    container.appendChild(canvas);
    ctx = canvas.getContext('2d');

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', endDrawing);
}

function startDrawing(e) {
    drawing = true;
    const rect = canvas.getBoundingClientRect();
    startX = e.clientX - rect.left;
    startY = e.clientY - rect.top;
}

function draw(e) {
    if (!drawing) return;

    const rect = canvas.getBoundingClientRect();
    const currentX = e.clientX - rect.left;
    const currentY = e.clientY - rect.top;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawAllBBoxes();

    ctx.strokeStyle = '#ff0000';
    ctx.lineWidth = 2;
    ctx.strokeRect(
        startX,
        startY,
        currentX - startX,
        currentY - startY
    );
}

function endDrawing(e) {
    if (!drawing) return;
    drawing = false;

    const rect = canvas.getBoundingClientRect();
    const endX = e.clientX - rect.left;
    const endY = e.clientY - rect.top;

    if (Math.abs(endX - startX) > 5 && Math.abs(endY - startY) > 5) {
        const classLabel = document.getElementById('classSelect').value;
        if (!classLabel) {
            alert('클래스 이름을 먼저 입력해주세요');
            return;
        }

        const bbox = {
            x: Math.min(startX, endX),
            y: Math.min(startY, endY),
            width: Math.abs(endX - startX),
            height: Math.abs(endY - startY),
            class: classLabel
        };

        if (!bboxes[currentImage]) {
            bboxes[currentImage] = [];
        }
        bboxes[currentImage].push(bbox);
        updateBBoxList();
        drawAllBBoxes();
    }
}

function drawAllBBoxes() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (currentImage && bboxes[currentImage]) {
        bboxes[currentImage].forEach(bbox => {
            ctx.strokeStyle = '#ff0000';
            ctx.lineWidth = 2;
            ctx.strokeRect(bbox.x, bbox.y, bbox.width, bbox.height);

            ctx.fillStyle = '#ff0000';
            ctx.font = '12px Arial';
            ctx.fillText(bbox.class, bbox.x, bbox.y - 5);
        });
    }
}

function updateBBoxList() {
    const list = document.getElementById('bboxList');
    list.innerHTML = '<h3>바운딩 박스:</h3>';
    if (currentImage && bboxes[currentImage]) {
        bboxes[currentImage].forEach((bbox, index) => {
            const item = document.createElement('div');
            item.className = 'bbox-item';
            item.innerHTML = `
                Box ${index + 1}: ${bbox.class}
                (x: ${Math.round(bbox.x)}, y: ${Math.round(bbox.y)},
                w: ${Math.round(bbox.width)}, h: ${Math.round(bbox.height)})
                <button onclick="deleteBBox(${index})">삭제</button>
            `;
            list.appendChild(item);
        });
    }
}

// 라벨 저장 및 삭제 관련 함수들
document.getElementById('undoLabel').onclick = function () {
    if (currentImage && bboxes[currentImage] && bboxes[currentImage].length > 0) {
        bboxes[currentImage].pop();
        updateBBoxList();
        drawAllBBoxes();
    }
};

document.getElementById('saveLabels').onclick = async function () {
    if (!currentImage) {
        alert('이미지를 먼저 선택해주세요');
        return;
    }

    if (!bboxes[currentImage] || bboxes[currentImage].length === 0) {
        alert('바운딩 박스를 하나 이상 그려주세요');
        return;
    }

    const normalizedBBoxes = bboxes[currentImage].map(bbox => ({
        x_center: (bbox.x + bbox.width / 2) / canvas.width,
        y_center: (bbox.y + bbox.height / 2) / canvas.height,
        width: bbox.width / canvas.width,
        height: bbox.height / canvas.height,
        class: bbox.class
    }));

    try {
        const response = await fetch('/save_labels', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                bboxes: normalizedBBoxes,
                image_name: currentImage
            })
        });
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error('Error saving labels:', error);
        alert('라벨 저장 중 오류가 발생했습니다');
    }
};

function deleteImage(index) {
    if (confirm('이 이미지를 삭제하시겠습니까?')) {
        const imageToDelete = uploadedImages[index];
        fetch('/delete_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                filename: imageToDelete.name
            })
        }).then(() => {
            uploadedImages.splice(index, 1);
            delete bboxes[imageToDelete.name];
            updateImagesList();
            if (currentImage === imageToDelete.name) {
                document.getElementById('results').innerHTML = '';
                currentImage = null;
            }
        }).catch(error => {
            console.error('Error deleting image:', error);
            alert('이미지 삭제 중 오류가 발생했습니다');
        });
    }
}

function deleteBBox(index) {
    if (currentImage && bboxes[currentImage]) {
        bboxes[currentImage].splice(index, 1);
        updateBBoxList();
        drawAllBBoxes();
    }
}

// 결과창 닫기는 버튼으로만 가능하도록 설정
window.onclick = function (event) {
    const trainingResults = document.getElementById('trainingResultsModal');
    if (event.target === trainingResults) {
        // 외부 클릭으로 닫지 않도록 주석 처리
        // trainingResults.style.display = 'none';
    }
}

// 페이지 로드 시 모델 목록 업데이트
document.addEventListener('DOMContentLoaded', updateModelList);

// 학습 완료 후 모델 목록 업데이트
const originalShowTrainingResults = showTrainingResults;
showTrainingResults = function(data) {
    originalShowTrainingResults(data);
    updateModelList();
};