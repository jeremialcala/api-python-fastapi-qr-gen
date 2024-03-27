# QR Code Generator

This is a component that generates Qr CODES, using FastAPI and Segno to process requests and create codes, storing code images in file system and data in mongoDB using mongoengine as ORM.

## Qr Code Lifecycle

### Operations:

| Endpoint         | Path | Operation | params | Description                                          |
|------------------|------|-----------|--------|------------------------------------------------------|
| Create Qr        | /qr  | POST      | None   | This endpoint creates a new QR Code from a QrRequest |
| Get Qr from UUID | /qr  | GET       | _uuid  | This endpoint retrieves a Qr code using its UUID     |


### Objects

#### QrRequest

This is the DTO in for the creation of qr Codes

| Name  | Type         | Description                                  | Example                         |
|-------|--------------|----------------------------------------------|---------------------------------|
| data  | String       | Value use to generate the QR Code            | https://github.com/jeremialcala |
| name  | String       | This is a simple Identifier for this QR Code | Jeremi Alcala GitHub            |
| email | EmailAddress | A email Address to resend this qr code       | jeremialcala6@gmail.com         |

``` Json
    {
      "data": "https://github.com/jeremialcala",
      "name": "Jeremi Alcala GitHub",
      "email": "jeremialcala6@gmail.com"
    }
```

