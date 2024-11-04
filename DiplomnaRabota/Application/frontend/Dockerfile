# Use Node.js image
FROM node:16

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the frontend port
EXPOSE 3001

# Run the frontend with npm start
CMD ["npm", "start"]
