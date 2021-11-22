# The first stage
# Build React static files
FROM node:lts-alpine AS build

# Install required build tools
RUN apk add --no-cache --virtual .gyp \
        python \
        make \
        g++

# Change dir and copy package.json
WORKDIR /app/frontend
COPY ./frontend/package.json ./
COPY ./frontend/yarn.lock ./
    
# Install all dependencies
RUN yarn install \
    && apk del .gyp

# Copy source and build it
COPY ./frontend/ ./
RUN yarn run build && yarn cache clean

# The second stage
# Copy React static files and start nginx
FROM nginx:stable-alpine
COPY --from=build /app/frontend/react-build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
