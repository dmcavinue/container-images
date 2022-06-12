package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
)

var message string = "demo"
var delay int = 5

func main() {
	m := os.Getenv("MESSAGE")
	if m != "" {
		log.Println("Loading message:", m)
		message = m
	}

	r := mux.NewRouter()
	r.HandleFunc("/message/{name}", messageHandler)

	log.Println("Starting server on port 8080")
	if err := http.ListenAndServe(":8080", r); err != nil {
		log.Fatal("Error while starting server:", err)
	}
}

func messageHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	name := vars["name"]

	time.Sleep(time.Duration(delay) * time.Millisecond)

	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]string{"message": fmt.Sprintf("%s %s", message, name)})
}