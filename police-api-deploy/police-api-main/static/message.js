// Function to add a new message
function addMessage(imgName, type, time) {
    let newMessage = `
        <div class="media w-70 mb-3">
        <img src="https://img2.daumcdn.net/thumb/R658x0.q70/?fname=http://t1.daumcdn.net/news/201305/02/fnnewsi/20130502143118517.jpg" alt="user" width="50" class="rounded-circle">
        <div class="media-body ml-3">
            <div class="fluid rounded py-2 px-3 mb-2" style="background-color: rgba(36, 120, 255, 0.5);">
                <p class="text-small mb-0 text font-weight-bold" id="typeText" style="color: #000000; font-size: 17px; "> Type = ${type}</p>
                <p class="text-small mb-0 text font-weight-bold"id="timeText" style="color: #000000; font-size: 17px;"> Time = ${time} </p>
                <div id="image-container">
                    <!-- Image and attributes will be displayed here -->
                    <img id="displayedImage" src="/static/ab_img/${imgName}" alt="Image" style="max-width: 100%; max-height: 100%;"/>
                </div>
            </div>
            <p class="small text font-weight-bold" style="color: #000000; font-size: 13px">${getCurrentTime()}</p>
        </div>
    </div>`;

    let chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += newMessage;
}


function getCurrentTime() {
    let currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
    return currentTime;
}


function connectEventSource() {
	const eventSource = new EventSource('/event');
	eventSource.addEventListener('abnormal', function(event) {
        const abnormal = JSON.parse(event.data);
        console.log(abnormal);
        addMessage(abnormal.img_name, abnormal.type, abnormal.time);
    }, false);
    eventSource.addEventListener('error', function(event) {
        console.log("Failed to connect to event stream. Is Redis running?");
        if (event.target.readyState === EventSource.CLOSED) {
            // Connection closed, try to reconnect after some time
            setTimeout(connectEventSource, 200); // Retry after 5 seconds
        }
    }, false);
}

connectEventSource(); // Initial connection attempt

