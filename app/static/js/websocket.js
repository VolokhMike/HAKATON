var ws = new WebSocket("ws://localhost:30001/ws");
        

        function sendMessage() {
            var input = document.getElementById("messageInput");
            ws.send(input.value);
            input.value = '';
        }
export default{
    ws, sendMessage 
}