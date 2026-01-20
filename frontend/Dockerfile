# Stage 1: Dependencies builder
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile
COPY . .

# --- IMPORTANTE: Definir los marcadores para el build ---
ENV NEXT_PUBLIC_SUPABASE_URL=https://replace-with-real-supabase-url.com
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=replace-with-real-supabase-anon-key
ENV NEXT_PUBLIC_FASTAPI_URL=https://replace-with-real-fastapi-url.com

RUN pnpm run build

# Stage 3: Production runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV HOSTNAME="0.0.0.0"
ENV PORT=3000

COPY --from=builder /app/public ./public

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Instalar su-exec para manejar permisos
RUN apk add --no-cache su-exec

# Crear usuario
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# --- SCRIPT DE ARRANQUE ROBUSTO ---
RUN echo '#!/bin/sh' > /app/entrypoint.sh && \
    echo 'echo "🔍 Verificando variables de entorno..."' >> /app/entrypoint.sh && \
    echo 'if [ -z "$NEXT_PUBLIC_FASTAPI_URL" ]; then echo "⚠️ WARNING: NEXT_PUBLIC_FASTAPI_URL no está definida"; fi' >> /app/entrypoint.sh && \
    echo 'echo "🔄 Reemplazando variables en tiempo de ejecución..."' >> /app/entrypoint.sh && \
    echo 'find /app/.next -type f -name "*.js" -exec sed -i "s|https://replace-with-real-supabase-url.com|$NEXT_PUBLIC_SUPABASE_URL|g" {} +' >> /app/entrypoint.sh && \
    echo 'find /app/.next -type f -name "*.js" -exec sed -i "s|replace-with-real-supabase-anon-key|$NEXT_PUBLIC_SUPABASE_ANON_KEY|g" {} +' >> /app/entrypoint.sh && \
    echo 'find /app/.next -type f -name "*.js" -exec sed -i "s|https://replace-with-real-fastapi-url.com|$NEXT_PUBLIC_FASTAPI_URL|g" {} +' >> /app/entrypoint.sh && \
    echo 'echo "✅ Variables reemplazadas. Iniciando Next.js..."' >> /app/entrypoint.sh && \
    echo 'exec su-exec nextjs "$@"' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

# Ejecutar script como root (él cambiará a nextjs internamente)
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["node", "server.js"]
