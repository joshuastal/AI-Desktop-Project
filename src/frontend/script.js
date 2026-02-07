
//---...---...---...---...---...---...---...---...---...---...---...---...---...---...---...---...---
//                                       JS code for pywebview frontend

// JavaScript function to call a Python function
async function callPython() {
    // Access the 'pywebview' object which bridges JS and Python
    // 'pywebview.api' exposes the Python functions defined in the API
    const response = await pywebview.api.say_hello_from_python('JavaScript');
    document.getElementById('message').innerText = response;
}


async function callSendGeminiMessage() {
    const userInput = document.getElementById('userInput').value;
    const response = await pywebview.api.send_message(userInput);
    document.getElementById('message').innerText = response;
}




//---...---...---...---...---...---...---...---...---...---...---...---...---...---...---...---...


function greetUser(firstName, lastName) {
    const greeting = `Hello, ${firstName} ${lastName}! Welcome to Pywebview!`;
    document.getElementById('greetingMessage').innerText = greeting;
}

// Attach a submit handler to support enter and greet button press
function _attachGreetFormHandler() {
    const form = document.getElementById('greetForm');
    if (!form) return;
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // ?. is used to safely access the form elements in case they are not present
        const name = form.elements['name']?.value || '';
        const surname = form.elements['surname']?.value || '';
        greetUser(name, surname);
    });
}

// Startup scripts go here
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', _attachGreetFormHandler);
} else {
    _attachGreetFormHandler();
}

// When the window is loaded, expose the JavaScript function to Python
// This makes 'updateMessage' available for Python to call
window.addEventListener('pywebviewready', function() {
    pywebview.api.init_js_ready(); // Notify Python that JS is ready
});