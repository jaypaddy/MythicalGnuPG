package main

import (
	"fmt"
	"log"
	"net/http"
	"time"
	"encoding/json"

	"github.com/gorilla/mux"
)

//WO A
type WO struct {
	Key    string `json:"Key,omitempty"`
	ID    string `json:"ID,omitempty"`
	Status   string `json:"Status,omitempty"`
	Zipcode string `json:"Zipcode,omitempty"`
}

func main() {
	router := mux.NewRouter()

	//WOX
	router.HandleFunc("/WOX/{Key}", AcceptWO).Methods("POST")

	log.Fatal(http.ListenAndServe(":80", router))
}

//AcceptWO gets a WO Endpoint
func AcceptWO(w http.ResponseWriter, req *http.Request) {

	LogIt("WOX","HELLO", req)
	var wo WO
	_ = json.NewDecoder(req.Body).Decode(&wo)
	params := mux.Vars(req)	
	wo.Key = params["Key"]
	fmt.Printf("%s %s %s %s\n",wo.Key,wo.ID, wo.Status, wo.Zipcode )
	woObj,_ := json.Marshal(wo)
	SendMessage(string(woObj))
	json.NewEncoder(w).Encode(wo)
}
func LogIt(pipeline1 string, pipeline2 string, req *http.Request) {
	ua := req.Header.Get("User-Agent")
	ip := req.Header.Get("X-Forwarded-For")
	fmt.Printf("%s,%s,%s,%s,%s\n", time.Now(), pipeline1,pipeline2, ua, ip)
}