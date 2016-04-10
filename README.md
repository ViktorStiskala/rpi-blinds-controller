# Blinds API #

Somfy blinds controller using RPi GPIO.

Channel numbers are the same as on the remote controller itself, starting from 1. Channel 5 is the channel when all LEDs are blinking.

Somfy Telis remote controller is stateless meaning that individual commands can affect the ones sent previously. For example sending `my` shortly after `down` or `up` will cancel the previous movement. It is up to you to add delays accordingly.

## Movement ##

### Move to specified position ###

`PUT /blinds/channel/5/down/`

Button can be one of `up`, `down` or `my`.
### Short move ###

`POST /blinds/channel/3/`
```json
{
    "direction": "up",
    "duration": 200
}
```
Direction can be either `up` or `down`.

Duration means the time in milliseconds between `up` or `down` and stop – `my` button.

---

## Internal status and debug ##

### Get current status ###

`GET /blinds/status/`
```json
{
    "channel": 3
}
```

### Set current status ###

`POST /blinds/status/`
```json
{
    "channel": 5
}
```

### Set channel without accesing remote ###

Can be used when internal state is different from remote state

`PUT /blinds/debug/channel/<int:channel>/`
```json
{
    "channel": 5
}
```