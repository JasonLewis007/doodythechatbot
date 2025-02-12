var socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("response", function (data) {
    let chatbox = document.getElementById("chatbox");
    let message = document.createElement("p");
    message.textContent = `Doody: ${data.text}`;
    chatbox.appendChild(message);
});

function sendMessage() {
    let inputField = document.getElementById("userInput");
    let message = inputField.value;
    if (!message.trim()) return;

    let chatbox = document.getElementById("chatbox");
    let userMessage = document.createElement("p");
    userMessage.textContent = `You: ${message}`;
    chatbox.appendChild(userMessage);

    socket.send({ text: message });
    inputField.value = "";
}
