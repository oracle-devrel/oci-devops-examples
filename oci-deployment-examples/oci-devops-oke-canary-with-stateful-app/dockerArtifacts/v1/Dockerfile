FROM golang:buster as builder

WORKDIR /usr/src/app
COPY go.mod go.sum ./
RUN go mod download
COPY main.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o /usr/local/bin/guestbook

FROM debian:buster
COPY ./public/index.html public/index.html
COPY ./public/script.js public/script.js
COPY ./public/style.css public/style.css
COPY --from=builder /usr/local/bin/guestbook /usr/local/bin/guestbook
CMD ["/usr/local/bin/guestbook"]
EXPOSE 8080