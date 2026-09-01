import { onRequestPost as __api_fetch_primary_ts_onRequestPost } from "/workspaces/Dios/functions/api/fetch-primary.ts"

export const routes = [
    {
      routePath: "/api/fetch-primary",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_fetch_primary_ts_onRequestPost],
    },
  ]