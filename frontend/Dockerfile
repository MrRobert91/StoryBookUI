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

# Definimos valores "falsos" únicos que luego buscaremos y reemplazaremos.
ENV NEXT_PUBLIC_SUPABASE_URL=REPLACE_WITH_REAL_SUPABASE_URL
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=REPLACE_WITH_REAL_SUPABASE_ANON_KEY
ENV NEXT_PUBLIC_API_URL=REPLACE_WITH_REAL_API_URL

# Build the application
RUN pnpm run build

# Stage 3: Production runner
FROM node:20-alpine AS runner
WORKDIR /app

# Set environment to production
ENV NODE_ENV=production

# Copy built application from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# --- CORRECCIÓN: Script de arranque con permisos correctos ---
# Creamos el script y le damos permisos.
# IMPORTANTE: No cambiamos a USER nextjs todavía. El script se ejecutará como root,
# hará los cambios, y luego usará 'su-exec' o 'su' para bajar privilegios al ejecutar la app.
RUN echo '#!/bin/sh' > /app/entrypoint.sh && \
    echo 'echo "Iniciando reemplazo de variables de entorno..."' >> /app/entrypoint.sh && \
    echo 'find /app/.next -type f -name "*.js" -exec sed -i "s|REPLACE_WITH_REAL_SUPABASE_URL|$NEXT_PUBLIC_SUPABASE_URL|g" {} +' >> /app/entrypoint.sh && \
    echo 'find /app/.next -type f -name "*.js" -exec sed -i "s|REPLACE_WITH_REAL_SUPABASE_ANON_KEY|$NEXT_PUBLIC_SUPABASE_ANON_KEY|g" {} +' >> /app/entrypoint.sh && \
    echo 'find /app/.next -type f -name "*.js" -exec sed -i "s|REPLACE_WITH_REAL_API_URL|$NEXT_PUBLIC_API_URL|g" {} +' >> /app/entrypoint.sh && \
    echo 'echo "Variables reemplazadas. Cambiando permisos y arrancando servidor..."' >> /app/entrypoint.sh && \
    echo '# Cambiamos el propietario de .next al usuario nextjs por si acaso' >> /app/entrypoint.sh && \
    echo 'chown -R nextjs:nodejs /app/.next' >> /app/entrypoint.sh && \
    echo '# Ejecutamos el comando original como el usuario nextjs' >> /app/entrypoint.sh && \
    echo 'exec su-exec nextjs "$@"' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Instalamos su-exec para bajar privilegios de forma segura
RUN apk add --no-cache su-exec

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

# Usamos el entrypoint. NO definimos USER nextjs aquí, lo maneja el script.
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["node_modules/.bin/next", "start"]
