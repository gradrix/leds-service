# Use an official Node.js runtime as the base image
FROM node:16

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and yarn.lock to the working directory
COPY ./ui/package.json ./ui/yarn.lock ./

# Install dependencies
RUN yarn install

# Copy the rest of the project files into the container
COPY ./ui .

RUN mkdir -p /frontend_build

# Build the React app
RUN yarn build

# Optionally, specify the command to run (if needed)
CMD ["sh", "-c", "rm -rf /frontend_build/* && cp -r build/* /frontend_build && echo Build complete. Files copied to /frontend_build"]
