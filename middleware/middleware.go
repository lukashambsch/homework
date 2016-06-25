package main

import (
  "crypto/sha1"
	"flag"
	"fmt"
	"log"
	"net/http"
	"net/http/httptest"
  "sort"
	"strconv"
)

const (
	crlf       = "\r\n"
	colonspace = ": "
)

func ChecksumMiddleware(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// your code goes here ...
    rec := httptest.NewRecorder()
    h.ServeHTTP(rec, r)

    canonical := strconv.Itoa(rec.Code) + crlf

    var keys []string
    for k, v := range rec.Header() {
      w.Header()[k] = v
      keys = append(keys, k)
    }
    sort.Strings(keys)

    var headers []string
    for _, k := range keys {
      val := rec.Header()[k][0]
      canonical += k + colonspace + val + crlf
      headers = append(headers, k)
    }

    canonical += "X-Checksum-Headers" + colonspace
    for i, header := range headers {
      canonical += header
      if i < len(headers) - 1 {
        canonical += ";"
      }
    }
    canonical += crlf + crlf
    canonical += string(rec.Body.Bytes())
    sha := sha1.New()
    sha.Write([]byte(canonical))

    w.Header().Set("X-Checksum", fmt.Sprintf("%x", sha.Sum(nil)))
    w.WriteHeader(rec.Code)

    w.Write(rec.Body.Bytes())
	})
}

// Do not change this function.
func main() {
	var listenAddr = flag.String("http", ":8080", "address to listen on for HTTP")
	flag.Parse()

	http.Handle("/", ChecksumMiddleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Foo", "bar")
		w.Header().Set("Content-Type", "text/plain")
		w.Header().Set("Date", "Sun, 08 May 2016 14:04:53 GMT")
		msg := "Curiosity is insubordination in its purest form.\n"
		w.Header().Set("Content-Length", strconv.Itoa(len(msg)))
		fmt.Fprintf(w, msg)
	})))

	log.Fatal(http.ListenAndServe(*listenAddr, nil))
}
