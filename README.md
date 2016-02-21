# Blinds #

Somfy blinds controller using RPi GPIO.

## API ##


### Button press ###

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

---

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