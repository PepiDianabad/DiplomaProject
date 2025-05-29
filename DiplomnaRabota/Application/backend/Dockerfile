# Use Node.js image
FROM node:16

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .
COPY .env .env 


# Expose the backend port
EXPOSE 5000

# Run the backend server with node server.js
CMD ["node", "server.js"]
