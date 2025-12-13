# Stage 1: Build the Docusaurus application
FROM node:18-alpine as builder

WORKDIR /app

# Copy package.json and package-lock.json (if available) to install dependencies
COPY docusaurus-book/package.json ./
COPY docusaurus-book/yarn.lock ./
# If you use npm, replace the above line with:
# COPY docusaurus-book/package-lock.json ./

# Install dependencies
RUN yarn install --frozen-lockfile
# If you use npm, replace the above line with:
# RUN npm ci

# Copy the rest of the application code
COPY docusaurus-book/ ./

# Build the Docusaurus site
RUN yarn build
# If you use npm, replace the above line with:
# RUN npm run build

# Stage 2: Serve the Docusaurus site with Nginx
FROM nginx:alpine

# Copy the built Docusaurus site from the builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom Nginx configuration (optional)
# If you have a custom nginx.conf, uncomment and adapt this:
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for web traffic
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
