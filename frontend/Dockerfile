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

# --- CAMBIO CLAVE 1: Definir Placeholders ---
# Definimos valores "falsos" únicos que luego buscaremos y reemplazaremos.
ENV NEXT_PUBLIC_SUPABASE_URL=REPLACE_WITH_REAL_SUPABASE_URL
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=REPLACE_WITH_REAL_SUPABASE_ANON_KEY
ENV NEXT_PUBLIC_API_URL=REPLACE_WITH_REAL_API_URL

# Build the application (se construirá con los valores falsos)
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

# --- CAMBIO CLAVE 2: Crear script de arranque (Entrypoint) ---
# Este script busca los placeholders en la carpeta .next y los cambia por las variables de entorno reales
RUN echo '#!/bin/sh' > /app/entrypoint.sh && \
    echo 'echo "Iniciando reemplazo de variables de entorno..."' >> /app/entrypoint.sh && \
    echo 'find /app/.next -type f -name "*.js" -exec sed -i "s|REPLACE_WITH_REAL_SUPABASE_URL|$NEXT_PUBLIC_SUPABASE_URL|g" {} +' >> /app/entrypoint.sh && \
    echo 'find /app/.next -type f -name "*.js" -exec sed -i "s|REPLACE_WITH_REAL_SUPABASE_ANON_KEY|$NEXT_PUBLIC_SUPABASE_ANON_KEY|g" {} +' >> /app/entrypoint.sh && \
    echo 'find /app/.next -type f -name "*.js" -exec sed -i "s|REPLACE_WITH_REAL_API_URL|$NEXT_PUBLIC_API_URL|g" {} +' >> /app/entrypoint.sh && \
    echo 'echo "Variables reemplazadas. Iniciando servidor..."' >> /app/entrypoint.sh && \
    echo 'exec "$@"' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

# --- CAMBIO CLAVE 3: Usar el entrypoint ---
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["node_modules/.bin/next", "start"]
