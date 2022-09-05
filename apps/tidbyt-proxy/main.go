package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"strconv"
	"text/template"

	"github.com/gorilla/mux"
	flags "github.com/jessevdk/go-flags"
	log "github.com/sirupsen/logrus"
)

const (
	pixletBinary = "pixlet"
	templatePath = "./templates/*.star"
	tmpDir       = "/tmp"
)

var config struct {
	API    `group:"HTTP Server Options" namespace:"http" env-namespace:"HTTP"`
	Tidbyt `group:"Tidbyt Options" namespace:"tidbyt" env-namespace:"TIDBYT"`

	Debug bool `long:"debug-mode" env:"DEBUG_MODE" description:"Debug Mode"`
}

var templates *template.Template

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

	// load all star templates
	templates = template.Must(template.ParseGlob(templatePath))
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
		n.TextColor = "#fff"
	}
	if n.TextSize == 0 {
		n.TextSize = 14
	}
	if n.BackgroundColor == "" {
		n.BackgroundColor = "#000"
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

	// create temporary template file
	templateFile, tmplErr := ioutil.TempFile(tmpDir, "tidbyt-notify*.star")
	if tmplErr != nil {
		log.Fatal(tmplErr)
	}

	// render from template
	renderErr := templates.ExecuteTemplate(templateFile, "notify", params)
	if renderErr != nil {
		log.Print(renderErr)
	}
	log.Debugf("rendered template to path %s", templateFile.Name())

	// render and push
	if _, err := exec.LookPath(pixletBinary); err != nil {
		log.Debug("pixlet binary doesn't exist")
	} else {
		log.Debug("pixlet binary exists")

		outputFile := fmt.Sprintf("%s.webp", templateFile.Name())
		// render webp file from star template file
		renderOutput, err := exec.Command(pixletBinary, "render", templateFile.Name(), "--output", outputFile).Output()
		if err != nil {
			log.Println(err.Error())
		}
		log.Debugf("render result:\n %s", string(renderOutput))

		// push rendered webp to target device if provided
		if config.ApiKey != "" && config.DeviceID != "" {
			pushOutput, err := exec.Command(pixletBinary, "push", "--api-token", config.ApiKey, config.DeviceID, outputFile).Output()
			if err != nil {
				log.Println(err.Error())
			}
			log.Debugf("push result:\n %s", string(pushOutput))
		}
		// cleanup template/render files
		defer os.Remove(templateFile.Name())
		defer os.Remove(outputFile)
	}

	w.WriteHeader(http.StatusOK)
}
