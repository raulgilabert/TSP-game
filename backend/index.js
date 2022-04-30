import { Server } from "socket.io"

const io = new Server(3000)

let players = 0
let matches = 0

let rooms = {}

io.on("connection", (socket) => {
    socket.on("newPlayer", (arg) => {
	++players;
	if (players%2 == 1) {
	    ++matches
	    socket.join(matches.toString())

	    rooms[matches.toString()] = {
		player1: {
		    name: arg,
		    points: 0
		},
		player2: {
		    name: "",
		    points: 0
		},
		match: 1
	    }
	}
	else {
	    socket.join(matches.toString())
	    rooms[matches.toString()].player2.name = arg

	    io.to(matches.toString()).emit("start", rooms[matches.toString()].player1.name, rooms[matches.toString()].player2.name)
	}

	console.log(arg)

	console.log(rooms)
    })
})
