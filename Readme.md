# url-shortner-tracker
## Base concept
This is/was a POC to track message receiver's client using open graph preview functionality.
The idea is simply to track client ip when a short url is used, teorically to generate the open graph preview the link must be opened.

## Results
| Service | Result | Info |
|---|---|---|
| Whatsapp | Failed | Whatsapp use the sender client to generate the preview, store it on Meta server and serve it to the receiver |
| Telegram | Failed | Telgram generate the preview using an internal server and serve it to both sender and receiver. |