# Use the official Node.js image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app/frontend

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the frontend code into the container
COPY frontend .

# Build the React app
RUN npm run build

# Expose the port on which the Vite server will run
EXPOSE 5173

# Command to run the Vite server
CMD ["npm", "run", "serve"]
