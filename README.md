# Simple SMTP

A (work in progress!) simple Python implementation of an SMTP server, leaning heavily on protocol defined in [RFC 5321](https://datatracker.ietf.org/doc/html/rfc5321).

## Usage

Install the given requirements: `pip install -r requirements.txt`

Rename `sample.env` to `.env`, and reconfigure as desired.

Open two separate terminals. In both, navigate to the `src` directory.
- In the first, launch the server: `python server.py`
- In the second, launch the client: `python client.py`

Note that the client is *only for demonstration purposes*. It's a very naive implementation
and relies on user input for everything.

By default, the server will run on `localhost:2525` (normally mailservers would
run on port 25, but that requires privileged access).

## Example Execution

CLIENT:
```
HELO example.org
DATA
this is my email
woohoo!
\r\n.\r\n
QUIT
```

## References

[RFC 5321 (SMTP Draft Standard)](https://datatracker.ietf.org/doc/html/rfc5321)

[RFC 9051 (IMAP Client Reference)](https://datatracker.ietf.org/doc/html/rfc9051)

[SMTP Transport Example (Wikipedia)](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol#SMTP_transport_example)
