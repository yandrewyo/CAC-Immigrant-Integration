// script.js

// script.js

// Groq API key
const API_KEY = "";
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

// const generateResponse = (incomingChatLi) => {
// 	const messageElement = incomingChatLi.querySelector("p");
// 	const userMessage = chatInput.value.trim();
// 	if (!userMessage) return;

// 	fetch('/chat/', {
// 		method: 'POST',
// 		headers: {
// 			'Content-Type': 'application/x-www-form-urlencoded'
// 		},
// 		body: new URLSearchParams({ 'message': userMessage })
// 	})
// 	.then(res => res.json())
// 	.then(data => {
// 		if (data.message) {
// 			messageElement.textContent = data.message;
// 		} else {
// 			messageElement.classList.add("error");
// 			messageElement.textContent = "Oops! Something went wrong. Please try again!";
// 		}
// 	})
// 	.catch(() => {
// 		messageElement.classList.add("error");
// 		messageElement.textContent = "Oops! Something went wrong. Please try again!";
// 	})
// 	.finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
// };


const generateResponse = (incomingChatLi) => {
	const API_URL = "https://api.groq.com/openai/v1/chat/completions"; // Replace with the actual Groq API endpoint
	const messageElement = incomingChatLi.querySelector("p");
	const requestOptions = {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"Authorization": `Bearer ${API_KEY}`
		},
		body: JSON.stringify({
			"model": "llama3-8b-8192", // Replace with the actual Groq model identifier
			"messages": [
				{
					role: "user",
					content: userMessage
				}
			]
		})
	};

	fetch(API_URL, requestOptions)
		.then(res => {
			if (!res.ok) {
				throw new Error("Network response was not ok");
			}
			return res.json();
		})
		.then(data => {
			messageElement.textContent = data.choices[0].message.content;
		})
		.catch((error) => {
			messageElement.classList.add("error");
			messageElement.textContent = "Oops! Something went wrong. Please try again!";
		})
		.finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
};


const handleChat = () => {
	userMessage = chatInput.value.trim();
	if (!userMessage) {
		return;
	}
	chatbox.appendChild(createChatLi(userMessage, "chat-outgoing"));
	chatbox.scrollTo(0, chatbox.scrollHeight);

	setTimeout(() => {
		const incomingChatLi = createChatLi("Thinking...", "chat-incoming")
		chatbox.appendChild(incomingChatLi);
		chatbox.scrollTo(0, chatbox.scrollHeight);
		generateResponse(incomingChatLi);
	}, 600);
}

sendChatBtn.addEventListener("click", handleChat);

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
