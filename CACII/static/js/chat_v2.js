// script.js

const chatInput = document.querySelector('.chat-input textarea');
const sendChatBtn = document.querySelector('.chat-input button');
const chatbox = document.querySelector(".chatbox");

let userMessage;

const createChatLi = (message, className) => {
	const chatLi = document.createElement("li");
	chatLi.classList.add("chat", className);
	let chatContent = className === "chat-outgoing" ? `<p>${message}</p>` : `<p>${message}</p>`;
	chatLi.innerHTML = chatContent;
	return chatLi;
}

const handleResponse = (response) => {
	const incomingChatLi = createChatLi(response.groq_response, "chat-incoming");
	chatbox.appendChild(incomingChatLi);
	chatbox.scrollTo(0, chatbox.scrollHeight);
};

const fetchLocalPdf = () => {
	fetch('/local_pdf/', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		},
	})
	.then(response => response.json())
	.then(data => {
		handleResponse(data);
	})
	.catch((error) => {
		const errorChatLi = createChatLi("Oops! Something went wrong. Please try again!", "chat-incoming");
		chatbox.appendChild(errorChatLi);
		chatbox.scrollTo(0, chatbox.scrollHeight);
	});
};

const handleChat = () => {
	userMessage = chatInput.value.trim();
	if (!userMessage) {
		return;
	}
	chatbox.appendChild(createChatLi(userMessage, "chat-outgoing"));
	chatbox.scrollTo(0, chatbox.scrollHeight);

	setTimeout(() => {
		const incomingChatLi = createChatLi("Thinking...", "chat-incoming");
		chatbox.appendChild(incomingChatLi);
		chatbox.scrollTo(0, chatbox.scrollHeight);
		fetchLocalPdf();
	}, 600);
};

sendChatBtn.addEventListener("click", handleChat);
sendChatBtn.addEventListener("keypress", function (e) {
    if (e.key === 'Enter') {
      handleChat();
    }
});

function cancel() {
	let chatbotcomplete = document.querySelector(".chatBot");
	if (chatbotcomplete.style.display != 'none') {
		chatbotcomplete.style.display = "none";
		let lastMsg = document.createElement("p");
		lastMsg.textContent = 'Thanks for using our Chatbot!';
		lastMsg.classList.add('lastMessage');
		document.body.appendChild(lastMsg)
	}
}
