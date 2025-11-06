FROM node:20-bullseye AS builder
WORKDIR /app

# build backend + frontend
COPY backend/package.json backend/package-lock.json ./backend/
RUN cd backend && npm ci

COPY backend ./backend
COPY frontend ./frontend

# build frontend
RUN cd frontend && npm ci && npm run build

# final image
FROM node:20-bullseye-slim
WORKDIR /app

COPY --from=builder /app/backend /app/backend
COPY --from=builder /app/frontend/build /app/frontend/build

WORKDIR /app/backend
ENV NODE_ENV=production
EXPOSE 8080

RUN npm ci --omit=dev

CMD ["node", "server.js"]
