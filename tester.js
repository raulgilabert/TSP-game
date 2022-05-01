import { io } from 'socket.io-client';

const socket = io("ws://localhost:3000");

let message = "newPlayer";
let arg = "hola";

socket.on("start", (player1, player2) => {
    console.log(player1, player2);
})

socket.emit(message, "Alice");
/*socket.emit(message, "Bob");
socket.emit("print");
socket.emit(message, "Neko");
socket.emit(message, "Nya");
*/
socket.emit("print");

