import { onRequestOptions as __api_fetch_primary_ts_onRequestOptions } from "/workspaces/Dios/functions/api/fetch-primary.ts"
import { onRequestPost as __api_fetch_primary_ts_onRequestPost } from "/workspaces/Dios/functions/api/fetch-primary.ts"

export const routes = [
    {
      routePath: "/api/fetch-primary",
      mountPath: "/api",
      method: "OPTIONS",
      middlewares: [],
      modules: [__api_fetch_primary_ts_onRequestOptions],
    },
  {
      routePath: "/api/fetch-primary",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_fetch_primary_ts_onRequestPost],
    },
  ]