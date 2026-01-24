# syntax=docker/dockerfile:1

ARG NODE_VERSION=22.13.1

# --- Build Stage ---
FROM node:${NODE_VERSION}-slim AS builder
WORKDIR /app

# Install dependencies (with cache for faster builds)
COPY package.json package-lock.json ./
RUN npm ci

# Copy all source files (excluding files in .dockerignore)
COPY . .

# Build the Next.js app (outputs to .next/)
RUN npm run build

# Remove dev dependencies to reduce image size
RUN npm prune --production

# --- Production Stage ---
FROM node:${NODE_VERSION}-slim AS final
WORKDIR /app

# Create non-root user for security
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

# Copy only what’s needed to run the app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/app ./app
COPY --from=builder /app/src ./src
COPY --from=builder /app/components.json ./components.json

# Set environment variables
ENV NODE_ENV=production
ENV NODE_OPTIONS="--max-old-space-size=4096"

# Use non-root user
USER appuser

# Expose Next.js default port
EXPOSE 3000

# Optional healthcheck (adjust endpoint if needed)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', res => process.exit(res.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"

# Start the app
CMD ["npm", "start"]
