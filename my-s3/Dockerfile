FROM dxflrs/garage:v2.2.0 AS garage
FROM alpine:3.19
RUN apk add --no-cache gawk

ARG RUST_LOG=garage=info

COPY --from=garage /garage /garage
COPY my-s3/garage.toml /etc/garage.toml
COPY my-s3/entrypoint.sh /entrypoint.sh
RUN chmod 777 /entrypoint.sh

EXPOSE 3900 3901 3902 3903
ENTRYPOINT [ "/entrypoint.sh", "data" ]