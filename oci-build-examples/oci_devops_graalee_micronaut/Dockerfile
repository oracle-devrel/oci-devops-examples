#
# This is a Dockerfile to create a small runtime container image by 
# packaging the Micronaut app native executable as a “mostly static” 
# native image which statically links everything except libc. 
# Statically linking all your libraries except glibc ensures your 
# application has all the libraries it needs to run on any 
# Linux glibc-based distribution like "gcr.io/distroless/base". 
# The application runtime image size is only 82.5 MB.
# 
# Reference: https://www.graalvm.org/22.1/reference-manual/native-image/StaticImages/#build-mostly-static-native-image
#

## Begin: Option 1
# FROM gcr.io/distroless/base AS runtime
## End: Option 1

## Begin: Option 2
FROM frolvlad/alpine-glibc:alpine-3.12
RUN apk update && apk add libstdc++
## End: Option 2

ARG APP_FILE
EXPOSE 8080
WORKDIR /home/app

COPY target/${APP_FILE} app
ENTRYPOINT ["./app"]