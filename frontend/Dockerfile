FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* yarn.lock* ./
COPY .env .env
RUN npm install

# Añade este comando para ver el valor en los logs de build:
RUN echo "VITE_API_URL en build: $VITE_API_URL"

COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
