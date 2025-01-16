let chatSocket = null;
let currentUserId = null;

function selectUser(userId, username) {
  currentUserId = userId;
  document.getElementById("message-container").innerHTML = "";
  document.getElementById("send-button").disabled = false;

  document.getElementById(
    "current-chat-user"
  ).innerText = `Chatting with ${username}`;

  if (chatSocket) {
    chatSocket.close();
  }

  chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${userId}/`);

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    displayMessage(data.sender, data.message);
  };

  chatSocket.onclose = function () {
    console.error("WebSocket closed unexpectedly");
  };

  fetch(`/messages/${userId}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to load messages");
      }
      return response.json();
    })
    .then((messages) => {
      messages.forEach((message) => {
        displayMessage(message.sender, message.content);
      });
    })
    .catch((error) => {
      console.error(error);
      alert("Failed to load messages.");
    });
}

function displayMessage(sender, content) {
  const messageContainer = document.getElementById("message-container");
  const messageDiv = document.createElement("div");
  messageDiv.className = "message";
  messageDiv.innerHTML = `<span class="sender">${sender}:</span> ${content}`;
  messageContainer.appendChild(messageDiv);

  messageContainer.scrollTop = messageContainer.scrollHeight;
}

document.getElementById("send-button").onclick = function () {
  const messageInput = document.getElementById("message-input");
  const message = messageInput.value;

  if (message && chatSocket) {
    chatSocket.send(
      JSON.stringify({
        message: message,
      })
    );
    messageInput.value = "";
  }
};
