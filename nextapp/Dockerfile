FROM node:18-alpine AS build
WORKDIR /app
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
ENV NODE_ENV=production
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
COPY --from=build /app .
EXPOSE 3000
CMD ["npm", "start"]
