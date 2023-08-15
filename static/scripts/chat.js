// Function to handle the chat button click
function chatButtonClick() {
  const fullChatBlock = document.querySelector('.full-chat-block');
  fullChatBlock.classList.toggle('expanded');
}

// Add event listener to the chat button
document.getElementById('chat-button').addEventListener('click', chatButtonClick);


var coll = document.getElementsByClassName("collapsible");

for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");

        var content = this.nextElementSibling;

        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }

    });
}


function showTypingAnimation() {
  const typingAnimationElement = document.createElement('div');
  typingAnimationElement.classList.add('typing-animation');

  const spanElements = document.createElement('div');
  spanElements.innerHTML = `
    <span></span>
    <span></span>
    <span></span>
  `;

  typingAnimationElement.appendChild(spanElements);
  document.getElementById("chatbox").appendChild(typingAnimationElement);
}

// Hide the typing animation
function hideTypingAnimation() {
  const typingAnimationElement = document.querySelector('.typing-animation');
  if (typingAnimationElement) {
    typingAnimationElement.remove();
  }
}

// gets the time and display's it in the chat
function getTime() {
    let today = new Date();
    hours = today.getHours();
    minutes = today.getMinutes();

    if (hours < 10) {
        hours = "0" + hours;
    }

    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    let time = hours + ":" + minutes;
    return time;
}

// Gets the first message
function firstBotMessage() {
    let firstMessage = "Hey! I'm Rivvi's AI powerd chatbot and I can answer all your queries related to HR and Payroll."
    document.getElementById("botStarterMessage").innerHTML = '<p class="botText"><span>' + firstMessage + '</span></p>';

    let time = getTime();

    $("#chat-timestamp").append(time);
    document.getElementById("userInput").scrollIntoView(false);
}

firstBotMessage();

function getHardResponse(userText) {
  // Show the typing animation
  showTypingAnimation();
  const url = 'http://127.0.0.1:5000/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ input: userText })
  })
    .then(response => response.json())
    .then(response => {
      if (response && response.response) {
        const botResponse = response.response;
        const botHtml = `<p class="botText"><span>${botResponse}</span></p>`;
        document.getElementById("chatbox").insertAdjacentHTML('beforeend', botHtml);
      } else {
        // Handle error response
        const errorMessage = "Oops! An error occurred. Can you please rephrase the question and provide more context?";
        const errorHtml = `<p class="botText"><span>${errorMessage}</span></p>`;
        document.getElementById("chatbox").insertAdjacentHTML('beforeend', errorHtml);
      }
      document.getElementById("chat-bar-bottom").scrollIntoView({ behavior: 'smooth', block: 'end' });
      hideTypingAnimation();
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle error from fetch or any other unexpected errors
      const errorMessage = "Oops! An error occurred. Can you please rephrase the question and provide more context?";
      const errorHtml = `<p class="botText"><span>${errorMessage}</span></p>`;
      document.getElementById("chatbox").insertAdjacentHTML('beforeend', errorHtml);
      document.getElementById("chat-bar-bottom").scrollIntoView({ behavior: 'smooth', block: 'end' });
      hideTypingAnimation();
    });
}



//Gets the text text from the input box and processes it
function getResponse() {
    let userText = $("#textInput").val();

    let userHtml = '<p class="userText"><span>' + userText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

    setTimeout(() => {
        getHardResponse(userText);
    }, 4000)

}

// Handles sending text via button clicks
function buttonSendText(sampleText) {
    let userHtml = '<p class="userText"><span>' + sampleText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

     setTimeout(() => {
         getHardResponse(sampleText);
     }, 4000)
}

function sendButton() {
    getResponse();
}


// Press enter to send a message
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getResponse();
    }
});