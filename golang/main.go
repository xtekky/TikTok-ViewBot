package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"regexp"
	"strings"
)

func sessid() string {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", "https://zefoy.com/", nil)
	req.Header.Set("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
	resp, _ := client.Do(req)

	re := regexp.MustCompile(`[a-z0-9]{26}`)
	sessid := string(re.Find([]byte(resp.Header.Get("set-cookie"))))

	return sessid
}

func solve_captcha(sessid string) string {
	client := &http.Client{}
	captcha_req, _ := http.NewRequest(
		"GET",
		"https://zefoy.com/a1ef290e2636bf553f39817628b6ca49.php?_CAPTCHA&t=0.04316800+1657582034",
		nil,
	)

	captcha_req.Header.Set("cookie", fmt.Sprintf("PHPSESSID=%s", sessid))
	captcha_req.Header.Set("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")

	captcha_res, _ := client.Do(captcha_req)
	captcha_bytes, _ := ioutil.ReadAll(captcha_res.Body)

	captcha_image := string(base64.StdEncoding.EncodeToString([]byte(captcha_bytes)))

	type Response struct {
		Captcha struct {
			Answer     string  `json:"answer"`
			Confidence int     `json:"confidence"`
			Latency    float64 `json:"latency"`
		} `json:"captcha"`
		StatusCode int    `json:"status_code"`
		StatusMsg  string `json:"status_msg"`
	}

	captcha_data := strings.NewReader(fmt.Sprintf(`{"image": "%s"}`, captcha_image))
	solve_req, _ := http.NewRequest("POST", "https://api.xtekky.com/ocr", captcha_data)

	solve_res, _ := client.Do(solve_req)
	solve_body, _ := ioutil.ReadAll(solve_res.Body)

	var result Response
	if err := json.Unmarshal(solve_body, &result); err != nil {
		solve_captcha(sessid)
	}

	var xdata = strings.NewReader(fmt.Sprintf(`captcha_secure=%s&r75619cf53f5a5d7aa6af82edfec3bf0=`, string(result.Captcha.Answer)))
	req, _ := http.NewRequest("POST", "https://zefoy.com/", xdata)

	req.Header.Set("content-type", "application/x-www-form-urlencoded")
	req.Header.Set("cookie", fmt.Sprintf("PHPSESSID=%s", string(sessid)))
	req.Header.Set("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
	resp, _ := client.Do(req)

	req_text, _ := ioutil.ReadAll(resp.Body)

	if strings.Contains(string(req_text), "c2VuZF9mb2xsb3dlcnNfdGlrdG9r") {
		fmt.Println("Success | Captcha: " + result.Captcha.Answer)
	} else {
		solve_captcha(sessid)
	}

	re := regexp.MustCompile(`"([a-z0-9]{16})`)
	return re.FindStringSubmatch(string(req_text))[1]
}

func reverse(s string) (result string) {
	for _, v := range s {
		result = string(v) + result
	}
	return
}

func decrypt(encryped string) string {
	reversed, _ := url.QueryUnescape(reverse(encryped))
	decrypted, _ := base64.StdEncoding.DecodeString(reversed)

	return string(decrypted)
}

func send_views(phpsessid, alpha_key, aweme_id string) {
	client := &http.Client{}
	data := strings.NewReader(fmt.Sprintf(`%s=https://www.tiktok.com/@onlp/video/%s/`, alpha_key, aweme_id))
	req, _ := http.NewRequest("POST", "https://zefoy.com/c2VuZC9mb2xsb3dlcnNfdGlrdG9V", data)

	req.Header.Set("cookie", fmt.Sprintf("PHPSESSID=%s", phpsessid))
	req.Header.Set("origin", "https://zefoy.com")
	req.Header.Set("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")
	req.Header.Set("x-requested-with", "XMLHttpRequest")
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := client.Do(req)
	bodyText, _ := ioutil.ReadAll(resp.Body)
	_data := decrypt(string(bodyText))

	re := regexp.MustCompile(`"([a-z0-9]{16})`)
	beta_key := re.FindStringSubmatch(string(_data))[1]

	fmt.Println("Beta    | " + beta_key)

}

func main() {
	aweme_id := "7114598963977751814"

	phpsessid := sessid()
	fmt.Println("Sessid  | " + phpsessid)
	alpha_key := solve_captcha(phpsessid)
	fmt.Println("Alpha   | " + alpha_key)
	send_views(phpsessid, alpha_key, aweme_id)
}
