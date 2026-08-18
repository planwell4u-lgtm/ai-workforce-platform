FROM node:22-bookworm-slim AS build

WORKDIR /app

COPY apps/frontend/package.json apps/frontend/package-lock.json ./
RUN npm ci

COPY apps/frontend ./
RUN npx vinext build

FROM node:22-bookworm-slim AS runtime

ENV NODE_ENV=production

WORKDIR /app

COPY --from=build /app/package.json ./
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist

EXPOSE 3000

CMD ["./node_modules/.bin/vinext", "start", "--host", "0.0.0.0", "--port", "3000"]
