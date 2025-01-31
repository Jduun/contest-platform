FROM node:alpine as builder

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# nginx to serve static files
FROM nginx:stable-alpine

COPY --from=builder /dist /usr/share/nginx/html
COPY --from=builder nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]