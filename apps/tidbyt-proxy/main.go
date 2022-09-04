package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"

	"github.com/gorilla/mux"
	flags "github.com/jessevdk/go-flags"
	log "github.com/sirupsen/logrus"
)

var config struct {
	API    `group:"HTTP Server Options" namespace:"http" env-namespace:"HTTP"`
	Tidbyt `group:"Tidbyt Options" namespace:"tidbyt" env-namespace:"TIDBYT"`

	Debug bool `long:"debug-mode" env:"DEBUG_MODE" description:"Debug Mode"`
}

type API struct {
	Host string `long:"http-ip" env:"HTTP_IP" description:"HTTP Server IP" default:"0.0.0.0"`
	Port int    `long:"http-port" env:"HTTP_PORT" description:"HTTP Server Port" default:"8080"`
}

type Tidbyt struct {
	ApiUrl   string `long:"api-url" env:"API_URL" description:"Tidbyt API Url" default:"api.tidbyt.com"`
	ApiKey   string `long:"api-key" env:"API_KEY" description:"Tidbyt API Key"`
	DeviceID string `long:"device-id" env:"DEVICE_ID" description:"Tidbyt Device ID"`
}

type notifyParameters struct {
	Text            string // Text to send in notifcation
	TextColor       string // Text Color to set. Default: White
	BackgroundColor string // Background color to set: Default: Black
	TextSize        int    // Test font size to set. Default: 14
}

var parser = flags.NewParser(&config, flags.Default)

func init() {
	// Log as JSON instead of the default ASCII formatter.
	log.SetFormatter(&log.JSONFormatter{})

	// Output to stdout instead of the default stderr
	// Can be any io.Writer, see below for File example
	log.SetOutput(os.Stdout)

	// Only log the warning severity or above.
	log.SetLevel(log.WarnLevel)
}

func main() {
	if _, err := parser.Parse(); err != nil {
		fmt.Printf("%+v", err)
		switch flagsErr := err.(type) {
		case flags.ErrorType:
			if flagsErr == flags.ErrHelp {
				os.Exit(0)
			}
			os.Exit(1)
		default:
			os.Exit(1)
		}
	}

	if config.Debug {
		log.SetLevel(log.DebugLevel)
	}

	r := mux.NewRouter()
	r.HandleFunc("/api/notify", notifyHandler)
	r.HandleFunc("/healthcheck", healthcheck)

	fmt.Println("Starting server on port", config.Port)
	if err := http.ListenAndServe(fmt.Sprintf(":%d", config.Port), r); err != nil {
		log.Fatal("Error while starting server:", err)
	}
}

// notifyDefaults: Set parameter defaults
func (n *notifyParameters) notifyDefaults() {

	// setting default values if no values present
	if n.TextColor == "" {
		n.TextColor = "white"
	}
	if n.TextSize == 0 {
		n.TextSize = 14
	}
	if n.BackgroundColor == "" {
		n.BackgroundColor = "black"
	}
}

// healthcheck: simple healthcheck
func healthcheck(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
}

// notifyHandler: send notification to tidbyt device
func notifyHandler(w http.ResponseWriter, r *http.Request) {
	log.Debug("notifyHandler:\nrequest:\n%+v", r)

	params := notifyParameters{
		Text:            r.URL.Query().Get("text"),
		TextColor:       r.URL.Query().Get("textcolor"),
		BackgroundColor: r.URL.Query().Get("bgcolor"),
	}
	var strErr error
	if r.URL.Query().Get("textsize") != "" {
		params.TextSize, strErr = strconv.Atoi(r.URL.Query().Get("textsize"))
		if strErr != nil {
			fmt.Printf("Error: %+v", strErr)
		}
	}
	params.notifyDefaults()

	// Image generate and tidbyt API logic goes here

	w.WriteHeader(http.StatusOK)
	err := json.NewEncoder(w).Encode(params)
	if err != nil {
		fmt.Printf("%+v", err)
	}
}
