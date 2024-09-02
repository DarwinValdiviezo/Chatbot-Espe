const conversations = [];
let currentChat = { title: "Chat 1", messages: [] };

document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (message) {
        addMessageToChatBox('Tú: ' + message, true);
        input.value = '';
        
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: message }),
        })
        .then(response => response.json())
        .then(data => {
            addMessageToChatBox('Chatbot: ' + data.response, false);
            saveMessage('Tú: ' + message, 'Chatbot: ' + data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessageToChatBox('Chatbot: Lo siento, hubo un error.', false);
        });
    }
}

function addMessageToChatBox(message, isUser = true) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.className = isUser ? 'message user-message' : 'message bot-message';
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Desplazar hacia abajo
}

document.getElementById('new-chat').addEventListener('click', () => {
    if (currentChat.messages.length > 0) {
        saveConversation(currentChat.title, currentChat.messages);
    }
    currentChat = { title: `Chat ${conversations.length + 1}`, messages: [] };
    document.getElementById('chat-box').innerHTML = '';
});

document.getElementById('clear-conversations').addEventListener('click', () => {
    if (confirm("¿Estás seguro de que deseas borrar todas las conversaciones?")) {
        document.getElementById('conversation-list').innerHTML = '';
        conversations.length = 0;
        document.getElementById('chat-box').innerHTML = '';
    }
});

function saveMessage(userMessage, botMessage) {
    currentChat.messages.push({ user: userMessage, bot: botMessage });
}

function saveConversation(title, messages) {
    const chat = { title: title, messages: [...messages] }; // Crear una copia del array de mensajes
    conversations.push(chat);

    const conversationList = document.getElementById('conversation-list');
    const listItem = document.createElement('li');
    listItem.textContent = title;

    listItem.addEventListener('click', () => {
        loadConversation(chat);
    });

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Borrar';
    deleteButton.onclick = function() {
        conversationList.removeChild(listItem);
        const index = conversations.findIndex(c => c.title === chat.title);
        conversations.splice(index, 1); // Eliminar de la lista de conversaciones
    };
    
    listItem.appendChild(deleteButton);
    conversationList.appendChild(listItem);
}

function loadConversation(chat) {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = ''; // Limpiar el chat actual

    chat.messages.forEach(message => {
        addMessageToChatBox(message.user, true);
        addMessageToChatBox(message.bot, false);
    });

    currentChat = chat; // Establecer la conversación cargada como la actual
}

document.getElementById('toggle-sidebar').addEventListener('click', function() {
    var sidebar = document.getElementById('sidebar');
    var chatArea = document.getElementById('chat-area');
    if (sidebar.classList.contains('collapsed')) {
        sidebar.classList.remove('collapsed');
        this.textContent = 'Ocultar';
    } else {
        sidebar.classList.add('collapsed');
        this.textContent = 'Mostrar';
    }
});
