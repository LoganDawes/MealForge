# Use official Node.js image
FROM node:22 AS build

# Set working directory
WORKDIR /app

# Install system dependencies
COPY package*.json ./
RUN npm install && npm cache clean --force

# Copy and build application
COPY . .
RUN npm run build

# Install http-server to serve the built files
RUN npm install http-server

# Expose port
EXPOSE 80

# Serve the build with http-server
CMD ["npx", "http-server", "dist"]