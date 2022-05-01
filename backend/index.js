import { Server } from "socket.io"

const io = new Server(3000)

let players = 0
let matches = 0

let rooms = {}

function find_room(player) {
    for (let key in rooms) {
	if (rooms[key].player1.name == player[0] || rooms[key].player2.name == player[0]) {
	    return key.toString()
	}
    }
}

function check_collision(points) {
    let last_point = points[points.length - 1]

    for (let i = 0; i < points.length - 1; ++i) {
	let distance = Math.sqrt((last_point[0]-points[i][0])**2 + (last_point[1]-points[i][1])**2)

	if (distance < 0.1) {
	    return true
	}
    }

    return false
}

function generate_points(num) {
    let points = []

    for (let i = 0; i < num; ++i) {
	points[i] = [Math.random(), Math.random()]

	while (check_collision(points)) {
	    points[i] = [Math.random(), Math.random()]
	}
    }

    return points
}

io.on("connection", (socket) => {
    socket.on("newPlayer", (arg) => {
	++players;
	if (players%2 == 1) {
	    ++matches
	    socket.join(matches.toString())

	    rooms[matches.toString()] = {
		player1: {
		    name: arg,
		    points: 0,
		    ready: false,
		    distance: 0.0
		},
		player2: {
		    name: "",
		    points: 0,
		    ready: false,
		    distance: 0.0
		},
		match: 1
	    }
	}
	else {
	    socket.join(matches.toString())
	    rooms[matches.toString()].player2.name = arg
    
	    console.log("sending start")

	    io.to(matches.toString()).emit("start", rooms[matches.toString()].player1.name, rooms[matches.toString()].player2.name, generate_points(5))
	    
	    console.log("sending ended")
	}
    })

    socket.on("ready", (name, distance) => {
	let room = find_room(name)

	if (rooms[room].player1.name == name) {
	    rooms[room].player1.ready = true
	    rooms[room].player1.distance = distance
	}
	else {
	    rooms[room].player2.ready = true
	    rooms[room].player2.distance = distance
	}

	console.log(rooms)

	if (rooms[room].player1.ready && rooms[room].player2.ready) {
	    let winner = ""
	    if (rooms[room].player1.distance > rooms[room].player2.distance) {
		winner = rooms[room].player1.name
	    }
	    else {
		winner = rooms[room].player2.name
	    }

	    console.log(winner)

	    io.to(room).emit("winner", winner)
	}
    })
})
