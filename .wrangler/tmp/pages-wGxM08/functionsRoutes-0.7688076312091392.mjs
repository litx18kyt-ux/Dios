import { onRequest as __api_fetch_primary_ts_onRequest } from "/workspaces/Dios/functions/api/fetch-primary.ts"

export const routes = [
    {
      routePath: "/api/fetch-primary",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_fetch_primary_ts_onRequest],
    },
  ]