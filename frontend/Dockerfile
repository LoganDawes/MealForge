# Use official Node.js image for building
FROM node:22 AS build

# Set working directory
WORKDIR /app

# Install system dependencies
COPY package*.json ./
RUN npm install && npm cache clean --force

# Copy and build application
COPY . .
RUN npm run build

# Use official Nginx image for serving
FROM nginx:stable-alpine

# Copy built files to Nginx's default HTML directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]