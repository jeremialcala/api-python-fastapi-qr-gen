# QR Code Generator

This is a component that generates Qr CODES

## Qr Code Lifecycle

### Operations:

| Endpoint         | Path | Operation | params | Description                                          |
|------------------|------|-----------|--------|------------------------------------------------------|
| Create Qr        | /qr  | POST      | None   | This endpoint creates a new QR Code from a QrRequest |
| Get Qr from UUID | /qr  | GET       | _uuid  | This endpoint retrieves a Qr code using its UUID     |



### Objects

``` Json
    {
      "data": "https://github.com/jeremialcala",
      "name": "Jeremi Alcala GitHub",
      "email": "jeremialcala6@gmail.com"
    }
```

