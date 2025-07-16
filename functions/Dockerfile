FROM denoland/deno:1.36.1
WORKDIR /app
COPY ./generate_tale ./generate_tale
COPY ./initialize_credits ./initialize_credits
EXPOSE 8000
CMD ["deno", "run", "--allow-net", "--allow-env", "--allow-read", "generate_tale/index.ts"]
