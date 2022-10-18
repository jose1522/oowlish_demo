const url = "ws://127.0.0.1:5000/api/v1/youtube/ws";
const output = document.getElementById('summaryBox');
const loader = document.getElementById('loading');
var socket = new WebSocket(url);

function reset_socket_connection(){
    socket = new WebSocket(url);
};

function get_form_data(form){
    const formData = new FormData(form);
    const formProps = Object.fromEntries(formData);
    return formProps;
};

function get_summary(event){
    displayLoading();
    event.preventDefault();
    var form_data = get_form_data(event.target);
    console.log(form_data);
    socket.send(JSON.stringify(form_data));  
    socket.onmessage = (event)=>{;
        data = JSON.parse(event.data);
        console.log(data);
        hideLoading();
        output.textContent = data["summary"];
    };
}; 

function displayLoading() {
    console.log("Activate Loader")
    loader.classList.add("display");
    setTimeout(() => {
        loader.classList.remove("display");
    }, 120000);
}

function hideLoading() {
    console.log("Deactivate Loader");
    loader.classList.remove("display");
}